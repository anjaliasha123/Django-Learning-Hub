from django.db import models       
from django.contrib import admin
from django.conf import settings
from django.core.validators import MinValueValidator, FileExtensionValidator
from uuid import uuid4

from store.validators import validate_file_size

# Create your models here.
class Promotion(models.Model):
    decription = models.CharField(max_length=255)
    discount = models.FloatField()


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering =['title']

class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=3)
    inventory = models.IntegerField()
    last_update = models.DateField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT, related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='store/images', validators=[validate_file_size])
    # image = models.FileField(upload_to='store/images', validators=[FileExtensionValidator(allowed_extensions=['pdf'])])


class Customer(models.Model):
    MEMBERSHIP_BRONZE = "B"
    MEMBERSHIP_GOLD = "G"
    MEMBERSHIP_SILVER = "S"

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, "Bronze"),
        (MEMBERSHIP_GOLD, "Gold"),
        (MEMBERSHIP_SILVER, "Silver"),
    ]

    # first_name = models.CharField(max_length=20)
    # last_name = models.CharField(max_length=20)
    # email = models.EmailField(max_length=254, unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #order_set

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
    
    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ('view_history', 'Can view history')
        ]

class Order(models.Model):
    PENDING = "P"
    COMPLETE = "C"
    FAILED = "F"

    PAYMENT_CHOICES = [
        (PENDING, "Pending"),
        (COMPLETE, "Complete"),
        (FAILED, "Failed")
    ]
    #orderitem_set
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_CHOICES, default=PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        permissions = [
            ('cancel_order', 'Can cancel order')
        ]

class OrderItem(models.Model):
    
    quantity = models.PositiveBigIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='orders')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orderitems')

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    zip = models.CharField(max_length=10)

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [['cart', 'product']]


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)