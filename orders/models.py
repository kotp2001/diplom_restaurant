from django.db import models
from django.contrib.auth.models import User
from menu.models import Dish
from tables.models import Table

class Order(models.Model):
    STATUS_CHOICES = [
        ('open', 'Открыт'),
        ('paid', 'Оплачен'),
        ('cancelled', 'Отменен'),
    ]
    
    PAYMENT_CHOICES = [  
        ('cash', 'Наличные'),
        ('card', 'Карта'),
        ('qr', 'QR-код'),
    ]
    
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name="Стол")
    waiter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Официант")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name="Время закрытия")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name="Статус")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0, verbose_name="Общая сумма")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, blank=True, null=True, verbose_name="Способ оплаты")
    payment_received = models.BooleanField(default=False, verbose_name="Оплачено")
    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заказ №{self.id} - Стол {self.table.number}"

class OrderItem(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('cooking', 'Готовится'),
        ('ready', 'Готов'),
        ('served', 'Подан'),
    ]
    
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name="Заказ", related_name='items')
    dish = models.ForeignKey(Dish, on_delete=models.PROTECT, verbose_name="Блюдо")
    quantity = models.IntegerField(default=1, verbose_name="Количество")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Статус")
    
    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказа"
    
    def __str__(self):
        return f"{self.dish.name} x{self.quantity}"
    
    def get_total(self):
        return self.price * self.quantity