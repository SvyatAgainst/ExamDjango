from django.urls import path
from . import views

urlpatterns = [
    # path('', views.product_list, name='product_list'),
    path('ping/', views.health_check, name='ping')
]