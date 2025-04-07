from django.contrib import admin
from .models import users, transaction
# Register your models here.

admin.site.register(users)
admin.site.register(transaction)