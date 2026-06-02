from sqlalchemy import ForeignKey, Table, Column

from app.core.database import Base

session_topics = Table(
    "session_topics",
    Base.metadata,
    Column("session_id", ForeignKey("sessions.id", ondelete="CASCADE"), primary_key=True),
    Column("topic_id", ForeignKey("topics.id", ondelete="CASCADE"), primary_key=True),
)