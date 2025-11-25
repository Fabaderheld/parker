from sqlalchemy.orm import Session
from typing import Optional
from app.models.collection import Collection, CollectionItem
from app.models.comic import Comic


class CollectionService:
    """Service for managing collections"""

    def __init__(self, db: Session):
        self.db = db

    def get_or_create_collection(self, name: str) -> Collection:
        """Get existing collection or create new one"""
        name = name.strip()
        collection = self.db.query(Collection).filter(Collection.name == name).first()

        if not collection:
            collection = Collection(name=name, auto_generated=1)
            self.db.add(collection)
            self.db.commit()
            self.db.refresh(collection)
            print(f"Created collection: {name}")

        return collection

    def add_comic_to_collection(self, comic: Comic, collection_name: str):
        """Add a comic to a collection"""
        collection = self.get_or_create_collection(collection_name)

        # Check if comic already in this collection
        existing = self.db.query(CollectionItem).filter(
            CollectionItem.collection_id == collection.id,
            CollectionItem.comic_id == comic.id
        ).first()

        if not existing:
            # Create new item
            item = CollectionItem(
                collection_id=collection.id,
                comic_id=comic.id
            )
            self.db.add(item)
            self.db.commit()
            print(f"Added {comic.filename} to collection '{collection_name}'")

    def remove_comic_from_all_collections(self, comic_id: int):
        """Remove a comic from all collections"""
        self.db.query(CollectionItem).filter(
            CollectionItem.comic_id == comic_id
        ).delete()
        self.db.commit()

    def update_comic_collections(self, comic: Comic, series_group: Optional[str]):
        """Update a comic's collection membership based on SeriesGroup tag"""
        # First, remove from all auto-generated collections
        self.remove_comic_from_all_collections(comic.id)

        # If comic has SeriesGroup, add to that collection
        if series_group:
            self.add_comic_to_collection(comic, series_group)

    def cleanup_empty_collections(self):
        """Remove collections that have no items"""
        empty_collections = self.db.query(Collection).filter(
            ~Collection.items.any()
        ).all()

        for collection in empty_collections:
            print(f"Removing empty collection: {collection.name}")
            self.db.delete(collection)

        if empty_collections:
            self.db.commit()