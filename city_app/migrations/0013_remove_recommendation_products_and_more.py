# Generated by Django 4.2.19 on 2025-03-13 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('city_app', '0012_alter_cart_quantity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recommendation',
            name='products',
        ),
        migrations.AddField(
            model_name='recommendation',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recommendation',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to='product_images'),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='name',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='recommendation',
            name='quantity',
            field=models.CharField(default='', max_length=50),
        ),
    ]
