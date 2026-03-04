from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import datetime, timedelta
from tables.models import Table
from .models import Booking
from django.contrib.auth.decorators import login_required

def calendar(request):
    # Получаем дату из GET параметра
    date_str = request.GET.get('date')
    if date_str:
        try:
            current_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except:
            current_date = timezone.now().date()
    else:
        current_date = timezone.now().date()
    
    # Все столы
    tables = Table.objects.all().order_by('number')
    
    # Все брони на выбранную дату
    bookings = Booking.objects.filter(booking_date=current_date)
    
    # Временные слоты с 8:00 до 21:00
    time_slots = []
    for hour in range(8, 22):
        time_slots.append(f"{hour:02d}:00")
    
    context = {
        'tables': tables,
        'bookings': bookings,
        'time_slots': time_slots,
        'current_date': current_date,
        'prev_date': current_date - timedelta(days=1),
        'next_date': current_date + timedelta(days=1),
    }
    return render(request, 'booking/calendar.html', context)

def create(request):
    if request.method == 'POST':
        table_id = request.POST.get('table_id')
        date = request.POST.get('date')
        time = request.POST.get('time')
        guests_count = int(request.POST.get('guests_count'))
        
        table = get_object_or_404(Table, id=table_id)
        
        # ПРОВЕРКА: количество гостей не больше мест за столом
        if guests_count > table.seats:
            messages.error(request, f'Ошибка: Стол №{table.number} вмещает только {table.seats} человек. Вы выбрали {guests_count}.')
            return redirect(request.META.get('HTTP_REFERER', 'booking_calendar'))
        
        # Проверка на существующую бронь
        exists = Booking.objects.filter(
            table=table,
            booking_date=date,
            booking_time=time
        ).exists()
        
        if exists:
            messages.error(request, 'Это время уже занято')
            return redirect('booking_calendar')
        
        # Создание брони
        Booking.objects.create(
            table=table,
            guest_name=request.POST.get('guest_name'),
            guest_phone=request.POST.get('guest_phone'),
            guests_count=guests_count,
            booking_date=date,
            booking_time=time,
        )
        
        messages.success(request, 'Стол успешно забронирован!')
        return redirect('booking_calendar')
    
    # GET запрос - показываем форму
    tables = Table.objects.all()
    context = {
        'tables': tables,
        'selected_table': request.GET.get('table'),
        'selected_date': request.GET.get('date'),
        'selected_time': request.GET.get('time'),
    }
    return render(request, 'booking/create.html', context)