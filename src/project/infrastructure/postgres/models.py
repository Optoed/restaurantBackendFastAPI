import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.project.infrastructure.postgres.database import Base


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    role: Mapped[str] = mapped_column(nullable=False)
    password_hash: Mapped[str] = mapped_column(nullable=False)

    customers = relationship("Customer", secondary="user_customer", back_populates="users")

class Recipe(Base):
    __tablename__ = "recipe"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    time_to_cook: Mapped[int] = mapped_column(nullable=False)

    products = relationship("Product", secondary="recipe_product", back_populates="recipes")
    dishes = relationship("Dish", back_populates="recipe")


class UserCustomer(Base):
    __tablename__ = "user_customer"

    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    id_customer: Mapped[int] = mapped_column(ForeignKey("customer.id"), primary_key=True)

class RecipeProduct(Base):
    __tablename__ = "recipe_product"

    id_recipe: Mapped[int] = mapped_column(ForeignKey("recipe.id"), primary_key=True)
    id_product: Mapped[int] = mapped_column(ForeignKey("product.id"), primary_key=True)


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    cost: Mapped[int] = mapped_column(nullable=False)

    recipes = relationship("Recipe", secondary="recipe_product", back_populates="products")
    batch_product = relationship("BatchProduct", back_populates="product")  # Исправлено


class Dish(Base):
    __tablename__ = "dish"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_recipe: Mapped[int] = mapped_column(ForeignKey("recipe.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    cost: Mapped[int] = mapped_column(nullable=False)
    rating: Mapped[float | None] = mapped_column(nullable=True)

    recipe = relationship("Recipe", back_populates="dishes")


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_waiter: Mapped[int] = mapped_column(ForeignKey("waiter.id"), nullable=False)
    id_customer: Mapped[int] = mapped_column(ForeignKey("customer.id"), nullable=False)
    total_cost: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)

    waiter = relationship("Waiter", back_populates="orders")
    customer = relationship("Customer", back_populates="orders")
    orders_dish_cook = relationship("OrdersDishCook", back_populates="order")  # Исправлено


class Cook(Base):
    __tablename__ = "cook"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    post: Mapped[str | None] = mapped_column(nullable=True)
    salary: Mapped[int | None] = mapped_column(nullable=True)
    rating: Mapped[float | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=False)

    orders_dish_cook = relationship("OrdersDishCook", back_populates="cook")


class Customer(Base):
    __tablename__ = "customer"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(nullable=True)
    rating: Mapped[float | None] = mapped_column(nullable=True)

    orders = relationship("Order", back_populates="customer")
    users = relationship("User", secondary="user_customer", back_populates="customer")

class Waiter(Base):
    __tablename__ = "waiter"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    salary: Mapped[int] = mapped_column(nullable=False)
    rating: Mapped[float | None] = mapped_column(nullable=True)
    status: Mapped[str] = mapped_column(nullable=False)

    orders = relationship("Order", back_populates="waiter")


class OrdersDishCook(Base):
    __tablename__ = "orders_dish_cook"

    id_orders: Mapped[int] = mapped_column(ForeignKey("orders.id"), primary_key=True)
    id_dish: Mapped[int] = mapped_column(ForeignKey("dish.id"), primary_key=True)
    id_cook: Mapped[int | None] = mapped_column(ForeignKey("cook.id"), nullable=True)
    status: Mapped[str] = mapped_column(nullable=False)

    order = relationship("Order", back_populates="orders_dish_cook")
    dish = relationship("Dish")
    cook = relationship("Cook")


class Warehouse(Base):
    __tablename__ = "warehouse"

    id: Mapped[int] = mapped_column(primary_key=True)
    location: Mapped[str] = mapped_column(nullable=False)
    how_full: Mapped[float] = mapped_column(nullable=False)

    batch = relationship("Batch", back_populates="warehouse")


class Supplier(Base):
    __tablename__ = "supplier"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    cost: Mapped[int] = mapped_column(nullable=False)
    rating: Mapped[float] = mapped_column(nullable=False)

    batch = relationship("Batch", back_populates="supplier")


class Batch(Base):
    __tablename__ = "batch"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_supplier: Mapped[int] = mapped_column(ForeignKey("supplier.id"), nullable=False)
    id_warehouse: Mapped[int] = mapped_column(ForeignKey("warehouse.id"), nullable=False)
    total_cost: Mapped[int] = mapped_column(nullable=False)

    supplier = relationship("Supplier", back_populates="batch")  # Исправлено
    warehouse = relationship("Warehouse", back_populates="batch")  # Исправлено
    batch_product = relationship("BatchProduct", back_populates="batch")  # Исправлено


class BatchProduct(Base):
    __tablename__ = "batch_product"

    id_batch: Mapped[int] = mapped_column(ForeignKey("batch.id"), primary_key=True)
    id_product: Mapped[int] = mapped_column(ForeignKey("product.id"), primary_key=True)
    amount: Mapped[int] = mapped_column(nullable=False)
    expiration_date: Mapped[datetime.date] = mapped_column(nullable=False)

    batch = relationship("Batch", back_populates="batch_product")
    product = relationship("Product", back_populates="batch_product")