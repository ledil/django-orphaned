from django.core.management.base import NoArgsCommand
from django.contrib.contenttypes.models import ContentType
from django_orphaned.app_settings import ORPHANED_MODEL_DIRS, ORPHANED_APPS

class Command(NoArgsCommand):
    help = "Delete all orphaned files"

    def handle_noargs(self, **options):
        for app in ORPHANED_APPS:
            for model in ContentType.objects.filter(app_label=app):
                mc = model.model_class()
                fields = []
                for field in mc._meta.fields:
                    if (field.get_internal_type() == 'FileField'):
                        fields.append(field.name)
    
                # we have found a model with FileFields
                if (len(fields)>0):
                    files = mc.objects.all().values_list(*fields,flat=True)
                    print files
                    print "--"
                    print model.model
