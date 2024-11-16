from django.db import models
from django.core.exceptions import ValidationError


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]
    EXPENSE_TYPES = [
        ("Office Supplies", "Office Supplies"),
        ("Travel", "Travel"),
        ("Utilities", "Utilities"),
        ("Salary", "Salary"),
        ("Miscellaneous", "Miscellaneous"),
        ("GST", "GST"),
        ("GeM", "GeM"),
        ("ESI", "ESI"),
    ]

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    expense_type = models.CharField(
        max_length=15, choices=EXPENSE_TYPES, null=True, blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.transaction_type} : {self.amount}"

    def clean(self):
        if self.transaction_type == "income" and self.expense_type is not None:
            raise ValidationError("Expense type cannot be set for income transactions")
