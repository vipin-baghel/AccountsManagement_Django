# views.py
from django.shortcuts import render
from django.views import View

from AccountsManagementApp.models.Project import Project
from AccountsManagementApp.models.Transaction import Transaction


class DashboardView(View):
    def post(self, request):
        pass

    def get(self, request):
        ongoing_projects = Project.objects.filter(status="ongoing")
        completed_projects = Project.objects.filter(status="completed")
        upcoming_projects = Project.objects.filter(status="upcoming")
        recent_transactions = Transaction.objects.select_related("project").order_by(
            "-date"
        )[
            :10
        ]  # Fetch the 10 most recent transactions

        return render(
            request,
            "AccountsManagementApp/dashboard.html",
            {
                "ongoing_projects": ongoing_projects,
                "completed_projects": completed_projects,
                "upcoming_projects": upcoming_projects,
                "recent_transactions": recent_transactions,
            },
        )
