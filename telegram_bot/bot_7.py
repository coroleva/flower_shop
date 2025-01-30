from config import TOKEN
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
import aiohttp
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup


API_TOKEN = TOKEN
API_URL_USERS = "http://127.0.0.1:8000/catalog/api/telegram_users/"  # API для работы с пользователями
API_URL = "http://127.0.0.1:8000"  # Адрес API каталога
# Логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Временный словарь для хранения состояния регистрации
registration_states = {}
# Временная корзина для хранения товаров пользователя
cart = {}
@dp.message(Command("start"))
async def start_command(message: types.Message):
    """Обработчик команды /start с проверкой регистрации"""
    user_id = message.from_user.id

    try:
        # Проверка регистрации пользователя через API
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL_USERS}?telegram_user_id={user_id}") as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("registered", False):
                        await show_main_menu(message)
                        return

        # Если пользователь не зарегистрирован
        await message.answer("Привет! Вас ещё нет в нашей системе. Давайте зарегистрируемся.")
        registration_states[user_id] = {"step": "name"}  # Устанавливаем шаг регистрации
        await message.answer("Введите ваше имя:")

    except Exception as e:
        logger.error(f"Ошибка проверки регистрации: {e}")
        await message.answer("Произошла ошибка. Попробуйте позже.")

async def show_main_menu(message: types.Message):
    """Отображает основное меню"""
    builder = ReplyKeyboardBuilder()
    builder.button(text="🛍️ Посмотреть каталог")
    builder.button(text="🛒 Оформить заказ")
    builder.button(text="📦 Мои заказы")
    builder.button(text="📢 Оставить отзыв")
    builder.button(text="☎️ Контакты")
    builder.adjust(2, 2)
    await message.answer(
        "Добро пожаловать! Чем могу помочь?",
        reply_markup=builder.as_markup(resize_keyboard=True),
    )

@dp.message(lambda message: message.from_user.id in registration_states)
async def handle_registration(message: types.Message):
    """Обрабатывает шаги регистрации пользователя"""
    user_id = message.from_user.id
    state = registration_states[user_id]

    if state["step"] == "name":
        # Сохраняем имя и переходим к следующему шагу
        state["name"] = message.text
        state["step"] = "email"
        await message.answer("Введите ваш email:")

    elif state["step"] == "email":
        # Сохраняем email и завершаем регистрацию
        email = message.text
        if "@" not in email or "." not in email:
            await message.answer("Пожалуйста, введите корректный email:")
            return

        state["email"] = email

        # Отправка данных на сервер
        try:
            async with aiohttp.ClientSession() as session:
                payload = {
                    "telegram_user_id": user_id,
                    "telegram_username": message.from_user.username,
                    "first_name": state["name"],
                    "email": state["email"],
                }
                async with session.post(API_URL_USERS, json=payload) as response:
                    if response.status == 201:
                        await message.answer("Вы успешно зарегистрированы!")
                        await show_main_menu(message)
                        registration_states.pop(user_id, None)  # Удаляем состояние регистрации
                    else:
                        await message.answer("Не удалось зарегистрироваться. Попробуйте позже.")
        except Exception as e:
            logger.error(f"Ошибка при регистрации: {e}")
            await message.answer("Произошла ошибка. Попробуйте позже.")




# @dp.message(lambda message: message.text == "🛍️ Посмотреть каталог")
# async def view_catalog(message: types.Message):
#     """Обработчик кнопки 'Посмотреть каталог'"""
#     try:
#         # Запрашиваем каталог с API
#         async with aiohttp.ClientSession() as session:
#             async with session.get(f"{API_URL}/catalog/api/catalog/") as response:
#                 if response.status == 200:
#                     data = await response.json()
#                     catalog = data.get("catalog", [])
#                 else:
#                     await message.answer("Не удалось получить данные о каталоге 😔")
#                     return
#
#         # Проверяем, есть ли товары
#         if not catalog:
#             await message.answer("Каталог пуст. Попробуйте позже.")
#             return
#
#         # Отправляем товары пользователю
#         for product in catalog:
#             # Получаем полный URL для изображения
#             image_url = product.get("image", "")
#             if image_url:
#                 image_url = image_url.replace("http://127.0.0.1:8000", API_URL)  # заменяем относительный путь на полный
#
#             text = (
#                 f"🌸 <b>{product['name']}</b>\n"
#                 f"Описание: {product['description']}\n"
#                 f"💰 Цена: {product['price']} руб.\n"
#                 f"В наличии: {product['count']} шт.\n"
#             )
#
#             # Создаем inline-кнопку для добавления в корзину
#             button = InlineKeyboardButton(
#                 text="Добавить в корзину",
#                 callback_data=f"add_to_cart:{product['id']}"  # передаем ID товара
#             )
#             markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
#
#             # Отправляем сообщение с текстом и кнопкой
#             if image_url:
#                 await message.answer(text, parse_mode="HTML", reply_markup=markup, photo=image_url)
#             else:
#                 await message.answer(text, parse_mode="HTML", reply_markup=markup)
#
#     except Exception as e:
#         logger.error(f"Ошибка при обработке каталога: {e}")
#         await message.answer("Произошла ошибка. Попробуйте позже.")

