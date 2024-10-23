
# expense/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('user/<int:user_id>/', views.user_details, name='user_details'),
]
