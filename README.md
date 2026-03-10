# BK Reports

API и Telegram-бот для автоматизации пересменок менеджеров ресторанов Burger King.

📖 **Полная документация:** [tembz.ru/bk/docs](https://tembz.ru/bk/docs)

---

### Зависимости

- Python 3.13+
- Poetry
- npm
- PostgreSQL (с расширением `uuid-ossp`)

---

### Быстрый старт
```console
npm install pm2 -g
pip install poetry
poetry install
poetry run alembic upgrade head
pm2 start
```

Создайте `config.toml` на основе `config.toml.example` перед запуском.

---

### Лицензия

MIT © 2026 tembz