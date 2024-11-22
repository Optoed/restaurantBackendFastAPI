from fastapi import APIRouter, HTTPException

from src.project.infrastructure.postgres.repository.cook_repo import CookRepository
from src.project.infrastructure.postgres.repository.customer_repo import CustomerRepository
from src.project.infrastructure.postgres.repository.dish_repo import DishRepository
from src.project.infrastructure.postgres.repository.order_dish_cook_repo import OrderDishCookRepository
from src.project.infrastructure.postgres.repository.order_repo import OrderRepository
from src.project.infrastructure.postgres.repository.product_repo import ProductRepository
from src.project.infrastructure.postgres.database import PostgresDatabase
from src.project.infrastructure.postgres.repository.recipe_product_repo import RecipeProductRepository
from src.project.infrastructure.postgres.repository.recipe_repo import RecipeRepository
from src.project.infrastructure.postgres.repository.users_repo import UsersRepository
from src.project.infrastructure.postgres.repository.waiter_repo import WaiterRepository
from src.project.schemas.cook import CookSchema
from src.project.schemas.customer import CustomerSchema
from src.project.schemas.dish import DishSchema
from src.project.schemas.order import OrderSchema
from src.project.schemas.order_dish_cook import OrderDishCookSchema
from src.project.schemas.product import ProductSchema
from src.project.schemas.recipe import RecipeSchema
from src.project.schemas.recipe_product import RecipeProductSchema
from src.project.schemas.user import UserSchema
from src.project.schemas.waiter import WaiterSchema

router = APIRouter()

# Registration of User


@router.post("/register", response_model=UserSchema)
async def register(user: UserSchema) -> UserSchema:
    users_repo = UsersRepository()
    database = PostgresDatabase()

    # TODO: убери потом
    if user.role != "admin" and user.role != "user":
        raise HTTPException(status_code=400, detail="role can be only 'user' or 'admin'")

    async with database.session() as session:
        await users_repo.check_connection(session=session)
        user = await users_repo.register_user(session=session,
                                              name=user.name,
                                              email=user.email,
                                              password_hash=user.password_hash,
                                              role=user.role)

    if not user:
        raise HTTPException(status_code=500, detail="Failed to register user")

    return user


# TODO: нужно добавить работу с JWT-token

@router.post("/login", response_model=UserSchema)
async def login(user: UserSchema) -> UserSchema:
    users_repo = UsersRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await users_repo.check_connection(session=session)
        find_user = await users_repo.get_user_by_email(session=session, email=user.email)

    if not find_user:
        raise HTTPException(status_code=400, detail="User is not found")
    return find_user


# other Users CRUD


@router.get("/all_users", response_model=list[UserSchema])
async def get_all_users() -> list[UserSchema]:
    users_repo = UsersRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await users_repo.check_connection(session=session)
        all_users = await users_repo.get_all_users(session=session)

    return all_users

