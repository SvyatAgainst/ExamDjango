from django.contrib import admin
from .models import *

@admin.register(Product)
class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'sku', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'sku')

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'event_date', 'max_guests', 'created_at')
    list_filter = ('event_date',)
    search_fields = ('title', 'location')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'product_name', 'quantity', 'order_date', 'status', 'created_at')
    list_filter = ('product_name', 'status')
    search_fields = ('order_date', 'customer_name')
