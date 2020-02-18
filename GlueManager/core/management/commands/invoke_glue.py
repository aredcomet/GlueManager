from django.core.management.base import BaseCommand, CommandError
from .models import GlueJob, GlueArguments





class Command(BaseCommand):
    help = 'Invoke Glue Job based on availability...'


    def handle(self, *args, **options):
        pass