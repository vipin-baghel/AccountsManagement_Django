from django.contrib import admin
from unfold.admin import ModelAdmin
from import_export.admin import ImportExportModelAdmin
from .models.Project import Project
from .models.Transaction import Transaction
from unfold.contrib.import_export.forms import ExportForm, ImportForm

class ProjectAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = ["name", "description", "status"]


admin.site.register(Project, ProjectAdmin)


class TransactionAdmin(ModelAdmin, ImportExportModelAdmin):
    import_form_class = ImportForm
    export_form_class = ExportForm
    list_display = (
        "project",
        "transaction_type",
        "amount",
        "date",
        "income_expense_type",
        "description",
    )
    list_filter = ("transaction_type", "amount", "date", "income_expense_type")
    search_fields = ("description",)


admin.site.register(Transaction, TransactionAdmin)
