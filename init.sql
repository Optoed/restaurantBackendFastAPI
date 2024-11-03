DROP TABLE IF EXISTS batch_product CASCADE;
DROP TABLE IF EXISTS batch CASCADE;
DROP TABLE IF EXISTS warehouse CASCADE;
DROP TABLE IF EXISTS supplier CASCADE;
DROP TABLE IF EXISTS orders_dish_cook CASCADE;
DROP TABLE IF EXISTS cook CASCADE;
DROP TABLE IF EXISTS discount CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS customer CASCADE;
DROP TABLE IF EXISTS waiter CASCADE;
DROP TABLE IF EXISTS dish CASCADE;
DROP TABLE IF EXISTS recipe CASCADE;
DROP TABLE IF EXISTS product CASCADE;
DROP TABLE IF EXISTS recipe_product CASCADE;

DROP TYPE IF EXISTS order_status CASCADE;
DROP TYPE IF EXISTS worker_status CASCADE;

-- типы статусов (status) в заказе (order)
CREATE TYPE order_status AS ENUM ('Pending', 'Completed', 'Cancelled', 'In Progress');

-- status для официантов и поваров
CREATE TYPE worker_status AS ENUM ('Not at work', 'Busy', 'Free');

-- Создание таблицы продуктов
CREATE TABLE product (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    cost INTEGER NOT NULL
);

-- Создание таблицы рецептов
CREATE TABLE recipe (
    id SERIAL PRIMARY KEY,
    time_to_cook TIME,
    name VARCHAR(100) NOT NULL
);

-- Промежуточная таблица
CREATE TABLE recipe_product (
    id_recipe INTEGER NOT NULL REFERENCES recipe(id) ON DELETE CASCADE,
    id_product INTEGER NOT NULL REFERENCES product(id) ON DELETE CASCADE,
    PRIMARY KEY (id_recipe, id_product)
);

-- Создание таблицы блюд (Dish)
CREATE TABLE dish (
    id SERIAL PRIMARY KEY,
    id_recipe INTEGER NOT NULL REFERENCES recipe(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    cost INTEGER NOT NULL,
    rating DECIMAL(3, 1)
);

-- Создание таблицы официантов
CREATE TABLE waiter (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    salary INTEGER NOT NULL,
    rating DECIMAL(3, 1),
    status worker_status NOT NULL
);

-- Создание таблицы клиентов
CREATE TABLE customer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    rating DECIMAL(3, 1)
);

-- Создание таблицы заказов
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    id_waiter INTEGER NOT NULL REFERENCES waiter(id) ON DELETE CASCADE,
    id_customer INTEGER NOT NULL REFERENCES customer(id) ON DELETE CASCADE,
    total_cost INTEGER NOT NULL,
    status order_status NOT NULL
);

-- Создание таблицы скидок
CREATE TABLE discount (
    id SERIAL PRIMARY KEY,
    id_customer INTEGER NOT NULL REFERENCES customer(id) ON DELETE CASCADE,
    percentage DECIMAL(3, 2) NOT NULL,
    expiration_date DATE
);

-- Создание таблицы поваров
CREATE TABLE cook (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    post VARCHAR(100),
    salary INTEGER,
    rating DECIMAL(3,1),
    status worker_status NOT NULL
);

-- Создание промежуточной таблицы для связей заказ-блюдо-повар
CREATE TABLE orders_dish_cook (
    id_orders INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
    id_dish INTEGER NOT NULL REFERENCES dish(id) ON DELETE CASCADE,
    id_cook INTEGER NOT NULL REFERENCES cook(id) ON DELETE SET NULL,  -- Устанавливаем NULL при удалении повара
    status order_status NOT NULL,
    PRIMARY KEY (id_orders, id_dish)
);

-- Создание таблицы поставщиков
CREATE TABLE supplier (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    cost INTEGER NOT NULL,
    rating DECIMAL(3,1)
);

-- Создание таблицы складов
CREATE TABLE warehouse (
    id SERIAL PRIMARY KEY,
    location VARCHAR(250),
    how_full DECIMAL(3,2)
);

-- Создание таблицы партий поставок
CREATE TABLE batch (
    id SERIAL PRIMARY KEY,
    id_supplier INTEGER NOT NULL REFERENCES supplier(id) ON DELETE CASCADE,
    id_warehouse INTEGER NOT NULL REFERENCES warehouse(id) ON DELETE CASCADE,
    total_cost INTEGER NOT NULL
);

-- Создание промежуточной таблицы партии-продукты
CREATE TABLE batch_product (
    id_batch INTEGER NOT NULL REFERENCES batch(id) ON DELETE CASCADE,
    id_product INTEGER NOT NULL REFERENCES product(id) ON DELETE CASCADE,
    amount INTEGER NOT NULL,
    expiration_date DATE,
    PRIMARY KEY (id_batch, id_product)
);


-- Заполнение таблиц

-- Очистим таблицу recipe_product
TRUNCATE TABLE recipe_product RESTART IDENTITY CASCADE;

-- Очистим таблицу recipe
TRUNCATE TABLE recipe RESTART IDENTITY CASCADE;

