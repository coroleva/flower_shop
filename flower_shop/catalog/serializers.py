from rest_framework import serializers
from .models import TelegramOrder, Product, TelegramUser


class TelegramOrderItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    total_price = serializers.FloatField()


class TelegramOrderSerializer(serializers.ModelSerializer):
    order_items = TelegramOrderItemSerializer(many=True)
    telegram_user_id = serializers.IntegerField()

    class Meta:
        model = TelegramOrder
        fields = ['telegram_user_id', 'order_items']

    def create(self, validated_data):
        telegram_user_id = validated_data.pop("telegram_user_id")
        order_items = validated_data.pop("order_items")

        # Проверяем, существует ли TelegramUser
        try:
            telegram_user = TelegramUser.objects.get(telegram_user_id=telegram_user_id)
        except TelegramUser.DoesNotExist:
            raise serializers.ValidationError("Пользователь Telegram не найден.")

        # Создаем заказ
        for item in order_items:
            product = Product.objects.get(id=item['product_id'])
            TelegramOrder.objects.create(
                telegram_user=telegram_user,
                product=product,
                quantity=item['quantity'],
                total_price=item['total_price']
            )

        return validated_data
