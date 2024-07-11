from email.headerregistry import Group
from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import OrderPlaced, Payment, Product, Customer, Cart, Wishlist
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .forms import CustomerRegistrationForm, MyPasswordChangeForm
from django.contrib.auth.forms import UserChangeForm

# Register your models here.
@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'discounted_price', 'category', 'product_image']
    
    
@admin.register(Customer)
class CustomerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'locality', 'city', 'state', 'zipcode']

@admin.register(Cart)
class CartModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'products', 'quantity']
    
    def products(self, obj):
        link = reverse("admin:online_shop_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">"{}"</a>', link, obj.product.title)

@admin.register(Payment)
class PaymentModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'stripe_order_id', 'stripe_payment_status', 'stripe_payment_id', 'paid']

@admin.register(OrderPlaced)
class OrderPlacedModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'customers', 'products', 'quantity', 'ordered_date', 'status', 'payments']
    
    def customers(self, obj):
        link = reverse("admin:online_shop_customer_change", args=[obj.customer.pk])
        return format_html('<a href="{}">"{}"</a>', link, obj.customer.name)
    
    def products(self, obj):
        link = reverse("admin:online_shop_product_change", args=[obj.product.pk])
        return format_html('<a href="{}">"{}"</a>', link, obj.product.title)
    
    def payments(self, obj):
        link = reverse("admin:online_shop_payment_change", args=[obj.payment.pk])
        return format_html('<a href="{}">"{}"</a>', link, obj.payment.stripe_order_id)

    
@admin.register(Wishlist)
class WishlistModelAdmin(admin.ModelAdmin):
    list_display =['id', 'user', 'product']            
    def products(self,obj):
        link = reverse("admin:app_product_change" ,args=[obj.product.pk])
        return format_html('<a href="{}">"{}"</a>',link, obj.product.title)

class CustomUserAdmin(UserAdmin):
    add_form = CustomerRegistrationForm
    form = UserChangeForm  # Changed from MyPasswordChangeForm to UserChangeForm
    model = User
    list_display = ['username', 'email', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_active']
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username',)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
    
  