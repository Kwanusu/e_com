from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import CarouselImage, Cart, Wishlist, Product, Customer, Payment, OrderPlaced
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str as force_text
from django.contrib.auth.tokens import default_token_generator as generate_token
from django.contrib.auth.tokens import default_token_generator


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.product = Product.objects.create(
            title='Test Product',
            category='Electronics',
            discounted_price=100
        )
        self.cart = Cart.objects.create(user=self.user, product=self.product, quantity=1)
        self.wishlist = Wishlist.objects.create(user=self.user, product=self.product)
        self.customer = Customer.objects.create(
            user=self.user,
            name='Test User',
            locality='Test Locality',
            city='Test City',
            mobile='1234567890',
            state='Test State',
            zipcode='123456'
        )

    def test_home_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_carousel_images_view(self):
        CarouselImage.objects.create(src='image1.jpg', alt='Image 1')
        response = self.client.get(reverse('carousel_images'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), [{'src': 'image1.jpg', 'alt': 'Image 1'}])

    def test_about_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'about.html')

    def test_search_view(self):
        response = self.client.get(reverse('search'), {'search': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'search.html')
        self.assertContains(response, 'Test Product')

    def test_contact_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('contact'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact.html')

    def test_contact_us_view(self):
        response = self.client.get(reverse('contact_us'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contact_us.html')

    def test_contact_us_post(self):
        response = self.client.post(reverse('contact_us'), {
            'name': 'Test User',
            'email': 'test@example.com',
            'message': 'Test message'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('contact_us_success'))

    def test_category_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('category', args=['Electronics']))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'category.html')
        self.assertContains(response, 'Test Product')

    def test_product_detail_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('product_detail', args=[self.product.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'product_detail.html')
        self.assertContains(response, 'Test Product')

    def test_customer_registration_view_get(self):
        response = self.client.get(reverse('customer_registration'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customerregistrationform.html')

    def test_customer_registration_view_post(self):
        response = self.client.post(reverse('customer_registration'), {
            'username': 'newuser',
            'password1': 'newpassword',
            'password2': 'newpassword',
            'email': 'newuser@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customerregistrationform.html')

    def test_password_reset_request_view_get(self):
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset.html')

    def test_password_reset_request_view_post(self):
        response = self.client.post(reverse('password_reset'), {'email': self.user.email})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_password_reset_confirm_view_get(self):
        uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        response = self.client.get(reverse('password_reset_confirm', args=[uidb64, token]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'password_reset_confirm.html')

    def test_profile_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profile.html')

    def test_address_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('address'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'address.html')

    def test_add_to_cart_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('add_to_cart'), {'prod_id': self.product.id})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show_cart'))

    def test_add_to_wishlist_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('add_to_wishlist'), {'prod_id': self.product.id})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('show_wishlist'))

    def test_show_cart_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('show_cart'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_to_cart.html')

    def test_show_wishlist_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('show_wishlist'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'wishlist.html')

    def test_checkout_view_get(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout.html')

    def test_payment_done_view_post(self):
        payment = Payment.objects.create(
            stripe_order_id='test_order_id',
            stripe_payment_id='test_payment_id',
            customer=self.customer,
            amount=100,
            paid=True
        )
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(reverse('payment_done'), {
            'order_id': payment.stripe_order_id,
            'payment_id': payment.stripe_payment_id,
            'cust_id': self.customer.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('orders'))

    def test_orders_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'orders.html')

    def test_plus_cart_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('plus_cart'), {'prod_id': self.product.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"quantity": 2')

    def test_minus_cart_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('minus_cart'), {'prod_id': self.product.id})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '"quantity": 1')
