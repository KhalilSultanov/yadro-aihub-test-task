# URL Alias Service (Short URL API)

Реализация тестового задания для команды **Applied AI web-сервисов / AI Hub**  
Стек: **Python 3.11 + Django 5.2 / DRF + PostgreSQL 15**

---

## Что умеет сервис

Редирект по короткой ссылке | `GET /api/code/<short_code>/`                      – Публичный  
Создать короткую ссылку | `POST /api/shorten/`                               – Basic Auth  
Список всех ссылок (pagination + фильтр)     | `GET /api/links/`                                  – Basic Auth  
Деактивировать ссылку | `PATCH /api/shorten/<short_code>/deactivate/`      – Basic Auth  
Статистика переходов (по click_count ↓)      | `GET /api/shorten/stats/`                          – Basic Auth  
Swagger / OpenAPI Docs | `GET /api/docs/`                                   – Публичный

*Срок жизни ссылки* — 1 день (можно переопределить в `expires_at`).  
Доступ по неактивным или истёкшим ссылкам — `403` / `410`.

---

## Быстрый старт (локально)

> Всё запускается без Docker; нужна только установленная PostgreSQL 15+.

1. **Клонируем репу и переходим в каталог**
   ```bash
   git clone ...

2. **Создаём и активируем виртуальное окружение**

   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

3. **Ставим зависимости**

   ```bash
   pip install -r requirements.txt
   ```

4. **Настраиваем Postgres**
   Создайте базу и пользователя, затем заполните файл `.env`:

   ```ini
   POSTGRES_DB=aihub
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=aihub
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   ```

5. **Миграции и суперпользователь**

   ```bash
   make migrate           
   make createsuperuser   
   ```

6. **Запуск**

   ```bash
   make run              
   ```

   Теперь API доступен на `http://localhost:8000`.

---

## Аутентификация

* **Метод**: HTTP Basic Auth
* **Как создать пользователя**

    * `make createsuperuser` (стандартный способ)
    * или запуск готового скрипта:

      ```bash
      python scripts/create_default_admin.py
      ```

      Создаст `admin / admin`.

---

## Примеры запросов

Вот корректные **JSON-примеры запросов и ответов** для каждого ключевого эндпоинта:

---

### POST `/api/shorten/` – **Создание короткой ссылки**

**Request**:

```json
{
  "original_url": "https://example.com/very/long/path"
}
```

**Response**:

```json
{
  "original_url": "https://example.com/very/long/path",
  "short_code": "aBcD123",
  "full_short_url": "http://localhost:8000/api/code/aBcD123",
  "expires_at": "2025-06-06 12:00:00",
  "is_active": true,
  "click_count": 0,
  "last_visited_at": null
}
```

---

### GET `/api/links/?is_active=true` – **Список ссылок (с фильтрацией)**

**Response**:

```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "original_url": "https://example.com/1",
      "short_code": "abc123",
      "full_short_url": "http://localhost:8000/api/code/abc123",
      "expires_at": "2025-06-05 15:00:00",
      "is_active": true,
      "click_count": 5,
      "last_visited_at": "2025-06-04 10:00:00"
    },
    {
      "original_url": "https://example.com/2",
      "short_code": "def456",
      "full_short_url": "http://localhost:8000/api/code/def456",
      "expires_at": "2025-06-06 15:00:00",
      "is_active": true,
      "click_count": 2,
      "last_visited_at": null
    }
  ]
}
```

---

### PATCH `/api/shorten/<short_code>/deactivate/` – **Деактивация ссылки**

**Response**:

```json
{
  "detail": "Link successfully deactivated."
}
```

*Если уже деактивирована:*

```json
{
  "detail": "Link is already deactivated."
}
```

---

### GET `/api/shorten/stats/` – **Статистика по кликам**

**Response**:

```json
[
  {
    "short_code": "abc123",
    "original_url": "https://example.com/1",
    "click_count": 7
  },
  {
    "short_code": "def456",
    "original_url": "https://example.com/2",
    "click_count": 3
  }
]
```

---

### GET `/api/code/<short_code>/` – **Редирект**

**Успешный редирект**: HTTP 302 → `Location: https://example.com/1`
**Если ссылка устарела**:

```json
{
  "detail": "Link is expired."
}
```

**Если деактивирована**:

```json
{
  "detail": "Link is inactive."
}
```

---

## Полезные ссылки

* **Swagger UI**:   `http://localhost:8000/api/docs/`
* **Admin-панель**: `http://localhost:8000/admin/`
