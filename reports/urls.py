from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.analytics, name='analytics'),  # URL for the reports page
]