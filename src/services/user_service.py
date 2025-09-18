"""
User Service - Foydalanuvchi bilan bog'liq operatsiyalar
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from src.database.models import User


class UserService:
    """Foydalanuvchi xizmatlari"""
    
    def __init__(self, db: Optional[AsyncSession] = None):
        self.db = db
    
    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        """Telegram ID orqali foydalanuvchini topish"""
        try:
            result = await self.db.execute(
                select(User).where(User.telegram_user_id == telegram_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            if self.db:
                await self.db.rollback()
            raise
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """ID orqali foydalanuvchini topish"""
        try:
            result = await self.db.execute(
                select(User).where(User.id == user_id)
            )
            return result.scalar_one_or_none()
        except Exception as e:
            if self.db:
                await self.db.rollback()
            raise
    
    async def create_user(self, telegram_user_id: int, name: str) -> User:
        """Yangi foydalanuvchi yaratish"""
        try:
            user = User(
                telegram_user_id=telegram_user_id,
                name=name
            )
            self.db.add(user)
            await self.db.commit()
            await self.db.refresh(user)
            return user
        except Exception as e:
            await self.db.rollback()
            raise
    
    async def update_user(self, user_id: str, **kwargs) -> Optional[User]:
        """Foydalanuvchini yangilash"""
        try:
            result = await self.db.execute(
                update(User)
                .where(User.id == user_id)
                .values(**kwargs)
            )
            
            if result.rowcount > 0:
                await self.db.commit()
                return await self.get_user_by_id(user_id)
            return None
        except Exception as e:
            await self.db.rollback()
            raise
    
    async def delete_user(self, user_id: str) -> bool:
        """Foydalanuvchini o'chirish"""
        try:
            result = await self.db.execute(
                delete(User).where(User.id == user_id)
            )
            
            if result.rowcount > 0:
                await self.db.commit()
                return True
            return False
        except Exception as e:
            await self.db.rollback()
            raise
    
    async def get_all_users(self) -> List[User]:
        """Barcha foydalanuvchilarni olish"""
        try:
            result = await self.db.execute(
                select(User).order_by(User.created_at.desc())
            )
            return result.scalars().all()
        except Exception as e:
            if self.db:
                await self.db.rollback()
            raise