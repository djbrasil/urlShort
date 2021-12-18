from django.core.management.base import BaseCommand

from core.models import AppURLModel


class Command(BaseCommand):
    help = 'Refreshes all AppURL'

    def add_arguments(self, parser):
        parser.add_argument('--items', type=int) 

    def handle(self, *args, **options):
        # print(options)
        return AppURLModel.objects.refresh_shortcodes(options.get('items'))
