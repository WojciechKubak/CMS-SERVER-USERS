"""comment_table

Revision ID: 2d27e06db114
Revises: 460e56e09103
Create Date: 2023-11-19 20:12:51.421513

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d27e06db114'
down_revision: Union[str, None] = '460e56e09103'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'comments',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('content', sa.String(1000)),
        sa.Column('article_id', sa.Integer()),
        sa.Column('user_id', sa.Integer()),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.Column('created_at', sa.DateTime()),
        sa.Column('updated_at', sa.DateTime()),
    )


def downgrade() -> None:
    op.drop_table('comments')
