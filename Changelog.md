### История изменения проекта по semver (https://semver.org/lang/ru/)

# 3.1.0 (22.11.2024)
- изменена схема UsersSchema на UserSchema
- добавлены routes для регистрации пользователя
- CRUD для users
- Нужно доработать /login (нужно еще передавать password и сравнивать с password_hash)
- Нужно добавить хэширование паролей
- Нужно улучшить сравнение role с доступными вариантами ('user', 'admin') через ENUM
- login должен возвращать JWT-token, который будем хранить в отдельной таблице
- Ограничить большинство запросов для пользователя с role = 'user'
- Ограничить абсолютное большинство запросов для незалогинненого (без jwt-token) пользователя

# 3.0.0 (21.11.2024)
- alembic наконец работает полноценно, 
  для этого было изменено:
  
- docker-compose.yml:
  
    для postgres-контейнера:
    ```bash
    ports:
    - '5433:5432'
    ```
    для app-контейнера:
    ```bash
    ports:
    - '8020:8000'
    ```
  То есть был убран лишний адрес localhost,
  так как внутри docker-контейнеров он не был виден
    
- обновлена миграция (добавлена таблица users)

# 2.1.0 (20.11.2024)
- добавляем таблицу users

# 2.0.0 (06.11.2024)
- в alembic.ini строку sqlalchemy.url обратно поменял на значение по умолчпанию
- Добавлены batch, warehouse, supplier, batch_product схемы

# 1.6.0 (05.11.2024)
- сделал CRUD для всех остальных таблиц:
  order, cook, waiter, customer...

# 1.5.0 (05.11.2024)
- дописал sqlalchemy.url на свой
- написал dish

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