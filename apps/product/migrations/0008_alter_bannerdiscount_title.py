# Generated by Django 3.2.18 on 2023-04-06 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_alter_bannerdiscount_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bannerdiscount',
            name='title',
            field=models.TextField(null=True),
        ),
    ]
