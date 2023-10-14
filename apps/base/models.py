from django.db import models

PRODUCT_TYPE = (
    ('book', 'Book'),
    ('clothing', 'Clothing'),
    ('product', 'Product')
)


class BaseAbstractDate(models.Model):
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Variant(BaseAbstractDate):
    name = models.CharField(max_length=50, null=True, blank=True)
    product_type = models.CharField(max_length=50, null=True, blank=True, choices=PRODUCT_TYPE)
    duration = models.IntegerField()
    percent = models.IntegerField()
    is_integration = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return str(self.duration)
