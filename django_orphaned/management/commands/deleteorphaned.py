from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django_orphaned.app_settings import ORPHANED_APPS_MEDIABASE_DIRS
from optparse import make_option
from django.core.exceptions import ImproperlyConfigured
import os
import shutil


class Command(BaseCommand):
    help = "Delete all orphaned files"
    base_options = (
        make_option('--info', action='store_true', dest='info', default=False,
                    help='If provided, the files will not be deleted.'),
    )
    option_list = BaseCommand.option_list + base_options

    def handle(self, **options):
        self.only_info = options.get('info')

        for app in ORPHANED_APPS_MEDIABASE_DIRS.keys():
            print('', "=" * 80, "\n\tProcessing App", app, '\n', "=" * 80)
            if (ORPHANED_APPS_MEDIABASE_DIRS[app].get('root')):
                file_paths_in_db = []
                files_in_app_root = []
                possible_empty_dirs = []
                empty_dirs = []
                total_freed_bytes = 0
                total_freed = '0'
                delete_files = []

                for model in ContentType.objects.filter(app_label=app):
                    mc = model.model_class()
                    fields = []
                    for field in mc._meta.fields:
                        if (field.get_internal_type() == 'FileField') or (field.get_internal_type() == 'ImageField'):
                            fields.append(field.name)

                    # we have found a model with FileFields or ImageFields
                    if (len(fields) > 0):
                        print("\nFound ", len(fields), " fields" if len(
                            fields) > 1 else "field", " - ", fields, " in model: ", mc.__name__, '\n', "-" * 80,)

                        for field in fields:
                            files = mc.objects.all().values_list(field, flat=True)
                            file_paths_in_db.extend([os.path.join(ORPHANED_APPS_MEDIABASE_DIRS[
                                                app]['root'], file) for file in files])
                        print(len(file_paths_in_db),
                              " files paths are stored database.")

                # traverse root folder and store all files and empty
                # directories
                for root, dirs, files in os.walk(ORPHANED_APPS_MEDIABASE_DIRS[app]['root']):
                    if (len(files) > 0):
                        for basename in files:
                            files_in_app_root.append(os.path.join(root, basename))
                    else:
                        if (root != ORPHANED_APPS_MEDIABASE_DIRS[app]['root']) and ((root + '/') != ORPHANED_APPS_MEDIABASE_DIRS[app]['root']):
                            possible_empty_dirs.append(root)

                if files_in_app_root:
                    print("--> Total files found in app root directory: ",
                          len(files_in_app_root))
                else:
                    print("+++ No file found in app root directory +++")

                if possible_empty_dirs:
                    print("--> empty directories found: ",
                          len(possible_empty_dirs), " - ", possible_empty_dirs)
                else:
                    print("+++ No empty directories found +++")

                # Ignore empty dirs with subdirs + files
                for ed in possible_empty_dirs:
                    dont_delete = False
                    for files in files_in_app_root:
                        try:
                            if (files.index(ed) == 0):
                                dont_delete = True
                        except ValueError:
                            pass
                    if (not dont_delete):
                        empty_dirs.append(ed)

                # select deleted files (delete_files = files_in_app_root -
                # file_paths_in_db)
                file_paths_in_filesystem = set(files_in_app_root)
                delete_files = list(file_paths_in_filesystem.difference(file_paths_in_db))
                print(len(file_paths_in_db), len(file_paths_in_filesystem))
                print(delete_files)

                delete_files.sort()
                empty_dirs.sort()

                #TODO: to be fried
                for df in delete_files:
                    total_freed_bytes += os.path.getsize(df)
                total_freed = "%0.1f MB" % (
                    total_freed_bytes / (1024 * 1024.0))

                # only show
                if (self.only_info):
                    if (len(delete_files) > 0):
                        print("\r\nFollowing files will be deleted:\r\n")
                        for file in delete_files:
                            print(" ", file)
                    if (len(empty_dirs) > 0):
                        print("\r\nFollowing empty dirs will be removed:\r\n")
                        for file in empty_dirs:
                            print(" ", file)

                    if (len(delete_files) > 0):
                        print("\r\nTotally %s files will be deleted, and totally %s will be freed\r\n" % (
                            len(delete_files), total_freed))
                    else:
                        print("No files to delete!")

                # DELETE NOW!
                else:
                    for file in delete_files:
                        # os.remove(file)
                        print("removing %s" % file)
                    for dirs in empty_dirs:
                        # shutil.rmtree(dirs,ignore_errors=True)
                        print("removing tree %s" % dirs)

            else:
                raise ImproperlyConfigured(
                    "MEDIA ROOT settings is not defined in ORPHANED_APPS_MEDIABASE_DIRS settings.")