-- Заполнение таблицы recipe
INSERT INTO recipe (name, time_to_cook) VALUES
    ('Салат с морковью и свёклой', '00:10:00'),
    ('Борщ №1 (с говядиной)', '00:55:00'),
    ('Борщ №2 (с курицей)', '00:45:00'),
    ('Говядина с сыром и сливочным маслом', '00:45:00'),
    ('Крем-суп с курицей', '00:40:00'),
    ('Салат Цезарь №1', '00:20:00'),
    ('Салат Цезарь №2 (веганский)', '00:07:00');

-- Очистим таблицу product
TRUNCATE TABLE product RESTART IDENTITY CASCADE;

-- Заполнение таблицы product
INSERT INTO product (name, cost) VALUES
    ('Морковь', 30),
    ('Капуста', 20),
    ('Картофель', 40),
    ('Свёкла', 30),
    ('Салат Айсберг', 250),
    ('Петрушка', 300),
    ('Курица', 300),
    ('Говядина', 800),
    ('Сливочное масло', 400),
    ('Сыр', 500),
    ('Молоко', 100);

-- Заполнение таблицы recipe_product
INSERT INTO recipe_product (id_recipe, id_product) VALUES
    (1, 1),
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
    (2, 6),
    (2, 8);

-- Очистим таблицу dish
TRUNCATE TABLE dish RESTART IDENTITY CASCADE;

-- Заполнение таблицы dish
INSERT INTO dish (id_recipe, name, cost, rating) VALUES
    (1, 'Салат с морковью и свёклой / Salad with carrot and beet', 75, 8.9),
    (2, 'Борщ с говядиной / Borscht with beef', 550, 7.5),
    (5, 'Крем-суп с курицей (Острый!) / Cream soup with chicken (Spicy!)', 500, 5.8);

-- Очистим таблицу warehouse
TRUNCATE TABLE warehouse RESTART IDENTITY CASCADE;

-- Заполнение таблицы warehouse
INSERT INTO warehouse (location, how_full) VALUES
    ('Склад №1', 0.75),
    ('Склад №2', 0.50),
    ('Склад №3', 0.80);

-- Очистим таблицу supplier
TRUNCATE TABLE supplier RESTART IDENTITY CASCADE;

-- Заполнение таблицы supplier
INSERT INTO supplier (name, cost, rating) VALUES
    ('Поставщик 1', 100, 4.5),
    ('Поставщик 2', 200, 4.0),
    ('Поставщик 3', 150, 4.8);

-- Очистим таблицу customer
TRUNCATE TABLE customer RESTART IDENTITY CASCADE;

-- Заполнение таблицы customer
INSERT INTO customer (name, rating) VALUES
    ('Иван Иванов', 4.7),
    ('Петр Петров', 4.5),
    ('Светлана Сидорова', 4.9);

-- Очистим таблицу waiter
TRUNCATE TABLE waiter RESTART IDENTITY CASCADE;

-- Заполнение таблицы waiter
INSERT INTO waiter (name, salary, rating, status) VALUES
    ('Алексей', 30000, 4.6, 'Free'),
    ('Мария', 32000, 4.2, 'Busy'),
    ('Дмитрий', 28000, 4.8, 'Free');

-- Очистим таблицу orders
TRUNCATE TABLE orders RESTART IDENTITY CASCADE;

-- Заполнение таблицы orders
INSERT INTO orders (id_waiter, id_customer, total_cost, status) VALUES
    (1, 1, 1000, 'Completed'),
    (2, 2, 750, 'Pending'),
    (3, 3, 500, 'In Progress');

-- Очистим таблицу discount
TRUNCATE TABLE discount RESTART IDENTITY CASCADE;

-- Заполнение таблицы discount
INSERT INTO discount (id_customer, percentage, expiration_date) VALUES
    (1, 0.10, '2024-12-31'),
    (2, 0.15, '2025-01-15'),
    (3, 0.05, '2024-06-30');

-- Очистим таблицу cook
TRUNCATE TABLE cook RESTART IDENTITY CASCADE;

-- Заполнение таблицы cook
INSERT INTO cook (name, post, salary, rating, status) VALUES
    ('Анна', 'Повар', 35000, 4.7, 'Free'),
    ('Сергей', 'Шеф-повар', 50000, 4.9, 'Busy'),
    ('Ольга', 'Помощник повара', 30000, 4.5, 'Free');

-- Очистим таблицу orders_dish_cook
TRUNCATE TABLE orders_dish_cook RESTART IDENTITY CASCADE;

-- Заполнение таблицы orders_dish_cook
INSERT INTO orders_dish_cook (id_orders, id_dish, id_cook, status) VALUES
    (1, 1, 1, 'Pending'),
    (1, 2, 1, 'Completed'),
    (2, 1, 2, 'In Progress');

-- Очистим таблицу batch
TRUNCATE TABLE batch RESTART IDENTITY CASCADE;

-- Заполнение таблицы batch
INSERT INTO batch (id_supplier, id_warehouse, total_cost) VALUES
    (1, 1, 5000),
    (2, 2, 3000),
    (3, 3, 4500);

-- Очистим таблицу batch_product
TRUNCATE TABLE batch_product RESTART IDENTITY CASCADE;

-- Заполнение таблицы batch_product
INSERT INTO batch_product (id_batch, id_product, amount, expiration_date) VALUES
    (1, 1, 100, '2025-12-31'),
    (1, 2, 200, '2025-06-30'),
    (2, 3, 150, '2025-08-15'),
    (3, 4, 80, '2024-11-01');

