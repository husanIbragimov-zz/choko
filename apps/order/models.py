from django.contrib.auth.models import User
from django.db import models

from apps.base.models import BaseAbstractDate
from apps.product.models import Product


# Create your models here.

class Variant(BaseAbstractDate):
    duration = models.IntegerField()
    percent = models.IntegerField()

    def __str__(self):
        return self.duration


class Cart(BaseAbstractDate):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True, blank=True)
    completed = models.BooleanField(default=False)
    session_id = models.CharField(max_length=100)

    @property
    def num_of_items(self):
        cart_items = self.cart_items.all()
        return sum([i.quantity for i in cart_items])

    @property
    def cart_total(self):
        cart_items = self.cart_items.all()
        return sum([i.subtotal for i in cart_items])

    def __str__(self):
        return str(self.session_id)


class CartItem(BaseAbstractDate):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True, blank=True, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField()

    def __str__(self):
        return str(self.subtotal)

    @property
    def subtotal(self):
        return self.quantity * self.product.price
