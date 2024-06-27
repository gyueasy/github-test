"""Add created_at column to Users

Revision ID: 269282cbecb4
Revises: 
Create Date: 2024-06-26 20:16:08.832395

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '269282cbecb4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('created_at', sa.DateTime(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('created_at')

    # ### end Alembic commands ###
