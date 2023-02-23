# Generated by Django 4.1.5 on 2023-02-05 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('monolith', '0002_client_product_guarantee_alter_product_rating_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='guarantee',
            field=models.IntegerField(null=True, verbose_name='Гарантия (мес)'),
        ),
        migrations.AddField(
            model_name='product',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='monolith.brand'),
        ),
    ]
