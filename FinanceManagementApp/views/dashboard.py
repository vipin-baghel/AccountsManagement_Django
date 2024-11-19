# views.py
from datetime import datetime, timedelta
from django.shortcuts import render
from django.views import View
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, Q
from ..models.Transaction import Transaction
import plotly.graph_objs as go


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

        current_date = datetime.now()
        if current_date.month < 4:
            this_year_start = (current_date - relativedelta(years=1)).replace(
                month=4, day=1
            )
            this_year_end = current_date.replace(month=3, day=31)
        else:
            this_year_start = current_date.replace(month=4, day=1)
            this_year_end = (current_date + relativedelta(years=1)).replace(
                month=3, day=31
            )

        revenue_this_month = (
            Transaction.objects.filter(
                date__gte=this_month_start,
                date__lte=this_month_end,
                transaction_type="Income",
            ).aggregate(total_amount=Sum("amount"))["total_amount"]
            or 0
        )

        expense_this_month = (
            Transaction.objects.filter(
                date__gte=this_month_start,
                date__lte=this_month_end,
                transaction_type="Expense",
            ).aggregate(total_amount=Sum("amount"))["total_amount"]
            or 0
        )

        revenue_this_year = (
            Transaction.objects.filter(
                date__gte=this_year_start,
                date__lte=this_year_end,
                transaction_type="Income",
            ).aggregate(total_amount=Sum("amount"))["total_amount"]
            or 0
        )

        expense_this_year = (
            Transaction.objects.filter(
                date__gte=this_year_start,
                date__lte=this_year_end,
                transaction_type="Expense",
            ).aggregate(total_amount=Sum("amount"))["total_amount"]
            or 0
        )

        # Get project-wise income and expense data, 5 most recent by start date
        project_data = (
            Transaction.objects.values("project__name")
            .annotate(
                income=Sum("amount", filter=Q(transaction_type="Income")),
                expense=Sum("amount", filter=Q(transaction_type="Expense")),
            )
            .order_by("project__start_date")
            .reverse()[:5]
        )

        # Create a Plotly figure
        fig = go.Figure(
            data=[
                go.Bar(
                    name="Income",
                    x=[data["project__name"] for data in project_data],
                    y=[data["income"] for data in project_data],
                    text=[f"{data['income']:,}" for data in project_data],
                    textposition="auto",
                ),
                go.Bar(
                    name="Expense",
                    x=[data["project__name"] for data in project_data],
                    y=[data["expense"] for data in project_data],
                    text=[f"{data['expense']:,}" for data in project_data],
                    textposition="auto",
                ),
            ]
        )

        # Update the layout
        fig.update_layout(barmode="group")

        # Convert the figure to HTML
        graph_html = fig.to_html(include_plotlyjs="cdn")

        # Render the dashboard template
        return render(
            request,
            "FinanceManagementApp/dashboard.html",
            {
                "revenue_this_month": revenue_this_month,
                "expense_this_month": expense_this_month,
                "revenue_this_year": revenue_this_year,
                "expense_this_year": expense_this_year,
                "recent_transactions": recent_transactions,
                "graph_html": graph_html,
            },
        )