@dp.message(lambda message: message.text == "🛍️ Посмотреть каталог")
async def view_catalog(message: types.Message):
    """Обработчик кнопки 'Посмотреть каталог'"""
    try:
        # Запрашиваем каталог с API
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/catalog/api/catalog/") as response:
                if response.status == 200:
                    data = await response.json()
                    catalog = data.get("catalog", [])
                else:
                    await message.answer("Не удалось получить данные о каталоге 😔")
                    return

        # Проверяем, есть ли товары
        if not catalog:
            await message.answer("Каталог пуст. Попробуйте позже.")
            return

        # Список URL изображений
        list_url = [
            'https://res.cloudinary.com/dbtyt71a4/image/upload/v1737656902/f2_fsasop.jpg',
            'https://res.cloudinary.com/dbtyt71a4/image/upload/v1737656902/f3_v07wqw.jpg',
            'https://res.cloudinary.com/dbtyt71a4/image/upload/v1737656902/f4_edgnde.jpg',
            'https://res.cloudinary.com/dbtyt71a4/image/upload/v1737656902/f8_tb0cme.jpg',
            'https://res.cloudinary.com/dbtyt71a4/image/upload/v1737656903/f6_d9obe7.jpg',
            'https://res.cloudinary.com/dbtyt71a4/image/upload/v1737656902/f1_wbudcx.jpg'
        ]

        # Отправляем товары пользователю
        for index, product in enumerate(catalog):
            # Получаем URL изображения
            image_url = list_url[index % len(list_url)]  # Циклично используем ссылки

            text = (
                f"🌸 <b>{product['name']}</b>\n"
                f"Описание: {product['description']}\n"
                f"💰 Цена: {product['price']} руб.\n"
                f"В наличии: {product['count']} шт.\n"
            )

            # Создаем inline-кнопку для добавления в корзину
            button = InlineKeyboardButton(
                text="Добавить в корзину",
                callback_data=f"add_to_cart:{product['id']}"  # передаем ID товара
            )
            markup = InlineKeyboardMarkup(inline_keyboard=[[button]])

            # Отправляем изображение отдельно
            try:
                await bot.send_photo(
                    chat_id=message.chat.id,
                    photo=image_url,
                    caption=text,
                    parse_mode="HTML",
                    reply_markup=markup
                )
            except Exception as e:
                # Если не удается отправить изображение, логируем ошибку
                logger.error(f"Ошибка при отправке изображения: {e}")
                # Отправляем текст без фото
                await message.answer(text, parse_mode="HTML", reply_markup=markup)

    except Exception as e:
        logger.error(f"Ошибка при обработке каталога: {e}")
        await message.answer("Произошла ошибка. Попробуйте позже.")



@dp.callback_query(lambda c: c.data.startswith('add_to_cart:'))
async def add_to_cart(callback_query: CallbackQuery):
    """Обработчик кнопки 'Добавить в корзину'"""
    product_id = callback_query.data.split(":")[1]  # Извлекаем ID товара
    user_id = callback_query.from_user.id  # Получаем ID пользователя

    # Сохраняем выбранный товар в корзину
    if user_id not in cart:
        cart[user_id] = []

    # Находим товар в каталоге по его ID
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{API_URL}/catalog/api/catalog/") as response:
            if response.status == 200:
                data = await response.json()
                catalog = data.get("catalog", [])
            else:
                await callback_query.message.answer("Не удалось получить данные о каталоге.")
                return

    product = next((item for item in catalog if item['id'] == int(product_id)), None)

    if product:
        # Добавляем товар в корзину с правильной структурой
        cart[user_id].append({'product': product, 'quantity': 0})
        await callback_query.message.answer(f"Товар '{product['name']}' добавлен в вашу корзину. Укажите количество.")
    else:
        await callback_query.message.answer("Этот товар больше не доступен.")

