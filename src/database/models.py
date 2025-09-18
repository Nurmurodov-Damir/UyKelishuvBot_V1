"""
UyKelishuv Bot Database Models
"""
import uuid
from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, String, Integer, Float, Boolean, DateTime, Text, 
    ForeignKey, Enum, Numeric, BigInteger
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class ListingType(enum.Enum):
    """E'lon turlari"""
    ijara = "ijara"
    sotuv = "sotuv"


class PropertyType(enum.Enum):
    """Uy turlari"""
    kvartira = "kvartira"
    uy = "uy"
    ofis = "ofis"


class ListingStatus(enum.Enum):
    """E'lon holatlari"""
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    archived = "archived"


class User(Base):
    """Foydalanuvchi modeli"""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    telegram_user_id = Column(BigInteger, unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    phone_number = Column(String(20), unique=True, nullable=True)
    locale = Column(String(10), default="uz", nullable=False)
    verified = Column(Boolean, default=False, nullable=False)
    blocked = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    listings = relationship("Listing", back_populates="owner")


class Listing(Base):
    """E'lon modeli"""
    __tablename__ = "listings"
    
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    
    # Location
    region_code = Column(String(2), nullable=False)
    city_name = Column(String(100), nullable=False)
    address = Column(Text, nullable=True)
    
    # Property details
    type = Column(Enum(ListingType), nullable=False)
    property_type = Column(Enum(PropertyType), nullable=True)  # Kvartira, Uy, Ofis
    rooms = Column(Integer, nullable=False)
    area_m2 = Column(Float, nullable=True)
    floor = Column(Integer, nullable=True)
    total_floors = Column(Integer, nullable=True)
    
    # Pricing
    price = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    
    # Features
    furnished = Column(Boolean, default=False)
    pets_allowed = Column(Boolean, default=False)
    
    # Content
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    media_urls = Column(Text, nullable=True)
    
    # Statistics
    views_count = Column(Integer, default=0, nullable=False)
    contacts_count = Column(Integer, default=0, nullable=False)
    
    # Status
    status = Column(Enum(ListingStatus), default=ListingStatus.pending, nullable=False)
    rejection_reason = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)
    
    # Relationships
    owner = relationship("User", back_populates="listings", foreign_keys=[user_id])