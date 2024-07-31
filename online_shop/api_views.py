
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from online_shop.validations import  validate_email, validate_password
from .models import Customer, Cart, Payment, OrderPlaced, Wishlist
from .serializers import ProductDetailSerializer, ProductSerializer, CustomerSerializer, CartSerializer, PaymentSerializer, OrderPlacedSerializer, ProfileSerializer, UserSerializer, UserLoginSerializer, RegisterSerializer, WishlistSerializer
from .models import Product
from rest_framework import generics, permissions, status
from rest_framework.permissions import IsAuthenticated
from .forms import LoginForm
from django.contrib.auth import login, logout
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from rest_framework.permissions import IsAuthenticated
from .serializers import ProfileSerializer
from .models import Customer
from django.db.models import Q
from .models import CarouselImage
from .serializers import CarouselImageSerializer
from django.shortcuts import get_object_or_404
from .models import Cart, Wishlist, Product
from .serializers import CartSerializer, WishlistSerializer
import json
import stripe
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.html import strip_tags

class HomeView(APIView):
   permission_classes = (IsAuthenticated, )
   def get(self, request):
       content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
       return Response(content)

class CarouselImagesAPIView(APIView):
    def get(self, request):
        images = CarouselImage.objects.all()
        serializer = CarouselImageSerializer(images, many=True)
        return Response(serializer.data)
   
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
          
        try:
            refresh_token = request.data["refresh_token"]
            token = refresh_token(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)              
                  


