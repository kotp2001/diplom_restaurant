from django.db import models

class Table(models.Model):
    STATUS_CHOICES = [
        ('free', 'Свободен'),
        ('occupied', 'Занят'),
        ('reserved', 'Забронирован'),
    ]
    
    number = models.IntegerField(unique=True, verbose_name="Номер стола")
    seats = models.IntegerField(verbose_name="Количество мест")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='free', verbose_name="Статус")
    
    class Meta:
        verbose_name = "Стол"
        verbose_name_plural = "Столы"
        ordering = ['number']
    
    def __str__(self):
        return f"Стол №{self.number} ({self.seats} мест)"