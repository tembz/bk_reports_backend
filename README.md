### API для пересменок менеджеров ресторанов Burger King

### Поддерживается:
- Создание отчёта (дневной/ночной)
- Учёт долгов ресторана
- Список отчётов за все время
- Авторизация по токену, а также Telegram Init Data для полноценных/мини-приложений

---

### Зависимости
- Python 3.13+
- Poetry
- npm
- PostgreSQL (с расширением `uuid-ossp`)

---

### Конфигурация

Создайте файл `config.toml` на основе `config.toml.example`.

> Таблицы в БД создаются автоматически при первом запуске.  
> Для работы UUID необходимо включить расширение PostgreSQL: `CREATE EXTENSION IF NOT EXISTS "uuid-ossp";`

---

### Установка и запуск

```console
npm install pm2 -g

python3.11 -m pip install poetry

poetry shell
poetry install
pm2 start
```

---

### Авторизация

API поддерживает два способа авторизации:

**1. Токен**
- Пользователь получает одноразовый `code` (добавляется в БД вручную в таблицу `tokens`)
- Обменивает его на токен через `POST /auth/createToken`
- Далее передаёт токен в заголовке `Authorization: Bearer <token>` (для POST-запросов) или в query-параметре `?token=<token>` (для GET-запросов)

**2. Telegram Init Data**
- Передаётся в заголовке `InitData` (POST) или в query-параметре `?init_data=` (GET)
- Используется для Telegram Mini Apps

---

### Эндпоинты

| Метод | Путь | Описание |
|-------|------|----------|
| `POST` | `/auth/createToken` | Получить токен по одноразовому коду |
| `GET` | `/api/report/get` | Список отчётов (`?limit=30&offset=0`) |
| `POST` | `/api/report/create` | Создать отчёт |
| `GET` | `/api/credit/get` | Список долгов (`?limit=30&offset=0`) |
| `POST` | `/api/credit/create` | Создать запись о долге |
| `GET` | `/api/credit/toggle` | Переключить статус долга (`?credit_id=`) |