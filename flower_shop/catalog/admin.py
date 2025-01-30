from django.contrib import admin
from .models import Product, Order, TelegramUser, TelegramOrder


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'image', 'description', 'price', 'count')
    search_fields = ('name',)
    list_filter = ('price', 'count')
    ordering = ('name',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'quantity', 'total_price', 'created_at')
    list_filter = ('created_at', 'user', 'product')
    search_fields = ('user__username', 'product__name')
    ordering = ('-created_at',)


@admin.register(TelegramUser)
class TelegramUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'telegram_user_id', 'telegram_username', 'email', 'first_name')
    list_filter = ('telegram_username', 'email', 'first_name')
    search_fields = ('telegram_username', 'email', 'first_name')
    ordering = ('telegram_username',)


@admin.register(TelegramOrder)
class TelegramOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'telegram_user', 'product', 'quantity', 'total_price', 'created_at')
    list_filter = ('created_at', 'telegram_user', 'product')
    search_fields = ('telegram_user__telegram_username', 'product__name')
    ordering = ('-created_at',)
