from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.project.infrastructure.postgres.database import Base


class Recipe(Base):
    __tablename__ = "recipe"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    time_to_cook: Mapped[int] = mapped_column(nullable=False)

    products = relationship("Product", secondary="recipe_product", back_populates="recipes")
    dishes = relationship("Dish", back_populates="recipe")

class RecipeProduct(Base):
    __tablename__ = "recipe_product"

    id_recipe: Mapped[int] = mapped_column(ForeignKey("recipes.id"), primary_key=True)
    id_product: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    cost: Mapped[int] = mapped_column(nullable=False)

    recipes = relationship("Recipe", secondary="recipe_product", back_populates="products")

class Dish(Base):
    __tablename__ = "dish"

    id: Mapped[int] = mapped_column(primary_key=True)
    id_recipe: Mapped[int] = mapped_column(ForeignKey("recipe.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)
    cost: Mapped[int] = mapped_column(nullable=False)
    rating: Mapped[float | None] = mapped_column(nullable=True)

    recipe = relationship("Recipe", back_populates="dishes")
