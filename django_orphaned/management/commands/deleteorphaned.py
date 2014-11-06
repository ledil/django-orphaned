from django.core.management.base import BaseCommand
from django.contrib.contenttypes.models import ContentType
from django_orphaned.app_settings import ORPHANED_APPS_MEDIABASE_DIRS
from itertools import chain
from optparse import make_option
from django.conf import settings

import os
import shutil


class Command(BaseCommand):
    help = "Delete all orphaned files"
    base_options = (
        make_option('--info', action='store_true', dest='info', default=False,
                    help='If provided, the files will not be deleted.'),
    )
    option_list = BaseCommand.option_list + base_options

    def _get_needed_files(self, app):
        """
        collects all needed files for an app. goes through every field of each
        model and detects FileFields and ImageFields
        """
        needed_files = []
        for model in ContentType.objects.filter(app_label=app):
            mc = model.model_class()
            if mc is None:
                continue
            fields = []
            for field in mc._meta.fields:
                if (field.get_internal_type() == 'FileField' or field.get_internal_type() == 'ImageField'):
                    fields.append(field.name)

            # we have found a model with FileFields
            if len(fields) > 0:
                files = mc.objects.all().values_list(*fields)
                needed_files.extend([os.path.join(settings.MEDIA_ROOT, file) for file in filter(None, chain.from_iterable(files))])

        return needed_files

    def _get_media_files(self, app):
        """
        collects all media files and empty directories for an app. respects
        the 'skip' and 'exclude' rules provided by the app settings.
        """
        skip = ORPHANED_APPS_MEDIABASE_DIRS[app].get('skip', ())
        exclude = ORPHANED_APPS_MEDIABASE_DIRS[app].get('exclude', ())

        # traverse root folder and store all files and empty directories
        def should_skip(dir):
            for skip_dir in skip:
                if dir.startswith(skip_dir):
                    return True
            return False

        # process each root of the app
        app_roots = ORPHANED_APPS_MEDIABASE_DIRS[app]['root']
        if isinstance(app_roots, basestring):  # backwards compatibility
            app_roots = [app_roots]

        all_files = []
        possible_empty_dirs = []
        for app_root in app_roots:
            for root, dirs, files in os.walk(app_root):
                if should_skip(root):
                    continue
                if len(files) > 0:
                    for basename in files:
                        if basename not in exclude:
                            all_files.append(os.path.join(root, basename))
                elif not os.path.samefile(root, app_root):
                    possible_empty_dirs.append(root)

        # ignore empty dirs with subdirs + files
        empty_dirs = []
        for ed in possible_empty_dirs:
            dont_delete = False
            for files in all_files:
                try:
                    if files.index(ed) == 0:
                        dont_delete = True
                except ValueError:
                    pass
            for skip_dir in skip:
                try:
                    if (skip_dir.index(ed) == 0):
                        dont_delete = True
                except ValueError:
                    pass
            if not dont_delete:
                empty_dirs.append(ed)

        return all_files, empty_dirs

    def handle(self, **options):
        """
        goes through ever app given in the settings. if option 'info' is given,
        nothing would be deleted.
        """
        self.only_info = options.get('info')

        all_files = []
        needed_files = []
        empty_dirs = []
        total_freed_bytes = 0
        total_freed = '0'

        for app in ORPHANED_APPS_MEDIABASE_DIRS.keys():
            if ('root' in ORPHANED_APPS_MEDIABASE_DIRS[app]):
                needed_files.extend(self._get_needed_files(app))
                a, e = self._get_media_files(app)
                all_files.extend(a)
                empty_dirs.extend(e)

        # select deleted files (delete_files = all_files - needed_files)
        delete_files = sorted(set(all_files).difference(needed_files))
        empty_dirs = sorted(set(empty_dirs))  # remove possible duplicates

        # only show
        if (self.only_info):
            # to be freed
            for df in delete_files:
                total_freed_bytes += os.path.getsize(df)
            total_freed = "%0.1f MB" % (total_freed_bytes / (1024 * 1024.0))

            print "\r\n=== %s ===" % app
            if len(empty_dirs) > 0:
                print "\r\nFollowing empty dirs will be removed:\r\n"
                for file in empty_dirs:
                    print " ", file

            if len(delete_files) > 0:
                print "\r\nFollowing files will be deleted:\r\n"
                for file in delete_files:
                    print " ", file
                print "\r\nTotally %s files will be deleted, and "\
                    "totally %s will be freed.\r\n" % (len(delete_files), total_freed)
            else:
                print "No files to delete!"

        # otherwise delete
        else:
            for file in delete_files:
                os.remove(file)
            for dirs in empty_dirs:
                shutil.rmtree(dirs, ignore_errors=True)
