"""
SMS Service - SMS yuborish xizmati
"""
import logging
import random
import string
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import httpx
from src.config import settings

logger = logging.getLogger(__name__)


class SMSService:
    """SMS yuborish xizmati"""
    
    def __init__(self):
        self.verification_codes: Dict[str, Dict[str, Any]] = {}
        self.code_expiry_minutes = 5
        self.max_attempts = 3
        self.cooldown_minutes = 1
    
    def generate_verification_code(self) -> str:
        """
        Tasdiqlash kodini yaratish
        
        Returns:
            str: 6 raqamli kod
        """
        return ''.join(random.choices(string.digits, k=6))
    
    def is_valid_uzbek_phone(self, phone: str) -> bool:
        """
        O'zbekiston telefon raqami formatini tekshirish
        
        Args:
            phone: Telefon raqami
            
        Returns:
            bool: To'g'ri formatda bo'lsa True
        """
        # O'zbekiston raqamlari: +998XXXXXXXXX
        import re
        pattern = r'^\+998[0-9]{9}$'
        return bool(re.match(pattern, phone))
    
    def format_phone_number(self, phone: str) -> str:
        """
        Telefon raqamini formatlash
        
        Args:
            phone: Telefon raqami
            
        Returns:
            str: Formatlangan telefon raqami
        """
        # Faqat raqamlarni qoldirish
        digits = ''.join(filter(str.isdigit, phone))
        
        # O'zbekiston kodi bilan boshlash
        if digits.startswith('998'):
            return f'+{digits}'
        elif digits.startswith('8') and len(digits) == 10:
            return f'+99{digits}'
        elif len(digits) == 9:
            return f'+998{digits}'
        else:
            return f'+998{digits}'
    
    async def send_verification_code(self, phone: str) -> Dict[str, Any]:
        """
        Tasdiqlash kodini yuborish
        
        Args:
            phone: Telefon raqami
            
        Returns:
            Dict[str, Any]: Natija ma'lumotlari
        """
        try:
            # Telefon raqamini formatlash
            formatted_phone = self.format_phone_number(phone)
            
            # Telefon raqami formatini tekshirish
            if not self.is_valid_uzbek_phone(formatted_phone):
                return {
                    'success': False,
                    'error': 'Noto\'g\'ri telefon raqami format. O\'zbekiston raqamini kiriting.'
                }
            
            # Cooldown tekshirish
            if self._is_in_cooldown(formatted_phone):
                return {
                    'success': False,
                    'error': f'Iltimos, {self.cooldown_minutes} daqiqa kutib turing.'
                }
            
            # Tasdiqlash kodini yaratish
            code = self.generate_verification_code()
            
            # Kodni saqlash
            self.verification_codes[formatted_phone] = {
                'code': code,
                'created_at': datetime.utcnow(),
                'attempts': 0,
                'verified': False
            }
            
            # SMS yuborish (test rejimda console ga chiqarish)
            if settings.debug:
                logger.info(f"SMS Verification Code for {formatted_phone}: {code}")
                print(f"📱 SMS Code for {formatted_phone}: {code}")
                return {
                    'success': True,
                    'message': f'Tasdiqlash kodi {formatted_phone} raqamiga yuborildi. (Test rejimda: {code})'
                }
            else:
                # Production da real SMS service ishlatish
                sms_sent = await self._send_real_sms(formatted_phone, code)
                
                if sms_sent:
                    return {
                        'success': True,
                        'message': f'Tasdiqlash kodi {formatted_phone} raqamiga yuborildi.'
                    }
                else:
                    return {
                        'success': False,
                        'error': 'SMS yuborishda xatolik yuz berdi. Qaytadan urinib ko\'ring.'
                    }
            
        except Exception as e:
            logger.error(f"Failed to send verification code to {phone}: {e}")
            return {
                'success': False,
                'error': 'SMS yuborishda xatolik yuz berdi.'
            }
    
    async def verify_code(self, phone: str, code: str) -> Dict[str, Any]:
        """
        Tasdiqlash kodini tekshirish
        
        Args:
            phone: Telefon raqami
            code: Tasdiqlash kodi
            
        Returns:
            Dict[str, Any]: Tekshirish natijasi
        """
        try:
            formatted_phone = self.format_phone_number(phone)
            
            # Kod mavjudligini tekshirish
            if formatted_phone not in self.verification_codes:
                return {
                    'success': False,
                    'error': 'Tasdiqlash kodi topilmadi. Yangi kod so\'rang.'
                }
            
            verification_data = self.verification_codes[formatted_phone]
            
            # Kod muddatini tekshirish
            if self._is_code_expired(verification_data['created_at']):
                del self.verification_codes[formatted_phone]
                return {
                    'success': False,
                    'error': 'Tasdiqlash kodining muddati tugagan. Yangi kod so\'rang.'
                }
            
            # Urinishlar sonini tekshirish
            if verification_data['attempts'] >= self.max_attempts:
                del self.verification_codes[formatted_phone]
                return {
                    'success': False,
                    'error': 'Juda ko\'p noto\'g\'ri urinish. Yangi kod so\'rang.'
                }
            
            # Kodni tekshirish
            if verification_data['code'] == code.strip():
                # Tasdiqlash muvaffaqiyatli
                self.verification_codes[formatted_phone]['verified'] = True
                return {
                    'success': True,
                    'message': 'Telefon raqami muvaffaqiyatli tasdiqlandi!'
                }
            else:
                # Noto'g'ri kod
                self.verification_codes[formatted_phone]['attempts'] += 1
                remaining_attempts = self.max_attempts - verification_data['attempts'] - 1
                
                if remaining_attempts > 0:
                    return {
                        'success': False,
                        'error': f'Noto\'g\'ri tasdiqlash kodi. {remaining_attempts} ta urinish qoldi.'
                    }
                else:
                    del self.verification_codes[formatted_phone]
                    return {
                        'success': False,
                        'error': 'Juda ko\'p noto\'g\'ri urinish. Yangi kod so\'rang.'
                    }
            
        except Exception as e:
            logger.error(f"Failed to verify code for {phone}: {e}")
            return {
                'success': False,
                'error': 'Kod tekshirishda xatolik yuz berdi.'
            }
    
    def is_phone_verified(self, phone: str) -> bool:
        """
        Telefon raqami tasdiqlanganligini tekshirish
        
        Args:
            phone: Telefon raqami
            
        Returns:
            bool: Tasdiqlangan bo'lsa True
        """
        formatted_phone = self.format_phone_number(phone)
        
        if formatted_phone in self.verification_codes:
            verification_data = self.verification_codes[formatted_phone]
            return verification_data.get('verified', False)
        
        return False
    
    def cleanup_expired_codes(self) -> None:
        """Muddati tugagan kodlarni tozalash"""
        try:
            current_time = datetime.utcnow()
            expired_phones = []
            
            for phone, data in self.verification_codes.items():
                if self._is_code_expired(data['created_at']):
                    expired_phones.append(phone)
            
            for phone in expired_phones:
                del self.verification_codes[phone]
            
            if expired_phones:
                logger.info(f"Cleaned up {len(expired_phones)} expired verification codes")
                
        except Exception as e:
            logger.error(f"Failed to cleanup expired codes: {e}")
    
    # Private methods
    
    def _is_code_expired(self, created_at: datetime) -> bool:
        """Kod muddatini tekshirish"""
        expiry_time = created_at + timedelta(minutes=self.code_expiry_minutes)
        return datetime.utcnow() > expiry_time
    
    def _is_in_cooldown(self, phone: str) -> bool:
        """Cooldown holatini tekshirish"""
        if phone in self.verification_codes:
            last_sent = self.verification_codes[phone]['created_at']
            cooldown_end = last_sent + timedelta(minutes=self.cooldown_minutes)
            return datetime.utcnow() < cooldown_end
        return False
    
    async def _send_real_sms(self, phone: str, code: str) -> bool:
        """
        Real SMS yuborish (production uchun)
        
        Args:
            phone: Telefon raqami
            code: Tasdiqlash kodi
            
        Returns:
            bool: Yuborildi bo'lsa True
        """
        try:
            # Bu yerda real SMS provider API'sini ishlatish kerak
            # Masalan: Eskiz.uz, Playmobile.uz, SMS.uz
            
            # Eskiz.uz API example:
            # async with httpx.AsyncClient() as client:
            #     response = await client.post(
            #         "https://notify.eskiz.uz/api/message/sms/send",
            #         headers={
            #             "Authorization": f"Bearer {settings.sms_token}"
            #         },
            #         json={
            #             "mobile_phone": phone,
            #             "message": f"UyKelishuv tasdiqlash kodi: {code}",
            #             "from": "4546"
            #         }
            #     )
            #     return response.status_code == 200
            
            # Hozircha test rejimda
            logger.info(f"Would send SMS to {phone} with code {code}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send real SMS to {phone}: {e}")
            return False
