from django.db import models
from django.core.exceptions import ValidationError


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("Income", "Income"),
        ("Expense", "Expense"),
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
    INCOME_TYPES = [
        ("Cash", "Cash"),
        ("Digital", "Digital"),
        ("Cheque", "Cheque"),
    ]
    project = models.ForeignKey("Project", on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    income_expense_type = models.CharField(
        max_length=15, choices=INCOME_TYPES + EXPENSE_TYPES, null=True, blank=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.transaction_type} : {self.amount}"

    def clean(self):
        if self.transaction_type == "Expense":
            if self.income_expense_type not in [t[0] for t in self.EXPENSE_TYPES]:
                raise ValidationError("Expense type cannot be Cash/Digital/Cheque")
        elif self.transaction_type == "Income":
            if self.income_expense_type not in [t[0] for t in self.INCOME_TYPES]:
                raise ValidationError("Income type can only be Cash/Digital/Cheque")
