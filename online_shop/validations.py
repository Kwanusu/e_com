from django.core.validators import validate_email as django_validate_email
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError

def custom_validation(data):
    errors = {}
    # Example validation: Ensure 'username' and 'email' are present
    if 'username' not in data:
        errors['username'] = 'This field is required.'
    if 'email' not in data:
        errors['email'] = 'This field is required.'
    
    # Example: Ensure password is strong enough
    password = data.get('password', '')
    if len(password) < 8:
        errors['password'] = 'Password must be at least 8 characters long.'
    
    if errors:
        raise ValidationError(errors)
    
    return data

def validate_email(data):
    email = data.get('email', '')
    try:
        django_validate_email(email)
    except DjangoValidationError:
        raise ValidationError({'email': 'Invalid email address.'})

def validate_password(data):
    password = data.get('password', '')
    if len(password) < 8:
        raise ValidationError({'password': 'Password must be at least 8 characters long.'})
