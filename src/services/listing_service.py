"""
Listing Service - E'lonlar bilan bog'liq operatsiyalar
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload
from src.database.models import Listing, User, ListingType, ListingStatus, PropertyType


class ListingService:
    """E'lon xizmatlari"""
    
    def __init__(self, db: Optional[AsyncSession] = None):
        self.db = db
    
    async def create_listing(self, user_id: str, listing_data: dict) -> Optional[Listing]:
        """Yangi e'lon yaratish"""
        try:
            listing = Listing(
                user_id=user_id,
                region_code=listing_data.get('region_code'),
                city_name=listing_data.get('city_name'),
                address=listing_data.get('address'),
                type=ListingType(listing_data.get('type')),
                property_type=PropertyType(listing_data.get('property_type')) if listing_data.get('property_type') else None,
                rooms=listing_data.get('rooms'),
                area_m2=listing_data.get('area_m2'),
                floor=listing_data.get('floor'),
                total_floors=listing_data.get('total_floors'),
                price=listing_data.get('price'),
                currency=listing_data.get('currency', 'USD'),
                furnished=listing_data.get('furnished', False),
                pets_allowed=listing_data.get('pets_allowed', False),
                title=listing_data.get('title'),
                description=listing_data.get('description'),
                media_urls=listing_data.get('media_urls'),
                status=ListingStatus.pending
            )
            
            self.db.add(listing)
            await self.db.commit()
            await self.db.refresh(listing)
            return listing
        except Exception as e:
            await self.db.rollback()
            raise
    
    async def get_listing_by_id(self, listing_id: str) -> Optional[Listing]:
        """ID orqali e'lonni topish"""
        try:
            result = await self.db.execute(
                select(Listing)
                .options(selectinload(Listing.owner))
                .where(Listing.id == listing_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            if self.db:
                await self.db.rollback()
            raise
    
    async def get_user_listings(self, user_id: str) -> List[Listing]:
        """Foydalanuvchining e'lonlarini olish"""
        try:
            result = await self.db.execute(
                select(Listing)
                .where(Listing.user_id == user_id)
                .order_by(Listing.created_at.desc())
            )
            return result.scalars().all()
        except Exception as e:
            if self.db:
                await self.db.rollback()
            raise
    
    async def update_listing(self, listing_id: str, update_data: dict) -> Optional[Listing]:
        """E'lonni yangilash"""
        try:
            result = await self.db.execute(
                update(Listing)
                .where(Listing.id == listing_id)
                .values(**update_data)
            )
            
            if result.rowcount > 0:
                await self.db.commit()
                return await self.get_listing_by_id(listing_id)
            return None
        except Exception as e:
            await self.db.rollback()
            raise
    
    async def delete_listing(self, listing_id: str) -> bool:
        """E'lonni o'chirish"""
        try:
            result = await self.db.execute(
                delete(Listing).where(Listing.id == listing_id)
            )
            
            if result.rowcount > 0:
                await self.db.commit()
                return True
            return False
        except Exception as e:
            await self.db.rollback()
            raise
    
    async def search_listings(self, filters: dict) -> List[Listing]:
        """E'lonlarni qidirish"""
        try:
            query = select(Listing).options(selectinload(Listing.owner))
            
            if filters.get('region_code'):
                query = query.where(Listing.region_code == filters['region_code'])
            
            if filters.get('city_name'):
                query = query.where(Listing.city_name == filters['city_name'])
            
            if filters.get('type'):
                query = query.where(Listing.type == ListingType(filters['type']))
            
            if filters.get('property_type'):
                query = query.where(Listing.property_type == PropertyType(filters['property_type']))
            
            if filters.get('rooms'):
                # rooms ni integer ga aylantirish
                rooms_value = int(filters['rooms']) if filters['rooms'].isdigit() else None
                if rooms_value:
                    query = query.where(Listing.rooms == rooms_value)
            
            if filters.get('min_price'):
                query = query.where(Listing.price >= filters['min_price'])
            
            if filters.get('max_price'):
                query = query.where(Listing.price <= filters['max_price'])
            
            if filters.get('furnished') is not None:
                query = query.where(Listing.furnished == filters['furnished'])
            
            if filters.get('pets_allowed') is not None:
                query = query.where(Listing.pets_allowed == filters['pets_allowed'])
            
            query = query.where(Listing.status == ListingStatus.approved)
            query = query.order_by(Listing.price.asc())  # Arzon narxlar yuqorida
            
            result = await self.db.execute(query)
            return result.scalars().all()
        except Exception as e:
            if self.db:
                await self.db.rollback()
            raise

