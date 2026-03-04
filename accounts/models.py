from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Администратор'),
        ('waiter', 'Официант'),
        ('chef', 'Повар'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='waiter', verbose_name="Роль")
    pin_code = models.CharField(max_length=4, blank=True, null=True, verbose_name="Пин-код")
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"