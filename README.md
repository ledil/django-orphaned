# about
Delete all orphaned files

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

now add this to your settings.py ('app1' and app2 are the app names where models.py is located):

    ORPHANED_APPS_MEDIABASE_DIRS = {
        'app1': {
            # MEDIA_ROOT => default location(s) of your uploaded items e.g. /var/www/mediabase
            # It can be a single value or a list of iterable
            'root': ( 
                os.path.join(MEDIA_ROOT, 'files'),
                os.path.join(MEDIA_ROOT, 'images'),
            ),
            # optional iterable of subfolders to preserve, e.g. sorl.thumbnail cache
            'skip': (               
                path.join(MEDIA_ROOT, 'cache'),
                path.join(MEDIA_ROOT, 'foobar'),
            ),
            # optional iterable of files to preserve
            'exclude': (
                '.gitignore',
            ) 
        }
        'app2': {
            ...
            # same as above
            ..
        }
    }
    # location where the log file will be stored
    # if not set or empty the log file will not be created
    ORPHANED_LOGS_DIR = MEDIA_ROOT

**NOTE**: from version 0.4.2 you can define ''root'' as string or iterable (list, array)

the least to do is to run this command to show all orphaned files

    python manage.py deleteorphaned --info

and to finally delete all orphaned files

    python manage.py deleteorphaned

# license
MIT-License, see [LICENSE](/ledil/django-orphaned/blob/master/LICENSE) file.