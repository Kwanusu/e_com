from django.forms import ValidationError
from rest_framework import serializers
from .models import  STATE_CHOICES, STATUS_CHOICES, Cart, Customer, OrderPlaced, Payment, Product, Wishlist
from django.contrib.auth.models import User       
from .models import CarouselImage   
from django.contrib.auth import get_user_model, authenticate
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_str

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'selling_price', 'discounted_price', 'description', 'composition', 'prodapp', 'category', 'product_image']
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'selling_price', 'discounted_price', 'description', 'composition', 'prodapp', 'category', 'product_image']
    
    
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


UserModel = get_user_model()
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def check_user(self, clean_data):
        user = authenticate(username=clean_data['email'], password=clean_data['password'])
        if not user: 
            raise ValidationError('User does not exist')
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('email', 'username')                   


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # Include all necessary fields

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

class SetPasswordSerializer(serializers.Serializer):
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'mobile', 'state', 'zipcode']

class CarouselImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarouselImage
        fields = ('id', 'src', 'alt')  

class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

class PasswordResetConfirmSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()
    new_password1 = serializers.CharField(write_only=True)
    new_password2 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        uid = attrs.get('uidb64')
        token = attrs.get('token')
        new_password1 = attrs.get('new_password1')
        new_password2 = attrs.get('new_password2')

        # Validate passwords match
        if new_password1 != new_password2:
            raise serializers.ValidationError("Passwords do not match.")

        # Validate reset token
        try:
            uid = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid user or token.")
        
        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError("Invalid token.")
        
        return attrs
