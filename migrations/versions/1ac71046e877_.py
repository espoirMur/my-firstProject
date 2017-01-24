"""empty message

Revision ID: 1ac71046e877
Revises: 81d86e8aa2b7
Create Date: 2017-01-24 15:31:40.518514

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '1ac71046e877'
down_revision = '81d86e8aa2b7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('company', sa.Column('country', sa.String(length=64), nullable=True))
    op.drop_index('country', table_name='employee')
    op.drop_column('employee', 'country')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('employee', sa.Column('country', mysql.VARCHAR(length=64), nullable=True))
    op.create_index('country', 'employee', ['country'], unique=True)
    op.drop_column('company', 'country')
    # ### end Alembic commands ###