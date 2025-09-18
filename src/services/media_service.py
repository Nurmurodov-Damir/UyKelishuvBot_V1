"""
Media Service - Rasm va fayl yuklash xizmati
"""
import logging
import os
import uuid
from typing import Optional, List, Dict, Any
from telegram import Update, PhotoSize, Document
from telegram.ext import ContextTypes
from src.config import settings

logger = logging.getLogger(__name__)


class MediaService:
    """Media fayllar bilan ishlash xizmati"""
    
    def __init__(self):
        self.media_dir = "media"
        self.allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.webp'}
        self.max_file_size = 20 * 1024 * 1024  # 20MB
        
    def _ensure_media_dir(self) -> None:
        """Media papkasini yaratish"""
        if not os.path.exists(self.media_dir):
            os.makedirs(self.media_dir)
            logger.info(f"Media directory created: {self.media_dir}")
    
    async def download_photo(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> Optional[str]:
        """
        Rasmni yuklab olish
        
        Args:
            update: Telegram update
            context: Bot context
            
        Returns:
            str: Yuklangan fayl yo'li yoki None
        """
        try:
            if not update.message or not update.message.photo:
                return None
            
            # Eng katta rasmni olish
            photo = update.message.photo[-1]
            
            # Fayl nomini yaratish
            file_id = photo.file_id
            file_name = f"{uuid.uuid4()}.jpg"
            file_path = os.path.join(self.media_dir, file_name)
            
            # Media papkasini yaratish
            self._ensure_media_dir()
            
            # Rasmni yuklab olish
            file = await context.bot.get_file(file_id)
            await file.download_to_drive(file_path)
            
            logger.info(f"Photo downloaded: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error downloading photo: {e}")
            return None
    
    async def download_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> Optional[str]:
        """
        Hujjatni yuklab olish
        
        Args:
            update: Telegram update
            context: Bot context
            
        Returns:
            str: Yuklangan fayl yo'li yoki None
        """
        try:
            if not update.message or not update.message.document:
                return None
            
            document = update.message.document
            
            # Fayl hajmini tekshirish
            if document.file_size and document.file_size > self.max_file_size:
                logger.warning(f"File too large: {document.file_size} bytes")
                return None
            
            # Fayl kengaytmasini tekshirish
            file_name = document.file_name or "document"
            file_ext = os.path.splitext(file_name)[1].lower()
            
            if file_ext not in self.allowed_extensions:
                logger.warning(f"File extension not allowed: {file_ext}")
                return None
            
            # Fayl nomini yaratish
            unique_name = f"{uuid.uuid4()}{file_ext}"
            file_path = os.path.join(self.media_dir, unique_name)
            
            # Media papkasini yaratish
            self._ensure_media_dir()
            
            # Hujjatni yuklab olish
            file = await context.bot.get_file(document.file_id)
            await file.download_to_drive(file_path)
            
            logger.info(f"Document downloaded: {file_path}")
            return file_path
            
        except Exception as e:
            logger.error(f"Error downloading document: {e}")
            return None
    
    async def process_media(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> Optional[str]:
        """
        Media faylni qayta ishlash (rasm yoki hujjat)
        
        Args:
            update: Telegram update
            context: Bot context
            
        Returns:
            str: Yuklangan fayl yo'li yoki None
        """
        try:
            logger.info(f"Processing media for user {update.effective_user.id}")
            
            # Rasmni tekshirish
            if update.message and update.message.photo:
                logger.info(f"Photo detected, count: {len(update.message.photo)}")
                return await self.download_photo(update, context)
            
            # Hujjatni tekshirish
            if update.message and update.message.document:
                logger.info(f"Document detected: {update.message.document.file_name}")
                return await self.download_document(update, context)
            
            logger.warning("No photo or document found in message")
            return None
            
        except Exception as e:
            logger.error(f"Error processing media: {e}")
            return None
    
    def get_media_url(self, file_path: str) -> str:
        """
        Fayl yo'lini URL ga aylantirish
        
        Args:
            file_path: Fayl yo'li
            
        Returns:
            str: Media URL
        """
        try:
            # Production da bu URL server URL bo'lishi kerak
            if settings.debug:
                return f"file://{os.path.abspath(file_path)}"
            else:
                # Production URL
                filename = os.path.basename(file_path)
                return f"{settings.bot_name}/media/{filename}"
                
        except Exception as e:
            logger.error(f"Error getting media URL: {e}")
            return file_path
    
    def validate_media(self, file_path: str) -> bool:
        """
        Media faylini tekshirish
        
        Args:
            file_path: Fayl yo'li
            
        Returns:
            bool: Fayl to'g'ri bo'lsa True
        """
        try:
            if not os.path.exists(file_path):
                return False
            
            # Fayl hajmini tekshirish
            file_size = os.path.getsize(file_path)
            if file_size > self.max_file_size:
                return False
            
            # Fayl kengaytmasini tekshirish
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext not in self.allowed_extensions:
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating media: {e}")
            return False
    
    def cleanup_media(self, file_path: str) -> bool:
        """
        Media faylni o'chirish
        
        Args:
            file_path: Fayl yo'li
            
        Returns:
            bool: O'chirilgan bo'lsa True
        """
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"Media file deleted: {file_path}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error cleaning up media: {e}")
            return False
