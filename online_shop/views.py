import stripe
from django.conf import settings
from django.http import BadHeaderError, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from .models import Cart, Customer, OrderPlaced, Payment, Product, Wishlist
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CustomerProfileForm, CustomerRegistrationForm, LoginForm, MyPasswordResetForm
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
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.core.mail import EmailMultiAlternatives

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
            form.save()
            messages.success(request, "Congratulations! User Register Successful")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'customerregistrationform.html', locals())    

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            email_subject = "Password Reset Requested"
            context = {
                'user': user,
                'domain': '127.0.0.1:8000',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            }
            
            text_content = render_to_string("password_reset_email.html", context)
            html_content = render_to_string("password_reset_email.html", context)
            
            # message = render_to_string("password_reset_email.html", {
            #     'user': user,
            #     'domain': '127.0.0.1:8000',
            #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            #     'token': default_token_generator.make_token(user),
            # })
            email_message = EmailMultiAlternatives(email_subject, text_content, settings.EMAIL_HOST_USER, [email])
            email_message.attach_alternative(html_content, "text/html")
            email_message.send()
            
            
            # email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
            # email_message.send()
            messages.success(request, 'A link to reset your password has been sent to your email.')
            return redirect('login')
        except User.DoesNotExist:
            messages.warning(request, "No user found with this email address.")
            return render(request, "password_reset.html")
    return render(request, 'password_reset.html')

def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            password = request.POST['pass1']
            confirm_password = request.POST['pass2']
            if password != confirm_password:
                messages.warning(request, "Passwords did not match.")
                return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
            user.set_password(password)
            user.save()
            messages.success(request, 'Your password has been successfully reset.')
            return redirect('login')
        return render(request, 'password_reset_confirm.html', {'uidb64': uidb64, 'token': token})
    else:
        messages.warning(request, 'The reset link is invalid, possibly because it has already been used.')
        return redirect('password_reset')
import logging

logger = logging.getLogger(__name__)
class PasswordResetView(View):
    def get(self, request):
        form = MyPasswordResetForm()
        return render(request, 'password_reset.html', {'form': form})
    
    def post(self, request):
        form = MyPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_users = User.objects.filter(Q(email=email))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "password_reset_email.html"
                    context = {
                        'email': user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Innovet Tech',
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'user': user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email_content = render_to_string(email_template_name, context)
                    try:
                        logger.info(f"Sending email to {user.email}")
                        send_mail(subject, email_content, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                        logger.info(f"Password reset email sent to {user.email}")
                    except BadHeaderError:
                        logger.error("Invalid header found.")
                        return HttpResponse('Invalid header found.')
                    except Exception as e:
                        logger.error(f"Error sending email: {str(e)}")
                    messages.success(request, 'A message with reset password instructions has been sent to your inbox.')
                    return redirect("password_reset_done")
            else:
                logger.warning(f"No user associated with email: {email}")
        else:
            logger.warning("Invalid form submission.")
        
        messages.error(request, 'An invalid email has been entered.')
        return render(request, 'password_reset.html', {'form': form})
class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            messages.info(request, "Account activated successfully")
            return redirect('login')
        return render(request, 'activatefail.html')  
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
        if request.user.is_authenticated:
            totalItem = Cart.objects.filter(user=request.user).count()
            wishItem = Wishlist.objects.filter(user=request.user).count()
        else:
            totalItem = 0
            wishItem = 0
        
        user = request.user
        add = Customer.objects.filter(user=user)
        cart = Cart.objects.filter(user=user)
        amount = sum(p.quantity * p.product.discounted_price for p in cart)
        totalamount = amount + 40  # Total amount in your currency
        stripeamount = int(totalamount * 100)  # Convert to cents for Stripe

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
    
def create_payment_intent(request):
    if request.method == 'POST':
        amount = int(request.POST['amount'])  # Amount in cents
        currency = 'usd'
        description = 'Example payment'

        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency=currency,
                description=description,
                payment_method_types=['card'],
            )

            context = {
                'client_secret': payment_intent.client_secret,
                'amount': amount,
                'currency': currency,
            }

            return render(request, 'payment.html', context)
        except stripe.error.StripeError as e:
            return render(request, 'error.html', {'error_message': str(e)})
    else:
        return render(request, 'payment_form.html')
    
def save_payment_method(request):
    if request.method == 'POST':
        payment_method_id = request.POST['payment_method_id']
        
        try:
            customer_id = request.user.profile.stripe_customer_id

            stripe.PaymentMethod.attach(payment_method_id, customer=customer_id)

            stripe.Customer.modify(
                customer_id,
                invoice_settings={'default_payment_method': payment_method_id}
            )

            return redirect('wallet_info')
        except stripe.error.StripeError as e:
            return render(request, 'error.html', {'error_message': str(e)})
    else:
        return render(request, 'payment_method_form.html')

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
            return redirect('checkout')

        try:
            user = request.user
            customer = get_object_or_404(Customer, id=cust_id)
            payment = get_object_or_404(Payment, stripe_order_id=order_id)

            payment.paid = True
            payment.stripe_payment_id = payment_id
            payment.save()

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

def plus_Cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        try:
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
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
        except Cart.DoesNotExist:
            data = {
                'error': 'Cart item not found'
            }
        return JsonResponse(data)

def minus_Cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        try:
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            if c.quantity > 1:
                c.quantity -= 1
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
        except Cart.DoesNotExist:
            data = {
                'error': 'Cart item not found'
            }
        return JsonResponse(data)

@login_required
def remove_Cart(request):
    if request.method == "GET":
        prod_id = request.GET.get('prod_id')
        try:
            c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
            c.delete()
            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = sum(p.quantity * p.product.discounted_price for p in cart)
            totalamount = amount + 40
            data = {
                'amount': amount,
                'totalamount': totalamount
            }
        except Cart.DoesNotExist:
            data = {
                'error': 'Cart item not found'
            }
        return JsonResponse(data)

@login_required
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data = {
            'message': 'Wishlist Added Successfully',
        }
        return JsonResponse(data)

@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
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
    return render(request, 'profile.html', {'form': form})

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
                if role == 'admin':
                    if user.is_superuser:
                        return redirect('custom_admin_dashboard')  # Redirect to custom admin dashboard
                    elif user.is_staff:
                        return redirect('admin_dashboard')  # Redirect to staff dashboard
                else:
                    return redirect('home')  # Redirect to user dashboard
            else:
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

