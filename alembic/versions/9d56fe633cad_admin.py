"""admin

Revision ID: 9d56fe633cad
Revises: 1171d4e5eecd
Create Date: 2023-03-29 11:56:39.573519

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d56fe633cad'
down_revision = '1171d4e5eecd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'admin',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer),
    )


def downgrade() -> None:
    op.drop_table('admin')
