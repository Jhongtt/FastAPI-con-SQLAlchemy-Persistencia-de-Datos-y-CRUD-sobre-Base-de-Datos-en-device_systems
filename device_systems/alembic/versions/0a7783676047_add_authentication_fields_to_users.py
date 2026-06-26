"""add authentication fields to users

Revision ID: 0a7783676047
Revises: d9ec828751f8
Create Date: 2026-06-25 10:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0a7783676047'
down_revision: Union[str, Sequence[str], None] = 'd9ec828751f8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('hashed_password', sa.String(length=255), nullable=False, server_default=''))


def downgrade() -> None:
    op.drop_column('users', 'hashed_password')
