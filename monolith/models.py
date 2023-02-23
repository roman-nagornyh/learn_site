from django.db import models
from django.contrib.auth.models import User

# Create your models here.

DB_SCHEMA = 'store'


class TypeProduct(models.Model):
    name = models.CharField(null=False, verbose_name='Наименование', max_length=100)

    class Meta:
        db_table = f'{DB_SCHEMA}\".\"product_types'
        verbose_name = 'Вид товара'
        verbose_name_plural = 'Виды товара'

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(null=False, verbose_name='Название', max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        db_table = f'{DB_SCHEMA}\".\"brands'
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, verbose_name='Название')
    price = models.IntegerField(null=False, verbose_name='Цена')
    product_type = models.ForeignKey(TypeProduct, on_delete=models.RESTRICT,
                                     verbose_name='Вид продукта')
    rating = models.IntegerField(null=False, verbose_name='Рейтинг продукта')
    guarantee = models.IntegerField(null=True, verbose_name='Гарантия (мес)')
    brand = models.ForeignKey(Brand, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = f'{DB_SCHEMA}\".\"products'
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name + f'({self.price})'


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    sale = models.IntegerField(null=True)

    class Meta:
        db_table = f'{DB_SCHEMA}\".\"clients'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'

    def __str__(self):
        return self.user.username


class Bucket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар', null=False)
    # count = models.IntegerField(null=False, verbose_name='Количество', default=1)
    user = models.ForeignKey(Client, null=False, verbose_name='Пользователь', on_delete=models.CASCADE)
    status = models.BooleanField(verbose_name='Статус корзины', null=False, default=False)

    class Meta:
        db_table = f'{DB_SCHEMA}\".\"buckets'
        verbose_name = 'Корзина заказов'
        verbose_name_plural = 'Корзины заказов'


class OrderStatus(models.Model):
    name = models.CharField(null=False, verbose_name='Название', max_length=100)

    class Meta:
        db_table = f'{DB_SCHEMA}\".\"order_statuses'
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'


class Order(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Пользователь', null=False)
    status = models.ForeignKey(OrderStatus, on_delete=models.CASCADE, null=False, verbose_name='Статус заказа')
    order_date = models.DateTimeField(null=False, verbose_name='Дата заказа')
    issue_date = models.DateTimeField(null=False, verbose_name='Дата выдачи')

    class Meta:
        db_table = f'{DB_SCHEMA}\".\"orders'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class ProductOrder(models.Model):
    order = models.ForeignKey(Order, verbose_name='Заказ', null=False, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='Продукт', null=False, on_delete=models.CASCADE)
    count = models.IntegerField(null=False, default=1, verbose_name='Количество товара')
    price = models.IntegerField(null=False, verbose_name='Цена')

    class Meta:
        db_table = f'{DB_SCHEMA}\".\"product_orders'
        verbose_name = 'Товар и заказ'
        verbose_name_plural = 'Товары и заказы'


#===============================Тестовый пример====================================================

DB_SCHEMA_TEST = 'test'


class Author(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    class Meta:
        db_table = f'{DB_SCHEMA_TEST}\".\"authors'
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'


class Publisher(models.Model):
    name = models.CharField(max_length=300)

    class Meta:
        db_table = f'{DB_SCHEMA_TEST}\".\"publishers'
        verbose_name = 'издатель'
        verbose_name_plural = 'издатели'


class Book(models.Model):
    name = models.CharField(max_length=300)
    pages = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    pubdate = models.DateField()

    class Meta:
        db_table = f'{DB_SCHEMA_TEST}\".\"books'
        verbose_name = 'книга'
        verbose_name_plural = 'книги'


class Store(models.Model):
    name = models.CharField(max_length=300)
    books = models.ManyToManyField(Book)

    class Meta:
        db_table = f'{DB_SCHEMA_TEST}\".\"stores'
        verbose_name = 'магазин'
        verbose_name_plural = 'магазины'