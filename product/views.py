from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import *
from .forms import *

def health_check(request):
    return JsonResponse({'status': 'ok'})

def product_list(request):
    """Список всех товаров, отсортированных по дате (сначала новые)"""
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'products/product_list.html', {'products': products})

def product_create(request):
    """Создание нового товара"""
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list') # после сохранения – на список
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'product': None})

def product_update(request, pk):
    """Редактирование товара по его id (pk)"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'product': product})

def product_delete(request, pk):
    """Удаление товара с подтверждением"""
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})