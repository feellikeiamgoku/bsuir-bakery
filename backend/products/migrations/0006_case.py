# Generated by Django 3.2.9 on 2021-11-21 13:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0005_auto_20211119_1628'),
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('products', models.ManyToManyField(blank=True, related_name='case', to='products.OrderProduct')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='case', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
