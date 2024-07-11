from django.conf import settings
from django.contrib.auth import views as auth_view
from Admin.urls import admin_dashboard, admin_product_create, admin_product_delete, admin_product_list, admin_product_update
from .import views, api_views
from django.urls import path, include
from django.conf.urls.static import static
from .forms import LoginForm, PasswordChangeForm, MyPasswordResetForm
from rest_framework.views import APIView

urlpatterns = [
    # api urls 
   path('api/login/', api_views.LoginView.as_view(), name='login'),
    path('api/register/', api_views.RegisterView.as_view(), name='register'),
    
    path('api/products/', api_views.ProductView.as_view(), name='product-list-create'),
    path('api/products/<int:id>/', api_views.ProductView.as_view(), name='product-detail'),
    
    path('api/customers/', api_views.CustomerView.as_view(), name='customer-list-create'),
    path('customers/<int:id>/', api_views.CustomerView.as_view(), name='customer-detail'),

    path('api/carts/', api_views.CartView.as_view(), name='cart-list-create'),
    path('api/carts/<int:id>/', api_views.CartView.as_view(), name='cart-detail'),

    path('api/payments/', api_views.PaymentView.as_view(), name='payment-list-create'),
    path('api/payments/<int:id>/', api_views.PaymentView.as_view(), name='payment-detail'),

    path('api/orders/', api_views.OrderPlacedView.as_view(), name='order-list-create'),
    path('orders/<int:id>/', api_views.OrderPlacedView.as_view(), name='order-detail'),

    path('api/wishlists/', api_views.WishlistView.as_view(), name='wishlist-list-create'),
    path('api/wishlists/<int:id>/', api_views.WishlistView.as_view(), name='wishlist-detail'),
    
    
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('products/', admin_product_list, name='admin_product_list'),
    path('products/create/', admin_product_create, name='admin_product_create'),
    path('products/update/<int:pk>/', admin_product_update, name='admin_product_update'),
    path('products/delete/<int:pk>/', admin_product_delete, name='admin_product_delete'),
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/<slug:val>', views.CategoryView.as_view(), name='category'),
    path('category_title/<val>', views.CategoryTitle.as_view(), name='category-title'),
    path('product_detail/<int:pk>', views.ProductDetail.as_view(), name='product_detail'),
    path('product_list/', views.product_list, name='product-list'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('contact/', views.contact_us, name='contact_us'),
    path('contact/success/', views.contact_us_success, name='contact_us_success'),
    path('updateAddress/<int:pk>', views.UpdateAddress.as_view(), name='updateAddress'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='login'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('show_wishlist/', views.show_wishlist, name='show_wishlist'),
    path('check_out/', views.Checkout.as_view(), name='check_out'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('orders/', views.orders, name='orders'),
    path('success/', views.success_view, name='success'),
    path('cancel/', views.cancel_view, name='cancel'),
    path('search/', views.search, name='search'),
    path('plus_Cart/', views.show_cart, name='plus_Cart'),
    path('minus_Cart/', views.show_cart, name='minus_Cart'),
    path('remove_Cart/', views.show_cart, name='remove_Cart'),
    path('pluswishlist/', views.plus_wishlist, name='pluswishlist'),
    path('minuswishlist/', views.minus_wishlist, name='minuswishlist'),

    #login authentication
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='passwordchange.html', form_class=PasswordChangeForm), name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='password-reset-done.html'), name='password_reset_done'),
    path('password_reset_confirm/', auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',form_class=MyPasswordResetForm), name='password_reset_confirm'),
    path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

        # Include router URLs
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
