# Generated by Django 4.2.3 on 2023-10-10 18:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_author_brand_product_type_category_product_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='product.author'),
        ),
        migrations.AddField(
            model_name='product',
            name='language',
            field=models.CharField(choices=[('english', 'english'), ('russian', 'russian'), ('uzbek', 'uzbek')], default='uzbek', max_length=25),
        ),
        migrations.AddField(
            model_name='product',
            name='yozuv',
            field=models.CharField(choices=[('krill', 'Krill'), ('lotin', 'Lotin')], default='lotin', max_length=25),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='image',
            field=models.FileField(upload_to='products'),
        ),
    ]
