from ckeditor.fields import RichTextField
from django.db import models
from apps.base.models import BaseAbstractDate
from apps.product.models import BannerDiscount, Advertisement, STATUS, Brand, Size


class Tag(BaseAbstractDate):
    title = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.title


class Clothing(BaseAbstractDate):
    banner_discount = models.ForeignKey(BannerDiscount, on_delete=models.SET_NULL, null=True, blank=True,
                                        related_name='clothing_banner_discount')
    advertisement = models.ForeignKey(Advertisement, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='clothing_advertisement')
    status = models.CharField(choices=STATUS, default='NEW', max_length=10, null=True, blank=True)
    title = models.CharField(max_length=200, null=True)
    description = RichTextField(null=True, blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, related_name='clothing_brand')
    size = models.ManyToManyField(Size, related_name='clothing_sizes', blank=True)
    tags = models.ManyToManyField(Tag, related_name='clothing_tags', blank=True)
    view = models.PositiveIntegerField(default=0)
    availability = models.PositiveIntegerField()
    has_size = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        if self.title:
            return self.title
        return self.id


