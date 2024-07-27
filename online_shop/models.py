from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
# models.py

CATEGORY_CHOICES = (
    ('EL', 'Electronics'),
    ('KI', 'Kitchen'),
    ('MP', 'Mobile Phones'),
    ('SS', 'Sound Systems'),
    ('CS', 'Cameras'),
    ('BG', 'Bags'),
    ('CL', 'Clothes'),
    ('BB', 'Beds and Bedding'),
    ('CP', 'Computers'),
    ('EE', 'Electrical'),
    ('SD', 'Smart/Digital Tvs'),
) 
STATE_CHOICES = (
    ('NRB', 'Nairobi'),
    ('MSA', 'Mombasa'),
    ('KSM', 'Kisumu'),
    ('NKR', 'Nakuru'),
    ('ELD', 'Eldoret'),
    ('THK', 'Thika'),
    ('KSM', 'Kisii'),
    ('KTL', 'Kitale'),
    ('MLF', 'Malindi'),
    ('NYK', 'Nyeri'),
    ('MRU', 'Meru'),
    ('KAK', 'Kakamega'),
    ('GAR', 'Garissa'),
    ('KSM', 'Kericho'),
    ('EMB', 'Embu'),
    ('NGO', 'Nanyuki'),
    ('LOI', 'Lodwar'),
    ('MWI', 'Machakos'),
    ('VHI', 'Voi'),
    ('HOM', 'Homa Bay'),
    ('KIT', 'Kitui'),
    ('MUM', 'Mumias'),
    ('WJH', 'Wajir'),
    ('NDA', 'Naivasha'),
    ('KNG', 'Kangundo'),
    ('KLP', 'Kilifi'),
    ('BUS', 'Busia'),
    ('THI', 'Thika'),
    ('RUU', 'Ruiru'),
    ('NAN', 'Nandi Hills'),
    ('MAR', 'Marsabit'),
    ('MWZ', 'Mwihoko'),
    ('KWL', 'Kwale'),
    ('OLK', 'Ol Kalou'),
    ('RBU', 'Ruiru'),
    ('KIK', 'Kikuyu'),
    ('KON', 'Konza'),
    ('KED', 'Kendu Bay'),
    ('LSG', 'Lamu'),
    ('MIG', 'Migori'),
    ('MRT', 'Maralal'),
    ('TUK', 'Tukuyu'),
)



# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price =models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    composition = models.TextField(default='')
    prodapp = models.TextField(default='')
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    product_image = models.ImageField(upload_to='product')
    
    def __str__(self):
        return self.title
    
class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True) 
    name = models.CharField(max_length=200,null=True,blank=True)
    rating = models.IntegerField(null=True,blank=True,default=0)
    comment = models.TextField(null=True,blank=True)
    
    def __str__(self):
        return self.name 
        
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    order = models.ForeignKey('OrderPlaced',on_delete=models.SET_NULL,null=True) 
    name = models.CharField(max_length=200,null=True,blank=True)
    qty = models.IntegerField(null=True,blank=True,default=0)
    price = models.DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    image = models.CharField(max_length=200,null=True,blank=True)

    
    def __str__(self):
        return self.name    
    
    
class Customer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name =models.CharField(max_length=200)
    locality =models.CharField(max_length=200)
    city =models.CharField(max_length=50)
    mobile = models.IntegerField(default=0)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=100)
    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
    
STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the way', 'On the way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
    ('Pending', 'Pending'),
)    
       

class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.FloatField()
    stripe_order_id = models.CharField(max_length=100)
    stripe_payment_status = models.CharField(max_length=100)
    stripe_payment_id = models.CharField(max_length=100)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return self.stripe_order_id

        
    
class OrderPlaced(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models. CASCADE)
    customer =models.ForeignKey(Customer,on_delete=models.CASCADE)
    product =models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity =models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
        
class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models. CASCADE)
    product =models.ForeignKey(Product,on_delete=models.CASCADE)
    
    
class CarouselImage(models.Model):
    src = models.ImageField(upload_to='carousel_image')
    alt = models.CharField(max_length=200)

    def __str__(self):
        return self.alt    
