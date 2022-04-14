"""Added new column to Orders table to store the status of the order

Revision ID: 3afa430c60a2
Revises: ee455ee4ec6d
Create Date: 2022-04-13 16:25:18.690388

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3afa430c60a2'
down_revision = 'ee455ee4ec6d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('orders', sa.Column('status', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('orders', 'status')
    # ### end Alembic commands ###