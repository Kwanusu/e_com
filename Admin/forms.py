from django import forms
from online_shop.models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = '__all__'

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = '__all__'

class OrderPlacedForm(forms.ModelForm):
    class Meta:
        model = OrderPlaced
        fields = '__all__'

class WishlistForm(forms.ModelForm):
    class Meta:
        model = Wishlist
        fields = '__all__'
