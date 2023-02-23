import random

from monolith.models import *
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def generate_hadbook(self):
        # Наполнение справочника брендов
        Brand.objects.create(name='Samsung')
        Brand.objects.create(name='Apple')
        Brand.objects.create(name='Xiaomi')
        Brand.objects.create(name='Lenovo')
        # Наполнение справочника типа продуков
        TypeProduct.objects.create(name='Компьютер')
        TypeProduct.objects.create(name='Смартфон')
        TypeProduct.objects.create(name='Планшет')
        OrderStatus.objects.create(name='Оформлен')
        OrderStatus.objects.create(name='Оплачен')
        OrderStatus.objects.create(name='Получен')

    def handle(self, *args, **options):
        brand_list = Brand.objects.all()
        type_product_list = TypeProduct.objects.all()
        br_last_index = len(brand_list) - 1
        tp_last_index = len(type_product_list) - 1
        for i in range(0, 50):
            tp_index = random.randint(0, tp_last_index)
            br_index = random.randint(0, br_last_index)
            brand = brand_list[br_index]
            type_product = type_product_list[tp_index]
            brand_name = brand_list[br_index].name
            product_name = type_product_list[tp_index].name + f' {brand_name} {i}'
            price = random.randint(20000, 100000)
            Product.objects.create(
                name=product_name,
                price=price,
                product_type_id=type_product.id,
                brand_id=brand.id,
                guarantee=random.randint(6, 18),
                rating=random.randint(1, 5)
            )