@dp.message(lambda message: message.text.isdigit())  # Отслеживаем, что пользователь ввел число
async def set_quantity(message: types.Message):
    """Обработчик ввода количества товара"""
    user_id = message.from_user.id  # Получаем ID пользователя
    quantity = int(message.text)  # Получаем количество

    # Проверяем, есть ли товары в корзине
    if user_id not in cart or not cart[user_id]:
        await message.answer("В вашей корзине нет товаров. Пожалуйста, добавьте товар.")
        return

    # Фильтруем товары в корзине, исключая шаги
    products_in_cart = [item for item in cart[user_id] if 'product' in item]

    if not products_in_cart:
        await message.answer("В вашей корзине нет товаров.")
        return

    # Получаем последний добавленный товар
    last_product = products_in_cart[-1]  # Берем последний добавленный товар
    product = last_product['product']  # Извлекаем товар из корзины

    if quantity > product['count']:
        await message.answer(
            f"Извините, на складе только {product['count']} единиц товара '{product['name']}'. Вы можете добавить максимум {product['count']}."
        )
        return

    # Обновляем количество товара в корзине
    last_product['quantity'] = quantity  # Присваиваем количество последнему добавленному товару

    # Подтверждаем, что количество обновлено
    await message.answer(f"Количество товара '{product['name']}' обновлено на {quantity} шт.")

    # Показать корзину
    await show_cart(message)

async def show_cart(message: types.Message):
    """Функция для отображения содержимого корзины"""
    user_id = message.from_user.id
    if user_id not in cart or not cart[user_id]:
        await message.answer("Ваша корзина пуста.")
        return

    cart_items = cart[user_id]
    cart_text = "Ваши товары в корзине:\n"
    for item in cart_items:
        if 'product' in item:
            product = item['product']
            cart_text += f"Товар: {product['name']} - Количество: {item['quantity']} шт.\n"
        else:
            cart_text += f"Товар: (не найден) - Количество: {item['quantity']} шт.\n"

    logger.info(f"Корзина пользователя {user_id}: {cart_text}")
    await message.answer(cart_text)


@dp.message(lambda message: message.text == "🛒 Оформить заказ")
async def checkout(message: types.Message):
    """Обработчик кнопки 'Оформить заказ'"""
    user_id = message.from_user.id

    # Проверяем, есть ли товары в корзине
    if user_id not in cart or not cart[user_id]:
        await message.answer("Ваша корзина пуста. Добавьте товары, чтобы оформить заказ.")
        return

    cart_items = cart[user_id]
    total_price = sum(item['product']['price'] * item['quantity'] for item in cart_items if item['quantity'] > 0)

    # Формируем текст для подтверждения заказа
    order_text = "Ваш заказ:\n"
    for item in cart_items:
        if 'product' in item and item['quantity'] > 0:
            product = item['product']
            order_text += f"🌸 {product['name']} - {item['quantity']} шт. - {item['quantity'] * product['price']} руб.\n"

    order_text += f"\nИтоговая стоимость: {total_price} руб.\n\nПодтвердите заказ или отмените его."

    # Кнопки для подтверждения или отмены заказа
    buttons = [
        InlineKeyboardButton(text="✅ Подтвердить заказ", callback_data="confirm_order"),
        InlineKeyboardButton(text="❌ Отменить заказ", callback_data="cancel_order")
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=[buttons])

    await message.answer(order_text, reply_markup=markup)


@dp.callback_query(lambda c: c.data == "confirm_order")
async def confirm_order(callback_query: CallbackQuery):
    """Обработчик подтверждения заказа"""
    user_id = callback_query.from_user.id

    # Проверяем, есть ли товары в корзине
    if user_id not in cart or not cart[user_id]:
        await callback_query.message.answer("Ваша корзина пуста.")
        return

    # Формируем заказ для API
    order_items = [
        {
            "product_id": item['product']['id'],
            "quantity": item['quantity'],
            "total_price": item['product']['price'] * item['quantity']
        }
        for item in cart[user_id] if item['quantity'] > 0
    ]

    try:
        async with aiohttp.ClientSession() as session:
            payload = {
                "telegram_user_id": user_id,
                "order_items": order_items
            }
            async with session.post(f"{API_URL}/catalog/api/telegram_orders/", json=payload) as response:
                if response.status == 201:
                    await callback_query.message.answer("Ваш заказ успешно оформлен! Спасибо за покупку 🌸")
                    cart.pop(user_id, None)  # Очищаем корзину
                else:
                    await callback_query.message.answer("Не удалось оформить заказ. Попробуйте позже.")
    except Exception as e:
        logger.error(f"Ошибка оформления заказа: {e}")
        await callback_query.message.answer("Произошла ошибка. Попробуйте позже.")


@dp.callback_query(lambda c: c.data == "cancel_order")
async def cancel_order(callback_query: CallbackQuery):
    """Обработчик отмены заказа"""
    await callback_query.message.answer("Ваш заказ был отменен.")




# Основная функция для запуска бота
async def main():
    """Запуск бота"""
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем.")
