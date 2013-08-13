# about
delete all orphaned files

# setup
install via easy_install or pip

    easy_install django-orphaned

with pip

    pip install django-orphaned

add it to installed apps in django settings.py

    INSTALLED_APPS = (
        'django_orphaned',
        ...
    )

now add this to your settings.py ('app' is your project name where models.py is located):

    ORPHANED_APPS_MEDIABASE_DIRS = {
        'app': {
            'root': MEDIABASE_ROOT,  # MEDIABASE_ROOT => default location of your uploaded items e.g. /var/www/mediabase
            'skip': (               # optional iterable of subfolders to preserve, e.g. sorl.thumbnail cache
                path.join(MEDIABASE_ROOT, 'cache'),
                path.join(MEDIABASE_ROOT, 'foobar'),
            ),
            'exclude': ('.gitignore') # optional iterable of files to preserve
        }
    }

the least to do is to run this command to show all orphaned files

    python manage.py deleteorphaned --info

and to finally delete all orphaned files

    python manage.py deleteorphaned

# license
MIT-License, see [LICENSE](/ledil/django-orphaned/blob/master/LICENSE) file.
