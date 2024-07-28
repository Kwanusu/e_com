import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .models import Cart, Customer, OrderPlaced, Payment, Product, Wishlist
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CustomerProfileForm, CustomerRegistrationForm, LoginForm, PaymentForm
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login
from .models import CarouselImage
from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str as force_text
from django.contrib.auth.tokens import default_token_generator as generate_token
from django.contrib.auth.models import User



stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.


@login_required
def home(request):
    totalItem = 0
    wishItem = 0
    if request.user.is_authenticated:
        totalItem = Cart.objects.filter(user=request.user).count()
        wishItem = Wishlist.objects.filter(user=request.user).count()
    return render(request, 'home.html', locals())

def carousel_images(request):
    images = CarouselImage.objects.values('src', 'alt')
    return JsonResponse(list(images), safe=False)


@login_required
def about(request):
    totalItem = 0
    wishItem = 0
    if request.user.is_authenticated:
        totalItem = Cart.objects.filter(user=request.user).count()
        wishItem = Wishlist.objects.filter(user=request.user).count()
    return render(request, 'about.html', locals())

@login_required
def search(request):
    query  = request.GET['search']
    totalItem = 0
    wishItem = 0
    if request.user.is_authenticated:
        totalItem = Cart.objects.filter(user=request.user).count()
        wishItem = Wishlist.objects.filter(user=request.user).count()
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request, 'search.html', locals())

@login_required
def contact(request):
    totalItem = 0
    wishItem = 0
    if request.user.is_authenticated:
        totalItem = Cart.objects.filter(user=request.user).count()
        wishItem = Wishlist.objects.filter(user=request.user).count()
    return render(request, 'contact.html', locals())

def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        send_mail(
            subject=f'Contact Us Message from {name}',
            message=message,
            from_email=email,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
        )
        return redirect('contact_us_success')
    
    return render(request, 'contact_us.html')

def contact_us_success(request):
    return render(request, 'contact_us_success.html')

@method_decorator(login_required, name='dispatch')
class CategoryView(View):
    def get(self, request, val):
        totalItem = 0
        wishItem = 0
        if request.user.is_authenticated:
           totalItem = Cart.objects.filter(user=request.user).count()
           wishItem = Wishlist.objects.filter(user=request.user).count()
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'category.html', locals())

@method_decorator(login_required, name='dispatch')    
class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalItem = 0
        wishItem = 0
        if request.user.is_authenticated:
           totalItem = Cart.objects.filter(user=request.user).count()
           wishItem = Wishlist.objects.filter(user=request.user).count() 
        return render(request, 'category.html', locals())

@method_decorator(login_required, name='dispatch')     
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user)) 
        totalItem = 0
        wishItem = 0
        if request.user.is_authenticated:
           totalItem = Cart.objects.filter(user=request.user).count()
           wishItem = Wishlist.objects.filter(user=request.user).count()
        return render(request, 'product_detail.html', locals())
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalItem = 0
        wishItem = 0
        if request.user.is_authenticated:
            totalItem = Cart.objects.filter(user=request.user).count()
            wishItem = Wishlist.objects.filter(user=request.user).count()
        return render(request, 'customerregistrationform.html', locals())     
   
    def post(self, request): 
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            email = user.email
            email_subject = "Activate Your Account"
            message = render_to_string("activate.html", {
                'user': user,
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': generate_token.make_token(user)
            })
            email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
            email_message.send()

            messages.success(request, "Congratulations! User registered successfully. Please activate your account by clicking the link sent to your email.")
            return redirect('login')
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'customerregistrationform.html', locals())

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if user is not None and generate_token.check_token(user, token):
            user.is_active=True
            user.save()
            messages.info(request, "Account activated successfully")
            return redirect('login')
        return render(request,'activatefail.html')                   

@method_decorator(login_required, name='dispatch')             
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalItem = 0
        wishItem = 0
        if request.user.is_authenticated:
           totalItem = Cart.objects.filter(user=request.user).count()
           wishItem = Wishlist.objects.filter(user=request.user).count()
        return render(request, 'profile.html', locals()) 
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
             
            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, zipcode=zipcode)
            reg.save()
            messages.success(request, "Congratulations! Profile Set Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'profile.html', locals())

@login_required     
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalItem = 0
    wishItem = 0
    if request.user.is_authenticated:
        totalItem = Cart.objects.filter(user=request.user).count()
        wishItem = Wishlist.objects.filter(user=request.user).count()
    return render(request, 'address.html', locals())

@method_decorator(login_required, name='dispatch')
class UpdateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalItem = 0
        wishItem = 0
        if request.user.is_authenticated:
           totalItem = Cart.objects.filter(user=request.user).count()
           wishItem = Wishlist.objects.filter(user=request.user).count()
        return render(request, 'updateAddress.html', locals())
    
    def post(self, request, pk):
        form = CustomerProfileForm(request.POST)      
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            add.save()
            messages.success(request, "Congratulations! Profile Set Successfully")
        else:
            messages.warning(request, "Invalid Input Data")
        return redirect('/address')

def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})

def update_cart_quantity(request):
    if request.method == 'POST':
        prod_id = request.POST.get('prod_id')
        quantity = int(request.POST.get('quantity', 1))

        cart_item = get_object_or_404(Cart, product_id=prod_id, user=request.user)
        cart_item.quantity = quantity
        cart_item.save()

        return JsonResponse({'success': True, 'message': 'Cart quantity updated successfully.'})

    return JsonResponse({'error': 'Invalid request method.'}, status=400)


