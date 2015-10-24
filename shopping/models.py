import datetime
from django.db import models
from django.utils import timezone

from financial.models import Tax

# Create your models here.
class Character(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

# Create your models here.
class Contact(models.Model):
    name   = models.CharField(max_length=200)
    age    = models.IntegerField(default=0)
    email  = models.EmailField()
    def __unicode__(self):
        return self.name

class Tag(models.Model):
    contact = models.ForeignKey(Contact)
    name    = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name




class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100)
    description = models.TextField(null=True, blank=True)
    pic = models.ImageField(upload_to='templates/images/category', null=True, blank=True)
    parent = models.ForeignKey('self', related_name='sub_categories', null=True, blank=True)
    tags = models.CharField(max_length=100, null=True, blank=True,
                            help_text='Comma-delimited set of SEO keywords for meta tag')
    display_order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    is_expended = models.BooleanField(default=False, help_text='Catergory will always shown expended')
    updated_by = models.CharField(null=True, blank=True,max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField( null=True, blank=True,max_length=100)
    def __str__(self):          # __unicode__ on Python 2
        return self.name
    def was_published_recently(self):
        return self.created_on >= timezone.now() - datetime.timedelta(days=1)



class Product(models.Model):
    """
    Represents a Product
    """
    name = models.CharField(max_length=100)
    slug = models.SlugField(null=True, blank=True,max_length=100)
    sku = models.CharField(max_length=50, verbose_name='SKU', null=True, blank=True)
    gtin = models.CharField(max_length=50, verbose_name='GTIN', null=True, blank=True,
                            help_text='Global Trade Item Number (GTIN)')
    category = models.ForeignKey(Category)
    gist = models.CharField(
        max_length=500, null=True, blank=True, help_text='Short description of the product')
    description = models.TextField(
        null=True, blank=True, help_text='Full description displayed on the product page')
    price = models.DecimalField(
        max_digits=9, decimal_places=2, help_text='Per unit price')
    old_price = models.DecimalField(
        max_digits=9, decimal_places=2, default=0.0)
    cost = models.DecimalField(
        max_digits=9, decimal_places=2, default=0.0, help_text='Per unit cost')
    shipping_cost = models.DecimalField(
        max_digits=9, decimal_places=2, default=0.0, help_text='Shipping cost per unit')
    quantity = models.IntegerField(help_text='Stock quantity')
    is_active = models.BooleanField(
        default=True, help_text='Product is available for listing and sale')
    is_bestseller = models.BooleanField(
        default=False, help_text='It has been best seller')
    is_featured = models.BooleanField(
        default=False, help_text='Promote this product on main pages')
    is_free_shipping = models.BooleanField(
        default=False, help_text='No shipping charges')
    tax = models.ForeignKey(
        Tax, null=True, blank=True,  help_text='Tax applied on this product, if tax exempt select none')
    tags = models.CharField(max_length=250, null=True, blank=True,
                            help_text='Comma-delimited set of SEO keywords for meta tag')
    weight = models.FloatField(default=0)
    length = models.FloatField(default=0)
    width = models.FloatField(default=0)
    height = models.FloatField(default=0)
    updated_by = models.CharField( null=True, blank=True,max_length=100)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField( null=True, blank=True,max_length=100)
    def __str__(self):              # __unicode__ on Python 2
        return self.name
    def was_published_recently(self):
        return self.created_on >= timezone.now() - datetime.timedelta(days=1)


class ProductSpec(models.Model):
    """
    Represents product specification attribute  related_name='specs'
    """
    product = models.ForeignKey(Product)
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=250)
    display_order = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(null=True, blank=True,max_length=100)
    def __str__(self):              # __unicode__ on Python 2
        return '%s: %s' % (self.name, self.value)



class ProductPic(models.Model):
    """
    Represents product picture related_name='pics'
    """
    product = models.ForeignKey(Product)
    url = models.ImageField(upload_to="templates/images/products")
    display_order = models.IntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    def __str__(self):
        return '%s [Pic #id %s]' % (self.product, self.id)
         #return self.url







