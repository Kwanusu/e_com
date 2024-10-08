from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
from django.urls import path
from . import views, api_views
from .forms import PasswordChangeForm

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
    path('api/update-address/<int:pk>/', api_views.UpdateAddressAPIView.as_view(), name='update-address'),
    path('api/password-reset/', views.password_reset_request, name='password_reset_request'),
    path('api/password-reset/confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    path('api/check-auth/', api_views.check_auth, name='check_auth'),
    path('api/login/', api_views.LoginView.as_view(), name='login'),
    path('api/logout/', api_views.UserLogout.as_view(), name='logout'),
    path('api/register/', api_views.RegisterView.as_view(), name='register'),
    path('api/products/', api_views.ProductView.as_view(), name='product-list-create'),
    path('api/products/<int:id>/', api_views.ProductView.as_view(), name='product-detail'),
    path('api/product_detail/<int:id>/', api_views.ProductDetailView.as_view(), name='product-detail-create'),
    path('api/category/<str:val>/', api_views.CategoryView.as_view(), name='category'),
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

    # Checkout views
    path('checkout/', views.Checkout.as_view(), name='checkout'),
    path('create-payment-intent/', views.create_payment_intent, name='create_payment_intent'),
    path('save-payment-method/', views.save_payment_method, name='save_payment_method'),
    path('success/', views.success_view, name='success'),
    path('cancel/', views.cancel_view, name='cancel'),
    path('payment-done/', views.payment_done, name='payment_done'),

    # Views URLs
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('category/<slug:val>/', views.CategoryView.as_view(), name='category'),
    path('category_title/<val>/', views.CategoryTitle.as_view(), name='category-title'),
    path('product_detail/<int:pk>/', views.ProductDetail.as_view(), name='product_detail'),
    path('product_list/', views.product_list, name='product-list'),
    path('profile/', views.profile_view, name='profile'),
    path('address/', views.address, name='address'),
    path('contact/', views.contact_us, name='contact_us'),
    path('contact/success/', views.contact_us_success, name='contact_us_success'),
    path('updateAddress/<int:pk>/', views.UpdateAddress.as_view(), name='updateAddress'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
    path('add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('update_cart_quantity/', views.update_cart_quantity, name='update_cart_quantity'),
    path('show_cart/', views.show_cart, name='show_cart'),
    path('show_wishlist/', views.show_wishlist, name='show_wishlist'),
    path('check_out/', views.Checkout.as_view(), name='check_out'),
    path('orders/', views.orders, name='orders'),
    path('search/', views.search, name='search'),
    path('plus_Cart/', views.plus_Cart, name='plus_Cart'),
    path('minus_Cart/', views.minus_Cart, name='minus_Cart'),
    path('remove_Cart/', views.remove_Cart, name='remove_Cart'),
    path('pluswishlist/', views.plus_wishlist, name='pluswishlist'),
    path('minuswishlist/', views.minus_wishlist, name='minuswishlist'),

    # Login authentication
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
    # path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(), name='activate'),
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    path('accounts/login/', views.login_view, name='login'),
    # path('reset/<uidb64>/<token>/', auth_view.PasswordResetView.as_view(template_name='passwordchange.html'), name='password_change'),
    # path('password_reset/', auth_view.PasswordResetView.as_view(template_name='password_reset.html', form_class=MyPasswordResetForm), name='password_reset'),
    path('passwordchange/', auth_view.PasswordChangeView.as_view(template_name='passwordchange.html', form_class=PasswordChangeForm), name='passwordchange'),
    path('password_change_done/', auth_view.PasswordChangeDoneView.as_view(template_name='passwordchangedone.html'), name='passwordchangedone'),
    path('password_reset/done/', auth_view.PasswordResetDoneView.as_view(template_name='password-reset-done.html'), name='password_reset_done'),
    path('password_reset_complete/', auth_view.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
