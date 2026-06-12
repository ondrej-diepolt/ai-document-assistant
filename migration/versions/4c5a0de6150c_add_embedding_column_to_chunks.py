"""add embedding column to chunks

Revision ID: 4c5a0de6150c
Revises: 33f98fe2401d
Create Date: 2026-06-12 17:58:48.747708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = '4c5a0de6150c'
down_revision: Union[str, Sequence[str], None] = '33f98fe2401d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.add_column('chunks', sa.Column('embedding', Vector(384), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('chunks', 'embedding')