from datetime import datetime, timedelta
from django.views.generic import TemplateView
from dateutil.relativedelta import relativedelta
from django.db.models import Sum, Q
from ..models.Transaction import Transaction
import plotly.graph_objs as go

RECENT_TRANSACTIONS_LIMIT = 10
FINANCIAL_YEAR_START_MONTH = 4
FINANCIAL_YEAR_END_MONTH = 3


class DashboardView(TemplateView):
    """
    A view that displays the dashboard.
    """

    template_name = "FinanceManagementApp/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["recent_transactions"] = Transaction.objects.select_related(
            "project"
        ).order_by("-date")[:RECENT_TRANSACTIONS_LIMIT]

        current_datetime = datetime.now()

        this_month_start, this_month_end = self.get_this_month_dates(current_datetime)
        this_year_start, this_year_end = self.get_financial_year_dates(current_datetime)

        context["graph_html_project_wise"] = self.generate_graph_project_wise()

        context["graph_html_this_month"] = self.generate_graph_this_month(
            this_month_start, this_month_end
        )

        context["graph_html_this_year"] = self.generate_graph_this_year(
            this_year_start, this_year_end
        )

        return context

    def get_this_month_dates(self, current_datetime: datetime) -> tuple:
        this_month_start = current_datetime.replace(day=1)
        this_month_end = (current_datetime + relativedelta(months=1)).replace(
            day=1
        ) - timedelta(days=1)
        return this_month_start, this_month_end

    def get_financial_year_dates(self, now: datetime) -> tuple:
        if now.month < FINANCIAL_YEAR_START_MONTH:
            this_year_start = (now - relativedelta(years=1)).replace(
                month=FINANCIAL_YEAR_START_MONTH, day=1
            )
            this_year_end = now.replace(month=FINANCIAL_YEAR_END_MONTH, day=31)
        else:
            this_year_start = now.replace(month=FINANCIAL_YEAR_START_MONTH, day=1)
            this_year_end = (now + relativedelta(years=1)).replace(
                month=FINANCIAL_YEAR_END_MONTH, day=31
            )
        return this_year_start, this_year_end

    def generate_graph_this_month(self, this_month_start, this_month_end):
        # Plot this month's revenue, expense, and profit

        this_month_revenue = (
            Transaction.objects.filter(
                date__gte=this_month_start,
                date__lte=this_month_end,
                transaction_type="Income",
            ).aggregate(total_amount=Sum("amount"))["total_amount"]
            or 0
        )
        this_month_expense = (
            Transaction.objects.filter(
                date__gte=this_month_start,
                date__lte=this_month_end,
                transaction_type="Expense",
            ).aggregate(total_amount=Sum("amount"))["total_amount"]
            or 0
        )
        this_month_profit = this_month_revenue - this_month_expense

        # Create a Plotly figure for this month's revenue, expense, and profit
        fig_this_month = go.Figure(
            data=[
                go.Bar(
                    name="Revenue",
                    x=["This Month"],
                    y=[this_month_revenue],
                    text=[f"{this_month_revenue:,}"],
                    textposition="auto",
                ),
                go.Bar(
                    name="Expense",
                    x=["This Month"],
                    y=[this_month_expense],
                    text=[f"{this_month_expense:,}"],
                    textposition="auto",
                ),
                go.Bar(
                    name="Profit",
                    x=["This Month"],
                    y=[this_month_profit],
                    text=[f"{this_month_profit:,}"],
                    textposition="auto",
                ),
            ]
        )
        # Update the layout
        fig_this_month.update_layout(
            title="This Month's Revenue, Expense, and Profit", barmode="group"
        )
        # Convert the figure to HTML
        graph_html_this_month = fig_this_month.to_html(include_plotlyjs="cdn")

        return graph_html_this_month

    def generate_graph_this_year(self, this_year_start, this_year_end):
        # Plot this financial year's revenue, expense, and profit

        this_year_revenue = (
            Transaction.objects.filter(
                date__gte=this_year_start,
                date__lte=this_year_end,
                transaction_type="Income",
            ).aggregate(total_amount=Sum("amount"))["total_amount"]
            or 0
        )

        this_year_expense = (
            Transaction.objects.filter(
                date__gte=this_year_start,
                date__lte=this_year_end,
                transaction_type="Expense",
            ).aggregate(total_amount=Sum("amount"))["total_amount"]
            or 0
        )
        this_year_profit = this_year_revenue - this_year_expense

        # Create a Plotly figure
        fig_this_year = go.Figure(
            data=[
                go.Bar(
                    name="Revenue",
                    x=["This Financial Year"],
                    y=[this_year_revenue],
                    text=[f"{this_year_revenue:,}"],
                    textposition="auto",
                ),
                go.Bar(
                    name="Expense",
                    x=["This Financial Year"],
                    y=[this_year_expense],
                    text=[f"{this_year_expense:,}"],
                    textposition="auto",
                ),
                go.Bar(
                    name="Profit",
                    x=["This Financial Year"],
                    y=[this_year_profit],
                    text=[f"{this_year_profit:,}"],
                    textposition="auto",
                ),
            ]
        )

        # Update the layout
        fig_this_year.update_layout(
            title="This Financial Year's Revenue, Expense, and Profit", barmode="group"
        )

        # Convert the figure to HTML
        graph_html_this_year = fig_this_year.to_html(include_plotlyjs="cdn")

        return graph_html_this_year

    def generate_graph_project_wise(self):
        # Plot project-wise income and expense data, 5 most recent by start date
        project_data = (
            Transaction.objects.values("project__name")
            .annotate(
                income=Sum("amount", filter=Q(transaction_type="Income")),
                expense=Sum("amount", filter=Q(transaction_type="Expense")),
            )
            .order_by("project__start_date")
            .reverse()[:5]
        )
        #  list to store profit values
        profit = [data["income"] - data["expense"] for data in project_data]

        # Create a Plotly figure for project-wise income, expense, and profit
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
                go.Bar(
                    name="Profit",
                    x=[data["project__name"] for data in project_data],
                    y=profit,
                    text=[f"{value:,}" for value in profit],
                    textposition="auto",
                ),
            ]
        )

        # Update the layout
        fig.update_layout(
            title="Revenue, Expense, and Profit report for Recent projects",
            barmode="group",
        )

        # Convert the figure to HTML
        graph_html_project_wise = fig.to_html(include_plotlyjs="cdn")

        return graph_html_project_wise
