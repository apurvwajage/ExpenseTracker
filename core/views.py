from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import RegisterForm, LoginForm, TransactionForm
from .models import users, transaction
from django.contrib import messages
from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone
from django.db.models import Sum
from django.contrib.auth import logout

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    form = LoginForm()  # Initialize the form
    context = {'form': form}  # Prepare context for rendering
    if request.method == 'POST':
        form = LoginForm(request.POST)  # Bind the form to the POST data
        if form.is_valid():  # Check if the form is valid
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                user = users.objects.get(email=email)  # Fetch user from custom table
                if check_password(password, user.password):  # Validate hashed password
                    # Store user ID in session
                    request.session['user_id'] = user.pk  # Use the primary key as user ID
                    return redirect('core:dashboard')  # Redirect to the dashboard view
                else:
                    context['error_message'] = "Invalid username or password. Please try again."
            except users.DoesNotExist:
                context['error_message'] = "User  not found. Please register first."
        else:
            context['error_message'] = "Invalid form input. Please check the following errors:"
            context['form_errors'] = form.errors  # Capture form errors
    return render(request, 'login.html', context)

def register(request):
    form = RegisterForm()
    success = False
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Prevent immediate save
            user.password = make_password(form.cleaned_data['password'])  # Hash password
            user.save()
            success = True
        else:
            messages.error(request, "Invalid input. Please correct the errors.")

    context = {
        'success': success,
        'form': form
    }
    return render(request, 'register.html', context)

def get_total_income(user_id):
    now = timezone.now()
    user = users.objects.get(pk=user_id)
    transactions = transaction.objects.filter(user=user, transaction_type='Income',date__year=now.year,
        date__month=now.month)
    total_income = sum(t.amount for t in transactions)
    return total_income


def get_total_expenses(user_id):
    user = users.objects.get(pk=user_id)  # Fetch user from custom table
    now = timezone.now()
    transactions = transaction.objects.filter(user=user, transaction_type='Expense', date__year = now.year,
        date__month = now.month)
    total_expenses = sum(t.amount for t in transactions)
    return total_expenses


def expenditure_by_category(user_id):
    total_expenses = transaction.objects.filter(
        user=users.objects.get(pk = user_id),
        transaction_type='Expense'  # Filter for expenses
    ).values('category').annotate(
        total_amount=Sum('amount')  # Sum the amounts for each category
    )
    print("Total expenses")
    return total_expenses

def dashboard(request):
    user_id = request.session.get('user_id')  # Retrieve user ID from session
    if not user_id:
        return redirect('login')  # Redirect to login if user ID is not found
    username = users.objects.get(pk=user_id).username  # Fetch username from the database
    total_income = get_total_income(user_id)  # Calculate total income
    total_expenses = get_total_expenses(user_id)  # Calculate total expenses
    net_balance = total_income-total_expenses
    # Retrieving the first 3 transactions
    recent_transactions = transaction.objects.filter(user=users.objects.get(pk = user_id)).order_by('-date')[:3]

    context = {
        'user_id':user_id,
        'username': username,
        'recent_transactions': recent_transactions,
        'total_income': total_income,
        'total_expenses': total_expenses,
        'net_balance': net_balance,
        'expenditure_by_category': expenditure_by_category(user_id),
    }
    return render(request, 'dashboard.html', context)

def logout_view(request):
    logout(request)  # Log out the user
    return redirect('/login/')  # Redirect to the login page or any other page 