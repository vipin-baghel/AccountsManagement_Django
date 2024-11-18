# management/commands/delete_data.py
from django.core.management.base import BaseCommand
from ...models.Project import Project
from ...models.Transaction import Transaction


class Command(BaseCommand):
    help = "Delete data from projects and transactions tables"

    def handle(self, *args, **options):
        Project.objects.all().delete()
        Transaction.objects.all().delete()
        self.stdout.write("Data deleted from projects and transactions tables")
