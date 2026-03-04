from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from tables.models import Table
from menu.models import Dish
from .models import Order, OrderItem

@login_required
def create_order(request, table_id):
    table = get_object_or_404(Table, id=table_id)
    
    if table.status == 'free':
        order = Order.objects.create(
            table=table,
            waiter=request.user,
            status='open'
        )
        table.status = 'occupied'
        table.save()
        return redirect('order_detail', order_id=order.id)
    else:
        order = Order.objects.filter(table=table, status='open').first()
        if order:
            return redirect('order_detail', order_id=order.id)
    
    return redirect('waiter_hall')

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    dishes = Dish.objects.filter(is_available=True)
    
    if request.method == 'POST':
        dish_id = request.POST.get('dish_id')
        quantity = int(request.POST.get('quantity', 1))
        dish = get_object_or_404(Dish, id=dish_id)
        
        order_item = order.items.filter(dish=dish).first()
        if order_item:
            order_item.quantity += quantity
            order_item.save()
        else:
            OrderItem.objects.create(
                order=order,
                dish=dish,
                quantity=quantity,
                price=dish.price
            )
        
        total = sum(item.get_total() for item in order.items.all())
        order.total_amount = total
        order.save()
        
        return redirect('order_detail', order_id=order.id)
    
    context = {
        'order': order,
        'dishes': dishes,
    }
    return render(request, 'order_detail.html', context)

@login_required
def payment(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        payment_method = request.POST.get('payment_method')
        order.payment_method = payment_method
        order.payment_received = True
        order.status = 'paid'
        order.closed_at = timezone.now()
        order.save()
        
        table = order.table
        table.status = 'free'
        table.save()
        
        messages.success(request, 'Заказ оплачен')
        return redirect('waiter_hall')
    
    context = {
        'order': order,
    }
    return render(request, 'payment.html', context)

@login_required
def kitchen_dashboard(request):
    # Получаем все столы
    tables = Table.objects.all().order_by('number')
    
    # Для каждого стола получаем активный заказ (если есть)
    for table in tables:
        table.active_order = Order.objects.filter(
            table=table, 
            status='open'
        ).prefetch_related('items__dish').first()
    
    context = {
        'tables': tables,
    }
    return render(request, 'kitchen.html', context)
@login_required
def update_order_item_status(request, item_id):
    if request.method == 'POST':
        item = get_object_or_404(OrderItem, id=item_id)
        new_status = request.POST.get('status')
        if new_status in ['cooking', 'ready']:
            item.status = new_status
            item.save()
    return redirect('kitchen_dashboard')