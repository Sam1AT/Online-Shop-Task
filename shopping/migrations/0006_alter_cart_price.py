# Generated by Django 5.1.4 on 2024-12-11 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping', '0005_cart_is_bought'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='price',
            field=models.IntegerField(default=0),
        ),
    ]
