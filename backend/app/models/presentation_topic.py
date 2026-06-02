from sqlalchemy import ForeignKey, Table, Column

from app.core.database import Base

presentation_topics = Table(
    "presentation_topics",
    Base.metadata,
    Column("presentation_id", ForeignKey("presentations.id", ondelete="CASCADE"), primary_key=True),
    Column("topic_id", ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True),
)