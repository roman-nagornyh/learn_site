# Generated by Django 4.1.7 on 2023-02-25 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monolith', '0013_remove_person_hometown_delete_book_delete_city_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Topping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Начинка пиццы',
                'verbose_name_plural': 'Начинки пиццы',
                'db_table': 'test"."toppings',
            },
        ),
        migrations.CreateModel(
            name='Pizza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('toppings', models.ManyToManyField(to='monolith.topping')),
            ],
            options={
                'verbose_name': 'Пицца',
                'verbose_name_plural': 'Пиццы',
                'db_table': 'test"."pizza',
            },
        ),
    ]
