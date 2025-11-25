from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Collection(Base):
    """A collection of related comics (thematic grouping without specific order)"""
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    description = Column(Text)

    # Track if this was auto-generated from SeriesGroup
    auto_generated = Column(Integer, default=1)  # SQLite uses 1/0 for boolean

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship to items (no ordering needed)
    items = relationship("CollectionItem", back_populates="collection", cascade="all, delete-orphan")


class CollectionItem(Base):
    """A comic in a collection (no specific order/position)"""
    __tablename__ = "collection_items"

    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(Integer, ForeignKey('collections.id', ondelete='CASCADE'), nullable=False)
    comic_id = Column(Integer, ForeignKey('comics.id', ondelete='CASCADE'), nullable=False)

    # Prevent duplicate comics in same collection
    __table_args__ = (
        UniqueConstraint('collection_id', 'comic_id', name='unique_collection_comic'),
    )

    # Relationships
    collection = relationship("Collection", back_populates="items")
    comic = relationship("Comic", back_populates="collection_items")