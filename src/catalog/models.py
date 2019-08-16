import decimal
import uuid
from datetime import datetime, timedelta
from django.db import models

from accounts.models import Vendor, Customer
from photos.models import Album, Photo
from users.models import User, Acl

# Create your models here.
class Category(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)
    # a2.parent = a1; a1.children.all()
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    visible = models.BooleanField(default=True)
    show_on_homepage = models.BooleanField(default=False)
    acl = models.ForeignKey(Acl, related_name='categories', on_delete=models.DO_NOTHING, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

class Product(models.Model):
    PRODUCT_TYPE_CHOICES = (
        ('PRODUCT', 'Product'),
        ('AUCTION', 'Auction'),
        ('SERVICE', 'Service'),
    )
    DURATION_MEASURE_CHOICES = (
        ('DAY', 'Day'),
        ('HOUR', 'Hour'),
    )

    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    product_type = models.CharField(max_length=30, choices=PRODUCT_TYPE_CHOICES, blank=True, null=True)
    # a2.parent = a1; a1.children.all()
    duration_measure = models.CharField(max_length=4, choices=DURATION_MEASURE_CHOICES, null=True, blank=True)
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    album = models.OneToOneField(Album, on_delete=models.CASCADE, related_name='product', null=True, blank=True)
    vendor = models.ForeignKey(Vendor, related_name='products', on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='products', blank=True)
    acl = models.ForeignKey(Acl, related_name='products', on_delete=models.DO_NOTHING, null=True, blank=True)
    is_aux = models.BooleanField(default=False)
    stock_quantity = models.PositiveIntegerField(default=0, blank=True)
    low_stock = models.BooleanField(default=False)
    out_of_stock = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    mark_as_new = models.BooleanField(default=False)
    new_start = models.DateTimeField(null=True, blank=True)
    new_end = models.DateTimeField(null=True, blank=True)
    not_returnable = models.BooleanField(default=False)
    show_on_homepage = models.BooleanField(default=False)
    featured = models.BooleanField(default=False)
    allow_reviews = models.BooleanField(default=False)
    vendor_comments = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=11, decimal_places=2, null=True, blank=True)
    sales_rate = models.FloatField(null=True, blank=True)
    on_sale = models.BooleanField(default=False)
    is_free = models.BooleanField(default=False)
    call_for_price = models.BooleanField(default=False)
    weight = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    lenght = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    width = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    sold = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_discount(self):
        discount = self.sales_rate * self.price
        return discount

    @property
    def get_sales_price(self):
        sales_price = self.price - self.get_discount
        return sales_price

    def __str__(self):
        return self.name

class Reservation(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    product = models.ForeignKey(Product, related_name="reservations", on_delete=models.CASCADE)
    reserved_start_date = models.DateField(null=True, blank=True)
    reserved_start_time = models.TimeField(null=True, blank=True)
    reserved_end_date = models.DateField(null=True, blank=True)
    reserved_end_time = models.TimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    client = models.ForeignKey(Customer, related_name='reservations', on_delete=models.CASCADE, null=True, blank=True)
    booked = models.BooleanField(default=False)

    def __str__(self):
        return self.product.name

    @property
    def duration(self):
        if self.product.duration_measure == 'HOUR':
            start = datetime.combine(self.reserved_start_date, self.reserved_start_time)
            end = datetime.combine(self.reserved_end_date, self.reserved_end_time)
            diff = end - start
            diff_in_hours = diff.total_seconds() / 3600
            return diff_in_hours
        elif self.product.duration_measure == 'DAY':
            diff =  self.reserved_end_date - self.reserved_start_date
            return diff.days
        else:
            return 0.0

    @property
    def total(self):
        return decimal.Decimal(self.duration) * self.product.price


class Review(models.Model):
    slug = models.SlugField(unique=True, default=uuid.uuid1, blank=True)
    customer = models.ForeignKey(User, related_name='reviews', on_delete=models.CASCADE)
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    is_approved = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    content = models.TextField(null=True, blank=True)
    reply = models.TextField(null=True, blank=True)
    rating = models.PositiveIntegerField(null=True, blank=True)
