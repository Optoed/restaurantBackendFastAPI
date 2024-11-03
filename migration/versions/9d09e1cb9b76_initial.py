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


def downgrade():
    # Удаление таблицы для связи между рецептами и продуктами
    op.drop_table('recipe_product', schema=settings.POSTGRES_SCHEMA)

    # Удаление таблицы recipe
    op.drop_table('recipe', schema=settings.POSTGRES_SCHEMA)

    # Удаление таблицы product
    op.drop_table('product', schema=settings.POSTGRES_SCHEMA)