from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar, name='booking_calendar'),
    path('create/', views.create, name='booking_create'),  
]