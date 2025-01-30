
---

## 🌸 Интернет-магазин цветов с Django и Telegram-ботом

### 📌 Описание проекта
Этот проект — интернет-магазин цветов, который позволяет пользователям:  
- Просматривать каталог букетов  
- Добавлять товары в корзину  
- Оформлять заказы через сайт и Telegram-бот  
- Просматривать историю заказов  

### 🚀 Функционал
- **Сайт (Django):**  
  ✅ Регистрация и авторизация пользователей  
  ✅ Каталог товаров  
  ✅ Оформление заказов  
  ✅ История заказов  
  ✅ Админ-панель для управления товарами  

- **Telegram-бот (Aiogram):**  
  ✅ Регистрация через Telegram  
  ✅ Просмотр каталога с картинками  
  ✅ Добавление товаров в корзину  
  ✅ Оформление заказов  

---

## 🔧 Установка и запуск

### 1️⃣ **Клонирование репозитория**
```sh
git clone [https://github.com/ВАШ_РЕПОЗИТОРИЙ.git](https://github.com/coroleva/flower_shop.git)
cd ВАШ_РЕПОЗИТОРИЙ
```

### 2️⃣ **Создание и активация виртуального окружения**
```sh
python -m venv venv
source venv/bin/activate  # для macOS/Linux
venv\Scripts\activate     # для Windows
```

### 3️⃣ **Установка зависимостей**
```sh
pip install -r requirements.txt
```

### 4️⃣ **Настройка базы данных**
```sh
python manage.py migrate
```

### 5️⃣ **Создание суперпользователя**
```sh
python manage.py createsuperuser
```

### 6️⃣ **Запуск сервера**
```sh
python manage.py runserver
```
Теперь сайт будет доступен по адресу: [`http://127.0.0.1:8000`](http://127.0.0.1:8000).

---

## 🤖 Запуск Telegram-бота
1. Укажите **TOKEN** в файле `config.py`
2. Запустите бота:
```sh
python bot.py
```

---

## 🔗 API
- `GET /catalog/api/catalog/` — Получение списка товаров  
- `POST /catalog/api/order/` — Создание заказа через Telegram  

---

## 📌 Технологии
- **Backend:** Python, Django, Django REST Framework  
- **Frontend:** HTML, CSS (Bootstrap)  
- **База данных:** SQLite (по умолчанию)  
- **Хостинг изображений:** Cloudinary  
- **Telegram-бот:** Aiogram  

---

## 📄 Лицензия
Этот проект распространяется под лицензией MIT.

---

Такое описание поможет другим людям (и вам в будущем) быстро разобраться в проекте! 😊🚀
