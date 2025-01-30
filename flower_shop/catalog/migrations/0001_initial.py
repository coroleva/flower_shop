# Generated by Django 5.1.4 on 2025-01-23 08:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


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
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='products/')),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('count', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Букет',
                'verbose_name_plural': 'Букеты',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('total_price', models.FloatField(verbose_name='Итоговая стоимость')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Продукт')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='TelegramUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telegram_user_id', models.BigIntegerField(unique=True, verbose_name='ID пользователя Telegram')),
                ('telegram_username', models.CharField(blank=True, max_length=150, null=True, verbose_name='Имя пользователя Telegram')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Электронная почта')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Имя пользователя')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Django Пользователь')),
            ],
            options={
                'verbose_name': 'Telegram Пользователь',
                'verbose_name_plural': 'Telegram Пользователи',
            },
        ),
        migrations.CreateModel(
            name='TelegramOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('total_price', models.FloatField(verbose_name='Итоговая стоимость')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.product', verbose_name='Продукт')),
                ('telegram_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='catalog.telegramuser', verbose_name='Telegram Пользователь')),
            ],
            options={
                'verbose_name': 'Telegram Заказ',
                'verbose_name_plural': 'Telegram Заказы',
            },
        ),
    ]
