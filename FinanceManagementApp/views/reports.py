from datetime import datetime
from ..models.Transaction import Transaction
from django.db.models import Sum, Q
import plotly.graph_objs as go
from dateutil.relativedelta import relativedelta
from django.views.generic import TemplateView

FINANCIAL_YEAR_START_MONTH = 4
FINANCIAL_YEAR_END_MONTH = 3


class ReportsView(TemplateView):
    """
    A view that displays the dashboard.
    """

    template_name = "FinanceManagementApp/reports.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        this_year_start, this_year_end = self.get_financial_year_dates(datetime.now())

        context["graph_html_project_wise"] = self.generate_graph_project_wise()

        context["graph_html_this_year_expense"] = self.generate_graph_this_year_expense(
            this_year_start, this_year_end
        )

        context["graph_html_this_year_income"] = self.generate_graph_this_year_income(
            this_year_start, this_year_end
        )

        return context

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

    def generate_graph_this_year_expense(self, this_year_start, this_year_end):
        """Plot this financial year's expense"""

        this_year_expense = (
            Transaction.objects.filter(
                date__gte=this_year_start,
                date__lte=this_year_end,
                transaction_type="Expense",
            )
            .values("income_expense_type")
            .annotate(total_amount=Sum("amount"))
        )
        total_expense_amount = sum(item["total_amount"] for item in this_year_expense)

        fig = go.Figure(
            data=[
                go.Pie(
                    labels=[data["income_expense_type"] for data in this_year_expense],
                    values=[data["total_amount"] for data in this_year_expense],
                    textinfo="label+percent",
                    textposition="auto",
                    hoverinfo="text",
                    hovertext=[
                        f"{data['total_amount']:,}" for data in this_year_expense
                    ],
                )
            ]
        )

        fig.update_layout(
            title=f"This Year's Expenses (Total: {total_expense_amount:,})",
        )

        this_year_expense_html = fig.to_html(include_plotlyjs="cdn")

        return this_year_expense_html

    def generate_graph_this_year_income(self, this_year_start, this_year_end):
        """Plot this financial year's income"""
        this_year_income = (
            Transaction.objects.filter(
                date__gte=this_year_start,
                date__lte=this_year_end,
                transaction_type="Income",
            )
            .values("income_expense_type")
            .annotate(total_amount=Sum("amount"))
        )

        total_income_amount = sum(item["total_amount"] for item in this_year_income)

        fig_income = go.Figure(
            data=[
                go.Pie(
                    labels=[data["income_expense_type"] for data in this_year_income],
                    values=[data["total_amount"] for data in this_year_income],
                    textinfo="label+percent",
                    textposition="auto",
                    hoverinfo="text",
                    hovertext=[
                        f"{data['total_amount']:,}" for data in this_year_income
                    ],
                )
            ]
        )

        fig_income.update_layout(
            title=f"This Year's Income (Total: {total_income_amount:,})",
        )

        this_year_income_html = fig_income.to_html(include_plotlyjs="cdn")

        return this_year_income_html

    def generate_graph_project_wise(self):
        """Plot project-wise income and expense data"""

        project_data = Transaction.objects.values("project__name").annotate(
            income=Sum("amount", filter=Q(transaction_type="Income")),
            expense=Sum("amount", filter=Q(transaction_type="Expense")),
        )

        profit = [data["income"] - data["expense"] for data in project_data]

        fig = go.Figure(
            data=[
                go.Bar(
                    name="Income",
                    y=[data["project__name"] for data in project_data],
                    x=[data["income"] for data in project_data],
                    text=[f"{data['income']:,}" for data in project_data],
                    textposition="auto",
                    orientation="h",
                ),
                go.Bar(
                    name="Expense",
                    y=[data["project__name"] for data in project_data],
                    x=[data["expense"] for data in project_data],
                    text=[f"{data['expense']:,}" for data in project_data],
                    textposition="auto",
                    orientation="h",
                ),
                go.Bar(
                    name="Profit",
                    y=[data["project__name"] for data in project_data],
                    x=profit,
                    text=[f"{value:,}" for value in profit],
                    textposition="auto",
                    orientation="h",
                ),
            ]
        )

        fig.update_layout(
            title="Report for All Projects",
            xaxis_title="Amount",
            yaxis_title="Project Name",
            barmode="group",
            autosize=True,
            height=300 + (len(project_data) * 70),
            yaxis=dict(ticklen=100),  # add more space between ticks
        )

        graph_html_project_wise = fig.to_html(include_plotlyjs="cdn")

        return graph_html_project_wise
