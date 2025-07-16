from django.urls import path
from . import views

app_name = 'transactions'

urlpatterns = [
    path('add_income/', views.add_income, name='add_income'),
    path('add_expense/', views.add_expense, name='add_expense'),
    path('view_transactions/', views.view_transactions, name='view_transactions'),
    path('view_transaction/<int:transaction_id>/', views.view_transaction, name='view_transaction'),
    path('delete/<int:transaction_id>/', views.delete, name='delete'),
    path('update/<int:transaction_id>/', views.update, name='update'),
    path('upload_pdf/', views.upload_pdf, name='upload_pdf'),
    path('save_pdf_transactions/', views.save_pdf_transactions, name ='save_pdf_transactions'),
]
