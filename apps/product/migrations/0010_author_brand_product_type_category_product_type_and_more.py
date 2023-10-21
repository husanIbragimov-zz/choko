from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_auto_20230406_2120'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='brand',
            name='product_type',
            field=models.CharField(choices=[('book', 'Book'), ('clothing', 'Clothing'), ('product', 'Product')], default='product', max_length=25),
        ),
        migrations.AddField(
            model_name='category',
            name='product_type',
            field=models.CharField(choices=[('book', 'Book'), ('clothing', 'Clothing'), ('product', 'Product')], default='product', max_length=25),
        ),
        migrations.AddField(
            model_name='product',
            name='product_type',
            field=models.CharField(choices=[('book', 'Book'), ('clothing', 'Clothing'), ('product', 'Product')], default='product', max_length=25),
        ),
        migrations.AddField(
            model_name='productimage',
            name='wrapper',
            field=models.CharField(blank=True, choices=[('qattiq', 'qattiq'), ('yumshoq', 'yumshoq')], max_length=25, null=True, verbose_name='Muqova'),
        ),
        migrations.AddField(
            model_name='size',
            name='product_type',
            field=models.CharField(choices=[('book', 'Book'), ('clothing', 'Clothing'), ('product', 'Product')], default='product', max_length=25),
        ),
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(db_index=True, default=True),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='product.color'),
        ),
        migrations.AlterField(
            model_name='productimage',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product_images', to='product.product'),
        ),
    ]
