from django.core.management.base import BaseCommand
from AccountsManagementApp.factories.project_factory import ProjectFactory


class Command(BaseCommand):
    def handle(self, *args, **options):
        ProjectFactory.create_batch(10)
