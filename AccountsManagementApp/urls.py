# urls.py
from django.urls import path

from .views.transactions import AllTransactionsView
from .views.dashboard import DashboardView


urlpatterns = [
    path("", DashboardView.as_view(), name=""),
    path("transactions/", AllTransactionsView.as_view(), name="transactions"),
]
