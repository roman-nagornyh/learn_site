# Generated by Django 4.1.7 on 2023-03-18 14:13

from django.db import migrations
from django.contrib.auth.models import User
from django.utils import timezone


def generate_data(apps, schema_editor):
    import random
    from application.models import Brand, TypeProduct, OrderStatus, Product

    User.objects.create_superuser(
        "nagornyhri",
        email="nagornyxr@mail.ru",
        password="ShUbQsp4Qj",
        last_login=timezone.now(),
    )
    brands = "Samsung", "Apple", "Xiaomi", "Lenovo"
    product_types = "Компьютер", "Смартфон", "Планшет"
    statuses = (
        "Оформлен",
        "Оплачен",
        "Получен",
    )
    br_objects = Brand.objects.bulk_create(Brand(name=i) for i in brands)
    tp_objects = TypeProduct.objects.bulk_create(
        TypeProduct(name=j) for j in product_types
    )
    OrderStatus.objects.bulk_create(OrderStatus(name=k) for k in statuses)
    br_last_index = len(br_objects) - 1
    tp_last_index = len(tp_objects) - 1
    product_list = list()
    for i in range(0, 50):
        tp_index = random.randint(0, tp_last_index)
        br_index = random.randint(0, br_last_index)
        brand = br_objects[br_index]
        type_product = tp_objects[tp_index]
        brand_name = br_objects[br_index].name
        product_name = tp_objects[tp_index].name + f" {brand_name} {i}"
        price = random.randint(20000, 100000)
        product_list.append(
            Product(
                name=product_name,
                price=price,
                product_type_id=type_product.id,
                brand_id=brand.id,
                guarantee=random.randint(6, 18),
                rating=random.randint(1, 5),
            )
        )
    Product.objects.bulk_create(product_list)


class Migration(migrations.Migration):

    dependencies = [
        ("application", "0001_initial"),
    ]

    operations = [migrations.RunPython(generate_data)]
