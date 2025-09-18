#!/usr/bin/env python3
"""
Simple health check for Railway deployment
"""
import asyncio
import sys
import os
from pathlib import Path

# Project root qo'shish
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

async def health_check():
    """Railway health check"""
    try:
        # Basic imports test
        from src.config import settings
        from src.database.database import engine
        
        print("✅ Imports successful")
        print(f"📊 Database URL configured: {bool(settings.database_url)}")
        print(f"🔑 Bot token configured: {bool(settings.bot_token)}")
        
        # Test database connection
        async with engine.begin() as conn:
            await conn.execute("SELECT 1")
        print("✅ Database connection successful")
        
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

if __name__ == "__main__":
    success = asyncio.run(health_check())
    sys.exit(0 if success else 1)