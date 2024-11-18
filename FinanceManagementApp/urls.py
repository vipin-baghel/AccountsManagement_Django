# urls.py
from django.urls import path

from .views.transactions import AllTransactionsView
from .views.dashboard import DashboardView
from .views.reports import ReportsView

urlpatterns = [
    path("", DashboardView.as_view(), name=""),
    path("transactions/", AllTransactionsView.as_view(), name="transactions"),
    path("reports/", ReportsView.as_view(), name="reports"),
]
