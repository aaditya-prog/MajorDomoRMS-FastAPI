"""Update Db

Revision ID: b6235cb21250
Revises: 
Create Date: 2022-04-19 15:05:37.245202

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b6235cb21250'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('inventory',
    sa.Column('item_id', sa.Integer(), nullable=False),
    sa.Column('item_name', sa.String(), nullable=True),
    sa.Column('item_category', sa.String(), nullable=True),
    sa.Column('item_price', sa.Float(), nullable=True),
    sa.Column('item_quantity', sa.String(), nullable=True),
    sa.Column('check_in', sa.String(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('item_id')
    )
    op.create_index(op.f('ix_inventory_item_id'), 'inventory', ['item_id'], unique=False)
    op.create_index(op.f('ix_inventory_item_name'), 'inventory', ['item_name'], unique=True)
    op.create_table('menu',
    sa.Column('food_id', sa.Integer(), nullable=False),
    sa.Column('food_name', sa.String(), nullable=True),
    sa.Column('food_category', sa.String(), nullable=True),
    sa.Column('food_price', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('food_id')
    )
    op.create_index(op.f('ix_menu_food_id'), 'menu', ['food_id'], unique=False)
    op.create_index(op.f('ix_menu_food_name'), 'menu', ['food_name'], unique=True)
    op.create_table('orders',
    sa.Column('order_id', sa.Integer(), nullable=False),
    sa.Column('items', sa.JSON(), nullable=False),
    sa.Column('order_date', sa.Date(), server_default=sa.text('now()'), nullable=True),
    sa.Column('table', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('order_id')
    )
    op.create_index(op.f('ix_orders_order_id'), 'orders', ['order_id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('full_name', sa.String(), nullable=True),
    sa.Column('password', sa.String(), nullable=True),
    sa.Column('staff', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_full_name'), 'users', ['full_name'], unique=False)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_full_name'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_orders_order_id'), table_name='orders')
    op.drop_table('orders')
    op.drop_index(op.f('ix_menu_food_name'), table_name='menu')
    op.drop_index(op.f('ix_menu_food_id'), table_name='menu')
    op.drop_table('menu')
    op.drop_index(op.f('ix_inventory_item_name'), table_name='inventory')
    op.drop_index(op.f('ix_inventory_item_id'), table_name='inventory')
    op.drop_table('inventory')
    # ### end Alembic commands ###
