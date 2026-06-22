"""crear tablas users, devices y loans

Revision ID: d9ec828751f8
Revises: 
Create Date: 2026-06-19 19:01:40.405931

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd9ec828751f8'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('role', sa.String(length=20), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('devices',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('serial_number', sa.String(length=50), nullable=False),
    sa.Column('device_type', sa.String(length=30), nullable=False),
    sa.Column('brand', sa.String(length=50), nullable=True),
    sa.Column('is_available', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('serial_number')
    )
    op.create_table('loans',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('device_id', sa.Integer(), nullable=False),
    sa.Column('loan_date', sa.DateTime(), nullable=True),
    sa.Column('return_date', sa.DateTime(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=False),
    sa.ForeignKeyConstraint(['device_id'], ['devices.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('loans')
    op.drop_table('devices')
    op.drop_table('users')
