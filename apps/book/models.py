from django.db import models

LANGUAGE = (
    ('krill', 'krill'),
    ('english', 'english'),
    ('russian', 'russian'),
    ('uzbek', 'uzbek'),
)

YOZUV = (
    ('krill', 'krill'),
    ('english', 'english'),
    ('russian', 'russian'),
    ('uzbek', 'uzbek'),

)

MUQOVA = (
    ('qattiq', 'qattiq'),
    ('yumshoq', 'yumshoq'),
)

FORMAT = (
    ('a5','A5'),
    ('a4','A4'),
    ('a3','A3'),
    ('a2','A2'),
    ('a1','A1'),
    ('a0','A0'),
)

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255,null=True,blank=True)
    author = models.CharField(max_length=255,null=True,blank=True)
    price = models.IntegerField(null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    image = models.ImageField(upload_to='books',null=True,blank=True)
    image1 = models.ImageField(upload_to='books',null=True,blank=True)
    image2 = models.ImageField(upload_to='books',null=True,blank=True)
    image3 = models.ImageField(upload_to='books',null=True,blank=True)
    count = models.IntegerField(null=True,blank=True)
    in_sell = models.BooleanField(default=True,null=True,blank=True)
    ISBN = models.CharField(max_length=255,null=True,blank=True)
    language = models.CharField(max_length=20, choices=LANGUAGE,null=True,blank=True)
    yozuv = models.CharField(max_length=20, choices=YOZUV,null=True,blank=True)
    page = models.PositiveIntegerField(null=True,blank=True)
    nashriyot = models.CharField(max_length=255,null=True,blank=True)
    muqova = models.CharField(max_length=20,choices=MUQOVA,blank=True,null=True)
    format = models.CharField(max_length=20,choices=FORMAT,blank=True,null=True)
    year_of_creation = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)
    is_active = models.BooleanField(default=True,null=True,blank=True)

    def __str__(self):
        return self.title

