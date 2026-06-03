"""add_indexes

Revision ID: c4a82f1d3e57
Revises: b93082b6384d
Create Date: 2026-06-03 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


revision: str = 'c4a82f1d3e57'
down_revision: Union[str, Sequence[str], None] = 'b93082b6384d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index('ix_sessions_conference_id', 'sessions', ['conference_id'])
    op.create_index('ix_sessions_source_session_id', 'sessions', ['source_session_id'])
    op.create_index('ix_sessions_start_time', 'sessions', ['start_time'])

    op.create_index('ix_presentations_conference_id', 'presentations', ['conference_id'])
    op.create_index('ix_presentations_session_id', 'presentations', ['session_id'])
    op.create_index('ix_presentations_source_presentation_id', 'presentations', ['source_presentation_id'])
    op.create_index('ix_presentations_source_content_id', 'presentations', ['source_content_id'])
    op.create_index('ix_presentations_presentation_number', 'presentations', ['presentation_number'])
    op.create_index('ix_presentations_abstract_number', 'presentations', ['abstract_number'])
    op.create_index('ix_presentations_doi', 'presentations', ['doi'])
    op.create_index('ix_presentations_clinical_trial_registry_number', 'presentations', ['clinical_trial_registry_number'])
    op.create_index('ix_presentations_start_time', 'presentations', ['start_time'])
    op.create_index('ix_presentations_summary_status', 'presentations', ['summary_status'])

    op.create_index('ix_presentation_authors_presentation_id', 'presentation_authors', ['presentation_id'])
    op.create_index('ix_presentation_authors_normalized_name', 'presentation_authors', ['normalized_name'])
    op.create_index('ix_presentation_authors_organization', 'presentation_authors', ['organization'])
    op.create_index('ix_presentation_authors_author_order', 'presentation_authors', ['author_order'])
    op.create_index('ix_presentation_authors_is_first_author', 'presentation_authors', ['is_first_author'])
    op.create_index('ix_presentation_authors_is_presenter', 'presentation_authors', ['is_presenter'])

    op.create_index('ix_attachments_presentation_id', 'attachments', ['presentation_id'])
    op.create_index('ix_attachments_preview_status', 'attachments', ['preview_status'])
    op.create_index('ix_attachments_content_type', 'attachments', ['content_type'])

    op.create_index('ix_comments_presentation_id', 'comments', ['presentation_id'])
    op.create_index('ix_comments_created_at', 'comments', ['created_at'])

    op.create_index('ix_annotations_presentation_id', 'annotations', ['presentation_id'])
    op.create_index('ix_annotations_attachment_id', 'annotations', ['attachment_id'])
    op.create_index('ix_annotations_created_at', 'annotations', ['created_at'])


def downgrade() -> None:
    op.drop_index('ix_annotations_created_at', table_name='annotations')
    op.drop_index('ix_annotations_attachment_id', table_name='annotations')
    op.drop_index('ix_annotations_presentation_id', table_name='annotations')

    op.drop_index('ix_comments_created_at', table_name='comments')
    op.drop_index('ix_comments_presentation_id', table_name='comments')

    op.drop_index('ix_attachments_content_type', table_name='attachments')
    op.drop_index('ix_attachments_preview_status', table_name='attachments')
    op.drop_index('ix_attachments_presentation_id', table_name='attachments')

    op.drop_index('ix_presentation_authors_is_presenter', table_name='presentation_authors')
    op.drop_index('ix_presentation_authors_is_first_author', table_name='presentation_authors')
    op.drop_index('ix_presentation_authors_author_order', table_name='presentation_authors')
    op.drop_index('ix_presentation_authors_organization', table_name='presentation_authors')
    op.drop_index('ix_presentation_authors_normalized_name', table_name='presentation_authors')
    op.drop_index('ix_presentation_authors_presentation_id', table_name='presentation_authors')

    op.drop_index('ix_presentations_summary_status', table_name='presentations')
    op.drop_index('ix_presentations_start_time', table_name='presentations')
    op.drop_index('ix_presentations_clinical_trial_registry_number', table_name='presentations')
    op.drop_index('ix_presentations_doi', table_name='presentations')
    op.drop_index('ix_presentations_abstract_number', table_name='presentations')
    op.drop_index('ix_presentations_presentation_number', table_name='presentations')
    op.drop_index('ix_presentations_source_content_id', table_name='presentations')
    op.drop_index('ix_presentations_source_presentation_id', table_name='presentations')
    op.drop_index('ix_presentations_session_id', table_name='presentations')
    op.drop_index('ix_presentations_conference_id', table_name='presentations')

    op.drop_index('ix_sessions_start_time', table_name='sessions')
    op.drop_index('ix_sessions_source_session_id', table_name='sessions')
    op.drop_index('ix_sessions_conference_id', table_name='sessions')