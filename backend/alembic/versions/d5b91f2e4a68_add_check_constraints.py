"""add_check_constraints

Revision ID: d5b91f2e4a68
Revises: c4a82f1d3e57
Create Date: 2026-06-03 12:10:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'd5b91f2e4a68'
down_revision: Union[str, Sequence[str], None] = 'c4a82f1d3e57'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        'ck_presentations_summary_status', 'presentations',
        "summary_status IN ('none', 'pending', 'processing', 'ready', 'failed')"
    )
    op.create_check_constraint(
        'ck_topics_type', 'topics',
        "type IN ('topic', 'keyword', 'track', 'subtrack')"
    )
    op.create_check_constraint(
        'ck_attachments_preview_status', 'attachments',
        "preview_status IN ('pending', 'processing', 'ready', 'failed', 'not_supported')"
    )
    op.create_check_constraint(
        'ck_watchlist_target_type', 'watchlist_items',
        "target_type IN ('conference', 'session', 'presentation')"
    )
    op.create_check_constraint(
        'ck_ai_summaries_scope_type', 'ai_summaries',
        "scope_type IN ('presentation', 'session', 'conference')"
    )
    op.create_check_constraint(
        'ck_ai_summaries_status', 'ai_summaries',
        "status IN ('pending', 'processing', 'ready', 'failed')"
    )


def downgrade() -> None:
    op.drop_constraint('ck_ai_summaries_status', 'ai_summaries', type_='check')
    op.drop_constraint('ck_ai_summaries_scope_type', 'ai_summaries', type_='check')
    op.drop_constraint('ck_watchlist_target_type', 'watchlist_items', type_='check')
    op.drop_constraint('ck_attachments_preview_status', 'attachments', type_='check')
    op.drop_constraint('ck_topics_type', 'topics', type_='check')
    op.drop_constraint('ck_presentations_summary_status', 'presentations', type_='check')