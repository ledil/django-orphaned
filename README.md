# about
delete all orphaned files

# setup
install via easy_install or pip

    easy_install django-orphaned

add it to installed apps in django settings.py

    INSTALLED_APPS = (
        'django_orphaned',
        ...
    )

now add this to your settings.py:

    ORPHANED_APPS = ['app']
    ORPHANED_MODEL_DIRS = {
        'app':{
            'modelname':'root directory'
        }
    }

the least to do is to run this command to delete all orphaned files

    python manage.py deleteorphaned 

# license
MIT-License, see [LICENSE](/ledil/django-orphaned/blob/master/LICENSE) file.
