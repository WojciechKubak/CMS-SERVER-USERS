"""user_table

Revision ID: 460e56e09103
Revises: 
Create Date: 2023-10-31 10:31:36.286973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '460e56e09103'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(20)),
        sa.Column('email', sa.String(255)),
        sa.Column('password', sa.String(255)),
        sa.Column('is_active', sa.Boolean()),
        sa.Column('role', sa.Enum('user', 'redactor', 'translator', 'admin', name='user_role'), nullable=False),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )


def downgrade() -> None:
    op.drop_table('users')
