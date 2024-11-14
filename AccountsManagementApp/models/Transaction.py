from django.db import models


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ("income", "Income"),
        ("expense", "Expense"),
    ]

    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(null=True, blank=True)
    project = models.ForeignKey("Project", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.transaction_type} : {self.amount}"
