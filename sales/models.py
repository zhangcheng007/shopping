from django.db import models
from shopping.models import Product
# Create your models here.

class Cart(models.Model):
    """
    Represents customer's shopping basket
    """
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

    def get_sub_total(self):
        """
        Sub total of cart items (without taxes)
        """
        sub_total = 0.0
        for item in self.items.all():
            sub_total += item.get_sub_total()

        return sub_total
    def get_taxes(self):
        """
        Total taxes applied on cart items
        """
        taxes = 0.0
        for item in self.get_items():
            taxes += item.get_taxes()

        return taxes

    def get_shipping_cost(self):
        """
        Return total cost for shipping
        """
        shipping_cost = 0.0
        for item in self.get_items():
            shipping_cost += item.get_shipping_cost()

        return shipping_cost

    def get_total(self):
        """
        Total price of cart items with taxes
        """
        return float(self.get_sub_total() + self.get_taxes() + self.get_shipping_cost())

    def get_items_count(self):
        """
        Returns total number of items
        """
        items_count = 0
        for item in self.get_items():
            items_count += item.quantity

        return items_count

    def add_item(self, product_id, quantity, user):
        """
        Add or augment quantity of product
        """
        if self.items.filter(product_id=product_id):
            item = self.items.get(product_id=product_id)
            item.quantity += quantity
            item.save()
            return item

        item = self.items.create(product_id=product_id,
                                 quantity=quantity,
                                 updated_by=str(user),
                                 created_by=str(user))

        return item

    def remove_item(self, product_id):
        """
        Remove an item from cart
        """
        try:
            cart_item = self.items.get(product_id=product_id)
            cart_item.delete()
        except CartItem.DoesNotExist:
            pass

    def remove_all_items(self):
        """
        Remove all items form cart
        """
        for item in self.get_items():
            item.delete()

    def update_item(self, product_id, quantity):
        """
        Update item quantity in database
        """
        self.items.filter(product_id=product_id).update(quantity=quantity)

    def get_items(self):
        """
        Fetch cart items with products and pics
        """
        return self.items.prefetch_related().all() # by zc

    def get_items_with_taxes(self):
        """
        Fetch cart items with products and taxes
        """
        return self.items.prefetch_related('product', 'product__tax').all()

    @classmethod
    def get_cart(cls, cart_id=None):
        """
        Returns existing cart or creates new one
        """
        if cart_id:
            return cls.objects.get(id=cart_id)

        return cls.objects.create()

class CartItem(models.Model):
    """
    Represents customer's product in basket
    """
    cart = models.ForeignKey(Cart, related_name='items')
    product = models.ForeignKey(Product)

    quantity = models.IntegerField(default=1)
    updated_on = models.DateTimeField(auto_now=True)
    updated_by = models.CharField(max_length=100)
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=100)

     #class Meta:
     #   db_table = 'sales_cart_item'
     #   ordering = ('id',)
     #   verbose_name_plural = 'Cart Items'
      #  unique_together = ('cart', 'product',)

    def get_sub_total(self):
        """
        Sub total of cart item (without taxes)
        """
        return float(self.product.price) * self.quantity

    def get_taxes(self):
        """
        Total taxes applied on cart item
        """
        product = self.product
        if product.tax:
            return product.tax.calculate(product.price, self.quantity)

        return 0.0

    def get_shipping_cost(self):
        """
        Returns total shipping cost
        """
        product = self.product
        if product.is_free_shipping:
            return 0.0

        return float(product.shipping_cost) * float(self.quantity)

    def get_total(self):
        """
        Total price of cart item with taxes
        """
        return self.get_sub_total() + self.get_taxes() + self.get_shipping_cost()