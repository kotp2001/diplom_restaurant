from django.shortcuts import render
from .models import Dish, Category

def index(request):
    return render(request, 'index.html')

def public_menu(request):
    dishes = Dish.objects.filter(is_available=True).select_related('category')
    categories = Category.objects.all().order_by('order')
    
    context = {
        'dishes': dishes,
        'categories': categories,
    }
    return render(request, 'public/menu.html', context)