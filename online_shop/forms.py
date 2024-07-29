from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm,SetPasswordForm,PasswordResetForm
from django.contrib.auth.models import User
from .models import Customer
from .models import Payment
from django.core.exceptions import ValidationError

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': 'True',
    'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
    'class': 'form-control'}))

class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'True', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))   
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError('A user with that email already exists.')
        return email
        
class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs=
    {'autofocus ':'True', 'autocomplete': 'current-password', 'class': 'form-control'}))        
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs=
    { 'autocomplete': 'current-password', 'class': 'form-control'}))        
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs=
    {'autocomplete': 'current-password', 'class': 'form-control'}))        
        
class MyPasswordResetForm(PasswordResetForm):
     email = forms.EmailField(widget=forms.EmailInput(attrs={
    'class': 'form-control'}))

class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs=
    { 'autocomplete': 'current-password', 'class': 'form-control'}))        
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput(attrs=
    {'autocomplete': 'current-password', 'class': 'form-control'}))        
    
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'locality', 'city', 'mobile', 'state', 'zipcode']
        widgets={
            'name':forms.TextInput(attrs={'class': 'form-control'}),
            'locality':forms.TextInput(attrs={'class': 'form-control'}),
            'city':forms.TextInput(attrs={'class': 'form-control'}),  
            'mobile':forms.NumberInput(attrs={'class': 'form-control'}),
            'state':forms.Select(attrs={'class': 'form-control'}),
            'zipcode':forms.TextInput(attrs={'class': 'form-control'}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount', 'stripe_order_id', 'stripe_payment_status', 'stripe_payment_id']

        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'stripe_order_id': forms.TextInput(attrs={'class': 'form-control'}),
            'stripe_payment_status': forms.TextInput(attrs={'class': 'form-control'}),
            'stripe_payment_id': forms.TextInput(attrs={'class': 'form-control'}),
        }
        
class PaymentIntentForm(forms.Form):
    amount = forms.DecimalField(label='Amount (USD)', max_digits=10, decimal_places=2) 
    
    
class PaymentMethodForm(forms.Form):
    payment_method_id = forms.CharField(widget=forms.HiddenInput())            