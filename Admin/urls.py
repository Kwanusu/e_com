
from django.urls import path
from .views import admin_dashboard, admin_product_list, admin_product_create, admin_product_update, admin_product_delete, admin_user_create, admin_user_delete, admin_user_list, admin_user_update

urlpatterns = [
    path('admin_dashboard/', admin_dashboard, name='admin_dashboard'),
    path('products/', admin_product_list, name='admin_product_list'),
    path('products/create/', admin_product_create, name='admin_product_create'),
    path('products/update/<int:pk>/', admin_product_update, name='admin_product_update'),
    path('products/delete/<int:pk>/', admin_product_delete, name='admin_product_delete'),
    path('users/', admin_user_list, name='admin_user_list'),
    path('users_create/', admin_user_create, name='admin_user_create'),
    path('users_update/<int:pk>/', admin_user_update, name='admin_user_update'),
    path('users_delete/<int:pk>/', admin_user_delete, name='admin_user_delete'),
]
