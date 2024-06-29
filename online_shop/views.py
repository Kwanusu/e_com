from django.db.models import Count
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import Cart, Customer, OrderPlaced, Payment, Product, Wishlist
from django.contrib import messages
from django.db.models import Q
...
from .models import (
   Payment 
)
import stripe
stripe.api_key = settings.STRIPE_PUBLISHABLE_KEY
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CustomerProfileForm, CustomerRegistrationForm

# Create your views here.
@login_required
def home(request):
    totalItem = 0
    wishItem = 0
    if request.user.is_authenticated:
        totalItem = len(Cart.objects.filter(user=request.user))
        wishItem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'home.html', locals())

@login_required
def about(request):
    totalItem = 0
    wishItem = 0
    if request.user.is_authenticated:
        totalItem = len(Cart.objects.filter(user=request.user))
        wishItem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'about.html', locals())

@login_required
def search(request):
    query  = request.GET['search']
    totalItem = 0
    wishItem = 0
    if request.user.is_authenticated:
        totalItem = len(Cart.objects.filter(user=request.user))
        wishItem = len(Wishlist.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render(request,'search.html', locals())

@login_required
def contact(request):
    totalItem = 0
    wishItem = 0
    if request.user.is_authenticated:
        totalItem = len(Cart.objects.filter(user=request.user))
        wishItem = len(Wishlist.objects.filter(user=request.user))
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


@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self, request, val):
        totalItem = 0
        wishItem = 0
        if request.user.is_authenticated:
           totalItem = len(Cart.objects.filter(user=request.user))
           wishItem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title = Product.objects.filter(category=val).values('title')
        return render(request, 'category.html', locals())

@method_decorator(login_required,name='dispatch')    
class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalItem = 0
        wishItem = 0
        if request.user.is_authenticated:
           totalItem = len(Cart.objects.filter(user=request.user))
           wishItem = len(Wishlist.objects.filter(user=request.user)) 
        return render(request, 'category.html', locals())

@method_decorator(login_required,name='dispatch')     
class ProductDetail(View):
    def get(self, request, pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user= request.user)) 
        totalItem = 0
        wishItem = 0
        if request.user.is_authenticated:
           totalItem = len(Cart.objects.filter(user=request.user))
           wishItem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'product_detail.html', locals())
    
class CustomerRegistrationView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        totalItem = 0
        wishItem = 0
        if request.user.is_authenticated:
           totalItem = len(Cart.objects.filter(user=request.user))
           wishItem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'customerregistrationform.html', locals())     
    def post(self, request): 
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! User Register Successful")
        else:
            messages.warning(request, "Invalid Input Data")
        return render(request, 'customerregistrationform.html', locals())              
     
@method_decorator(login_required,name='dispatch')             
class ProfileView(View):
    def get(self, request):
        form = CustomerProfileForm()
        totalItem = 0
        wishItem = 0
        if request.user.is_authenticated:
           totalItem = len(Cart.objects.filter(user=request.user))
           wishItem = len(Wishlist.objects.filter(user=request.user))
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
             
            reg = Customer(user=user, name=name, locality=locality, mobile=mobile, city=city, state=state, 
            zipcode=zipcode)
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
        totalItem = len(Cart.objects.filter(user=request.user))
        wishItem = len(Wishlist.objects.filter(user=request.user))
    return render(request, 'address.html', locals())

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self, request, pk):
        add = Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalItem = 0
        wishItem = 0
        if request.user.is_authenticated:
           totalItem = len(Cart.objects.filter(user=request.user))
           wishItem = len(Wishlist.objects.filter(user=request.user))
        return render(request, 'updateAddress.html', locals())
    
    def post(self, request,pk):
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
        return redirect("/address")
    
def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_list.html', {'products': products})
    

@login_required    
def add_to_cart(request):
    user = request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user, product=product).save()
    return redirect("/show_cart" )
    
@login_required    
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount =amount + 40
    totalItem = 0
    wishItem = 0
    if request.user.is_authenticated:
        totalItem = len(Cart.objects.filter(user=request.user))
        wishItem = len(Wishlist.objects.filter(user=request.user))      
    return render(request,"add_to_cart.html", locals())

@login_required
def show_wishlist(request):
    user = request.user
    totalItem = 0
    wishItem = 0
    if request.user.is_authenticated:
        totalItem = len(Cart.objects.filter(user=request.user))
        wishItem = len(Wishlist.objects.filter(user=request.user))      
    return render(request,"wishlist.html", locals())

    

# @method_decorator(login_required,name='dispatch')
# class Checkout(View):
#     def get(self, request):
#         totalItem = 0
#         wishItem = 0
#         if request.user.is_authenticated:
#            totalItem = len(Cart.objects.filter(user=request.user))
#            wishItem = len(Wishlist.objects.filter(user=request.user))
#         user = request.user
#         add = Customer.objects.filter(user=user)
#         cart = Cart.objects.filter(user=user)
#         amount = 0
#         for p in cart:
#             value = p.quantity * p.product.discounted_price
#             amount = amount + value
#         totalamount =amount + 40
#         stripeamount = int(totalamount * 100)
#         client = stripe.Client(auth=(settings.STRIPE_KEY_ID, settings.STRIPE_KEY_SECRET))
#         data = {'amount': stripeamount, 'currency': "Kshs", 'receipt': "order_rcptid_12"}    
#         return render(request, 'checkout.html',locals())


stripe.api_key = settings.STRIPE_SECRET_KEY

class Checkout(View):
    def get(self, request):
        totalItem = 0
        wishItem = 0
        if request.user.is_authenticated:
            totalItem = len(Cart.objects.filter(user=request.user))
            wishItem = len(Wishlist.objects.filter(user=request.user))
        user = request.user
        add = Customer.objects.filter(user=user)
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
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
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    cust_id = request.GET.get('cust_id')    
    user = request.user
    customer = Customer.objects.get(id=cust_id)
    payment = Payment.objects.get(stripe_order_id=order_id)
    payment.paid = True
    payment.stripe_payment_id = payment_id
    payment.save()
    cart = Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()
        
    return redirect('orders')

@login_required
def orders(request):
    totalItem = 0
    wishItem = 0
    if request.user.is_authenticated:
        totalItem = len(Cart.objects.filter(user=request.user))
        wishItem = len(Wishlist.objects.filter(user=request.user))
    order_placed = OrderPlaced.objects.filter(user=request.user)
    return render(request, 'orders.html',locals())    

def plus_Cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount =amount + 40 
        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount 
        }
        return JsonResponse(data)
    

def minus_Cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount =amount + 40 
        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount 
        }
        return JsonResponse(data)
    
    
@login_required    
def remove_Cart(request):
    if request.method == "GET":
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity+=1
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount =amount + 40 
        data={
            'quantity': c.quantity,
            'amount': amount,
            'totalamount': totalamount 
        }
        return JsonResponse(data)
    
    
@login_required    
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data ={
            'message':'Wishlist Added Successfully',
        }    
        return JsonResponse(data)
    
@login_required    
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).delete()
        data ={
            'message':'Wishlist Removed Successfully',
        }    
        return JsonResponse(data)




