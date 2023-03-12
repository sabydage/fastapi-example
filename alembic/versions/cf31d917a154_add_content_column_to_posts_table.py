"""add content column to posts table

Revision ID: cf31d917a154
Revises: c891dc50f51d
Create Date: 2023-03-11 12:39:03.794513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf31d917a154'
down_revision = 'c891dc50f51d'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content',sa.String(), nullable = False))
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
