from django.shortcuts import render
from django.views import View

from AccountsManagementApp.models.Transaction import Transaction


class AllTransactionsView(View):

    def get(self, request):
        transactions = Transaction.objects.all()
        return render(
            request,
            "AccountsManagementApp/all_transactions.html",
            {"transactions": transactions},
        )
