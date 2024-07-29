from django.shortcuts import render, get_object_or_404, redirect
from online_shop.models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist
from .forms import ProductForm, CustomerForm, CartForm, PaymentForm, OrderPlacedForm, WishlistForm, UserForm
from django.contrib.auth.decorators import user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User

def admin_check(user):
    return user.is_staff

# A decorator to restrict access to admin users
def admin_required(view_func):
    decorated_view_func = user_passes_test(lambda u: u.is_staff, login_url='/login/')(view_func)
    return decorated_view_func

@admin_required
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

@admin_required
def admin_product_list(request):
    products = Product.objects.all()
    return render(request, 'admin_product_list.html', {'products': products})

@admin_required
def admin_product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_product_list')
    else:
        form = ProductForm()
    return render(request, 'admin_product_form.html', {'form': form})

@admin_required
def admin_product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('admin_product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin_product_form.html', {'form': form})

@admin_required
def admin_product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('admin_product_list')
    return render(request, 'admin_product_confirm_delete.html', {'product': product})

@admin_required
def admin_user_list(request):
    users = User.objects.all()
    return render(request, 'admin_user_list.html', {'users': users})

@admin_required
def admin_user_create(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully.')
            return redirect('admin_user_list')
    else:
        form = UserForm()
    return render(request, 'admin_user_form.html', {'form': form})

@admin_required
def admin_user_update(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('admin_user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'admin_user_form.html', {'form': form})

@admin_required
def admin_user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'User deleted successfully.')
        return redirect('admin_user_list')
    return render(request, 'admin_user_confirm_delete.html', {'user': user})
