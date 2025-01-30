from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Order
from django.http import JsonResponse
from django.views import View
from .models import TelegramUser
import json
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TelegramOrderSerializer








def catalog(request):
    product = Product.objects.all()
    return render(request,  'catalog/catalog.html', {'product': product})

@login_required
def order(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == "POST":
        quantity = int(request.POST.get('quantity', 1))
        total_price = product.price * quantity
        # Создание заказа
        order = Order.objects.create(
            user=request.user,
            product=product,
            quantity=quantity,
            total_price=total_price
        )
        # Уменьшаем количество товара
        product.count -= quantity
        product.save()
        # Перенаправляем на страницу с заказами пользователя
        return redirect('catalog:user_orders')  # Переходим на страницу с заказами
    return render(request, 'catalog/order.html', {'product': product})

# для отображения всех заказов текущего пользователя
@login_required
def user_orders(request):
    # Получаем все заказы пользователя
    orders = Order.objects.filter(user=request.user).order_by('-created_at')  # Сортировка по дате создания
    return render(request, 'catalog/user_orders.html', {'orders': orders})

# Создание API в Django
def api_get_catalog(request):
    products = Product.objects.all().values('id', 'name', 'description', 'price', 'count', 'image')
    data = list(products)
    for product in data:
        # product['image'] = request.build_absolute_uri(product['image'])  # Полный URL изображения
        product['image'] = request.build_absolute_uri(product['image'])  # Полный URL изображения
    return JsonResponse({'catalog': data}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class TelegramUserAPI(View):
    """API для работы с пользователями Telegram"""

    def get(self, request):
        """Обрабатывает GET-запрос для проверки регистрации"""
        telegram_user_id = request.GET.get('telegram_user_id')

        if not telegram_user_id:
            return JsonResponse({'error': 'Не указан telegram_user_id'}, status=400)

        try:
            user = TelegramUser.objects.get(telegram_user_id=telegram_user_id)
            return JsonResponse({'registered': True, 'username': user.telegram_username})
        except TelegramUser.DoesNotExist:
            return JsonResponse({'registered': False})

    def post(self, request):
        """Обрабатывает POST-запрос для регистрации нового пользователя"""
        try:
            # Извлечение данных из тела запроса
            data = json.loads(request.body)
            telegram_user_id = data.get('telegram_user_id')
            telegram_username = data.get('telegram_username', '')
            first_name = data.get('first_name', '')
            email = data.get('email', '')

            if not telegram_user_id or not email:
                return JsonResponse({'error': 'telegram_user_id и email обязательны'}, status=400)

            # Проверяем, существует ли пользователь с таким email
            user, created = User.objects.get_or_create(
                username=email,  # Используем email как username
                defaults={
                    'first_name': first_name,
                    'email': email,
                }
            )

            if created:
                # Если Django пользователь создан, создаем запись в TelegramUser
                TelegramUser.objects.create(
                    user=user,
                    telegram_user_id=telegram_user_id,
                    telegram_username=telegram_username,
                    first_name=first_name,
                    email=email
                )
                return JsonResponse({'message': 'Пользователь успешно зарегистрирован'}, status=201)
            else:
                # Если пользователь с таким email существует, проверяем TelegramUser
                telegram_user, tg_created = TelegramUser.objects.get_or_create(
                    user=user,
                    telegram_user_id=telegram_user_id,
                    defaults={
                        'telegram_username': telegram_username,
                        'first_name': first_name,
                        'email': email,
                    }
                )

                if tg_created:
                    return JsonResponse({'message': 'Telegram пользователь зарегистрирован'}, status=201)
                else:
                    return JsonResponse({'message': 'Пользователь уже существует'}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Некорректный JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class TelegramOrderView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = TelegramOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Заказ успешно создан."}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)