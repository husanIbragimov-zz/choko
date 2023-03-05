from django.contrib.auth.models import User
from django.db import models
from ckeditor.fields import RichTextField
from mptt.models import MPTTModel
from apps.base.models import BaseAbstractDate


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
        verbose_name = 'Kitob'
        verbose_name_plural = 'Kitoblar'
        order_insertion_by = ['title']

    def __str__(self):
        return self.title


class Banner(BaseAbstractDate):
    desc = RichTextField(null=True, blank=True)
    title = models.CharField(max_length=223, null=True, blank=True)
    image = models.ImageField(upload_to='banner', null=True)

    def __str__(self):
        return self.title


class Tag(BaseAbstractDate):
    title = models.CharField(max_length=223)

    def __str__(self):
        return self.title


class Brand(BaseAbstractDate):
    title = models.CharField(max_length=223)

    def __str__(self):
        return self.title


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
    mid_rate = models.FloatField(default=0.0, null=True, blank=True)
    description = RichTextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    guarantee = models.CharField(max_length=223, null=True, blank=True)
    availability = models.IntegerField(default=0, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    @property
    def get_mid_rate(self):
        rates = self.rate_set.all()
        mid = 0
        try:
            mid = sum(i.rate for i in rates) / rates.count()
        except ZeroDivisionError:
            pass
        self.mid_rate = mid
        self.save()
        return mid

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


class ProductImage(BaseAbstractDate):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images', null=True)
    image = models.ImageField(upload_to='products', null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'Image of {self.product}'


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
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.IntegerField(choices=RATE, default=0)
    comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'rate of {self.user}'
