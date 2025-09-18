"""
Validation Service - Ma'lumotlar tekshirish xizmati
"""
import re
from typing import Optional, Tuple, Dict, Any
from decimal import Decimal
from src.utils.constants import BotConstants, ErrorMessages
from src.config import REGIONS

class ValidationService:
    """Ma'lumotlar tekshirish xizmati"""
    
    @staticmethod
    def validate_price(price_text: str) -> Tuple[bool, Optional[float], Optional[str]]:
        """
        Narxni tekshirish
        
        Args:
            price_text: Narx matni
            
        Returns:
            Tuple[bool, Optional[float], Optional[str]]: (is_valid, price_value, error_message)
        """
        try:
            price = float(price_text.strip())
            
            if price < BotConstants.MIN_PRICE:
                return False, None, f"Narx {BotConstants.MIN_PRICE} dan kam bo'lmasligi kerak"
            
            if price > BotConstants.MAX_PRICE:
                return False, None, f"Narx {BotConstants.MAX_PRICE} dan ko'p bo'lmasligi kerak"
            
            return True, price, None
            
        except ValueError:
            return False, None, ErrorMessages.INVALID_PRICE
    
    @staticmethod
    def validate_price_range(price_text: str) -> Tuple[bool, Optional[float], Optional[float], Optional[str]]:
        """
        Narx oralig'ini tekshirish
        
        Args:
            price_text: Narx oralig'i matni (masalan: "100-500", "500+", "500")
            
        Returns:
            Tuple[bool, Optional[float], Optional[float], Optional[str]]: (is_valid, min_price, max_price, error_message)
        """
        try:
            price_text = price_text.strip()
            
            if '-' in price_text:
                # Oralik format: 100-500
                parts = price_text.split('-')
                if len(parts) != 2:
                    return False, None, None, "Noto'g'ri narx oralig'i format"
                
                min_price = float(parts[0].strip())
                max_price = float(parts[1].strip())
                
                if min_price >= max_price:
                    return False, None, None, "Minimal narx maksimal narxdan kam bo'lishi kerak"
                
                if min_price < BotConstants.MIN_PRICE or max_price > BotConstants.MAX_PRICE:
                    return False, None, None, f"Narx {BotConstants.MIN_PRICE} dan {BotConstants.MAX_PRICE} gacha bo'lishi kerak"
                
                return True, min_price, max_price, None
            
            elif price_text.endswith('+'):
                # Yuqori chegarasiz: 500+
                min_price = float(price_text[:-1].strip())
                
                if min_price < BotConstants.MIN_PRICE:
                    return False, None, None, f"Narx {BotConstants.MIN_PRICE} dan kam bo'lmasligi kerak"
                
                return True, min_price, None, None
            
            else:
                # Aniq narx: 500
                price = float(price_text)
                
                if price < BotConstants.MIN_PRICE or price > BotConstants.MAX_PRICE:
                    return False, None, None, f"Narx {BotConstants.MIN_PRICE} dan {BotConstants.MAX_PRICE} gacha bo'lishi kerak"
                
                return True, price, price, None
                
        except ValueError:
            return False, None, None, "Noto'g'ri narx format!\n\nTo'g'ri formatlar:\n• 100-500 (oralik)\n• 500+ (500 dan yuqori)\n• 500 (aniq narx)"
    
    @staticmethod
    def validate_title(title: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Sarlavhani tekshirish
        
        Args:
            title: Sarlavha matni
            
        Returns:
            Tuple[bool, Optional[str], Optional[str]]: (is_valid, cleaned_title, error_message)
        """
        if not title or not title.strip():
            return False, None, "Sarlavha bo'sh bo'lmasligi kerak"
        
        cleaned_title = title.strip()
        
        if len(cleaned_title) < BotConstants.MIN_TITLE_LENGTH:
            return False, None, f"Sarlavha kamida {BotConstants.MIN_TITLE_LENGTH} ta belgi bo'lishi kerak"
        
        if len(cleaned_title) > BotConstants.MAX_TITLE_LENGTH:
            return False, None, f"Sarlavha maksimum {BotConstants.MAX_TITLE_LENGTH} ta belgi bo'lishi kerak"
        
        return True, cleaned_title, None
    
    @staticmethod
    def validate_description(description: str) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Tavsifni tekshirish
        
        Args:
            description: Tavsif matni
            
        Returns:
            Tuple[bool, Optional[str], Optional[str]]: (is_valid, cleaned_description, error_message)
        """
        if not description:
            return True, None, None  # Tavsif ixtiyoriy
        
        cleaned_description = description.strip()
        
        if len(cleaned_description) > BotConstants.MAX_DESCRIPTION_LENGTH:
            return False, None, f"Tavsif maksimum {BotConstants.MAX_DESCRIPTION_LENGTH} ta belgi bo'lishi kerak"
        
        return True, cleaned_description, None
    
    @staticmethod
    def validate_rooms(rooms: int) -> Tuple[bool, Optional[str]]:
        """
        Xonalar sonini tekshirish
        
        Args:
            rooms: Xonalar soni
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        if not isinstance(rooms, int):
            return False, "Xonalar soni butun son bo'lishi kerak"
        
        if rooms < BotConstants.MIN_ROOMS or rooms > BotConstants.MAX_ROOMS:
            return False, f"Xonalar soni {BotConstants.MIN_ROOMS} dan {BotConstants.MAX_ROOMS} gacha bo'lishi kerak"
        
        return True, None
    
    @staticmethod
    def validate_region_code(region_code: str) -> Tuple[bool, Optional[str]]:
        """
        Viloyat kodini tekshirish
        
        Args:
            region_code: Viloyat kodi
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        if not region_code or region_code not in REGIONS:
            return False, "Noto'g'ri viloyat kodi"
        
        return True, None
    
    @staticmethod
    def validate_listing_data(listing_data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        E'lon ma'lumotlarini to'liq tekshirish
        
        Args:
            listing_data: E'lon ma'lumotlari
            
        Returns:
            Tuple[bool, Optional[str]]: (is_valid, error_message)
        """
        required_fields = ['region_code', 'city_name', 'type', 'rooms', 'price', 'title']
        
        # Kerakli maydonlarni tekshirish
        for field in required_fields:
            if field not in listing_data or not listing_data[field]:
                return False, f"Kerakli maydon topilmadi: {field}"
        
        # Viloyat kodini tekshirish
        is_valid, error = ValidationService.validate_region_code(listing_data['region_code'])
        if not is_valid:
            return False, error
        
        # Xonalar sonini tekshirish
        is_valid, error = ValidationService.validate_rooms(listing_data['rooms'])
        if not is_valid:
            return False, error
        
        # Narxni tekshirish
        is_valid, price, error = ValidationService.validate_price(str(listing_data['price']))
        if not is_valid:
            return False, error
        
        # Sarlavhani tekshirish
        is_valid, title, error = ValidationService.validate_title(listing_data['title'])
        if not is_valid:
            return False, error
        
        # Tavsifni tekshirish (agar mavjud bo'lsa)
        if 'description' in listing_data and listing_data['description']:
            is_valid, desc, error = ValidationService.validate_description(listing_data['description'])
            if not is_valid:
                return False, error
        
        return True, None

class ErrorHandler:
    """Xatolik boshqarish"""
    
    @staticmethod
    def get_user_friendly_error(error: Exception) -> str:
        """
        Xatolikni foydalanuvchi uchun tushunarli qilish
        
        Args:
            error: Xatolik obyekti
            
        Returns:
            str: Foydalanuvchi uchun tushunarli xatolik xabari
        """
        error_type = type(error).__name__
        
        if "database" in str(error).lower():
            return "Ma'lumotlar bazasi bilan bog'lanishda xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring."
        
        if "network" in str(error).lower() or "connection" in str(error).lower():
            return "Internet aloqasi bilan bog'lanishda xatolik yuz berdi. Iltimos, internetni tekshiring."
        
        if "timeout" in str(error).lower():
            return "So'rov vaqti tugadi. Iltimos, qaytadan urinib ko'ring."
        
        if "permission" in str(error).lower():
            return "Sizda bu amalni bajarish uchun ruxsat yo'q."
        
        if "not found" in str(error).lower():
            return "Kerakli ma'lumot topilmadi."
        
        # Umumiy xatolik
        return ErrorMessages.GENERIC_ERROR
    
    @staticmethod
    def log_error(error: Exception, context: str = "") -> None:
        """
        Xatolikni log qilish
        
        Args:
            error: Xatolik obyekti
            context: Xatolik konteksti
        """
        import logging
        logger = logging.getLogger(__name__)
        
        error_msg = f"Error in {context}: {type(error).__name__}: {str(error)}"
        logger.error(error_msg, exc_info=True)
