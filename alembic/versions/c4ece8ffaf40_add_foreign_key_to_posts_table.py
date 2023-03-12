"""add foreign key to posts table

Revision ID: c4ece8ffaf40
Revises: 6d8a3835febb
Create Date: 2023-03-11 15:44:16.369416

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4ece8ffaf40'
down_revision = '6d8a3835febb'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key('posts_users_fk', source_table = "posts", referent_table = "users" , local_cols = ['owner_id'], remote_cols = ['id'], ondelete = "CASCADE")
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name = "posts")
    op.drop_column('posts', 'owner_id')
    pass
