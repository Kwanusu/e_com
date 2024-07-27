from django.conf import settings
from django.contrib.auth import views as auth_view
from Admin.urls import admin_dashboard, admin_product_create, admin_product_delete, admin_product_list, admin_product_update
from . import views, api_views
from django.urls import path
from django.conf.urls.static import static
from .forms import LoginForm, PasswordChangeForm, MyPasswordResetForm

urlpatterns = [
    path('', views.home, name='home'),

    # API URLs
    path('api/checkout/create-session/', api_views.create_checkout_session, name='create_checkout_session'),
    path('api/stripe-key/', api_views.get_stripe_key, name='get_stripe_key'),
    path('api/carousel_images/', api_views.CarouselImagesAPIView.as_view(), name='carousel_images_api'),
    path('api/search/', api_views.SearchView.as_view(), name='search'),
    path('api/password_change/', api_views.PasswordChangeView.as_view(), name='password_change'),
    path('api/password_reset/', api_views.PasswordResetView.as_view(), name='password_reset'),
    path('api/set_password/', api_views.SetPasswordView.as_view(), name='set_password'),
    path('api/profile/', api_views.ProfileView.as_view(), name='profile'),
    path('api/check-auth/', api_views.check_auth, name='check_auth'),
    path('api/login/', api_views.LoginView.as_view(), name='api_login'),
    path('api/logout/', api_views.UserLogout.as_view(), name='api_logout'),
    path('api/register/', api_views.RegisterView.as_view(), name='register'),
    path('api/products/', api_views.ProductView.as_view(), name='product-list-create'),
    path('api/products/<int:id>/', api_views.ProductView.as_view(), name='product-detail'),
    path('api/product_detail/<int:id>/', api_views.ProductDetailView.as_view(), name='product-detail-create'),
    path('api/customers/', api_views.CustomerView.as_view(), name='customer-list-create'),
    path('api/customers/<int:pk>/', api_views.CustomerView.as_view(), name='customer-detail'),
    path('api/cart/', api_views.CartView.as_view(), name='cart-list-create'),
    path('api/cart/<int:pk>/', api_views.CartView.as_view(), name='cart-detail'),
    path('api/payments/', api_views.PaymentView.as_view(), name='payment-list-create'),
    path('api/payments/<int:pk>/', api_views.PaymentView.as_view(), name='payment-detail'),
    path('api/orders/', api_views.OrderPlacedView.as_view(), name='order-list-create'),
    path('api/orders/<int:pk>/', api_views.OrderPlacedView.as_view(), name='order-detail'),
    path('api/wishlists/', api_views.WishlistView.as_view(), name='wishlist-list-create'),
    path('api/wishlists/<int:id>/', api_views.WishlistView.as_view(), name='wishlist-detail'),
    path('api/add_to_cart/', api_views.AddToCartView.as_view(), name='add_to_cart'),
    path('api/add_to_cart/<int:id>/', api_views.AddToCartView.as_view(), name='add_to_cart'),
    path('api/update_cart_quantity/', api_views.UpdateCartQuantity.as_view(), name='update_cart_quantity'),
    path('api/remove_cart_item/', api_views.RemoveCartItemView.as_view(), name='remove_cart_item'),
    path('api/add_to_wishlist/', api_views.AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('api/remove_wishlist_item/', api_views.RemoveWishlistItemView.as_view(), name='remove_wishlist_item'),

    # Admin URLs
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('products/', api_views.AdminProductList.as_view(), name='admin_product_list'),
    path('products/create/', api_views.AdminProductCreate.as_view(), name='admin_product_create'),
    path('products/update/<int:pk>/', api_views.AdminProductUpdate.as_view(), name='admin_product_update'),
    path('products/delete/<int:pk>/', api_views.AdminProductDelete.as_view(), name='admin_product_delete'),

    # Views URLs
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/<slug:val>/', views.CategoryView.as_view(), name='category'),
    path('category_title/<val>/', views.CategoryTitle.as_view(), name='category-title'),
    path('product_detail/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('product_list/', views.product_list, name='product-list'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('contact/', views.contact_us, name='contact_us'),
    path('contact/success/', views.contact_us_success, name='contact_us_success'),
    path('updateAddress/<int:pk>/', views.UpdateAddress.as_view(), name='updateAddress'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('update_cart_quantity/', views.update_cart_quantity, name='update_cart_quantity'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('show_wishlist/', views.show_wishlist, name='show_wishlist'),
    path('check_out/', views.Checkout.as_view(), name='check_out'),
    path('payment_done/', views.payment_done, name='payment_done'),
    path('orders/', views.orders, name='orders'),
    path('success/', views.success_view, name='success'),
    path('cancel/', views.cancel_view, name='cancel'),
    path('search/', views.search, name='search'),
    path('plus_Cart/', views.plus_Cart, name='plus_Cart'),
    path('minus_Cart/', views.minus_cart, name='minus_Cart'),
    path('remove_Cart/', views.remove_Cart, name='remove_Cart'),
    path('pluswishlist/', views.plus_wishlist, name='pluswishlist'),
    path('minuswishlist/', views.minus_wishlist, name='minuswishlist'),

    # Login authentication
    path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', auth_view.LoginView.as_view(template_name='login.html', authentication_form=LoginForm), name='login'),
    path('password_reset/', auth_view.PasswordResetView.as_view(template_name='password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='passwordchange.html', form_class=PasswordChangeForm), name='passwordchange'),
    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='password-reset-done.html'), name='password_reset_done'),
    path('password_reset_confirm/', auth_view.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html', form_class=MyPasswordResetForm), name='password_reset_confirm'),
    path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