@router.get("/user/{id}", response_model=UserSchema)
async def get_user_by_id(id: int) -> UserSchema:
    users_repo = UsersRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await users_repo.check_connection(session=session)
        user = await users_repo.get_user_by_id(session=session, id_user=id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


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

# Dishes CRUD

@router.get("/all_dishes", response_model=list[DishSchema])
async def get_all_dishes() -> list[DishSchema]:
    dish_repo = DishRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await dish_repo.check_connection(session=session)
        all_dishes = await dish_repo.get_all_dishes(session=session)

    return all_dishes


@router.get("/dish/{id}", response_model=DishSchema)
async def get_dish_by_id(id: int) -> DishSchema:
    dish_repo = DishRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await dish_repo.check_connection(session=session)
        dish = await dish_repo.get_dish_by_id(session=session, id_dish=id)

    if not dish:
        raise HTTPException(status_code=404, detail="Dish not found")

    return dish


@router.post("/dish", response_model=DishSchema)
async def insert_dish(dish: DishSchema) -> DishSchema:
    dish_repo = DishRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await dish_repo.check_connection(session=session)
        new_dish = await dish_repo.insert_dish(
            session=session,
            id_recipe=dish.id_recipe,
            name=dish.name,
            cost=dish.cost,
            rating=dish.rating
        )

    if not new_dish:
        raise HTTPException(status_code=500, detail="Failed to insert dish")

    return new_dish


@router.put("/dish/{id}", response_model=DishSchema)
async def update_dish(id: int, dish: DishSchema) -> DishSchema:
    dish_repo = DishRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await dish_repo.check_connection(session=session)
        updated_dish = await dish_repo.update_dish_by_id(
            session=session,
            id_dish=id,
            id_recipe=dish.id_recipe,
            name=dish.name,
            cost=dish.cost,
            rating=dish.rating
        )

    if not updated_dish:
        raise HTTPException(status_code=404, detail="Dish not found or failed to update")

    return updated_dish


@router.delete("/dish/{id}", response_model=dict)
async def delete_dish(id: int) -> dict:
    dish_repo = DishRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await dish_repo.check_connection(session=session)
        deleted = await dish_repo.delete_dish_by_id(session=session, id_dish=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Dish not found or failed to delete")

    return {"message": "Dish deleted successfully"}


# Orders CRUD

@router.get("/all_orders", response_model=list[OrderSchema])
async def get_all_orders() -> list[OrderSchema]:
    order_repo = OrderRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await order_repo.check_connection(session=session)
        all_orders = await order_repo.get_all_orders(session=session)

    return all_orders


@router.get("/order/{id}", response_model=OrderSchema)
async def get_order_by_id(id: int) -> OrderSchema:
    order_repo = OrderRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await order_repo.check_connection(session=session)
        order = await order_repo.get_order_by_id(session=session, id_order=id)

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@router.post("/order", response_model=OrderSchema)
async def insert_order(order: OrderSchema) -> OrderSchema:
    order_repo = OrderRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await order_repo.check_connection(session=session)
        new_order = await order_repo.insert_order(session=session, **order.dict())

    if not new_order:
        raise HTTPException(status_code=500, detail="Failed to insert order")

    return new_order


@router.put("/order/{id}", response_model=OrderSchema)
async def update_order(id: int, order: OrderSchema) -> OrderSchema:
    order_repo = OrderRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await order_repo.check_connection(session=session)
        updated_order = await order_repo.update_order_by_id(session=session, id_order=id, **order.dict())

    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found or failed to update")

    return updated_order


@router.delete("/order/{id}", response_model=dict)
async def delete_order(id: int) -> dict:
    order_repo = OrderRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await order_repo.check_connection(session=session)
        deleted = await order_repo.delete_order_by_id(session=session, id_order=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Order not found or failed to delete")

    return {"message": "Order deleted successfully"}


# Cooks CRUD

@router.get("/all_cooks", response_model=list[CookSchema])
async def get_all_cooks() -> list[CookSchema]:
    cook_repo = CookRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await cook_repo.check_connection(session=session)
        all_cooks = await cook_repo.get_all_cooks(session=session)

    return all_cooks


@router.get("/cook/{id}", response_model=CookSchema)
async def get_cook_by_id(id: int) -> CookSchema:
    cook_repo = CookRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await cook_repo.check_connection(session=session)
        cook = await cook_repo.get_cook_by_id(session=session, id_cook=id)

    if not cook:
        raise HTTPException(status_code=404, detail="Cook not found")

    return cook


@router.post("/cook", response_model=CookSchema)
async def insert_cook(cook: CookSchema) -> CookSchema:
    cook_repo = CookRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await cook_repo.check_connection(session=session)
        new_cook = await cook_repo.insert_cook(session=session, **cook.dict())

    if not new_cook:
        raise HTTPException(status_code=500, detail="Failed to insert cook")

    return new_cook


@router.put("/cook/{id}", response_model=CookSchema)
async def update_cook(id: int, cook: CookSchema) -> CookSchema:
    cook_repo = CookRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await cook_repo.check_connection(session=session)
        updated_cook = await cook_repo.update_cook_by_id(session=session, id_cook=id, **cook.dict())

    if not updated_cook:
        raise HTTPException(status_code=404, detail="Cook not found or failed to update")

    return updated_cook


@router.delete("/cook/{id}", response_model=dict)
async def delete_cook(id: int) -> dict:
    cook_repo = CookRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await cook_repo.check_connection(session=session)
        deleted = await cook_repo.delete_cook_by_id(session=session, id_cook=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Cook not found or failed to delete")

    return {"message": "Cook deleted successfully"}


# Customers CRUD

@router.get("/all_customers", response_model=list[CustomerSchema])
async def get_all_customers() -> list[CustomerSchema]:
    customer_repo = CustomerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await customer_repo.check_connection(session=session)
        all_customers = await customer_repo.get_all_customers(session=session)

    return all_customers


@router.get("/customer/{id}", response_model=CustomerSchema)
async def get_customer_by_id(id: int) -> CustomerSchema:
    customer_repo = CustomerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await customer_repo.check_connection(session=session)
        customer = await customer_repo.get_customer_by_id(session=session, id_customer=id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    return customer


@router.post("/customer", response_model=CustomerSchema)
async def insert_customer(customer: CustomerSchema) -> CustomerSchema:
    customer_repo = CustomerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await customer_repo.check_connection(session=session)
        new_customer = await customer_repo.insert_customer(session=session, **customer.dict())

    if not new_customer:
        raise HTTPException(status_code=500, detail="Failed to insert customer")

    return new_customer


@router.put("/customer/{id}", response_model=CustomerSchema)
async def update_customer(id: int, customer: CustomerSchema) -> CustomerSchema:
    customer_repo = CustomerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await customer_repo.check_connection(session=session)
        updated_customer = await customer_repo.update_customer_by_id(session=session, id_customer=id, **customer.dict())

    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found or failed to update")

    return updated_customer


@router.delete("/customer/{id}", response_model=dict)
async def delete_customer(id: int) -> dict:
    customer_repo = CustomerRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await customer_repo.check_connection(session=session)
        deleted = await customer_repo.delete_customer_by_id(session=session, id_customer=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found or failed to delete")

    return {"message": "Customer deleted successfully"}


# Waiters CRUD

@router.get("/all_waiters", response_model=list[WaiterSchema])
async def get_all_waiters() -> list[WaiterSchema]:
    waiter_repo = WaiterRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await waiter_repo.check_connection(session=session)
        all_waiters = await waiter_repo.get_all_waiters(session=session)

    return all_waiters


@router.get("/waiter/{id}", response_model=WaiterSchema)
async def get_waiter_by_id(id: int) -> WaiterSchema:
    waiter_repo = WaiterRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await waiter_repo.check_connection(session=session)
        waiter = await waiter_repo.get_waiter_by_id(session=session, id_waiter=id)

    if not waiter:
        raise HTTPException(status_code=404, detail="Waiter not found")

    return waiter


@router.post("/waiter", response_model=WaiterSchema)
async def insert_waiter(waiter: WaiterSchema) -> WaiterSchema:
    waiter_repo = WaiterRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await waiter_repo.check_connection(session=session)
        new_waiter = await waiter_repo.insert_waiter(session=session, **waiter.dict())

    if not new_waiter:
        raise HTTPException(status_code=500, detail="Failed to insert waiter")

    return new_waiter


@router.put("/waiter/{id}", response_model=WaiterSchema)
async def update_waiter(id: int, waiter: WaiterSchema) -> WaiterSchema:
    waiter_repo = WaiterRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await waiter_repo.check_connection(session=session)
        updated_waiter = await waiter_repo.update_waiter_by_id(session=session, id_waiter=id, **waiter.dict())

    if not updated_waiter:
        raise HTTPException(status_code=404, detail="Waiter not found or failed to update")

    return updated_waiter


@router.delete("/waiter/{id}", response_model=dict)
async def delete_waiter(id: int) -> dict:
    waiter_repo = WaiterRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await waiter_repo.check_connection(session=session)
        deleted = await waiter_repo.delete_waiter_by_id(session=session, id_waiter=id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Waiter not found or failed to delete")

    return {"message": "Waiter deleted successfully"}


# OrderDishCook CRUD

@router.get("/all_order_dish_cook", response_model=list[OrderDishCookSchema])
async def get_all_order_dish_cook() -> list[OrderDishCookSchema]:
    order_dish_cook_repo = OrderDishCookRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await order_dish_cook_repo.check_connection(session=session)
        all_order_dish_cook = await order_dish_cook_repo.get_all_entries(session=session)

    return all_order_dish_cook


@router.get("/order_dish_cook/{id_order}/{id_dish}", response_model=OrderDishCookSchema)
async def get_order_dish_cook_by_id(id_order: int, id_dish: int) -> OrderDishCookSchema:
    order_dish_cook_repo = OrderDishCookRepository()
    database = PostgresDatabase()

    async with database.session() as session:
        await order_dish_cook_repo.check_connection(session=session)
        order_dish_cook = await order_dish_cook_repo.get_order_dish_cook_by_id(session=session, id_order=id_order,
                                                                               id_dish=id_dish)

    if not order_dish_cook:
        raise HTTPException(status_code=404, detail="OrderDishCook not found")

    return order_dish_cook