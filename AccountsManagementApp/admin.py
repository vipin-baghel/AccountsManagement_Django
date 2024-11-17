from django.contrib import admin
from unfold.admin import ModelAdmin

from .models.Project import Project
from .models.Transaction import Transaction


class ProjectAdmin(ModelAdmin):
    list_display = ["name", "description", "status"]


admin.site.register(Project, ProjectAdmin)


class TransactionAdmin(ModelAdmin):
    list_display = (
        "transaction_type",
        "amount",
        "date",
        "income_expense_type",
        "description",
    )
    list_filter = ("transaction_type", "amount", "date", "income_expense_type")
    search_fields = ("description",)


admin.site.register(Transaction, TransactionAdmin)
