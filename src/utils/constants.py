"""
Constants - Dastur konstantalari
"""
from typing import Dict, List

# Bot konfiguratsiyasi
class BotConstants:
    """Bot konstantalari"""
    
    # Pagination
    ITEMS_PER_PAGE = 5
    MAX_SEARCH_RESULTS = 100
    
    # Text limits
    MIN_TITLE_LENGTH = 5
    MAX_TITLE_LENGTH = 255
    MAX_DESCRIPTION_LENGTH = 2000
    
    # Price limits
    MIN_PRICE = 0.01
    MAX_PRICE = 1000000.0
    
    # Rooms limits
    MIN_ROOMS = 1
    MAX_ROOMS = 10
    
    # Area limits
    MIN_AREA = 1.0
    MAX_AREA = 10000.0
    
    # Floor limits
    MIN_FLOOR = 1
    MAX_FLOOR = 100

# Callback data patterns
class CallbackPatterns:
    """Callback data naqshlari"""
    
    # Listing creation
    POST_LISTING = "POST_LISTING"
    LISTING_REGION = "LISTING_REGION"
    LISTING_CITY = "LISTING_CITY"
    LISTING_TYPE = "LISTING_TYPE"
    LISTING_PROPERTY_TYPE = "LISTING_PROPERTY_TYPE"
    LISTING_ROOMS = "LISTING_ROOMS"
    LISTING_CURRENCY = "LISTING_CURRENCY"
    LISTING_FURNISHED = "LISTING_FURNISHED"
    LISTING_PETS = "LISTING_PETS"
    LISTING_SUBMIT = "LISTING_SUBMIT"
    LISTING_CANCEL = "LISTING_CANCEL"
    LISTING_SKIP_DESCRIPTION = "LISTING_SKIP_DESCRIPTION"
    
    # Search
    SEARCH_LISTINGS = "SEARCH_LISTINGS"
    SEARCH_REGION = "SEARCH_REGION"
    SEARCH_CITY = "SEARCH_CITY"
    SEARCH_TYPE = "SEARCH_TYPE"
    SEARCH_PROPERTY_TYPE = "SEARCH_PROPERTY_TYPE"
    SEARCH_ROOMS = "SEARCH_ROOMS"
    SEARCH_PRICE = "SEARCH_PRICE"
    SEARCH_FURNISHED = "SEARCH_FURNISHED"
    SEARCH_PETS = "SEARCH_PETS"
    SEARCH_EXECUTE = "SEARCH_EXECUTE"
    SEARCH_PAGE = "SEARCH_PAGE"
    
    # Navigation
    MAIN_MENU = "MAIN_MENU"
    HELP = "HELP"
    SETTINGS = "SETTINGS"
    MY_LISTINGS = "MY_LISTINGS"
    
    # Admin Panel
    ADMIN_PANEL = "ADMIN_PANEL"
    ADMIN_PENDING_LISTINGS = "ADMIN_PENDING_LISTINGS"
    ADMIN_USERS_MANAGEMENT = "ADMIN_USERS_MANAGEMENT"
    ADMIN_STATISTICS = "ADMIN_STATISTICS"
    ADMIN_APPROVE = "ADMIN_APPROVE"
    ADMIN_REJECT = "ADMIN_REJECT"
    ADMIN_DELETE = "ADMIN_DELETE"
    ADMIN_PREV_LISTING = "ADMIN_PREV_LISTING"
    ADMIN_NEXT_LISTING = "ADMIN_NEXT_LISTING"
    ADMIN_SEARCH_USER = "ADMIN_SEARCH_USER"
    ADMIN_ALL_USERS = "ADMIN_ALL_USERS"
    ADMIN_BLOCKED_USERS = "ADMIN_BLOCKED_USERS"

