from django.conf import settings
from django.utils.importlib import import_module

ORPHANED_APPS_MEDIABASE_DIRS = getattr(settings, 'ORPHANED_APPS_MEDIABASE_DIRS',{})
