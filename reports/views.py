from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from orders.models import Order, OrderItem
from menu.models import Dish, Category

@staff_member_required
def dashboard(request):
    # Статистика за сегодня
    today = timezone.now().date()
    
    today_orders = Order.objects.filter(
        created_at__date=today,
        status='paid'
    )
    
    today_revenue = today_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    today_count = today_orders.count()
    
    # Статистика за неделю
    week_ago = today - timedelta(days=7)
    week_orders = Order.objects.filter(
        created_at__date__gte=week_ago,
        status='paid'
    )
    
    week_revenue = week_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    week_count = week_orders.count()
    
    # Статистика за месяц
    month_ago = today - timedelta(days=30)
    month_orders = Order.objects.filter(
        created_at__date__gte=month_ago,
        status='paid'
    )
    
    month_revenue = month_orders.aggregate(total=Sum('total_amount'))['total'] or 0
    month_count = month_orders.count()
    
    # Популярные блюда
    popular_dishes = OrderItem.objects.values(
        'dish__name'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('price')
    ).order_by('-total_quantity')[:5]
    
    # Продажи по категориям
    category_sales = []
    categories = Category.objects.all()
    for category in categories:
        total_sold = OrderItem.objects.filter(
            dish__category=category
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        total_revenue = OrderItem.objects.filter(
            dish__category=category
        ).aggregate(total=Sum('price'))['total'] or 0
        
        category_sales.append({
            'name': category.name,
            'total_sold': total_sold,
            'total_revenue': total_revenue
        })
    
    # График продаж по дням (последние 7 дней)
    daily_sales = []
    for i in range(7):
        day = today - timedelta(days=i)
        day_orders = Order.objects.filter(
            created_at__date=day,
            status='paid'
        )
        revenue = day_orders.aggregate(total=Sum('total_amount'))['total'] or 0
        daily_sales.append({
            'date': day.strftime('%d.%m'),
            'revenue': revenue
        })
    
    context = {
        'today_revenue': today_revenue,
        'today_count': today_count,
        'week_revenue': week_revenue,
        'week_count': week_count,
        'month_revenue': month_revenue,
        'month_count': month_count,
        'popular_dishes': popular_dishes,
        'category_sales': category_sales,
        'daily_sales': daily_sales,
    }
    return render(request, 'reports/dashboard.html', context)

@staff_member_required
def orders_report(request):
    orders = Order.objects.filter(status='paid').select_related('table', 'waiter').order_by('-created_at')
    
    # Фильтры
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if date_from:
        orders = orders.filter(created_at__date__gte=date_from)
    if date_to:
        orders = orders.filter(created_at__date__lte=date_to)
    
    total_sum = orders.aggregate(total=Sum('total_amount'))['total'] or 0
    
    context = {
        'orders': orders,
        'total_sum': total_sum,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'reports/orders_report.html', context)

@staff_member_required
def dishes_report(request):
    dishes = Dish.objects.annotate(
        total_sold=Sum('orderitem__quantity'),
        total_revenue=Sum('orderitem__price')
    ).order_by('-total_sold')
    
    context = {
        'dishes': dishes,
    }
    return render(request, 'reports/dishes_report.html', context)