from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название категории")
    order = models.IntegerField(default=0, verbose_name="Порядок сортировки")
    
    class Meta:
        verbose_name = "Категория"              # как в единственном числе
        verbose_name_plural = "Категории"       # как во множественном
        ordering = ['order']
    
    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название блюда")
    description = models.TextField(blank=True, verbose_name="Описание")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    is_available = models.BooleanField(default=True, verbose_name="Доступно")
    image = models.ImageField(upload_to='dishes/', blank=True, null=True, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        verbose_name = "Блюдо"
        verbose_name_plural = "Блюда"
        ordering = ['category__order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.price} руб."