"""
Yordamchi funksiyalar
"""
import re
from typing import Optional
from src.config import PHONE_REGEX


def format_phone_number(phone: str) -> str:
    """Telefon raqamini formatlash"""
    # Faqat raqamlarni qoldirish
    phone = re.sub(r'\D', '', phone)
    
    # +998 bilan boshlash
    if phone.startswith('998'):
        return f"+{phone}"
    elif phone.startswith('8') and len(phone) == 9:
        return f"+998{phone[1:]}"
    elif len(phone) == 9:
        return f"+998{phone}"
    
    return phone


def validate_phone(phone: str) -> bool:
    """Telefon raqamini validatsiya qilish"""
    if not phone:
        return False
    
    formatted_phone = format_phone_number(phone)
    return bool(re.match(PHONE_REGEX, formatted_phone))