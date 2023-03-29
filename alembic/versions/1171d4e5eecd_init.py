"""init

Revision ID: 1171d4e5eecd
Revises: 
Create Date: 2023-03-28 11:00:18.020275

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1171d4e5eecd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String),
        sa.Column('email', sa.String, unique=True),
        sa.Column('password', sa.String)
    )


def downgrade() -> None:
    op.drop_table('user')
