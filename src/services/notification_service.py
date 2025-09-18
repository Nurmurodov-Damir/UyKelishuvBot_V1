"""
Notification Service - Xabar yuborish xizmati
"""
import logging
from typing import Optional, Dict, Any
from telegram import Update, Bot
from telegram.ext import ContextTypes
from src.database.models import User, Listing, ListingStatus
from src.config import settings, REGIONS

logger = logging.getLogger(__name__)


class NotificationService:
    """Xabar yuborish xizmati"""
    
    def __init__(self, bot: Optional[Bot] = None):
        self.bot = bot
    
    async def send_listing_approved_notification(self, listing: Listing, user: User) -> bool:
        """
        E'lon tasdiqlangan xabarini yuborish
        
        Args:
            listing: Tasdiqlangan e'lon
            user: E'lon egasi
            
        Returns:
            bool: Xabar yuborilgan bo'lsa True
        """
        try:
            if not self.bot:
                logger.error("Bot instance not available for notifications")
                return False
            
            # Xabar matnini yaratish
            message = self._create_approval_message(listing)
            
            # Xabarni yuborish
            await self.bot.send_message(
                chat_id=user.telegram_user_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info(f"Approval notification sent to user {user.telegram_user_id} for listing {listing.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending approval notification: {e}")
            return False
    
    async def send_listing_rejected_notification(self, listing: Listing, user: User, reason: str = None) -> bool:
        """
        E'lon rad etilgan xabarini yuborish
        
        Args:
            listing: Rad etilgan e'lon
            user: E'lon egasi
            reason: Rad etish sababi
            
        Returns:
            bool: Xabar yuborilgan bo'lsa True
        """
        try:
            if not self.bot:
                logger.error("Bot instance not available for notifications")
                return False
            
            # Xabar matnini yaratish
            message = self._create_rejection_message(listing, reason)
            
            # Xabarni yuborish
            await self.bot.send_message(
                chat_id=user.telegram_user_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info(f"Rejection notification sent to user {user.telegram_user_id} for listing {listing.id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending rejection notification: {e}")
            return False
    
    def _create_approval_message(self, listing: Listing) -> str:
        """Tasdiqlash xabari matnini yaratish"""
        region_name = REGIONS.get(listing.region_code, listing.region_code)
        type_name = "Ijara" if listing.type.value == "ijara" else "Sotuv"
        
        # Narx formatini tayyorlash
        if listing.currency == "UZS":
            price_text = f"{listing.price:,.0f} so'm"
        else:
            price_text = f"${listing.price:,.0f}"
        
        message = f"""✅ **E'loningiz tasdiqlandi!**

🏠 **{listing.title}**
📍 {region_name} - {listing.city_name}
🏠 {type_name} • {listing.rooms} xona
💰 {price_text}

E'loningiz endi barcha foydalanuvchilar tomonidan ko'riladi va qidirish natijalarida paydo bo'ladi.

Rahmat! 🎉"""
        
        return message
    
    def _create_rejection_message(self, listing: Listing, reason: str = None) -> str:
        """Rad etish xabari matnini yaratish"""
        region_name = REGIONS.get(listing.region_code, listing.region_code)
        type_name = "Ijara" if listing.type.value == "ijara" else "Sotuv"
        
        # Narx formatini tayyorlash
        if listing.currency == "UZS":
            price_text = f"{listing.price:,.0f} so'm"
        else:
            price_text = f"${listing.price:,.0f}"
        
        message = f"""❌ **E'loningiz rad etildi**

🏠 **{listing.title}**
📍 {region_name} - {listing.city_name}
🏠 {type_name} • {listing.rooms} xona
💰 {price_text}"""
        
        if reason:
            message += f"\n\n**Sabab:** {reason}"
        
        message += "\n\nIltimos, e'lon qoidalariga rioya qiling va qayta urinib ko'ring."
        
        return message
    
    async def send_admin_notification(self, message: str, admin_user_id: int) -> bool:
        """
        Admin ga xabar yuborish
        
        Args:
            message: Xabar matni
            admin_user_id: Admin user ID
            
        Returns:
            bool: Xabar yuborilgan bo'lsa True
        """
        try:
            if not self.bot:
                logger.error("Bot instance not available for notifications")
                return False
            
            await self.bot.send_message(
                chat_id=admin_user_id,
                text=message,
                parse_mode='Markdown'
            )
            
            logger.info(f"Admin notification sent to {admin_user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error sending admin notification: {e}")
            return False
