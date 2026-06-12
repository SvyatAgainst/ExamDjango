from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date

class Product(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    category = models.CharField(max_length=150, verbose_name="Категория")
    sku = models.CharField(max_length=100, unique=True, verbose_name="Артикул")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.name

    def clean(self):
        if not self.name or self.name.strip() == "":
            raise ValidationError({'name':"Название не может быть пустым"})
        if not self.category or self.category.strip() == "":
            raise ValidationError({'category':"Категория не может быть пустой"})
        if Product.objects.filter(sku=self.sku).exclude(pk=self.pk).exists():
            raise ValidationError({'sku':"Артикул должен быть уникальный!"})
        if not self.price or self.price <= 0:
            raise ValidationError({'price':"Цена должна быть больше нуля"})
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Event(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название")
    location = models.CharField(max_length=150, verbose_name="Локация")
    event_date = models.DateTimeField(verbose_name="Дата проведения")
    max_guests = models.IntegerField(verbose_name="Максимальное количество гостей", default=0)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title

    def clean(self):
        if not self.title or self.title.strip() == "":
            raise ValidationError({'title':"Название не может быть пустым"})
        if not self.location or self.location.strip() == '':
            raise ValidationError({'location':"Поле 'Локация' не может быть пустым"})
        if not self.event_date or self.event_date < timezone.now():
            raise ValidationError({'event_date':"Дата должна быть в будущем"})
        if not self.max_guests or self.max_guests <= 0:
            raise ValidationError({'max_guests':"Количество гостей должно быть больше нуля"})
        
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class Order(models.Model):
    STATUS_CHOICES = {
        'new': 'New',
        'processing': 'Processing',
        'shipped': 'Shipped',
        'delivered': 'Delivered',
    }
    customer_name = models.CharField(max_length=200, verbose_name='Имя покупателя')
    product_name = models.CharField(max_length=200, verbose_name='Название продукта')
    quantity = models.PositiveIntegerField(verbose_name='Количество товаров')
    order_date = models.DateField(default=timezone.now())
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default = 'new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.customer_name
    
    def clean(self):
        if not self.customer_name or self.customer_name.strip() == "":
            raise ValidationError({'customer_name': 'Имя пользователя не может быть пустым'})
        if not self.product_name or self.product_name.strip() == "":
            raise ValidationError({'product_name': "Имя продукта не может быть пустым"})
        if not self.quantity or self.quantity <= 0:
            raise ValidationError({'quantity': "Количество товара не может быть отрицательным или 0"})
        if not self.order_date or self.order_date > timezone.now().date():
            raise ValidationError({'order_date': "Дата заказа не может быть в будущем"})
        if not self.status or self.status not in self.STATUS_CHOICES:
            raise ValidationError({'status': f"Статус может только один из четырёх: {self.STATUS_CHOICES}"})
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
