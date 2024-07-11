
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Product
from .models import Customer, Cart, Payment, OrderPlaced, Wishlist
from .serializers import ProductSerializer, CustomerSerializer, CartSerializer, PaymentSerializer, OrderPlacedSerializer, WishlistSerializer

# Create your views here.

class ProductView(APIView):

    def get(self, request, *args, **kwargs):
        result = Product.objects.all()
        serializers = ProductSerializer(result, many=True)
        return Response({'status': 'success', "products": serializers.data}, status=200)

    def post(self, request):
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
    
    
# Import your forms from forms.py
from .forms import LoginForm, CustomerRegistrationForm, MyPasswordChangeForm, MyPasswordResetForm, MySetPasswordForm, CustomerProfileForm, PaymentForm

class LoginView(APIView):
    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            # Process login form (authentication logic)
            # Example: authenticate user
            # user = form.get_user()
            return JsonResponse({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        else:
            return JsonResponse({'errors': form.errors}, status=status.HTTP_400_BAD_REQUEST)
