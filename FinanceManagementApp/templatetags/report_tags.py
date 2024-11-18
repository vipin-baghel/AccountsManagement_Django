# report_tags.py

from django import template
from ..models.Transaction import Transaction
from django.db.models import Sum

register = template.Library()


@register.filter
def get_income(project):
    return (
        Transaction.objects.filter(
            project=project, transaction_type="Income"
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )


@register.filter
def get_expenses(project):
    return (
        Transaction.objects.filter(
            project=project, transaction_type="Expense"
        ).aggregate(Sum("amount"))["amount__sum"]
        or 0
    )


@register.filter
def get_profit(project):
    income = get_income(project)
    expenses = get_expenses(project)
    return income - expenses