# Error messages
class ErrorMessages:
    """Xatolik xabarlari"""
    
    GENERIC_ERROR = "❌ Xatolik yuz berdi"
    INVALID_PRICE = "❌ Noto'g'ri narx format!\n\nFaqat raqam kiriting (masalan: 500)"
    INVALID_TITLE = "❌ Sarlavha noto'g'ri!\n\nKamida 5 ta, maksimum 255 ta belgi kiriting."
    INVALID_ROOMS = "❌ Xonalar soni noto'g'ri!\n\n1 dan 10 gacha raqam kiriting."
    MISSING_DATA = "❌ Ma'lumotlar topilmadi!\n\nQaytadan boshlang."
    USER_NOT_FOUND = "❌ Foydalanuvchi topilmadi!\n\nQaytadan boshlang."
    LISTING_NOT_FOUND = "❌ E'lon topilmadi!"
    NO_SEARCH_RESULTS = "🔍 Sizning qidiruv mezonlaringizga mos e'lonlar topilmadi."

# Success messages
class SuccessMessages:
    """Muvaffaqiyat xabarlari"""
    
    LISTING_CREATED = "✅ **E'lon muvaffaqiyatli yuborildi!**\n\nE'loningiz tekshirish jarayonida. Tasdiqlanganidan so'ng barcha foydalanuvchilar ko'ra oladi.\n\nRahmat!"
    LISTING_UPDATED = "✅ E'lon muvaffaqiyatli yangilandi!"
    LISTING_DELETED = "✅ E'lon muvaffaqiyatli o'chirildi!"

# UI Messages
class UIMessages:
    """UI xabarlari"""
    
    WELCOME = """🏠 **UyKelishuv**ga xush kelibsiz, {name}!

**"Ijaradan sotuvgacha, egadan bevosita"**

Bu yerda siz:
• 🏡 Uy ijara/sotuv e'lonlarini joylashtirish
• 🔍 Kerakli uyni qidirish
• 💬 Ega bilan bevosita aloqa qilish

imkoniyatiga egasiz.

Boshlash uchun quyidagi tugmalardan birini tanlang:"""
    
    HELP_TEXT = """📖 **Yordam**

Bu bot uy-joy kelishuvi uchun yaratilgan.

**Asosiy funksiyalar:**
• 📝 E'lon joylashtirish
• 🔍 Uy qidirish
• 👤 Profil boshqarish
• 💬 Ega bilan aloqa

**Komandalar:**
/start - Botni ishga tushirish
/help - Yordam olish"""
    
    SEARCH_START = "🔍 **E'lon qidirish**\n\nAvval viloyatni tanlang:"
    LISTING_START = "🏠 **E'lon joylashtirish**\n\nAvval viloyatni tanlang:"

# Keyboard texts
class KeyboardTexts:
    """Klaviatura matnlari"""
    
    # Main menu
    POST_LISTING = "📝 E'lon joylashtirish"
    SEARCH_LISTINGS = "🔎 E'lon izlash"
    MY_LISTINGS = "📦 Mening e'lonlarim"
    SETTINGS = "⚙️ Sozlamalar"
    HELP = "❗️ Yordam"
    ADMIN_PANEL = "🛡️ Admin Panel"
    
    # Navigation
    BACK_TO_MAIN = "🔙 Asosiy menyu"
    BACK = "🔙 Orqaga"
    CANCEL = "❌ Bekor qilish"
    
    # Listing types
    RENT = "🏠 Ijara"
    SALE = "💰 Sotuv"
    ALL_TYPES = "🔄 Barcha turlar"
    
    # Search
    ALL_REGIONS = "🌍 Barcha viloyatlar"
    ALL_CITIES = "🏙️ Barcha shaharlar"
    ALL_ROOMS = "🔄 Barcha"
    CUSTOM_PRICE = "💰 Narx oralig'ini kiriting"
    EXECUTE_SEARCH = "🔍 Qidirishni boshlash"
    REFRESH_SEARCH = "🔄 Qayta qidirish"
    
    # Features
    FURNISHED = "🪑 Mebellar"
    PETS_ALLOWED = "🐕 Hayvonlar"
    SKIP_DESCRIPTION = "⏭️ Tavsifni o'tkazib yuborish"
    
    # Pagination
    PREV_PAGE = "⬅️"
    NEXT_PAGE = "➡️"
