from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('orders/', views.orders_report, name='orders_report'),
    path('dishes/', views.dishes_report, name='dishes_report'),
]