from django.shortcuts import redirect, render
from django.http import HttpResponse
from core.models import transaction,users  # Assuming you have a Transaction model defined in core.models
from .forms import filters
from django.db import models

def total_income_period(user_id, start_date, end_date):
    if not start_date:
        start_date = '1800-01-01'
    if not end_date:
        end_date = '9999-12-31'
    total_income = transaction.objects.filter(
        user=users.objects.get(pk=user_id),
        transaction_type='Income',
        date__range=[start_date, end_date]
    ).aggregate(total_income=models.Sum('amount'))['total_income']

    return total_income if total_income else 0  # Return 0 if no income found

def total_expense_period(user_id, start_date, end_date):
    if not start_date:
        start_date = '1800-01-01'
    if not end_date:
        end_date = '9999-12-31'
    total_expense = transaction.objects.filter(
        user=users.objects.get(pk=user_id),
        transaction_type='Expense',
        date__range=[start_date, end_date]
    ).aggregate(total_expense=models.Sum('amount'))['total_expense']
    return total_expense if total_expense else 0  # Return 0 if no expense found

def analytics(request):
    user_id = request.session.get('user_id')  # Retrieve user ID from session
    if not user_id:
        return redirect('login')  # Redirect to login if user ID is not found
    form = filters()  # Initialize the form with POST data if available
    context = {
        'form':form,
    }
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        category = request.GET.get('category')
        amount_min = request.GET.get('amount_min')
        amount_max = request.GET.get('amount_max')
        transaction_type = request.GET.get('transaction_type')

        transactions = transaction.objects.filter(user=users.objects.get(pk=user_id))

        if start_date:
            transactions = transactions.filter(date__gte=start_date)
        if end_date:
            transactions = transactions.filter(date__lte=end_date)
        if category:
            transactions = transactions.filter(category=category)
        if amount_min:
            transactions = transactions.filter(amount__gte=amount_min)
        if amount_max:
            transactions = transactions.filter(amount__lte=amount_max)
        if transaction_type:
            transactions = transactions.filter(transaction_type=transaction_type)
        
        context['transactions'] = transactions  # Add transactions to context
        context['total_income'] = total_income_period(user_id, start_date, end_date)
        context['total_expense'] = total_expense_period(user_id, start_date, end_date)
        context['balance'] = context['total_income'] - context['total_expense']
    
    return render(request, 'analytics.html',context)