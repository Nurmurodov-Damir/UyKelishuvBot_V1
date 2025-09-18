"""
UyKelishuv Bot Configuration
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Bot sozlamalari"""
    
    # Telegram Bot
    bot_token: str = Field(env="TELEGRAM_BOT_TOKEN")
    
    # Database
    database_url: str = Field(default="sqlite:///uykelishuv.db", env="DATABASE_URL")
    
    # Security
    secret_key: str = Field(default="your_secret_key_here", env="SECRET_KEY")
    jwt_secret_key: str = Field(default="your_jwt_secret_key", env="JWT_SECRET_KEY")
    
    # Debug
    debug: bool = Field(default=False, env="DEBUG")
    
    # Admin Settings
    admin_ids: str = Field(default="", env="ADMIN_IDS")
    
    # Bot Settings
    bot_name: str = Field(default="UyKelishuv Bot", env="BOT_NAME")
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "ignore"
    }


def create_settings():
    """Settings obyektini soddalashtirilgan yaratish"""
    try:
        # Bot token olish - Railway da majburiy
        bot_token = os.getenv('TELEGRAM_BOT_TOKEN', '')
        if not bot_token:
            if os.getenv('RAILWAY_ENVIRONMENT'):
                raise ValueError("TELEGRAM_BOT_TOKEN environment variable kerak Railway da!")
            else:
                print("⚠️ TELEGRAM_BOT_TOKEN topilmadi! Test token ishlatilmoqda...")
                bot_token = '123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ'  # Test token
        
        # Database URL ni environment dan olish
        database_url = os.getenv('DATABASE_URL')
        if not database_url:
            # Default SQLite for local development
            database_url = 'sqlite+aiosqlite:///uykelishuv_new.db'
        else:
            # URL formatini tuzatish
            if database_url.startswith('postgresql://'):
                database_url = database_url.replace('postgresql://', 'postgresql+asyncpg://')
            elif database_url.startswith('postgres://'):
                database_url = database_url.replace('postgres://', 'postgresql+asyncpg://')
        
        # Settings yaratish
        data = {
            'bot_token': bot_token,
            'database_url': database_url,
            'secret_key': os.getenv('SECRET_KEY', 'local_secret_key'),
            'jwt_secret_key': os.getenv('JWT_SECRET_KEY', 'local_jwt_secret'),
            'debug': os.getenv('DEBUG', 'true').lower() == 'true',
            'admin_ids': os.getenv('ADMIN_IDS', '924016177'),
            'bot_name': os.getenv('BOT_NAME', 'UyKelishuv Bot')
        }
        
        return Settings(**data)
    except Exception as e:
        print(f"❌ Config yuklashda xatolik: {e}")
        raise


settings = create_settings()


# Viloyatlar va shaharlar
REGIONS = {
    "01": "Andijon",
    "02": "Buxoro", 
    "03": "Farg'ona",
    "04": "Jizzax",
    "05": "Xorazm",
    "06": "Namangan",
    "07": "Navoiy",
    "08": "Qashqadaryo",
    "09": "Qoraqalpog'iston",
    "10": "Samarqand",
    "11": "Sirdaryo",
    "12": "Surxondaryo",
    "13": "Toshkent viloyati",
    "14": "Toshkent shahri"
}

TASHKENT_DISTRICTS = [
    "Bektemir",
    "Chilonzor", 
    "Mirobod",
    "Mirzo Ulug'bek",
    "Olmazor",
    "Sergeli",
    "Shayxontohur",
    "Uchtepa",
    "Yakkasaroy",
    "Yashnobod",
    "Yunusobod"
]

