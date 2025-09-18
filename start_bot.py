#!/usr/bin/env python3
"""
UyKelishuv Bot - Oddiy ishga tushirish scripti
"""

import asyncio
import sys
import os
from pathlib import Path

# Project root qo'shish
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_requirements():
    """Kerakli fayllarni tekshirish"""
    print("🔍 Kerakli fayllarni tekshirish...")
    
    # Railway environment check
    if os.getenv('RAILWAY_ENVIRONMENT'):
        print("🚀 Railway muhitida ishlamoqda...")
        # Railway da environment variables to'g'ridan-to'g'ri o'rnatiladi
        required_vars = ['TELEGRAM_BOT_TOKEN', 'DATABASE_URL']
        missing_vars = []
        
        for var in required_vars:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            print(f"❌ Quyidagi environment variables yetishmayapti: {', '.join(missing_vars)}")
            return False
        
        print("✅ Barcha kerakli environment variables mavjud")
        return True
    else:
        # Local development uchun .env fayli kerak
        env_file = project_root / ".env"
        if not env_file.exists():
            print("❌ .env fayli topilmadi!")
            print("📝 .env fayl yarating va kerakli o'zgaruvchilarni qo'shing:")
            print("""
TELEGRAM_BOT_TOKEN=your_bot_token_here
DATABASE_URL=sqlite:///uykelishuv.db
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key
DEBUG=True
            """)
            return False
    
    # requirements.txt ni tekshirish
    req_file = project_root / "requirements.txt"
    if not req_file.exists():
        print("❌ requirements.txt fayli topilmadi!")
        return False
    
    print("✅ Barcha kerakli fayllar mavjud")
    return True

def check_dependencies():
    """Dependencies ni tekshirish"""
    print("📦 Dependencies ni tekshirish...")
    
    try:
        import telegram
        import sqlalchemy
        import pydantic
        import alembic
        print("✅ Barcha dependencies o'rnatilgan")
        return True
    except ImportError as e:
        print(f"❌ Dependencies yetishmayapti: {e}")
        print("📥 Dependencies ni o'rnating:")
        print("pip install -r requirements.txt")
        return False

async def start_bot():
    """Bot ni ishga tushirish"""
    print("🚀 UyKelishuv Bot ishga tushmoqda...")
    
    try:
        from src.main import main
        await main()
    except KeyboardInterrupt:
        print("\n⏹️ Bot to'xtatildi")
    except Exception as e:
        print(f"❌ Bot ishga tushishda xatolik: {e}")
        print("🔧 Xatoliklarni tekshiring va qayta urinib ko'ring")

def main():
    """Asosiy funksiya"""
    print("🏠 UyKelishuv Bot")
    print("=" * 50)
    
    # Kerakli fayllarni tekshirish
    if not check_requirements():
        sys.exit(1)
    
    # Dependencies ni tekshirish
    if not check_dependencies():
        sys.exit(1)
    
    # Bot ni ishga tushirish
    try:
        asyncio.run(start_bot())
    except Exception as e:
        print(f"❌ Umumiy xatolik: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()