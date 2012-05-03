from django.conf import settings
from django.utils.importlib import import_module

ORPHANED_MODEL_DIRS = getattr(settings, 'ORPHANED_MODEL_DIRS',{})
ORPHANED_APPS = getattr(settings, 'ORPHANED_APPS',[])
