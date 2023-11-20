from django.db import models
from django.contrib.auth.models import User

PRODUCT_TYPE = (
    ('book', 'Book'),
    ('clothing', 'Clothing'),
    ('product', 'Product')
)


ROLE = (
    ('admin', 'Admin'),
    ('content_maker', 'Content_Maker'),
    ('staff', 'Staff'),
)


class BaseAbstractDate(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Profile(BaseAbstractDate):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True)
    role = models.CharField(max_length=15, choices=ROLE, default='staff')

    def __str__(self):
        return f"{self.user}"


class Variant(BaseAbstractDate):
    name = models.CharField(max_length=50, null=True, blank=True)
    product_type = models.CharField(max_length=50, null=True, blank=True, choices=PRODUCT_TYPE)
    duration = models.IntegerField()
    percent = models.IntegerField()
    is_integration = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return str(self.duration)
