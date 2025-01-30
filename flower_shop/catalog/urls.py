from django.urls import path
from . import views
from .views import api_get_catalog, TelegramOrderView
from django.urls import path

from django.contrib.auth import views as auth_views

app_name = 'catalog'
urlpatterns = [
    path('', views.catalog, name='catalog'), # страница каталога, но я не понимаю '' - тут ничего не стоит?
    # Поняла! пусто, потому что основной адрес прописан в flower_shop/urls.py в строке <path('catalog/', include('catalog.urls'))>

    path('order/<int:pk>/', views.order, name='order'),
    path('user_orders/', views.user_orders, name='user_orders'),  # Страница с заказами пользователя


    # Настроить URL-адрес для API
#
    path('api/catalog/', api_get_catalog, name='api_get_catalog'),

    # path('api/create_order/', views.api_create_order, name='api_create_order'),
    path('api/telegram_users/', views.TelegramUserAPI.as_view(), name='telegram_users_api'),
    path('api/telegram_orders/', TelegramOrderView.as_view(), name='telegram_orders'),


]