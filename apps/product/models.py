from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from django.db.models import Avg
from django.utils.safestring import mark_safe
from mptt.models import MPTTModel
from apps.base.models import BaseAbstractDate
from colorfield.fields import ColorField


class Advertisement(BaseAbstractDate):
    icon = models.ImageField(upload_to='advertisement/icons/', null=True, blank=True)
    title = models.CharField(max_length=223, null=True)
    description = RichTextField(null=True, blank=True)
    banner_image = models.ImageField(upload_to='advertisement/banners/', null=True)

    def __str__(self):
        if self.title:
            return self.title
        return 'None title'


class Category(MPTTModel, BaseAbstractDate):
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Parent Category',
                               limit_choices_to={'is_active': True},
                               related_name='children', null=True, blank=True, )
    title = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        verbose_name = 'Kategoriya'
        verbose_name_plural = 'Kategoriyalar'
        order_insertion_by = ['title']

    def __str__(self):
        return self.title


class Banner(BaseAbstractDate):
    desc = RichTextField(null=True, blank=True)
    title = models.CharField(max_length=223, null=True, blank=True)
    image = models.ImageField(upload_to='banner', null=True)

    def __str__(self):
        return self.title


class Brand(BaseAbstractDate):
    title = models.CharField(max_length=223)

    def __str__(self):
        return self.title


class Color(BaseAbstractDate):
    name = ColorField(default='#FF0000')

    def __str__(self):
        return self.name


class Product(BaseAbstractDate):
    STATUS = (
        ('NEW', 'NEW'),
        ('HOT', 'HOT'),
        ('BEST SELL', 'BEST SELL'),
        ('SALE', 'SALE'),
    )

    advertisement = models.ForeignKey(Advertisement, on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(choices=STATUS, default='NEW', max_length=10, null=True, blank=True)
    title = models.CharField(max_length=223, null=True)
    category = models.ManyToManyField(Category, blank=True,
                                      limit_choices_to={'is_active': True})
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True)
    price = models.IntegerField(default=0, null=True)
    percentage = models.IntegerField(default=0, null=True, blank=True)
    discount = models.IntegerField(default=0, null=True, blank=True)
    view = models.IntegerField(default=0, null=True, blank=True)
    # mid_rate = models.IntegerField(default=0, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    # guarantee = models.CharField(max_length=223, null=True, blank=True)
    availability = models.IntegerField(default=0, null=True, blank=True)
    has_size = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)

    @property
    def mid_rate(self):
        result = Rate.objects.filter(product=self.id).aggregate(avarage=Avg("rate"))
        if result['avarage']:
            return round(result['avarage'], 1)
        else:
            return 0.0

    @property
    def mid_rate_percent(self):
        result = Rate.objects.filter(product=self.id).aggregate(avarage=Avg("rate"))
        if result['avarage']:
            percent = result['avarage'] * 100 / 5
            return percent
        else:
            return 0.0

    @property
    def get_discount_price(self):
        if self.percentage:
            discount_sell = self.price - (self.price * (self.percentage / 100))
            self.discount = discount_sell
            self.save()
            return discount_sell
        return 0

    def __str__(self):
        if self.title:
            return self.title
        return f'{self.id}'

    def image_tag(self):
        if self.product_images.all().first().image.url is not None:
            return mark_safe('<img src="{}" height="80"/>'.format(self.product_images.all().first().image.url))
        else:
            return ""

    image_tag.short_description = 'Mahsulot rasmi'
    # image_tag.allow_tags = True


class ProductImage(BaseAbstractDate):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images', null=True)
    image = models.ImageField(upload_to='products', null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Image of {self.product}'


class AdditionalInfo(BaseAbstractDate):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='additional_info')
    title = models.CharField(max_length=255)
    description = RichTextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Rate(BaseAbstractDate):
    RATE = (
        (0, 0),
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_rate")
    rate = models.IntegerField(choices=RATE, default=0)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'rate of {self.user}'

    @property
    def rate_percent(self):
        return round(self.rate * 100 / 5, 1)