@login_required    
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    print('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/show_cart")

@login_required    
def add_to_wishlist(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    print('prod_id')
    product = Product.objects.get(id=product_id)
    Wishlist(user=user, product=product).save()
    return redirect("/show_wishlist")

@login_required    
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = sum(p.quantity * p.product.discounted_price for p in cart)
    totalamount = amount + 40
    totalItem = 0
    wishItem = 0
    if request.user.is_authenticated:
        totalItem = Cart.objects.filter(user=request.user).count()
        wishItem = Wishlist.objects.filter(user=request.user).count()      
    return render(request, "add_to_cart.html", locals())

@login_required
def show_wishlist(request):
    user = request.user
    totalItem = 0
    wishItem = 0
    if request.user.is_authenticated:
        totalItem = Cart.objects.filter(user=request.user).count()
        wishItem = Wishlist.objects.filter(user=request.user).count()      
    return render(request, "wishlist.html", locals())

@method_decorator(login_required, name='dispatch')
class Checkout(View):
    def get(self, request):
        totalItem = 0
        wishItem = 0
        if request.user.is_authenticated:
            totalItem = Cart.objects.filter(user=request.user).count()
            wishItem = Wishlist.objects.filter(user=request.user).count()
        user = request.user
        add = Customer.objects.filter(user=user)
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        totalamount = amount + 40
        stripeamount = int(totalamount * 100)

        payment_intent = stripe.PaymentIntent.create(
            amount=stripeamount,
            currency='usd',
            metadata={'integration_check': 'accept_a_payment'},
        )

        context = {
            'add': add,
            'cart': cart,
            'totalamount': totalamount,
            'client_secret': payment_intent['client_secret'],
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
            'totalItem': totalItem,
            'wishItem': wishItem,
        }

        return render(request, 'checkout.html', context)


def success_view(request):
    return render(request, 'success.html')

def cancel_view(request):
    return render(request, 'cancel.html')

@login_required    
def payment_done(request):
    if request.method == "POST":
        order_id = request.POST.get('order_id')
        payment_id = request.POST.get('payment_id')
        cust_id = request.POST.get('cust_id')

        if not all([order_id, payment_id, cust_id]):
            messages.error(request, "Missing payment details.")
            return redirect('check_out')

        try:
            user = request.user
            customer = get_object_or_404(Customer, id=cust_id)
            payment = get_object_or_404(Payment, stripe_order_id=order_id)

            # Update payment details
            payment.paid = True
            payment.stripe_payment_id = payment_id
            payment.save()

            # Process cart items into orders
            cart_items = Cart.objects.filter(user=user)
            for item in cart_items:
                OrderPlaced.objects.create(
                    user=user,
                    customer=customer,
                    product=item.product,
                    quantity=item.quantity,
                    payment=payment
                )
                item.delete()

            messages.success(request, "Payment successful! Your order has been placed.")
            return redirect('orders')

        except Customer.DoesNotExist:
            messages.error(request, "Customer not found.")
            return redirect('checkout')

        except Payment.DoesNotExist:
            messages.error(request, "Payment not found.")
            return redirect('checkout')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return redirect('checkout')

    return redirect('checkout')


@login_required
def orders(request):
    totalItem = 0
    wishItem = 0
    if request.user.is_authenticated:
        totalItem = Cart.objects.filter(user=request.user).count()
        wishItem = Wishlist.objects.filter(user=request.user).count()
        order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'orders.html', locals())

@login_required
def plus_Cart(request):
    if request.method == "GET":
        product_id = request.GET.get('prod_id')
        print('prod_id')
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        totalamount = amount + 40 
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount 
        }
        return JsonResponse(data)

@login_required
def minus_cart(request):
    if request.method == "GET":
        product_id = request.GET.get('prod_id')
        print('prod_id')
        c = Cart.objects.get(Q(product=product_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        print(f'User: {user}')
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        totalamount = amount + 40 
        data = {
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount 
        }
        return JsonResponse(data)

@login_required

def remove_Cart(request):
    if request.method == "GET":
        product_id = request.GET.get('prod_id')
        
        if not product_id:
            return JsonResponse({'error': 'Product ID is required'}, status=400)
        
        # Fetch the cart items for the given product and user
        cart_items = Cart.objects.filter(Q(product_id=product_id) & Q(user=request.user))
        
        if not cart_items.exists():
            return JsonResponse({'error': 'Cart item does not exist'}, status=404)
        
        # Delete all matching cart items
        cart_items.delete()
        
        # Calculate the total cart amount
        cart = Cart.objects.filter(user=request.user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        total_amount = amount + 40  # assuming 40 is some fixed additional charge
        
        data = {
            'amount': amount,
            'total_amount': total_amount 
        }
        
        return JsonResponse(data)
    
    return redirect(JsonResponse, 'checkout.html')

@login_required    
def plus_wishlist(request):
    if request.method == 'GET':
        product_id = request.GET.get('prod_id')
        print('prod_id')
        product = Product.objects.get(id=product_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data = {
            'message': 'Wishlist Added Successfully',
        }    
        return JsonResponse(data)

@login_required    
def minus_wishlist(request):
    if request.method == 'GET':
        product_id = request.GET.get('prod_id')
        print('prod_id')
        product = Product.objects.get(id=product_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data = {
            'message': 'Wishlist Removed Successfully',
        }    
        return JsonResponse(data)

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = CustomerProfileForm(instance=request.user)
    return render(request, 'custom_profile.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        role = request.POST.get('role')
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if role == 'admin' and user.is_staff:
                    return redirect('admin:index')  # Redirect to admin dashboard
                return redirect('user_dashboard')  # Redirect to user dashboard
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

# def admin_dashboard(request):
#     data = {
#         'message': 'Welcome to the admin dashboard'
#     }
#     return Response(data)

# class AdminProductList(View):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# class AdminProductCreate(View):
#     def get(self, request):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer

# class AdminProductUpdate(View):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'pk'

# class AdminProductDelete(View):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#     lookup_field = 'pk'

    
    
    