from sqlalchemy import (
    Column,
    Integer,
    String,
    ARRAY,
    ForeignKey,
    TIMESTAMP,
    func,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()


class StatusEnum(enum.Enum):
    liked = "liked"
    loved = "loved"
    disliked = "disliked"
    strongly_disliked = "strongly_disliked"
    to_watch = "to_watch"


class CinemaPreference(Base):
    __tablename__ = "cinema_preferences"
    __table_args__ = (
        CheckConstraint(
            "(status = 'liked' OR status = 'loved' OR status = 'disliked' OR status = 'strongly_disliked' OR status = 'to_watch')",
            name="status_check",
        ),
        {"schema": "public"},
    )
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("auth.users.id"), nullable=False)
    title = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    type = Column(String, nullable=False)
    genre = Column(ARRAY(String), nullable=False)
    status = Column(String, nullable=False)  # Now a string
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="preferences")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if self.status not in [status.value for status in StatusEnum]:
            raise ValueError(f"Invalid status: {self.status}")


class User(Base):
    __tablename__ = "users"
    __table_args__ = {"schema": "auth"}
    id = Column(UUID(as_uuid=True), primary_key=True)
    preferences = relationship("CinemaPreference", back_populates="user")
