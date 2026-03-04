from django.db import models
from tables.models import Table

class Booking(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE, verbose_name="Стол")
    guest_name = models.CharField(max_length=100, verbose_name="Имя гостя")
    guest_phone = models.CharField(max_length=20, verbose_name="Телефон")
    guests_count = models.IntegerField(verbose_name="Количество гостей")
    booking_date = models.DateField(verbose_name="Дата брони")
    booking_time = models.TimeField(verbose_name="Время брони")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    
    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"
        ordering = ['booking_date', 'booking_time']
    
    def __str__(self):
        return f"Стол {self.table.number} - {self.guest_name} - {self.booking_date} {self.booking_time}"