class ProductView(APIView):

    def get(self, request, *args, **kwargs):
        result = Product.objects.all()
        for product in result:
            print(f"Product: {product.title}")  # Debug statement
        serializer = ProductSerializer(result, many=True)
        print(f"Serialized Data: {serializer.data}")  # Debug statement
        return Response({'status': 'success', 'data': serializer.data}, status=200)
    
    def post(self, request):
        print(f"Request data: {request.data}")  # Debug statement
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs['id'])
        except Product.DoesNotExist:
            return Response({"status": "error", "data": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        print(f"Updating product {product.id} with data: {request.data}")  # Debug statement
        serializer = ProductSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs['id'])
        except Product.DoesNotExist:
            return Response({"status": "error", "data": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
        return Response({"status": "success", "data": "Product deleted"}, status=status.HTTP_200_OK)

class ProductDetailView(APIView):

    def get(self, request, *args, **kwargs):
        result = Product.objects.all()
        for product in result:
            print(f"Product: {product.title}")  # Debug statement
        serializer = ProductDetailSerializer(result, many=True)
        print(f"Serialized Data: {serializer.data}")  # Debug statement
        return Response({'status': 'success', 'data': serializer.data}, status=200)
    
    def post(self, request):
        print(f"Request data: {request.data}")  # Debug statement
        serializer = ProductDetailSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs['id'])
        except Product.DoesNotExist:
            return Response({"status": "error", "data": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        print(f"Updating product {product.id} with data: {request.data}")  # Debug statement
        serializer = ProductDetailSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            product = Product.objects.get(id=kwargs['id'])
        except Product.DoesNotExist:
            return Response({"status": "error", "data": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
        
        product.delete()
        return Response({"status": "success", "data": "Product deleted"}, status=status.HTTP_200_OK)

class CustomerView(APIView):

    def get(self, request, *args, **kwargs):
        result = Customer.objects.all()
        serializers = CustomerSerializer(result, many=True)
        return Response({'status': 'success', "customers": serializers.data}, status=200)

    def post(self, request):
        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.get(id=kwargs['id'])
        except Customer.DoesNotExist:
            return Response({"status": "error", "data": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CustomerSerializer(customer, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.get(id=kwargs['id'])
        except Customer.DoesNotExist:
            return Response({"status": "error", "data": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)
        
        customer.delete()
        return Response({"status": "success", "data": "Customer deleted"}, status=status.HTTP_200_OK)


class CartView(APIView):

    def get(self, request, *args, **kwargs):
        result = Cart.objects.all()
        serializers = CartSerializer(result, many=True)
        return Response({'status': 'success', "carts": serializers.data}, status=200)

    def post(self, request):
        serializer = CartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(id=kwargs['id'])
        except Cart.DoesNotExist:
            return Response({"status": "error", "data": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CartSerializer(cart, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            cart = Cart.objects.get(id=kwargs['id'])
        except Cart.DoesNotExist:
            return Response({"status": "error", "data": "Cart not found"}, status=status.HTTP_404_NOT_FOUND)
        
        cart.delete()
        return Response({"status": "success", "data": "Cart deleted"}, status=status.HTTP_200_OK)


class PaymentView(APIView):

    def get(self, request, *args, **kwargs):
        result = Payment.objects.all()
        serializers = PaymentSerializer(result, many=True)
        return Response({'status': 'success', "payments": serializers.data}, status=200)

    def post(self, request):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            payment = Payment.objects.get(id=kwargs['id'])
        except Payment.DoesNotExist:
            return Response({"status": "error", "data": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = PaymentSerializer(payment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            payment = Payment.objects.get(id=kwargs['id'])
        except Payment.DoesNotExist:
            return Response({"status": "error", "data": "Payment not found"}, status=status.HTTP_404_NOT_FOUND)
        
        payment.delete()
        return Response({"status": "success", "data": "Payment deleted"}, status=status.HTTP_200_OK)


class OrderPlacedView(APIView):

    def get(self, request, *args, **kwargs):
        result = OrderPlaced.objects.all()
        serializers = OrderPlacedSerializer(result, many=True)
        return Response({'status': 'success', "orders": serializers.data}, status=200)

    def post(self, request):
        serializer = OrderPlacedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            order = OrderPlaced.objects.get(id=kwargs['id'])
        except OrderPlaced.DoesNotExist:
            return Response({"status": "error", "data": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = OrderPlacedSerializer(order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            order = OrderPlaced.objects.get(id=kwargs['id'])
        except OrderPlaced.DoesNotExist:
            return Response({"status": "error", "data": "Order not found"}, status=status.HTTP_404_NOT_FOUND)
        
        order.delete()
        return Response({"status": "success", "data": "Order deleted"}, status=status.HTTP_200_OK)


class WishlistView(APIView):

    def get(self, request, *args, **kwargs):
        result = Wishlist.objects.all()
        serializers = WishlistSerializer(result, many=True)
        return Response({'status': 'success', "wishlists": serializers.data}, status=200)

    def post(self, request):
        serializer = WishlistSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        try:
            wishlist = Wishlist.objects.get(id=kwargs['id'])
        except Wishlist.DoesNotExist:
            return Response({"status": "error", "data": "Wishlist not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = WishlistSerializer(wishlist, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({"status": "error", "data": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        try:
            wishlist = Wishlist.objects.get(id=kwargs['id'])
        except Wishlist.DoesNotExist:
            return Response({"status": "error", "data": "Wishlist not found"}, status=status.HTTP_404_NOT_FOUND)
        
        wishlist.delete()
        return Response({"status": "success", "data": "Wishlist deleted"}, status=status.HTTP_200_OK)

class LoginView(APIView):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            return JsonResponse({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def check_auth(request):
    is_authenticated = request.user.is_authenticated
    return Response({'isAuthenticated': is_authenticated})
        

@api_view(['GET'])
def admin_dashboard(request):
    data = {
        'message': 'Welcome to the admin dashboard'
    }
import logging

logger = logging.getLogger(__name__)

class SearchView(APIView):
    def get(self, request):
        try:
            query = request.GET.get('q', '')
            logger.debug(f"Search query: {query}")
            
            totalItem = 0
            wishItem = 0
            
            if request.user.is_authenticated:
                totalItem = Cart.objects.filter(user=request.user).count()
                wishItem = Wishlist.objects.filter(user=request.user).count()
            
            if query:
                products = Product.objects.filter(Q(title__icontains=query))
            else:
                products = Product.objects.none()
                
            product_list = ProductSerializer(products, many=True).data  # Serialize the products
            
            logger.debug(f"Products found: {len(product_list)}")
            
            return JsonResponse({'products': product_list, 'totalItem': totalItem, 'wishItem': wishItem})
        except Exception as e:
            logger.error(f"Error during search: {e}")
            return JsonResponse({'error': str(e)}, status=500)
        
class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)
    
    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.check_user(data)
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
class UserLogout(APIView):
    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)
    
    
class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({'user': serializer.data}, status=status.HTTP_200_OK) 
            
class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        form = PasswordChangeForm(user=request.user, data=request.data)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            return Response({'status': 'password_changed'}, status=status.HTTP_200_OK)
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

from .serializers import PasswordResetRequestSerializer, SetPasswordSerializer

class PasswordResetView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
                email_subject = "Password Reset Requested"
                frontend_domain = 'http://127.0.0.1:5173'
                context = {
                    'user': user,
                    'frontend_domain': frontend_domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                }
                
                html_content = render_to_string("password_reset_email.html", context)
                text_content = strip_tags(html_content)
                
                email_message = EmailMultiAlternatives(
                    subject=email_subject,
                    body=text_content,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[email]
                )
                email_message.attach_alternative(html_content, "text/html")
                email_message.send()
                
                return Response({'status': 'password_reset_email_sent'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'error': 'No user found with this email address.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SetPasswordView(APIView):

    def post(self, request, *args, **kwargs):
        serializer = SetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            uidb64 = serializer.validated_data['uidb64']
            token = serializer.validated_data['token']
            new_password1 = serializer.validated_data['new_password1']
            new_password2 = serializer.validated_data['new_password2']
            
            try:
                uid = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk=uid)
            except (TypeError, ValueError, OverflowError, User.DoesNotExist):
                return Response({'error': 'Invalid token or user ID.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if user is not None and default_token_generator.check_token(user, token):
                form = SetPasswordForm(user=user, data=request.data)
                if form.is_valid():
                    form.save()
                    return Response({'status': 'password_set'}, status=status.HTTP_200_OK)
                return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({'error': 'Invalid token or user ID.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        serializer = ProfileSerializer(customer)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        serializer = ProfileSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)           

class AddToCartView(APIView):
    def post(self, request, *args, **kwargs):
        product_id = request.data.get('prod_id')
        product = get_object_or_404(Product, id=product_id)
        user = request.user

        cart_item, created = Cart.objects.get_or_create(user=user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()

        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
     
class UpdateCartQuantity(APIView):
    def post(self, request, *args, **kwargs):
        prod_id = request.data.get('prod_id')
        quantity = int(request.POST.get('quantity', 1))
        user = request.user

        cart_item, created = Cart.objects.get_or_create(product_id=prod_id, user=user)
        if not created:
           cart_item.quantity += 1
           cart_item.save()
        serializer = CartSerializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ShowCartView(APIView):
    def get(self, request, *args, **kwargs):
        user = request.user
        cart_items = Cart.objects.filter(user=user)
        serializer = CartSerializer(cart_items, many=True)
        amount = sum(p.quantity * p.product.discounted_price for p in cart_items)
        totalamount = amount + 40
        data = {
            'cart_items': serializer.data,
            'total_amount': totalamount,
            'total_items': cart_items.count()
        }
        return Response(data, status=status.HTTP_200_OK)

class RemoveCartItemView(APIView):
    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('prod_id')
        user = request.user
        cart_item = get_object_or_404(Cart, user=user, product_id=product_id)
        cart_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AddToWishlistView(APIView):
    def post(self, request, *args, **kwargs):
        product_id = request.data.get('prod_id')
        product = get_object_or_404(Product, id=product_id)
        user = request.user

        wishlist_item, created = Wishlist.objects.get_or_create(user=user, product=product)
        serializer = WishlistSerializer(wishlist_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class RemoveWishlistItemView(APIView):
    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('prod_id')
        user = request.user
        wishlist_item = get_object_or_404(Wishlist, user=user, product_id=product_id)
        wishlist_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

stripe.api_key = settings.STRIPE_SECRET_KEY

@csrf_exempt
@require_POST
def create_checkout_session(request):
    try:
        data = json.loads(request.body)
        items = data.get('items', [])
        
        if not items:
            return JsonResponse({'error': 'No items provided'}, status=400)
        
        line_items = []
        for item in items:
            price_data = item.get('price_data')
            quantity = item.get('quantity')
            if not price_data or not quantity:
                return JsonResponse({'error': 'Invalid item data'}, status=400)
            if not all(key in price_data for key in ('unit_amount', 'currency', 'product_data')):
                return JsonResponse({'error': 'Missing key in price_data'}, status=400)
            if not all(key in price_data['product_data'] for key in ('name', 'description')):
                return JsonResponse({'error': 'Missing key in product_data'}, status=400)
            line_items.append({
                'price_data': {
                    'currency': price_data['currency'],
                    'product_data': {
                        'name': price_data['product_data']['name'],
                        'description': price_data['product_data']['description'],
                    },
                    'unit_amount': price_data['unit_amount']
                },
                'quantity': quantity
            })
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://localhost:8000/success/',
            cancel_url='http://localhost:8000/cancel/',
        )
        
        return JsonResponse({'id': session.id})
    
    except KeyError as e:
        return JsonResponse({'error': f'Missing key: {str(e)}'}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': f'Internal server error: {str(e)}'}, status=500)

@require_GET
def get_stripe_key(request):
    return JsonResponse({'publishableKey': settings.STRIPE_PUBLISHABLE_KEY})
