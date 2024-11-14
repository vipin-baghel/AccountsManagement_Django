from django.contrib import admin

from .models.Project import Project
from .models.Transaction import Transaction


class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "description", "status"]


admin.site.register(Project, ProjectAdmin)


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("transaction_type", "amount", "date", "description")
    list_filter = ("transaction_type",)
    search_fields = ("description",)


admin.site.register(Transaction, TransactionAdmin)
