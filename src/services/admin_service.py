"""
Admin Service - Admin panel operatsiyalari
"""
import logging
from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from sqlalchemy.orm import selectinload
from src.database.models import User, Listing, ListingStatus, ListingType
from src.config import settings

logger = logging.getLogger(__name__)


class AdminService:
    """Admin xizmatlari"""
    
    def __init__(self, db: Optional[AsyncSession] = None):
        self.db = db
    
    def is_admin(self, user_id: int) -> bool:
        """
        Foydalanuvchi admin ekanligini tekshirish
        
        Args:
            user_id: Telegram user ID
            
        Returns:
            bool: Admin bo'lsa True
        """
        try:
            # Admin ID larni olish
            admin_ids_str = settings.admin_ids.strip()
            if not admin_ids_str:
                logger.warning("Admin IDs not configured, using default admin")
                return user_id == 924016177
            
            # Admin ID larni list ga aylantirish
            admin_ids = [int(admin_id.strip()) for admin_id in admin_ids_str.split(',') if admin_id.strip()]
            
            # Debug uchun log
            logger.info(f"Checking admin access for user {user_id}, admin IDs: {admin_ids}")
            
            return user_id in admin_ids
        except Exception as e:
            logger.error(f"Error checking admin status: {e}")
            # Fallback: check if user ID is the default admin
            return user_id == 924016177
    
    async def approve_listing(self, listing_id: str, admin_user_id: int) -> Optional[Listing]:
        """
        E'lonni tasdiqlash
        
        Args:
            listing_id: E'lon ID
            admin_user_id: Admin user ID
            
        Returns:
            Listing: Tasdiqlangan e'lon yoki None
        """
        try:
            # E'lonni topish
            result = await self.db.execute(
                select(Listing)
                .options(selectinload(Listing.owner))
                .where(Listing.id == listing_id)
            )
            listing = result.scalar_one_or_none()
            
            if not listing:
                logger.warning(f"Listing not found: {listing_id}")
                return None
            
            # Status ni yangilash
            await self.db.execute(
                update(Listing)
                .where(Listing.id == listing_id)
                .values(
                    status=ListingStatus.approved,
                    approved_at=func.now()
                )
            )
            
            await self.db.commit()
            await self.db.refresh(listing)
            
            logger.info(f"Listing {listing_id} approved by admin {admin_user_id}")
            return listing
            
        except Exception as e:
            logger.error(f"Error approving listing {listing_id}: {e}")
            await self.db.rollback()
            raise
    
    async def reject_listing(self, listing_id: str, admin_user_id: int, reason: str = None) -> Optional[Listing]:
        """
        E'lonni rad etish
        
        Args:
            listing_id: E'lon ID
            admin_user_id: Admin user ID
            reason: Rad etish sababi
            
        Returns:
            Listing: Rad etilgan e'lon yoki None
        """
        try:
            # E'lonni topish
            result = await self.db.execute(
                select(Listing)
                .options(selectinload(Listing.owner))
                .where(Listing.id == listing_id)
            )
            listing = result.scalar_one_or_none()
            
            if not listing:
                logger.warning(f"Listing not found: {listing_id}")
                return None
            
            # Status ni yangilash
            await self.db.execute(
                update(Listing)
                .where(Listing.id == listing_id)
                .values(
                    status=ListingStatus.rejected,
                    rejected_at=func.now(),
                    rejection_reason=reason
                )
            )
            
            await self.db.commit()
            await self.db.refresh(listing)
            
            logger.info(f"Listing {listing_id} rejected by admin {admin_user_id}, reason: {reason}")
            return listing
            
        except Exception as e:
            logger.error(f"Error rejecting listing {listing_id}: {e}")
            await self.db.rollback()
            raise
    
    async def get_pending_listings(self) -> List[Listing]:
        """
        Tasdiqlanmagan e'lonlarni olish
        
        Returns:
            List[Listing]: Pending e'lonlar ro'yxati
        """
        try:
            result = await self.db.execute(
                select(Listing)
                .options(selectinload(Listing.owner))
                .where(Listing.status == ListingStatus.pending)
                .order_by(Listing.created_at.desc())
            )
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Failed to get pending listings: {e}")
            return []
    
    async def get_all_listings(self, status: Optional[ListingStatus] = None) -> List[Listing]:
        """
        Barcha e'lonlarni olish
        
        Args:
            status: E'lon statusi filter
            
        Returns:
            List[Listing]: E'lonlar ro'yxati
        """
        try:
            query = select(Listing).options(selectinload(Listing.owner))
            
            if status:
                query = query.where(Listing.status == status)
            
            query = query.order_by(Listing.created_at.desc())
            
            result = await self.db.execute(query)
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Failed to get all listings: {e}")
            return []
    
    
    async def get_new_listings_count(self) -> int:
        """Yangi e'lonlar sonini olish"""
        try:
            query = select(func.count(Listing.id)).where(
                Listing.status == ListingStatus.pending
            )
            result = await self.db.execute(query)
            return result.scalar() or 0
            
        except Exception as e:
            logger.error(f"Error getting new listings count: {e}")
            return 0
    
    async def get_approved_listings(self) -> List[Listing]:
        """
        Tasdiqlangan e'lonlarni olish
        
        Returns:
            List[Listing]: Tasdiqlangan e'lonlar ro'yxati
        """
        try:
            from sqlalchemy.orm import selectinload
            query = select(Listing).options(selectinload(Listing.owner)).where(Listing.status == ListingStatus.approved).order_by(Listing.created_at.desc())
            result = await self.db.execute(query)
            return result.scalars().all()
        except Exception as e:
            logger.error(f"Failed to get approved listings: {e}")
            return []
    
    async def approve_listing(self, listing_id: str, admin_id: int) -> bool:
        """
        E'lonni tasdiqlash
        
        Args:
            listing_id: E'lon ID
            admin_id: Admin ID
            
        Returns:
            bool: Muvaffaqiyat holati
        """
        try:
            # Check if user is admin
            if not self.is_admin(admin_id):
                logger.warning(f"Non-admin user {admin_id} tried to approve listing {listing_id}")
                return False
            
            # Update listing status
            result = await self.db.execute(
                update(Listing)
                .where(Listing.id == listing_id)
                .values(
                    status=ListingStatus.approved,
                    approved_at=func.now()
                )
            )
            
            await self.db.commit()
            
            if result.rowcount > 0:
                logger.info(f"Listing {listing_id} approved by admin {admin_id}")
                return True
            else:
                logger.warning(f"Listing {listing_id} not found for approval")
                return False
                
        except Exception as e:
            logger.error(f"Failed to approve listing {listing_id}: {e}")
            await self.db.rollback()
            return False
    
    async def reject_listing(self, listing_id: str, admin_id: int, reason: str = None) -> bool:
        """
        E'lonni rad etish
        
        Args:
            listing_id: E'lon ID
            admin_id: Admin ID
            reason: Rad etish sababi
            
        Returns:
            bool: Muvaffaqiyat holati
        """
        try:
            # Check if user is admin
            if not self.is_admin(admin_id):
                logger.warning(f"Non-admin user {admin_id} tried to reject listing {listing_id}")
                return False
            
            # Update listing status
            result = await self.db.execute(
                update(Listing)
                .where(Listing.id == listing_id)
                .values(
                    status=ListingStatus.rejected,
                    rejection_reason=reason
                )
            )
            
            await self.db.commit()
            
            if result.rowcount > 0:
                logger.info(f"Listing {listing_id} rejected by admin {admin_id}: {reason}")
                return True
            else:
                logger.warning(f"Listing {listing_id} not found for rejection")
                return False
                
        except Exception as e:
            logger.error(f"Failed to reject listing {listing_id}: {e}")
            await self.db.rollback()
            return False
    
    async def delete_listing(self, listing_id: str, admin_id: int) -> bool:
        """
        E'lonni o'chirish
        
        Args:
            listing_id: E'lon ID
            admin_id: Admin ID
            
        Returns:
            bool: Muvaffaqiyat holati
        """
        try:
            # Check if user is admin
            if not self.is_admin(admin_id):
                logger.warning(f"Non-admin user {admin_id} tried to delete listing {listing_id}")
                return False
            
            # Delete listing
            result = await self.db.execute(
                delete(Listing)
                .where(Listing.id == listing_id)
            )
            
            await self.db.commit()
            
            if result.rowcount > 0:
                logger.info(f"Listing {listing_id} deleted by admin {admin_id}")
                return True
            else:
                logger.warning(f"Listing {listing_id} not found for deletion")
                return False
                
        except Exception as e:
            logger.error(f"Failed to delete listing {listing_id}: {e}")
            await self.db.rollback()
            return False
    
    async def get_all_users(self) -> List[User]:
        """
        Barcha foydalanuvchilarni olish
        
        Returns:
            List[User]: Foydalanuvchilar ro'yxati
        """
        try:
            result = await self.db.execute(
                select(User)
                .order_by(User.created_at.desc())
            )
            return result.scalars().all()
            
        except Exception as e:
            logger.error(f"Failed to get all users: {e}")
            return []
    
    async def block_user(self, user_id: str, admin_id: int, reason: str = None) -> bool:
        """
        Foydalanuvchini bloklash
        
        Args:
            user_id: User ID
            admin_id: Admin ID
            reason: Bloklash sababi
            
        Returns:
            bool: Muvaffaqiyat holati
        """
        try:
            # Check if user is admin
            if not self.is_admin(admin_id):
                logger.warning(f"Non-admin user {admin_id} tried to block user {user_id}")
                return False
            
            # Update user status
            result = await self.db.execute(
                update(User)
                .where(User.id == user_id)
                .values(blocked=True)
            )
            
            await self.db.commit()
            
            if result.rowcount > 0:
                logger.info(f"User {user_id} blocked by admin {admin_id}: {reason}")
                return True
            else:
                logger.warning(f"User {user_id} not found for blocking")
                return False
                
        except Exception as e:
            logger.error(f"Failed to block user {user_id}: {e}")
            await self.db.rollback()
            return False
    
    async def unblock_user(self, user_id: str, admin_id: int) -> bool:
        """
        Foydalanuvchini blokdan chiqarish
        
        Args:
            user_id: User ID
            admin_id: Admin ID
            
        Returns:
            bool: Muvaffaqiyat holati
        """
        try:
            # Check if user is admin
            if not self.is_admin(admin_id):
                logger.warning(f"Non-admin user {admin_id} tried to unblock user {user_id}")
                return False
            
            # Update user status
            result = await self.db.execute(
                update(User)
                .where(User.id == user_id)
                .values(blocked=False)
            )
            
            await self.db.commit()
            
            if result.rowcount > 0:
                logger.info(f"User {user_id} unblocked by admin {admin_id}")
                return True
            else:
                logger.warning(f"User {user_id} not found for unblocking")
                return False
                
        except Exception as e:
            logger.error(f"Failed to unblock user {user_id}: {e}")
            await self.db.rollback()
            return False
    
    async def get_statistics(self) -> Dict[str, Any]:
        """
        Statistika olish
        
        Returns:
            Dict[str, Any]: Statistika ma'lumotlari
        """
        try:
            # Users statistics
            total_users = await self.db.execute(select(func.count(User.id)))
            verified_users = await self.db.execute(select(func.count(User.id)).where(User.verified == True))
            blocked_users = await self.db.execute(select(func.count(User.id)).where(User.blocked == True))
            
            # Listings statistics
            total_listings = await self.db.execute(select(func.count(Listing.id)))
            pending_listings = await self.db.execute(select(func.count(Listing.id)).where(Listing.status == ListingStatus.pending))
            approved_listings = await self.db.execute(select(func.count(Listing.id)).where(Listing.status == ListingStatus.approved))
            rejected_listings = await self.db.execute(select(func.count(Listing.id)).where(Listing.status == ListingStatus.rejected))
            
            # Listing types
            rental_listings = await self.db.execute(select(func.count(Listing.id)).where(Listing.type == ListingType.ijara))
            sale_listings = await self.db.execute(select(func.count(Listing.id)).where(Listing.type == ListingType.sotuv))
            
            return {
                'users': {
                    'total': total_users.scalar(),
                    'verified': verified_users.scalar(),
                    'blocked': blocked_users.scalar()
                },
                'listings': {
                    'total': total_listings.scalar(),
                    'pending': pending_listings.scalar(),
                    'approved': approved_listings.scalar(),
                    'rejected': rejected_listings.scalar(),
                    'rental': rental_listings.scalar(),
                    'sale': sale_listings.scalar()
                }
            }
            
        except Exception as e:
            logger.error(f"Failed to get statistics: {e}")
            return {
                'users': {'total': 0, 'verified': 0, 'blocked': 0},
                'listings': {'total': 0, 'pending': 0, 'approved': 0, 'rejected': 0, 'rental': 0, 'sale': 0}
            }
    
    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """
        Telegram ID orqali foydalanuvchini topish
        
        Args:
            telegram_id: Telegram user ID
            
        Returns:
            Optional[User]: Foydalanuvchi yoki None
        """
        try:
            result = await self.db.execute(
                select(User)
                .where(User.telegram_user_id == telegram_id)
            )
            return result.scalar_one_or_none()
            
        except Exception as e:
            logger.error(f"Failed to get user by telegram ID {telegram_id}: {e}")
            return None
