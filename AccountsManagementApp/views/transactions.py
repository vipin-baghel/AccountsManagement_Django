from django.shortcuts import render
from django.views import View

from AccountsManagementApp.models.Transaction import Transaction
from AccountsManagementApp.models.Project import Project


class AllTransactionsView(View):
    def get(self, request):
        transactions = Transaction.objects.all().order_by("-date")
        projects = Project.objects.all()

        # Get filter parameters from the request
        project_id = request.GET.get("project")
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        # Apply filters
        if project_id:
            transactions = transactions.filter(project_id=project_id)
        if start_date:
            transactions = transactions.filter(date__gte=start_date)
        if end_date:
            transactions = transactions.filter(date__lte=end_date)

        # Render the template with the filtered transactions
        return render(
            request,
            "AccountsManagementApp/transactions.html",
            {"transactions": transactions, "projects": projects},
        )
