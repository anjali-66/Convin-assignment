
# expense/views.py
from django.shortcuts import render
from .models import User, Expense

def home(request):
    return render(request, 'expense/home.html')

def user_details(request, user_id):
    user = User.objects.get(id=user_id)
    expenses = Expense.objects.filter(created_by=user)
    context = {
        'user': user,
        'expenses': expenses
    }
    return render(request, 'expense/user_details.html', context)
