# views.py
from datetime import datetime, timedelta
from django.shortcuts import render
from django.views import View
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from AccountsManagementApp.models.Transaction import Transaction


class DashboardView(View):
    def post(self, request):
        pass

    def get(self, request):
        # Fetch the 10 most recent transactions
        recent_transactions = Transaction.objects.select_related("project").order_by(
            "-date"
        )[:10]

        this_month_start = datetime.now().replace(day=1)
        this_month_end = (datetime.now() + relativedelta(months=1)).replace(
            day=1
        ) - timedelta(days=1)

        this_year_start = datetime.now().replace(month=1, day=1)
        this_year_end = datetime.now().replace(month=12, day=31)

        revenue_this_month = (
            Transaction.objects.filter(
                date__gte=this_month_start,
                date__lte=this_month_end,
                transaction_type="income",
            ).aggregate(total_amount=Sum("amount"))["total_amount"]
            or 0
        )

        expense_this_month = (
            Transaction.objects.filter(
                date__gte=this_month_start,
                date__lte=this_month_end,
                transaction_type="expense",
            ).aggregate(total_amount=Sum("amount"))["total_amount"]
            or 0
        )

        revenue_this_year = (
            Transaction.objects.filter(
                date__gte=this_year_start,
                date__lte=this_year_end,
                transaction_type="income",
            ).aggregate(total_amount=Sum("amount"))["total_amount"]
            or 0
        )

        expense_this_year = (
            Transaction.objects.filter(
                date__gte=this_year_start,
                date__lte=this_year_end,
                transaction_type="expense",
            ).aggregate(total_amount=Sum("amount"))["total_amount"]
            or 0
        )

        return render(
            request,
            "AccountsManagementApp/dashboard.html",
            {
                "revenue_this_month": revenue_this_month,
                "expense_this_month": expense_this_month,
                "revenue_this_year": revenue_this_year,
                "expense_this_year": expense_this_year,
                "recent_transactions": recent_transactions,
            },
        )
