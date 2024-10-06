# KamiBOT
Bot for Kami that will help teach students.

### Installing:
```
poetry install --no-root
```
```
pre-commit install
```
```
cp .env-example .env
```

### Run checkers:
```
poetry run ruff check --fix .
```
```
poetry run mypy .
```
```
pre-commit run --all-files
```

### Create migration:
```
poetry run alembic revision --autogenerate -m 'migration name'
```

### Run migrations:
```
poetry run alembic upgrade head
```

### Run in Docker:
```
docker compose up --build -d
```

### Run locally:
```
poetry run python -m kami
```

### Tips for i18n in aiogram 3:
**Extract all words and phrases from code**
```
poetry run pybabel extract -k __ --input-dirs=. -o ./kami/locales/kami.pot
```
**Add translates kami.po and update:**
```
poetry run pybabel update -d ./kami/locales -D kami -i ./kami/locales/kami.pot
```
**Compile files:**
```
poetry run pybabel compile -d kami/locales -D kami
```
**Add language**:
```
poetry run pybabel init -i ./kami/locales/kami.pot -d ./kami/locales -D kami -l ru
```
**Using in regular text:**
```
from aiogram.utils.i18n import gettext as _

await message.answer(
    text=_("Hello World!"),
)
```
**Using in text with varibles:**
```
from aiogram.utils.i18n import gettext as _

await message.answer(
    text=_("Welcome to {bot_name}").format(bot_name=callback_data.bot_name),
)
```
**Using in filters:**
```
from aiogram.utils.i18n import lazy_gettext as __

@router.message(F.text == __("My menu entry"))
    ...
```

#### © Eugene Denkevich, 2024.
