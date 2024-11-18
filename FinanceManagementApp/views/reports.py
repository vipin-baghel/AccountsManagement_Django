from django.shortcuts import render
from django.views import View

from ..models.Transaction import Transaction
from ..models.Project import Project


class ReportsView(View):
    def get(self, request):
        transactions = Transaction.objects.all().order_by("-date")
        projects = Project.objects.all()

        # Render the template with the filtered transactions
        return render(
            request,
            "FinanceManagementApp/reports.html",
            {"transactions": transactions, "projects": projects},
        )
