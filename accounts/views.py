from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count
from .models import Profile
from tables.models import Table
from orders.models import Order

def waiter_login(request):
    if request.method == 'POST':
        pin = request.POST.get('pin')
        try:
            profile = Profile.objects.get(pin_code=pin, role='waiter')
            login(request, profile.user)
            return redirect('waiter_hall')
        except Profile.DoesNotExist:
            return render(request, 'waiter_login.html', {'error': 'Неверный пин-код'})
    return render(request, 'waiter_login.html')

def waiter_hall(request):
    if not request.user.is_authenticated:
        return redirect('waiter_login')
    
    tables = Table.objects.all()
    
    # Для каждого стола найдём текущий открытый заказ
    for table in tables:
        table.current_order = Order.objects.filter(table=table, status='open').first()
    
    return render(request, 'waiter_hall.html', {'tables': tables})

@login_required
def waiter_history(request):
    if not request.user.is_authenticated or request.user.profile.role != 'waiter':
        return redirect('waiter_login')
    
    # Получаем параметры фильтрации
    period = request.GET.get('period', 'today')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    # Базовый запрос - только заказы текущего официанта
    orders = Order.objects.filter(
        waiter=request.user,
        status='paid'
    ).order_by('-created_at')
    
    # Фильтр по периоду
    today = timezone.now().date()
    
    if period == 'today':
        orders = orders.filter(created_at__date=today)
    elif period == 'week':
        week_ago = today - timedelta(days=7)
        orders = orders.filter(created_at__date__gte=week_ago)
    elif period == 'month':
        month_ago = today - timedelta(days=30)
        orders = orders.filter(created_at__date__gte=month_ago)
    elif period == 'custom':
        if date_from:
            orders = orders.filter(created_at__date__gte=date_from)
        if date_to:
            orders = orders.filter(created_at__date__lte=date_to)
    
    # Статистика
    total_orders = orders.count()
    total_revenue = orders.aggregate(total=Sum('total_amount'))['total'] or 0
    avg_order = total_revenue / total_orders if total_orders > 0 else 0
    
    # Статистика по дням (для графика)
    daily_stats = []
    if period == 'week':
        for i in range(7):
            day = today - timedelta(days=i)
            day_orders = orders.filter(created_at__date=day)
            daily_stats.append({
                'date': day.strftime('%d.%m'),
                'count': day_orders.count(),
                'revenue': day_orders.aggregate(total=Sum('total_amount'))['total'] or 0
            })
    
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'avg_order': avg_order,
        'daily_stats': daily_stats,
        'period': period,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'waiter_history.html', context)

def chef_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and hasattr(user, 'profile') and user.profile.role == 'chef':
            auth_login(request, user)
            return redirect('kitchen_dashboard')
        else:
            return render(request, 'chef_login.html', {'error': 'Неверные данные или недостаточно прав'})
    return render(request, 'chef_login.html')