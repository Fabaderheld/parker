from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

# Import the junction tables
from app.models.tags import comic_characters, comic_teams, comic_locations

class Volume(Base):
    __tablename__ = "volumes"

    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey("series.id"))
    volume_number = Column(Integer, default=1)

    series = relationship("Series", back_populates="volumes")
    comics = relationship("Comic", back_populates="volume", cascade="all, delete-orphan")


class Comic(Base):
    __tablename__ = "comics"

    id = Column(Integer, primary_key=True, index=True)
    volume_id = Column(Integer, ForeignKey("volumes.id"))

    filename = Column(String, nullable=False)
    file_path = Column(String, unique=True, nullable=False)
    file_modified_at = Column(Float)
    page_count = Column(Integer, default=0)

    # Basic metadata
    number = Column(String)
    title = Column(String)
    summary = Column(Text)
    year = Column(Integer)
    month = Column(Integer)
    day = Column(Integer)

    # Credits
    writer = Column(String)
    penciller = Column(String)
    inker = Column(String)
    colorist = Column(String)
    letterer = Column(String)
    cover_artist = Column(String)
    editor = Column(String)

    # Publishing info
    publisher = Column(String)
    imprint = Column(String)
    format = Column(String)  # e.g., "Limited Series", "Ongoing", etc.
    series_group = Column(String)

    # Scan info
    scan_information = Column(String)

    # Many-to-many relationships for tags
    characters = relationship("Character", secondary=comic_characters, back_populates="comics")
    teams = relationship("Team", secondary=comic_teams, back_populates="comics")
    locations = relationship("Location", secondary=comic_locations, back_populates="comics")

    # Reading list support
    alternate_series = Column(String)
    alternate_number = Column(String)
    story_arc = Column(String)

    # Store full metadata as JSON for anything we missed
    metadata_json = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    volume = relationship("Volume", back_populates="comics")