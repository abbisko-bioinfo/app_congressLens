from sqlalchemy import String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base, UUIDMixin, TimestampMixin


class Topic(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "topics"
    __table_args__ = (UniqueConstraint("normalized_name", "type", name="uq_topic_normalized_name_type"),)

    name: Mapped[str] = mapped_column(String(500), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(500), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)