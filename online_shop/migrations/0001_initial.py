# Generated by Django 4.2.13 on 2024-07-19 18:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CarouselImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('src', models.ImageField(upload_to='carousel_image')),
                ('alt', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('locality', models.CharField(max_length=200)),
                ('city', models.CharField(max_length=50)),
                ('mobile', models.IntegerField(default=0)),
                ('zipcode', models.IntegerField()),
                ('state', models.CharField(choices=[('NRB', 'Nairobi'), ('MSA', 'Mombasa'), ('KSM', 'Kisumu'), ('NKR', 'Nakuru'), ('ELD', 'Eldoret'), ('THK', 'Thika'), ('KSM', 'Kisii'), ('KTL', 'Kitale'), ('MLF', 'Malindi'), ('NYK', 'Nyeri'), ('MRU', 'Meru'), ('KAK', 'Kakamega'), ('GAR', 'Garissa'), ('KSM', 'Kericho'), ('EMB', 'Embu'), ('NGO', 'Nanyuki'), ('LOI', 'Lodwar'), ('MWI', 'Machakos'), ('VHI', 'Voi'), ('HOM', 'Homa Bay'), ('KIT', 'Kitui'), ('MUM', 'Mumias'), ('WJH', 'Wajir'), ('NDA', 'Naivasha'), ('KNG', 'Kangundo'), ('KLP', 'Kilifi'), ('BUS', 'Busia'), ('THI', 'Thika'), ('RUU', 'Ruiru'), ('NAN', 'Nandi Hills'), ('MAR', 'Marsabit'), ('MWZ', 'Mwihoko'), ('KWL', 'Kwale'), ('OLK', 'Ol Kalou'), ('RBU', 'Ruiru'), ('KIK', 'Kikuyu'), ('KON', 'Konza'), ('KED', 'Kendu Bay'), ('LSG', 'Lamu'), ('MIG', 'Migori'), ('MRT', 'Maralal'), ('TUK', 'Tukuyu')], max_length=100)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('selling_price', models.FloatField()),
                ('discounted_price', models.FloatField()),
                ('description', models.TextField()),
                ('composition', models.TextField(default='')),
                ('prodapp', models.TextField(default='')),
                ('category', models.CharField(choices=[('EL', 'Electronics'), ('KI', 'Kitchen'), ('MP', 'Mobile Phones'), ('SS', 'Sound Systems'), ('CS', 'Cameras'), ('BG', 'Bags'), ('CL', 'Clothes'), ('BB', 'Beds and Bedding'), ('CP', 'Computers'), ('EE', 'Electrical'), ('SD', 'Smart/Digital Tvs')], max_length=2)),
                ('product_image', models.ImageField(upload_to='product')),
            ],
        ),
        migrations.CreateModel(
            name='Wishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_shop.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('rating', models.IntegerField(blank=True, default=0, null=True)),
                ('comment', models.TextField(blank=True, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='online_shop.product')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('stripe_order_id', models.CharField(max_length=100)),
                ('stripe_payment_status', models.CharField(max_length=100)),
                ('stripe_payment_id', models.CharField(max_length=100)),
                ('paid', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderPlaced',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('ordered_date', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('Accepted', 'Accepted'), ('Packed', 'Packed'), ('On the way', 'On the way'), ('Delivered', 'Delivered'), ('Cancel', 'Cancel'), ('Pending', 'Pending')], default='Pending', max_length=50)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_shop.customer')),
                ('payment', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='online_shop.payment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_shop.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('qty', models.IntegerField(blank=True, default=0, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True)),
                ('image', models.CharField(blank=True, max_length=200, null=True)),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='online_shop.orderplaced')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='online_shop.product')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='online_shop.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
