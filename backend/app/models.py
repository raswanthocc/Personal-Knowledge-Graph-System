from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Text, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from backend.app.database import Base

class Note(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Text, nullable=False, unique=True, index=True)
    content = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, default=lambda: datetime.now(timezone.utc))

    # Relationships
    note_tags = relationship("NoteTag", back_populates="note", cascade="all, delete-orphan")
    outgoing_links = relationship(
        "Link",
        foreign_keys="[Link.source_id]",
        back_populates="source_note",
        cascade="all, delete-orphan"
    )
    incoming_links = relationship(
        "Link",
        foreign_keys="[Link.target_id]",
        back_populates="target_note",
        cascade="all, delete-orphan"
    )


class Link(Base):
    __tablename__ = "links"

    source_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True)
    target_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True)

    source_note = relationship("Note", foreign_keys=[source_id], back_populates="outgoing_links")
    target_note = relationship("Note", foreign_keys=[target_id], back_populates="incoming_links")


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, unique=True, index=True)

    note_tags = relationship("NoteTag", back_populates="tag", cascade="all, delete-orphan")


class NoteTag(Base):
    __tablename__ = "note_tags"

    note_id = Column(Integer, ForeignKey("notes.id", ondelete="CASCADE"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)

    note = relationship("Note", back_populates="note_tags")
    tag = relationship("Tag", back_populates="note_tags")
