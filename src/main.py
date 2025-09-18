"""
UyKelishuv Bot - Asosiy fayl
"""
import asyncio
import logging
from src.config import settings
from src.database.database import init_db, close_db
from src.bot.client_telegram import UyKelishuvBot


# Logging sozlash
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


async def main():
    """Asosiy funksiya"""
    try:
        logger.info("Bot ishga tushmoqda...")
        
        # Ma'lumotlar bazasini ishga tushirish
        await init_db()
        logger.info("Ma'lumotlar bazasi muvaffaqiyatli ishga tushdi")
        
        # Botni yaratish va ishga tushirish
        bot = UyKelishuvBot()
        await bot.start()
        
        logger.info("Bot muvaffaqiyatli ishga tushdi")
        
        # Botni ishlatish
        await bot.run_until_disconnected()
        
    except Exception as e:
        logger.error(f"Bot ishga tushishda xatolik: {e}")
        raise
    finally:
        # Ma'lumotlar bazasini yopish
        await close_db()
        logger.info("Ma'lumotlar bazasi yopildi")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot to'xtatildi")
    except Exception as e:
        logger.error(f"Kutilmagan xatolik: {e}")
        raise