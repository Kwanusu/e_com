from django.urls import path
from .views import admin_dashboard, admin_product_list, admin_product_create, admin_product_update, admin_product_delete

urlpatterns = [
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('products/', admin_product_list, name='admin_product_list'),
    path('products/create/', admin_product_create, name='admin_product_create'),
    path('products/update/<int:pk>/', admin_product_update, name='admin_product_update'),
    path('products/delete/<int:pk>/', admin_product_delete, name='admin_product_delete'),
    # Add more admin URLs as needed
]
