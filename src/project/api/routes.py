from fastapi import APIRouter, HTTPException

from src.project.infrastructure.postgres.repository.product_repo import ProductRepository
from src.project.infrastructure.postgres.database import PostgresDatabase
from src.project.schemas.product import ProductSchema

router = APIRouter()


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
