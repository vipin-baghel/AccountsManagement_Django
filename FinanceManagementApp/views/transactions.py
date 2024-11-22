from ..models.Transaction import Transaction
from ..models.Project import Project

from django.views.generic import TemplateView


class AllTransactionsView(TemplateView):
    template_name = "FinanceManagementApp/transactions.html"

    def get_transactions(self, request):

        transactions = Transaction.objects.all().order_by("-date")

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

        # Return the filtered transactions
        return transactions

    def get_projects(self):
        # Return the projects
        return Project.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["transactions"] = self.get_transactions(request=self.request)
        context["projects"] = self.get_projects()
        return context
