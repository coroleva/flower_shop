from django.db import models
from django.contrib.auth.models import User  # Импорт модели User


class Product(models.Model):
    name = models.CharField(max_length=100)  # Название
    image = models.ImageField(upload_to='products/')  # Загрузка изображения
    description = models.TextField()  # Описание
    price = models.FloatField()  # Цена
    count = models.IntegerField()  # Количество

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Букет"
        verbose_name_plural = "Букеты"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")  # Связь с Django User
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")  # Связь с продуктом
    quantity = models.PositiveIntegerField(verbose_name="Количество")  # Количество
    total_price = models.FloatField(verbose_name="Итоговая стоимость")  # Итоговая стоимость
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")  # Дата создания

    def __str__(self):
        return f"Заказ {self.id} - {self.user.username}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class TelegramUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Django Пользователь")  # Связь с Django User
    telegram_user_id = models.BigIntegerField(unique=True, verbose_name="ID пользователя Telegram")
    telegram_username = models.CharField(max_length=150, blank=True, null=True, verbose_name="Имя пользователя Telegram")
    email = models.EmailField(verbose_name="Электронная почта", blank=True, null=True)
    first_name = models.CharField(max_length=100, verbose_name="Имя пользователя", blank=True, null=True)

    def __str__(self):
        return f"Пользователь {self.first_name} ({self.telegram_username})"

    class Meta:
        verbose_name = "Telegram Пользователь"
        verbose_name_plural = "Telegram Пользователи"


class TelegramOrder(models.Model):
    telegram_user = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, verbose_name="Telegram Пользователь")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")
    quantity = models.PositiveIntegerField(verbose_name="Количество")
    total_price = models.FloatField(verbose_name="Итоговая стоимость")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def save(self, *args, **kwargs):
        # Проверяем, достаточно ли товара на складе
        if self.product.count < self.quantity:
            raise ValueError(f"Недостаточно товара '{self.product.name}' на складе. Осталось {self.product.count}.")

        # Уменьшаем количество товара на складе
        self.product.count -= self.quantity
        self.product.save()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Заказ {self.id} - {self.telegram_user.telegram_username}"

    class Meta:
        verbose_name = "Telegram Заказ"
        verbose_name_plural = "Telegram Заказы"
