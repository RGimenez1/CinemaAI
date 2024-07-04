from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from typing import List, Literal
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
from sqlalchemy.dialects.postgresql import UUID as SQLUUID
from sqlalchemy.orm import relationship, declarative_base
from app.domain.value_objects.status_enum import StatusEnum

Base = declarative_base()


class CinemaPreferenceCreate(BaseModel):
    user_id: UUID
    title: str
    year: int
    type: Literal["movie", "series"]
    genre: List[str]
    status: str = Field(...)

    @field_validator("status")
    def validate_status(cls, v):
        if v not in [status.value for status in StatusEnum]:
            raise ValueError(f"Invalid status: {v}")
        return v


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
    user_id = Column(SQLUUID(as_uuid=True), ForeignKey("auth.users.id"), nullable=False)
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
    id = Column(SQLUUID(as_uuid=True), primary_key=True)
    preferences = relationship("CinemaPreference", back_populates="user")
