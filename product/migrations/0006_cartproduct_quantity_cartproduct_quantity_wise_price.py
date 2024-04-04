# Generated by Django 5.0.3 on 2024-04-04 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_alter_cartproduct_carts'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartproduct',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='quantity_wise_price',
            field=models.FloatField(default=0.0),
        ),
    ]