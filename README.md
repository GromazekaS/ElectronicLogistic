Electronics Distribution Network
Веб-приложение для управления дистрибьюторской сетью электроники с REST API и административной панелью. Реализована иерархическая структура звеньев (заводы, розничные сети, ИП), учёт продуктов и задолженности. Проект выполнен в рамках тестового задания и демонстрирует профессиональный подход к разработке на Django + DRF.

🚀 Технологический стек
Backend: Python 3.12, Django 5.2, Django REST Framework 3.15

База данных: PostgreSQL 16

Дополнительно: django-filter, python-dotenv

Инструменты качества: flake8, coverage (покрытие тестами ~98%)

📦 Установка и запуск
1. Клонирование репозитория
bash
git clone https://github.com/yourusername/electronics-network.git
cd electronics-network
2. Создание и активация виртуального окружения
bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
3. Установка зависимостей
bash
pip install -r requirements.txt
4. Настройка базы данных PostgreSQL
Создайте базу данных, например electronics_db.
Скопируйте файл .env.example в .env и укажите свои параметры подключения:

env
DB_NAME=electronics_db
DB_USER=your_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
DJANGO_SECRET_KEY=your-secret-key
5. Применение миграций
bash
python manage.py migrate
6. Загрузка фикстур (демонстрационные данные)
bash
python manage.py loaddata initial_data.json
Фикстура содержит 10 продуктов и 45 звеньев сети (заводы, дистрибьюторы, ритейлеры), что позволяет сразу оценить функциональность.

7. Создание суперпользователя (для доступа в админку)
bash
python manage.py createsuperuser
8. Запуск сервера
bash
python manage.py runserver
Админка доступна по адресу: http://127.0.0.1:8000/admin/
API — http://127.0.0.1:8000/api/nodes/

🧪 Тестирование
Запуск всех тестов:

bash
python manage.py test
Покрытие тестами можно оценить с помощью coverage:

bash
coverage run manage.py test
coverage report
Текущее покрытие — 98% (по модулям проекта не ниже 94%).

📚 API документация
Эндпоинты
GET /api/nodes/ — список всех звеньев (поддерживается фильтрация по country, например ?country=Russia)

POST /api/nodes/ — создание нового звена

GET /api/nodes/{id}/ — детальная информация о звене

PUT /api/nodes/{id}/ — полное обновление (поле debt игнорируется)

PATCH /api/nodes/{id}/ — частичное обновление (поле debt игнорируется)

DELETE — запрещён

Права доступа
Доступ к API имеют только активные сотрудники (пользователи с is_active=True).

Формат поля debt
На входе ожидается строка вида "123.45" (рубли с копейками, не более двух знаков после запятой).

В базе хранится целое число в копейках.

При получении объекта поле возвращается в виде строки с двумя знаками после запятой.

Пример запроса (создание звена)
bash
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
🛠 Возможности админ-панели
Просмотр и редактирование звеньев и продуктов.

В списке звеньев отображаются: название, город, роль в иерархии (вычисляется автоматически), кликабельная ссылка на поставщика, задолженность (с разделителями тысяч).

Фильтр по городу.

Действие «Очистить задолженность перед поставщиком» для выбранных объектов.

В форме редактирования: поле debt вводится в рублях, read-only поле показывает текущую задолженность в читаемом формате.

🔄 Сброс базы данных и загрузка фикстур заново
Если нужно полностью очистить базу и загрузить исходные данные:

Очистить таблицы (сбросить последовательности):

bash
python manage.py flush
Загрузить фикстуры:

bash
python manage.py loaddata initial_data.json
При использовании flush все последовательности (счётчики id) автоматически сбрасываются, новые объекты будут получать id начиная с 1. Если требуется ручной сброс последовательности после удаления данных (например, через SQL), можно выполнить:

sql
SELECT setval('elogistic_networknode_id_seq', 1, false);
SELECT setval('elogistic_product_id_seq', 1, false);
📁 Структура проекта
text
electronics-network/
├── config/               # Настройки проекта (settings.py, urls.py)
├── elogistic/            # Основное приложение
│   ├── fixtures/         # Фикстуры с демо-данными
│   ├── migrations/       # Миграции Django
│   ├── tests/            # Тесты (разделены по модулям)
│   ├── admin.py          # Настройки админки
│   ├── models.py         # Модели данных
│   ├── serializers.py    # DRF сериализаторы (кастомное поле RublesField)
│   ├── views.py          # ViewSet с правами доступа
│   └── urls.py           # Маршруты API
├── .env.example          # Пример файла переменных окружения
├── .flake8               # Конфигурация flake8
├── .gitignore
├── manage.py
├── README.md
└── requirements.txt
📈 Покрытие тестами (отчёт coverage)
text
Name                  Stmts   Miss  Cover
-----------------------------------------
elogistic/admin.py       62      4    94%
elogistic/models.py      37      2    95%
elogistic/serializers.py 35      1    97%
... (остальные 100%)
-----------------------------------------
TOTAL                   316      5    98%
✉️ Контакты
Проект разработан в рамках тестового задания.
Репозиторий: https://github.com/yourusername/electronics-network

По всем вопросам обращаться: [ваш email или Telegram]

Спасибо за внимание!