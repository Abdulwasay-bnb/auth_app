# Generated by Django 5.0.3 on 2024-04-15 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_remove_cartproduct_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='image2',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='products',
            name='image3',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='products',
            name='image4',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='products',
            name='image5',
            field=models.ImageField(null=True, upload_to='uploads/'),
        ),
    ]
