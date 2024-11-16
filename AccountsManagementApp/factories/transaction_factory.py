import factory
from faker import Faker
from ..models.Transaction import Transaction
from ..models.Project import Project
from datetime import datetime

fake = Faker()


class TransactionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Transaction

    transaction_type = factory.Iterator(["income", "expense"], cycle=True)
    amount = factory.Faker("pyint", min_value=1, max_value=100000)
    project = factory.Iterator(Project.objects.all())

    @factory.lazy_attribute
    def date(self):
        end_date = (
            self.project.end_date if self.project.end_date else datetime.now().date()
        )
        return fake.date_between(start_date=self.project.start_date, end_date=end_date)

    @factory.lazy_attribute
    def expense_type(self):
        if self.transaction_type == "income":
            return None
        else:
            return fake.random_element(
                elements=[
                    "Office Supplies",
                    "Travel",
                    "Utilities",
                    "Salary",
                    "Miscellaneous",
                    "GST",
                    "GeM",
                    "ESI",
                ]
            )
