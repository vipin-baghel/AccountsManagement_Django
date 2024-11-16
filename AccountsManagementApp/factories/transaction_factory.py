import factory
from faker import Faker
from ..models.Transaction import Transaction
from .project_factory import ProjectFactory

fake = Faker()


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    transaction_type = factory.Iterator(Transaction.TRANSACTION_TYPES, cycle=True)
    amount = fake.random_int(min=1, max=10000)
    date = fake.date()
    project = factory.SubFactory(ProjectFactory)

    @factory.lazy_attribute
    def expense_type(self):
        if self.transaction_type == "income":
            return None
        else:
            return fake.random_element(elements=Transaction.EXPENSE_TYPES)
