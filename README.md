# Electronics Distribution Network
  Веб-приложение для управления дистрибьюторской сетью электроники с REST API и административной панелью. 
Проект выполнен в рамках тестового задания №1.

## 🚀 Технологический стек
- Backend: Python 3.12, Django 5.2, Django REST Framework 3.15
- База данных: PostgreSQL 16
- Дополнительно: django-filter, python-dotenv
- Инструменты качества: flake8, coverage (покрытие тестами ~98%)

## 📦 Установка и запуск
### 1. Клонирование репозитория:
```bash
git clone https://github.com/GromazekaS/ElectronicLogistic.git

cd electroniclogistic
```
### 2. Создание и активация виртуального окружения
```bash
python -m venv venv

source venv/bin/activate      # Linux/Mac

venv\Scripts\activate         # Windows
```
### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```
### 4. Настройка базы данных PostgreSQL

Создайте базу данных, например electronics_db.
### 5. Скопируйте файл .env.example в .env и укажите свои параметры подключения:
```
DB_NAME=electronics_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

DJANGO_SECRET_KEY=your-secret-key
```
### 6. Применение миграций
```bash
python manage.py migrate
```
### 7. Загрузка фикстур (демонстрационные данные)
```bash
python manage.py loaddata initial_data.json
```
Фикстура содержит 10 продуктов и 45 звеньев сети (заводы, дистрибьюторы, ритейлеры), что позволяет сразу оценить функциональность.

### 8. Создание суперпользователя (для доступа в админку)
```bash
python manage.py createsuperuser
```
### 9. Запуск сервера
```bash
python manage.py runserver
```
Админка доступна по адресу: http://127.0.0.1:8000/admin/

API — http://127.0.0.1:8000/api/nodes/

## 🧪 Тестирование

#### Запуск всех тестов:
```bash
python manage.py test
```
#### Покрытие тестами можно оценить с помощью coverage:
```bash
coverage run manage.py test
coverage report
```
## 📚 API документация
#### Эндпоинты:
```
GET /api/nodes/ — список всех звеньев (поддерживается фильтрация по country, например ?country=Russia)

POST /api/nodes/ — создание нового звена

GET /api/nodes/{id}/ — детальная информация о звене

PUT /api/nodes/{id}/ — полное обновление (поле debt игнорируется)

PATCH /api/nodes/{id}/ — частичное обновление (поле debt игнорируется)

DELETE — запрещён
```
## Права доступа
- API доступно только активным сотрудникам (`is_active=True`).
- **Поле `debt`:**
    - При обращении по API любые попытки изменения игнорируются
    - Обнуление поля из админ панели администратора через `actions`
    - Изменение значения в окне детальной информации под администратором 

## Пример запроса (создание звена):
```
curl -X POST http://127.0.0.1:8000/api/nodes/ \
  -H "Content-Type: application/json" \
  -u username:password \
  -d '{
    "type": "retail",
    "name": "Магазин у дома",
    "email": "shop@example.com",
    "country": "Russia",
    "city": "Moscow",
    "street": "Тверская",
    "house_number": "10",
    "debt": "1500.50",
    "currency": "RUB",
    "products": [1, 2]
  }'
```
## 🛠 Возможности админ-панели:
- Просмотр и редактирование звеньев и продуктов.
- Отображение полей в списке звеньев: название, город, роль в иерархии (вычисляется автоматически), кликабельная ссылка на поставщика, задолженность (с разделителями тысяч).
- Фильтр по городу.
- Действие «Очистить задолженность перед поставщиком» для выбранных объектов.
- В форме редактирования: поле debt вводится в рублях, read-only поле показывает текущую задолженность в читаемом формате.

## 🔄 Сброс базы данных и загрузка фикстур заново
#### Если нужно полностью очистить базу и загрузить исходные данные:

Очистить таблицы (со сбросом индексов):
```bash
python manage.py flush
```
Загрузить фикстуры:
```bash
python manage.py loaddata initial_data.json
```
## 📁 Структура проекта

```
electronics-network/
├── config/                # Настройки проекта (settings.py, urls.py)
├── elogistic/             # Основное приложение
│   ├── fixtures/          # Фикстуры с демо-данными
│   ├── migrations/        # Миграции Django
│   ├── tests/             # Тесты (разделены по модулям)
│   ├── admin.py           # Настройки админки
│   ├── models.py          # Модели данных
│   ├── serializers.py     # DRF сериализаторы (кастомное поле RublesField)
│   ├── views.py           # ViewSet с правами доступа
│   └── urls.py            # Маршруты API
├── .env.example           # Пример файла переменных окружения
├── .flake8                # Конфигурация flake8
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
```

## ✉️ Контакты
Проект разработан в рамках тестового задания.
Репозиторий: https://github.com/GromazekaS/ElectronicLogistic.git

По всем вопросам обращаться: kinst@inbox.ru, @KinstantinVRN

# Спасибо за внимание!