# Barcha viloyatlar uchun shaharlar ro'yxati
CITIES_BY_REGION = {
    "01": [  # Andijon
        "Andijon",
        "Asaka",
        "Baliqchi",
        "Bo'z",
        "Buloqboshi",
        "Izboskan",
        "Jalaquduq",
        "Qo'rg'ontepa",
        "Marhamat",
        "Oltinko'l",
        "Pakhtaobod",
        "Paxtaobod",
        "Shahrixon",
        "Ulug'nor",
        "Xonobod"
    ],
    "02": [  # Buxoro
        "Buxoro",
        "Vobkent",
        "G'ijduvon",
        "Jondor",
        "Kogon",
        "Olot",
        "Peshku",
        "Qorako'l",
        "Qorovulbozor",
        "Romitan",
        "Shofirkon"
    ],
    "03": [  # Farg'ona
        "Farg'ona",
        "Beshariq",
        "Bog'dod",
        "Buvayda",
        "Dang'ara",
        "Furqat",
        "Qo'qon",
        "Qo'shtepa",
        "Rishton",
        "So'x",
        "Toshloq",
        "Uchko'prik",
        "Yozyovon"
    ],
    "04": [  # Jizzax
        "Jizzax",
        "Arnasoy",
        "Baxmal",
        "Do'stlik",
        "Forish",
        "G'allaorol",
        "Mirzacho'l",
        "Paxtakor",
        "Yangibozor",
        "Zomin",
        "Zafarobod"
    ],
    "05": [  # Xorazm
        "Urganch",
        "Bog'ot",
        "Gurlan",
        "Qo'shko'pir",
        "Shovot",
        "Xazorasp",
        "Xiva",
        "Yangiariq",
        "Yangibozor"
    ],
    "06": [  # Namangan
        "Namangan",
        "Chortoq",
        "Chust",
        "Kosonsoy",
        "Mingbuloq",
        "Norin",
        "Pop",
        "To'raqo'rg'on",
        "Uchqo'rg'on",
        "Uychi",
        "Yangiqo'rg'on"
    ],
    "07": [  # Navoiy
        "Navoiy",
        "Karmana",
        "Konimex",
        "Navbahor",
        "Nurota",
        "Qiziltepa",
        "Tomdi",
        "Uchquduq",
        "Xatirchi",
        "Zarafshon",
        "G'ozg'on"
    ],
    "08": [  # Qashqadaryo
        "Qarshi",
        "Dehqonobod",
        "G'uzor",
        "Kasbi",
        "Kitob",
        "Koson",
        "Mirishkor",
        "Muborak",
        "Nishon",
        "Qamashi",
        "Shahrisabz",
        "Yakkabog'",
        "Chiroqchi"
    ],
    "09": [  # Qoraqalpog'iston
        "Nukus",
        "Xo'jayli",
        "Qo'ng'irot",
        "Taxiatosh",
        "Chimboy",
        "Shumanay",
        "Qorauzyak",
        "Kegeyli",
        "Amudaryo",
        "Beruniy",
        "Ellikqal'a",
        "Mo'ynoq",
        "Taxtako'pir",
        "To'rtko'l"
    ],
    "10": [  # Samarqand
        "Samarqand",
        "Bulungur",
        "Ishtixon",
        "Jomboy",
        "Kattaqo'rg'on",
        "Narpay",
        "Nurobod",
        "Oqdaryo",
        "Paxtachi",
        "Payariq",
        "Pastdarg'om",
        "Qo'shrabot",
        "Urgut"
    ],
    "11": [  # Sirdaryo
        "Guliston",
        "Boyovut",
        "Guliston",
        "Mirzaobod",
        "Oqoltin",
        "Sayxunobod",
        "Sardoba",
        "Sirdaryo",
        "Xovos"
    ],
    "12": [  # Surxondaryo
        "Termiz",
        "Angor",
        "Bandixon",
        "Boysun",
        "Denov",
        "Jarqo'rg'on",
        "Qiziriq",
        "Qumqo'rg'on",
        "Muzrabot",
        "Oltinsoy",
        "Sariosiyo",
        "Sherobod",
        "Sho'rchi",
        "Termiz",
        "Uzun"
    ],
    "13": [  # Toshkent viloyati
        "Nurafshon",
        "Bektemir",
        "Bostanliq",
        "Bo'ka",
        "Chinoz",
        "Qibray",
        "Ohangaron",
        "Oqqo'rg'on",
        "Parkent",
        "Piskent",
        "Quyi Chirchiq",
        "O'rta Chirchiq",
        "Yangiyo'l",
        "Yuqori Chirchiq",
        "Zangiota"
    ],
    "14": [  # Toshkent shahri
        "Bektemir",
        "Chilonzor", 
        "Mirobod",
        "Mirzo Ulug'bek",
        "Olmazor",
        "Sergeli",
        "Shayxontohur",
        "Uchtepa",
        "Yakkasaroy",
        "Yashnobod",
        "Yunusobod"
    ]
}

# Eski ro'yxatlar (compatibility uchun)
TASHKENT_DISTRICTS = CITIES_BY_REGION["14"]
KARAKALPAKSTAN_CITIES = CITIES_BY_REGION["09"]

# Valyuta ro'yxati
CURRENCIES = {
    "USD": "💵 Dollar (USD)",
    "UZS": "🇺🇿 So'm (UZS)"
}

# Regex patterns
PHONE_REGEX = r"^\+998[0-9]{9}$"
EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

# Admin ID lari
ADMIN_IDS = [int(x) for x in settings.admin_ids.split(',') if x.strip()]

# Debug rejimi
DEBUG = settings.debug