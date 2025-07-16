import io
from django.shortcuts import render,redirect
from datetime import datetime
from core.models import users,transaction
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from .forms import ExpenseForm, IncomeForm, PDFform
from django.utils.text import slugify
from core.forms import TransactionForm
from django.conf import settings
import fitz
import re
import uuid
import os


#-------------------------------------------- Function to add Income---------------------------------------------
def add_income(request):
    user_id = request.session.get('user_id')  # Retrieve user ID from session
    if not user_id:
        return redirect('login')  # Redirect to login if user ID is not found
    if request.method == 'POST':
        try:
            user = users.objects.get(pk=user_id)  # Fetch user from custom table
            amount = request.POST.get('amount')
            description = request.POST.get('description')
            category = request.POST.get('category')
            transaction_type = 'Income'
            date = request.POST.get('date')
            
            # Create a new transaction object and save it to the database
            new_transaction = transaction(
                user=user,
                amount=amount,
                description=description,
                category=category,
                transaction_type=transaction_type,
                date=date
            )
            new_transaction.save()
        except:
            return HttpResponse("Error: Invalid data or user not found.")
        
        return redirect('/dashboard/')
    else:
        form = IncomeForm()
        context = {'form': form}
        return render(request, 'add_income.html', context)
    
#------------------------------------------------------- Function to add Expense--------------------------------------------------
def add_expense(request):
    user_id = request.session.get('user_id')  # Retrieve user ID from session
    if not user_id:
        return redirect('login')  # Redirect to login if user ID is not found
    if request.method == 'POST':
        try:
            user = users.objects.get(pk=user_id)  # Fetch user from custom table
            amount = request.POST.get('amount')
            description = request.POST.get('description')
            category = request.POST.get('category')
            transaction_type = 'Expense'
            date = request.POST.get('date')
            
            # Create a new transaction object and save it to the database
            new_transaction = transaction(
                user=user,
                amount=amount,
                description=description,
                category=category,
                transaction_type=transaction_type,
                date=date
            )
            new_transaction.save()
        except:
            return HttpResponse("Error: Invalid data or user not found.")
        
        return redirect('/dashboard/')
    else:
        form = ExpenseForm()
        context = {'form': form}
        return render(request, 'add_expense.html', context)
    
#------------------------------------------------------- Function to view all transactions---------------------------------------------------------
def view_transactions(request):
    user_id = request.session.get('user_id')  # Retrieve user ID from session
    if not user_id:
        return redirect('login')  # Redirect to login if user ID is not found
    transactions = transaction.objects.filter(user=users.objects.get(pk=user_id)).order_by('-date')  # Fetch transactions for the logged-in user
    context = {
        'transactions': transactions,  # Pass transactions to the template
    }
    return render(request, 'view_transactions.html', context)


#------------------------------------------------------- Function to view a single transaction----------------------------------------------------
def view_transaction(request, transaction_id):
    user_id = request.session.get('user_id')  # Retrieve user ID from session
    if not user_id:
        return redirect('login')  # Redirect to login if user ID is not found
    try:
        transaction_obj = transaction.objects.get(pk=transaction_id, user= users.objects.get(pk = user_id))  # Fetch transaction by ID
        context = {'transaction': transaction_obj}
        return render(request, 'view_transaction.html', context)
    except transaction.DoesNotExist:
        return HttpResponse("Transaction not found.")
    
#------------------------------------------------------- Function to update transaction--------------------------------------------------------------
def update(request,transaction_id):
    user_id = request.session.get('user_id')  # Retrieve user ID from session
    if not user_id:
        return redirect('login')  # Redirect to login if user ID is not found
    try:
        transaction_instance = transaction.objects.get(pk=transaction_id)  # Fetch transaction instance
    except transaction.DoesNotExist:
        return HttpResponse("Transaction not found.")
    
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction_instance)  # Bind the form to the instance
        if form.is_valid():
            form.save()  # Save the updated transaction
            return redirect( "transactions:view_transactions")
    else:
        form = TransactionForm(instance=transaction_instance)  # Pre-fill the form with existing data
    
    context = {'form': form}
    return render(request, 'update_transaction.html', context)

