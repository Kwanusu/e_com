from rest_framework import serializers
from .models import CATEGORY_CHOICES, STATE_CHOICES, STATUS_CHOICES, Cart, Customer, OrderPlaced, Payment, Product, Wishlist
from django.contrib.auth.models import User

class ProductSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=100)
    selling_price =serializers.FloatField()
    discounted_price = serializers.FloatField()
    description = serializers.DictField()
    composition = serializers.DictField(default='')
    prodapp = serializers.DictField(default='')
    category = serializers.ChoiceField(choices=CATEGORY_CHOICES)
    product_image = serializers.ImageField()
    
    class Meta:
        model = Product
        fields = '__all__'
    
    
class CustomerSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    name =serializers.CharField(max_length=200)
    locality =serializers.CharField(max_length=200)
    city =serializers.CharField(max_length=50)
    mobile = serializers.IntegerField(default=0)
    zipcode = serializers.IntegerField()
    state = serializers.ChoiceField(choices=STATE_CHOICES)
    class Meta:
        model = Customer
        fields = '__all__'
    
class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(default=1)
    
    class Meta:
        model = Cart
        fields = '__all__'
    
    
class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    amount = serializers.FloatField()
    stripe_order_id = serializers.CharField(max_length=100)
    stripe_payment_status = serializers.CharField(max_length=100)
    stripe_payment_id = serializers.CharField(max_length=100)
    paid = serializers.BooleanField(default=False)

    class Meta:
        model = Payment
        fields = '__all__'

        
    
class OrderPlacedSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField(default=1)
    ordered_date = serializers.DateTimeField()
    status = serializers.ChoiceField(choices=STATUS_CHOICES, default='Pending')
    payment = serializers.PrimaryKeyRelatedField(queryset=Payment.objects.all(), default="")

    class Meta:
        model = OrderPlaced
        fields = '__all__'
        
class WishlistSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all()) 
    
    
    class Meta:
        model = Wishlist
        fields = '__all__'