#!/usr/bin/env python3
"""
Minimal Railway test script
"""
import os
import sys
import time

def main():
    print("=" * 50)
    print("🧪 Railway Test Script")
    print("=" * 50)
    
    # Environment info
    print(f"🐍 Python: {sys.version}")
    print(f"📁 CWD: {os.getcwd()}")
    print(f"🗂️ Files: {os.listdir('.')[:10]}")
    
    # Environment variables
    print("\n📊 Environment Variables:")
    env_vars = ['TELEGRAM_BOT_TOKEN', 'DATABASE_URL', 'SECRET_KEY', 'DEBUG', 'ADMIN_IDS', 'RAILWAY_ENVIRONMENT']
    for var in env_vars:
        value = os.getenv(var, 'NOT SET')
        if var == 'TELEGRAM_BOT_TOKEN' and value != 'NOT SET':
            print(f"  {var}: {'*' * 20}...{value[-10:]}")
        elif var == 'DATABASE_URL' and value != 'NOT SET':
            print(f"  {var}: {value[:40]}...")
        else:
            print(f"  {var}: {value}")
    
    # Railway database variables ni ham tekshirish
    print("\n🗄️ Railway Database Variables:")
    db_vars = [v for v in os.environ.keys() if 'database' in v.lower() or 'postgres' in v.lower() or 'db' in v.lower()]
    for var in sorted(db_vars):
        value = os.getenv(var, '')
        if len(value) > 50:
            print(f"  {var}: {value[:40]}...")
        else:
            print(f"  {var}: {value}")
    
    # Test imports
    print("\n🔍 Testing imports...")
    try:
        import telegram
        print("✅ telegram imported")
    except Exception as e:
        print(f"❌ telegram import failed: {e}")
        
    try:
        import sqlalchemy
        print("✅ sqlalchemy imported")
    except Exception as e:
        print(f"❌ sqlalchemy import failed: {e}")
        
    try:
        import asyncpg
        print("✅ asyncpg imported")
    except Exception as e:
        print(f"❌ asyncpg import failed: {e}")
    
    # Test config
    print("\n⚙️ Testing config...")
    try:
        sys.path.insert(0, '.')
        from src.config import settings
        print(f"✅ Config loaded")
        print(f"  Database URL: {settings.database_url[:40]}...")
        print(f"  Bot token set: {bool(settings.bot_token)}")
    except Exception as e:
        print(f"❌ Config failed: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        
    # Keep container alive for Railway
    if os.getenv('RAILWAY_ENVIRONMENT'):
        print("\n⏱️ Keeping container alive for 30 seconds...")
        for i in range(30):
            print(f"⏳ {i+1}/30 seconds...")
            time.sleep(1)
    
    print("✅ Test completed successfully!")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        print(f"Full traceback: {traceback.format_exc()}")
        sys.exit(1)