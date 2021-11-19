# Generated by Django 3.2.9 on 2021-11-17 17:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название продукта')),
                ('description', models.TextField(verbose_name='Описание')),
                ('price', models.PositiveIntegerField(verbose_name='Цена')),
                ('weight', models.PositiveIntegerField(verbose_name='Вес')),
                ('time_to_cook', models.PositiveIntegerField(verbose_name='Время готовки в минутах')),
                ('image', models.ImageField(upload_to='products', verbose_name='Изображение')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Ждет обработку', 'Ждет обработку'), ('Готовится', 'Готовится'), ('Готов', 'Готов'), ('Выполнен', 'Выполнен')], max_length=20)),
                ('payment_method', models.CharField(choices=[('Наличными', 'Наличными'), ('Картой', 'Картой')], max_length=20)),
                ('products', models.ManyToManyField(to='products.OrderProduct')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.ManyToManyField(to='products.OrderProduct')),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]