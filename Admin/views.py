from django.shortcuts import render, get_object_or_404, redirect
from online_shop.models import Product, Customer, Cart, Payment, OrderPlaced, Wishlist
from .forms import ProductForm, CustomerForm, CartForm, PaymentForm, OrderPlacedForm, WishlistForm
from django.contrib.auth.decorators import user_passes_test

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
