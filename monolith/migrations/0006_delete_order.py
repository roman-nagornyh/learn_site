# Generated by Django 4.1.5 on 2023-02-06 14:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monolith', '0005_brand_product_brand'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Order',
        ),
    ]
