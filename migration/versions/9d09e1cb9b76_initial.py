"""initial

Revision ID: 9d09e1cb9b76
Revises: 
Create Date: 2024-10-14 09:33:50.162970

"""
from alembic import op
import sqlalchemy as sa

from src.project.core.config import settings


# revision identifiers, used by Alembic.
revision = '9d09e1cb9b76'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    # Create the 'users' table with a foreign key reference to 'roles'
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False, unique=True),
        sa.Column('role', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], name='fk_users_roles'),
        sa.PrimaryKeyConstraint('id', name='users_pkey'),
        schema=settings.POSTGRES_SCHEMA
    )

    # Создание таблицы product
    op.create_table(
        'product',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
        sa.Column('cost', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema=settings.POSTGRES_SCHEMA
    )

    # Создание таблицы recipe
    op.create_table(
        'recipe',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('time_to_cook', sa.Time(), nullable=False),
        sa.Column('name', sa.String().with_variant(sa.String(length=255), 'postgresql'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema=settings.POSTGRES_SCHEMA
    )

    # Создание таблицы для связи между рецептами и продуктами
    op.create_table(
        'recipe_product',
        sa.Column('id_recipe', sa.Integer(), nullable=False),
        sa.Column('id_product', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['id_recipe'], [f'{settings.POSTGRES_SCHEMA}.recipe.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['id_product'], [f'{settings.POSTGRES_SCHEMA}.product.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id_recipe', 'id_product'),
        schema=settings.POSTGRES_SCHEMA
    )

    # Создание таблицы dish
    op.create_table(
        'dish',
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('id_recipe', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('cost', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Numeric(3, 1), nullable=True),
        sa.ForeignKeyConstraint(['id_recipe'], [f'{settings.POSTGRES_SCHEMA}.recipe.id'], ondelete='CASCADE'),
        schema=settings.POSTGRES_SCHEMA
    )

    # Создание таблицы warehouse
    op.create_table(
        'warehouse',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('location', sa.String(length=255), nullable=False),
        sa.Column('how_full', sa.Numeric(3, 2), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema=settings.POSTGRES_SCHEMA
    )

    # Создание таблицы supplier
    op.create_table(
        'supplier',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('cost', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Numeric(3, 2), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema=settings.POSTGRES_SCHEMA
    )

    # Создание таблицы customer
    op.create_table(
        'customer',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('rating', sa.Numeric(3, 2), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema=settings.POSTGRES_SCHEMA
    )

    # Создание таблицы waiter
    op.create_table(
        'waiter',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('salary', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Numeric(3, 2), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema=settings.POSTGRES_SCHEMA
    )

    # Создание таблицы orders
    op.create_table(
        'orders',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_waiter', sa.Integer(), nullable=False),
        sa.Column('id_customer', sa.Integer(), nullable=False),
        sa.Column('total_cost', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(['id_waiter'], [f'{settings.POSTGRES_SCHEMA}.waiter.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['id_customer'], [f'{settings.POSTGRES_SCHEMA}.customer.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        schema=settings.POSTGRES_SCHEMA
    )


    # Создание таблицы discount
    op.create_table(
        'discount',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_customer', sa.Integer(), nullable=False),
        sa.Column('percentage', sa.Numeric(5, 2), nullable=False),
        sa.Column('expiration_date', sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(['id_customer'], [f'{settings.POSTGRES_SCHEMA}.customer.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        schema=settings.POSTGRES_SCHEMA
    )

    # Создание таблицы cook
    op.create_table(
        'cook',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('post', sa.String(length=100), nullable=False),
        sa.Column('salary', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Numeric(3, 2), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        schema=settings.POSTGRES_SCHEMA
    )

    # Создание таблицы orders_dish_cook
    op.create_table(
        'orders_dish_cook',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_orders', sa.Integer(), nullable=False),
        sa.Column('id_dish', sa.Integer(), nullable=False),
        sa.Column('id_cook', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.ForeignKeyConstraint(['id_orders'], [f'{settings.POSTGRES_SCHEMA}.orders.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['id_dish'], [f'{settings.POSTGRES_SCHEMA}.dish.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['id_cook'], [f'{settings.POSTGRES_SCHEMA}.cook.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        schema=settings.POSTGRES_SCHEMA
    )

    # Создание таблицы batch
    op.create_table(
        'batch',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_supplier', sa.Integer(), nullable=False),
        sa.Column('id_warehouse', sa.Integer(), nullable=False),
        sa.Column('total_cost', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['id_supplier'], [f'{settings.POSTGRES_SCHEMA}.supplier.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['id_warehouse'], [f'{settings.POSTGRES_SCHEMA}.warehouse.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        schema=settings.POSTGRES_SCHEMA
    )

    # Создание таблицы batch_product
    op.create_table(
        'batch_product',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('id_batch', sa.Integer(), nullable=False),
        sa.Column('id_product', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Integer(), nullable=False),
        sa.Column('expiration_date', sa.Date(), nullable=False),
        sa.ForeignKeyConstraint(['id_batch'], [f'{settings.POSTGRES_SCHEMA}.batch.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['id_product'], [f'{settings.POSTGRES_SCHEMA}.product.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        schema=settings.POSTGRES_SCHEMA
    )


def downgrade():
    op.drop_table('users')

    # Удаление таблицы batch_product
    op.drop_table('batch_product', schema=settings.POSTGRES_SCHEMA)

    # Удаление таблицы batch
    op.drop_table('batch', schema=settings.POSTGRES_SCHEMA)

    # Удаление таблицы orders_dish_cook
    op.drop_table('orders_dish_cook', schema=settings.POSTGRES_SCHEMA)

    # Удаление таблицы cook
    op.drop_table('cook', schema=settings.POSTGRES_SCHEMA)

    # Удаление таблицы discount
    op.drop_table('discount', schema=settings.POSTGRES_SCHEMA)

    # Удаление таблицы orders
    op.drop_table('orders', schema=settings.POSTGRES_SCHEMA)

    # Удаление таблицы waiter
    op.drop_table('waiter', schema=settings.POSTGRES_SCHEMA)

    # Удаление таблицы customer
    op.drop_table('customer', schema=settings.POSTGRES_SCHEMA)

    # Удаление таблицы supplier
    op.drop_table('supplier', schema=settings.POSTGRES_SCHEMA)

    # Удаление таблицы warehouse
    op.drop_table('warehouse', schema=settings.POSTGRES_SCHEMA)

    # Удаление таблицы dish
    op.drop_table('dish', schema=settings.POSTGRES_SCHEMA)

    # Удаление таблицы для связи между рецептами и продуктами
    op.drop_table('recipe_product', schema=settings.POSTGRES_SCHEMA)

    # Удаление таблицы recipe
    op.drop_table('recipe', schema=settings.POSTGRES_SCHEMA)

    # Удаление таблицы product
    op.drop_table('product', schema=settings.POSTGRES_SCHEMA)