#------------------------------------------------------- Function delete transaction-----------------------------------------------------------------
def delete(request,transaction_id):
    user_id = request.session.get('user_id')  # Retrieve user ID from session
    if not user_id:
        return redirect('login')  # Redirect to login if user ID is not found
    try:
        transaction_instance = transaction.objects.get(pk=transaction_id,user = users.objects.get(pk=user_id))  # Fetch transaction instance
        transaction_instance.delete()  # Delete the transaction
        return redirect("transactions:view_transactions")
    except transaction.DoesNotExist:
        return HttpResponse("Transaction not found.")
    
    #-----------------------------------------------------------PDF Extraction-----------------------------------------------------------------------

def data_extraction(pdf_file):
    try:
        # Open the PDF file
        print("Inside data extraction method")
        # Use BytesIO to ensure fitz.open gets a proper stream
        file_stream = io.BytesIO(pdf_file.read())

        doc = fitz.open(stream=file_stream, filetype="pdf")
        print("2")

        # Extract text from all pages
        text = ''
        for page in doc:
            text += page.get_text("text")  # Extract text from each page

        # Convert the extracted text to a single line and clean it
        single_line_text = ''.join(text.split())
        single_line_text = single_line_text.replace("\x01", "")  # Remove unwanted characters
        single_line_text = re.sub(r'(\d{1,2})f(\d{1,2}\s*[APMapm]{2})', r'\1:\2', single_line_text)
        

        print(single_line_text)

        # Define the regex pattern
        pattern = r"(\w{3}\d{2},\d{4})(\d{1,2}:\d{2}[APMapm]{2})(DEBIT|CREDIT)₹(\d{1,3}(?:,\d{3})*(?:\.\d{2})?)(\w+(?:\s+\w+)*)(TransactionID[A-Z0-9]+\d{1})"

        # Find matches using the regex pattern
        matches = re.finditer(pattern, single_line_text)

        # Create a list to hold dictionaries of matches
        matches_list = []

        # Iterate through matches and create dictionaries
        for match in matches:
            date = match.group(1)

            # Convert the string to a datetime object
            date_object = datetime.strptime(date, "%b%d,%Y")

            # Format the datetime object to a desired format (e.g., YYYY-MM-DD)
            formatted_date = date_object.strftime("%Y-%m-%d")
            
            match_dict = {
                "formatted_date": formatted_date,
                "date": match.group(1),
                "time": match.group(2),
                "type": match.group(3),
                "amount": match.group(4),
                "details": match.group(5),
                "transaction_id": match.group(6)
            }
            matches_list.append(match_dict)  # Append the dictionary to the list

        return matches_list  # Return the list of matches
    except Exception as e:
            print("❌ Error extracting PDF:", e)
        

def upload_pdf(request):
    user_id = request.session.get('user_id')  # Retrieve user ID from session
    if not user_id:
        return redirect('login')  # Redirect to login if user ID is not found
    form = PDFform()
    context = {'form': form}
    if request.method == 'POST':
        form = PDFform(request.POST, request.FILES)
        if form.is_valid():
            pdf_file = form.cleaned_data['pdf']  # Get the uploaded PDF file
            matches_list = data_extraction(pdf_file)
            return render(request, 'pdf_result.html', {'matches_list': matches_list})
    return render(request, 'upload_pdf.html', context)

def save_pdf_transactions(request):
    user_id = request.session.get('user_id')  # Retrieve user ID from session
    if not user_id:
        return redirect('login')  # Redirect to login if user ID is not found
    if request.method == "POST":
        selected_transactions = request.POST.getlist('selectedTransactions')  # Get the list of selected transaction IDs
        
        for transaction_id in selected_transactions:
            description  = request.POST.get(f'details_{transaction_id}') +" " +transaction_id
            amount_str =request.POST.get(f'amount_{transaction_id}')
            amount = amount_str.replace(',', '')
            type = request.POST.get(f'type_{transaction_id}')
            if type.lower() == 'debit':
                type = 'Expense'
            else:
                type = 'Income'
            
            # Create a new transaction object and save it to the database
            new_transaction = transaction(
                user=users.objects.get(pk =user_id),
                amount=amount,
                description=description,
                category=request.POST.get(f'category_{transaction_id}'),
                transaction_type=type,
                date= request.POST.get(f'date_{transaction_id}')
            )
            new_transaction.save()

    return redirect('transactions:view_transactions')
    
