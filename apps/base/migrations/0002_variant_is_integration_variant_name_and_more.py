# Generated by Django 4.2.3 on 2023-10-16 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='variant',
            name='is_integration',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='variant',
            name='name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='variant',
            name='product_type',
            field=models.CharField(blank=True, choices=[('book', 'Book'), ('clothing', 'Clothing'), ('product', 'Product')], max_length=50, null=True),
        ),
    ]
