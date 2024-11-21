from django.shortcuts import render
from django.views import View
from datetime import datetime
from ..models.Transaction import Transaction
from django.db.models import Sum, Q
import plotly.graph_objs as go
from dateutil.relativedelta import relativedelta


class ReportsView(View):
    def get(self, request):

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

        # Create a Plotly figure for this year's income
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

        # Create a Plotly figure for this year's expense
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

        # Update the layout
        fig.update_layout(
            title=f"This Year's Expenses (Total: {total_expense_amount:,})",
        )
        # Convert the figure to HTML
        this_year_expense_html = fig.to_html(include_plotlyjs="cdn")

        #####################################################################
        # Get project-wise income and expense data
        project_data = Transaction.objects.values("project__name").annotate(
            income=Sum("amount", filter=Q(transaction_type="Income")),
            expense=Sum("amount", filter=Q(transaction_type="Expense")),
        )
        #  list to store profit values
        profit = [data["income"] - data["expense"] for data in project_data]
        # Create a Plotly figure for project-wise income, expense, and profit
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
        # Update the layout
        fig.update_layout(
            title="Report for All Projects",
            xaxis_title="Amount",
            yaxis_title="Project Name",
            barmode="group",
            autosize=True,
            height=300 + (len(project_data) * 70),
            yaxis=dict(ticklen=100),  # add more space between ticks
        )
        # Convert the figure to HTML
        graph_html_project_wise = fig.to_html(include_plotlyjs="cdn")

        ###################################################
        # Render the template with the graphs
        return render(
            request,
            "FinanceManagementApp/reports.html",
            {
                "graph_html_project_wise": graph_html_project_wise,
                "graph_html_this_year_expense": this_year_expense_html,
                "graph_html_this_year_income": this_year_income_html,
            },
        )
