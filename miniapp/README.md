# CARAVAN TRANZIT Mini App

Telegram Mini App для сервиса таможенного оформления CARAVAN TRANZIT Caravan Broker LTD.

## 🎨 Дизайн

- **Основной цвет**: #8304F9 (фиолетовый)
- **Логотип**: Фирменный стиль CARAVAN TRANZIT
- **Адаптивный**: Мобильные и десктопные устройства
- **Простой интерфейс**: Разработан для водителей

## 📱 Функционал

### Главная страница
- 4 основных карточки:
  - EPI KOD AT DEKLARATSIYA
  - MB DEKLARATSIYA
  - ARIZALARIM (Мои заявки)
  - NARXLAR KATALOGI (Прайс-лист)

### 5-шаговый процесс подачи заявки

**Шаг 1: Выбор направления**
- IMPORT (из-за рубежа в Узбекистан)
- EKSPORT (из Узбекистана за рубеж)
- TRANZIT (транзит через Узбекистан)

**Шаг 2: Выбор пограничного поста**
- 59 пограничных постов с поиском
- Автоматическая фильтрация

**Шаг 3: Выбор пункта назначения**
- IMPORT: 33 TIF поста
- TRANZIT: 59 пограничных постов
- EKSPORT: пропускается

**Шаг 4: Номер автомобиля**
- Формат: 01A777AA
- Валидация в реальном времени
- Подсказки

**Шаг 5: Загрузка документов**
- EPI: Паспорт, Тех-паспорт, CMR, Invoice
- MB: Паспорт, Тех-паспорт
- Drag & Drop поддержка
- Превью изображений

### Индикатор прогресса
- 5 шагов с визуальными индикаторами
- Прогресс-бар
- Анимация переходов

## 🔧 Интеграция с ботом

### 1. Создать Web App в BotFather

```
/newapp
@caravan_tranzit_bot
CARAVAN TRANZIT
Telegram Mini App for customs services
https://your-domain.com/miniapp/index.html
https://your-domain.com/miniapp/assets/logo.svg
```

### 2. Добавить кнопку в бота

```python
from aiogram.types import WebAppInfo, KeyboardButton

web_app_button = KeyboardButton(
    text="🌐 MINI APP",
    web_app=WebAppInfo(url="https://your-domain.com/miniapp/index.html")
)
```

### 3. Получить данные от Mini App

```python
from aiogram import F

@router.message(F.web_app_data)
async def handle_webapp_data(message: Message):
    data = json.loads(message.web_app_data.data)

    # Получаем данные заявки
    service_type = data['service_type']  # 'EPI' or 'MB'
    direction = data['direction']  # 'IMPORT', 'EKSPORT', 'TRANZIT'
    border_post = data['border_post']
    dest_post = data['dest_post']
    vehicle_number = data['vehicle_number']

    # Сохраняем в БД и обрабатываем...
```

### 4. API endpoints (опционально)

Добавить в `handlers.py`:

```python
from aiogram.types import Update
from aiohttp import web

async def handle_miniapp_submit(request):
    """Получить данные из Mini App"""
    data = await request.json()

    # Создать заявку
    app_code = await db.create_application(
        user_id=data['user_id'],
        service_type=data['service_type'],
        direction=data['direction'],
        border_post=data['border_post'],
        dest_post=data['dest_post'],
        car_number=data['vehicle_number']
    )

    return web.json_response({'success': True, 'app_code': app_code})

# Добавить роут
app.router.add_post('/api/applications', handle_miniapp_submit)
```

## 📂 Структура файлов

```
miniapp/
├── index.html          # Основной HTML
├── style.css           # Стили (CSS с переменными)
├── app.js              # JavaScript логика
├── assets/
│   └── logo.svg        # Логотип CARAVAN TRANZIT
└── README.md           # Документация
```

## 🌐 Деплой

### Вариант 1: GitHub Pages

1. Push в репозиторий
2. Settings → Pages → Source: main → /miniapp
3. URL: `https://username.github.io/CARAVAN TRANZIT/miniapp`

### Вариант 2: Netlify

```bash
cd miniapp
netlify deploy --prod
```

### Вариант 3: Vercel

```bash
cd miniapp
vercel --prod
```

### Вариант 4: Свой сервер

```nginx
server {
    listen 443 ssl;
    server_name your-domain.com;

    location /miniapp {
        root /var/www;
        index index.html;
    }
}
```

## 🔐 Безопасность

- Валидация Telegram initData
- HTTPS обязателен
- CORS настройки
- Проверка подписи

Пример проверки в Python:

```python
import hmac
import hashlib
from urllib.parse import parse_qs

def validate_telegram_webapp(init_data: str, bot_token: str) -> bool:
    """Проверить подпись Telegram Web App"""
    try:
        data = parse_qs(init_data)
        hash_value = data.get('hash', [''])[0]

        # Создать строку для проверки
        check_string = '\n'.join(f"{k}={v[0]}" for k, v in sorted(data.items()) if k != 'hash')

        # Вычислить подпись
        secret_key = hmac.new(b"WebAppData", bot_token.encode(), hashlib.sha256).digest()
        calculated_hash = hmac.new(secret_key, check_string.encode(), hashlib.sha256).hexdigest()

        return calculated_hash == hash_value
    except Exception as e:
        print(f"Validation error: {e}")
        return False
```

## 📊 Данные

### Border Posts (59)
См. константу `BORDER_POSTS` в `app.js`

### TIF Posts (33)
См. константу `TIF_POSTS` в `app.js`

## 🎯 TODO

- [x] Создать UI/UX дизайн
- [x] Реализовать frontend (HTML/CSS/JS)
- [ ] Добавить backend API endpoint
- [ ] Интегрировать с Telegram bot
- [ ] Протестировать на мобильных устройствах
- [ ] Деплой на production
- [ ] Добавить страницу "Мои заявки"
- [ ] Добавить уведомления о статусе

## 📞 Контакты

- Telegram: @CARAVAN TRANZIT, @caravan_tranzit1
- Телефон: +998 91 702 00 99, +998 94 312 00 99
- WhatsApp: +998 91 702 00 99

---

© 2024 CARAVAN TRANZIT Caravan Broker LTD
