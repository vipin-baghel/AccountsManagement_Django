from django.shortcuts import render
from django.views import View

from AccountsManagementApp.models.Transaction import Transaction
from AccountsManagementApp.models.Project import Project


class ReportsView(View):
    def get(self, request):
        transactions = Transaction.objects.all().order_by("-date")
        projects = Project.objects.all()

        # Render the template with the filtered transactions
        return render(
            request,
            "AccountsManagementApp/reports.html",
            {"transactions": transactions, "projects": projects},
        )
