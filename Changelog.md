### История изменения проекта по semver (https://semver.org/lang/ru/)

# 1.4.0 (03.11.2024)
- заменена restaurant_schema на public в docker-compose
- однако проблема с alembic upgrade head по-прежнему не решена

# 1.3.0 (03.11.2024)
- добавлен CRUD для recipe_product (связь many to many таблиц recipe и product)
- init.sql для создания и заполнения таблиц
- init.sql в docker-compose

# 1.2.0 (03.11.2024)
- Добавлены get, post запросы для recipe

# 1.1.0 (03.11.2024)
- Добавлены schemas для recipe, recipe_product
- Добавлены в models recipe, recipe_product

# 1.0.1 (03.11.2024)
- Убраны некоторые ошибки в стилизации кода:
    ID заменен на id_product
    string заменен на str

# 1.0.0 (29.10.2024)
- Работающие контейнеры Docker
- Работающие CRUD запросы с таблицей product
- Дописана инструкция в README.md

# 0.2.0 (29.10.2024)
- Добавлены model: product
- Добавлены CRUD-запросы к product в routes
- product repo_product

# 0.1.0 (29.10.2024)
- Добавлена в schemas таблица product