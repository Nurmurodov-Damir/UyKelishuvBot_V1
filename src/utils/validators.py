"""
Validatsiya funksiyalari
"""
import re
from typing import Optional
from src.config import PHONE_REGEX, REGIONS


def validate_phone(phone: str) -> bool:
    """Telefon raqamini validatsiya qilish"""
    if not phone:
        return False
    
    # Faqat raqamlarni qoldirish
    phone_clean = re.sub(r'\D', '', phone)
    
    # +998 formatiga keltirish
    if phone_clean.startswith('998'):
        formatted_phone = f"+{phone_clean}"
    elif phone_clean.startswith('8') and len(phone_clean) == 9:
        formatted_phone = f"+998{phone_clean[1:]}"
    elif len(phone_clean) == 9:
        formatted_phone = f"+998{phone_clean}"
    else:
        return False
    
    return bool(re.match(PHONE_REGEX, formatted_phone))


def validate_region(region_code: str) -> bool:
    """Viloyat kodini validatsiya qilish"""
    return region_code in REGIONS


def validate_price(price: float) -> bool:
    """Narxni validatsiya qilish"""
    return price > 0 and price <= 1000000