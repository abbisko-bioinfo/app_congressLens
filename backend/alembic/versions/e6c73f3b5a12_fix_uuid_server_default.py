"""fix_uuid_server_default

Revision ID: e6c73f3b5a12
Revises: d5b91f2e4a68
Create Date: 2026-06-03 12:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e6c73f3b5a12'
down_revision: Union[str, Sequence[str], None] = 'd5b91f2e4a68'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('watchlist_items', 'id',
                    existing_type=sa.UUID(),
                    server_default=sa.text('gen_random_uuid()'),
                    existing_nullable=False)
    op.alter_column('ai_summaries', 'id',
                    existing_type=sa.UUID(),
                    server_default=sa.text('gen_random_uuid()'),
                    existing_nullable=False)
    op.alter_column('presentation_entities', 'id',
                    existing_type=sa.UUID(),
                    server_default=sa.text('gen_random_uuid()'),
                    existing_nullable=False)


def downgrade() -> None:
    op.alter_column('presentation_entities', 'id',
                    existing_type=sa.UUID(),
                    server_default=None,
                    existing_nullable=False)
    op.alter_column('ai_summaries', 'id',
                    existing_type=sa.UUID(),
                    server_default=None,
                    existing_nullable=False)
    op.alter_column('watchlist_items', 'id',
                    existing_type=sa.UUID(),
                    server_default=None,
                    existing_nullable=False)