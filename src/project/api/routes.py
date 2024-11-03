from fastapi import APIRouter, HTTPException

from src.project.infrastructure.postgres.repository.product_repo import ProductRepository
from src.project.infrastructure.postgres.database import PostgresDatabase
from src.project.infrastructure.postgres.repository.recipe_product_repo import RecipeProductRepository
from src.project.infrastructure.postgres.repository.recipe_repo import RecipeRepository
from src.project.schemas.product import ProductSchema
from src.project.schemas.recipe import RecipeSchema
from src.project.schemas.recipe_product import RecipeProductSchema

router = APIRouter()


# Products CRUD

@router.get("/all_products", response_model=list[ProductSchema])
async def get_all_products() -> list[ProductSchema]:
    product_repo = ProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_repo.check_connection(session=session)
        all_products = await product_repo.get_all_products(session=session)

    return all_products


@router.get("/product/{id}", response_model=ProductSchema)
async def get_product_by_id(id: int) -> ProductSchema:
    product_repo = ProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_repo.check_connection(session=session)
        product = await product_repo.get_product_by_id(session=session, id_product=id)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.post("/product", response_model=ProductSchema)
async def insert_product(product: ProductSchema) -> ProductSchema:
    product_repo = ProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_repo.check_connection(session=session)
        new_product = await product_repo.insert_product(session=session, name=product.name, cost=product.cost)

    if not new_product:
        raise HTTPException(status_code=500, detail="Failed to insert product")

    return new_product


@router.delete("/product/{id}", response_model=dict)
async def delete_product(id: int) -> dict:
    product_repo = ProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_repo.check_connection(session=session)
        deleted = await product_repo.delete_product_by_id(session=session, id_product=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Product not found or failed to delete")

    return {"message": "Product deleted successfully"}


@router.put("/product/{id}", response_model=ProductSchema)
async def update_product(id: int, product: ProductSchema) -> ProductSchema:
    product_repo = ProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await product_repo.check_connection(session=session)
        updated_product = await product_repo.update_product_by_id(session=session, id_product=id, name=product.name,
                                                                  cost=product.cost)

    if not updated_product:
        raise HTTPException(status_code=404, detail="Product not found or failed to update")

    return updated_product


# Recipes CRUD

@router.get("/all_recipes", response_model=list[RecipeSchema])
async def get_all_recipes() -> list[RecipeSchema]:
    recipe_repo = RecipeRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await recipe_repo.check_connection(session=session)
        all_recipes = await recipe_repo.get_all_recipes(session=session)

    return all_recipes


@router.get("/recipe/{id}", response_model=RecipeSchema)
async def get_recipe_by_id(id: int) -> RecipeSchema:
    recipe_repo = RecipeRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await recipe_repo.check_connection(session=session)
        recipe = await recipe_repo.get_recipe_by_id(session=session, id_recipe=id)

    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    return recipe


@router.post("/recipe", response_model=RecipeSchema)
async def insert_recipe(recipe: RecipeSchema) -> RecipeSchema:
    recipe_repo = RecipeRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await recipe_repo.check_connection(session=session)
        new_recipe = await recipe_repo.insert_recipe(session=session, time_to_cook=recipe.time_to_cook,
                                                     name=recipe.name)

    if not new_recipe:
        raise HTTPException(status_code=500, detail="Failed to insert recipe")

    return new_recipe


@router.put("/recipe/{id}", response_model=RecipeSchema)
async def update_recipe(id: int, recipe: RecipeSchema) -> RecipeSchema:
    recipe_repo = RecipeRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await recipe_repo.check_connection(session=session)
        updated_recipe = await recipe_repo.update_recipe_by_id(session=session, id_recipe=id,
                                                               time_to_cook=recipe.time_to_cook, name=recipe.name)

    if not updated_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found or failed to update")

    return updated_recipe


@router.delete("/recipe/{id}", response_model=dict)
async def delete_recipe(id: int) -> dict:
    recipe_repo = RecipeRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await recipe_repo.check_connection(session=session)
        deleted = await recipe_repo.delete_recipe_by_id(session=session, id_recipe=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Recipe not found or failed to delete")

    return {"message": "Recipe deleted successfully"}


# CRUD recipe_products

@router.get("/all_recipe_products", response_model=list[RecipeProductSchema])
async def get_all_recipe_products() -> list[RecipeProductSchema]:
    recipe_product_repo = RecipeProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await recipe_product_repo.check_connection(session=session)
        all_recipe_products = await recipe_product_repo.get_all_recipe_products(session=session)

    return all_recipe_products


@router.get("/recipe_product/{id_recipe}/{id_product}", response_model=RecipeProductSchema)
async def get_recipe_product_by_id(id_recipe: int, id_product: int) -> RecipeProductSchema:
    recipe_product_repo = RecipeProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await recipe_product_repo.check_connection(session=session)
        recipe_product = await recipe_product_repo.get_recipe_product_by_id(session=session,
                                                                            id_recipe=id_recipe, id_product=id_product)

    if not recipe_product:
        raise HTTPException(status_code=404, detail="RecipeProduct not found")

    return recipe_product


@router.post("/recipe_product", response_model=RecipeProductSchema)
async def insert_recipe_product(recipe_product: RecipeProductSchema) -> RecipeProductSchema:
    recipe_product_repo = RecipeProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await recipe_product_repo.check_connection(session=session)
        new_recipe_product = await recipe_product_repo.insert_recipe_product(session=session,
                                                                             id_recipe=recipe_product.id_recipe,
                                                                             id_product=recipe_product.id_product)

    if not new_recipe_product:
        raise HTTPException(status_code=500, detail="Failed to insert RecipeProduct")

    return new_recipe_product


@router.delete("/recipe_product/{id_recipe}/{id_product}", response_model=dict)
async def delete_recipe_product(id_recipe: int, id_product: int) -> dict:
    recipe_product_repo = RecipeProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await recipe_product_repo.check_connection(session=session)
        deleted = await recipe_product_repo.delete_recipe_product_by_id(session=session, id_recipe=id_recipe,
                                                                        id_product=id_product)

    if not deleted:
        raise HTTPException(status_code=404, detail="RecipeProduct not found or failed to delete")

    return {"message": "RecipeProduct deleted successfully"}


@router.put("/recipe_product/{id_recipe}/{id_product}", response_model=RecipeProductSchema)
async def update_recipe_product(id_recipe: int, id_product: int, new_id_product: int) -> RecipeProductSchema:
    recipe_product_repo = RecipeProductRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await recipe_product_repo.check_connection(session=session)
        updated_recipe_product = await recipe_product_repo.update_recipe_product_by_id(session=session,
                                                                                       id_recipe=id_recipe,
                                                                                       id_product=id_product)

    if not updated_recipe_product:
        raise HTTPException(status_code=404, detail="RecipeProduct not found or failed to update")

    return updated_recipe_product
