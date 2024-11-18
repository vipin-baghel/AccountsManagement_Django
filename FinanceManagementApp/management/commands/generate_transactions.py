# management/commands/generate_transactions.py
from django.core.management.base import BaseCommand
from ...factories.transaction_factory import TransactionFactory


class Command(BaseCommand):
    def handle(self, *args, **options):
        TransactionFactory.create_batch(100)
        self.stdout.write("Transactions created")
