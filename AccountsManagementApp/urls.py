# urls.py
from django.urls import path

from AccountsManagementApp.views.all_transactions import AllTransactionsView
from .views.dashboard import DashboardView

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("all_transactions/", AllTransactionsView.as_view(), name="all_transactions"),
]
