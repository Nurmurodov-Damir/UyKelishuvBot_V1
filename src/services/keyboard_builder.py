"""
Keyboard Builder Service - Klaviatura yaratish xizmati
"""
from typing import List, Optional
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from src.utils.constants import (
    CallbackPatterns, KeyboardTexts, BotConstants
)
from src.config import REGIONS, CITIES_BY_REGION, TASHKENT_DISTRICTS, KARAKALPAKSTAN_CITIES, CURRENCIES

class KeyboardBuilder:
    """Klaviatura yaratish xizmati"""
    
    @staticmethod
    def create_main_menu(is_admin: bool = False) -> InlineKeyboardMarkup:
        """Asosiy menyu klaviaturasi"""
        keyboard = [
            [InlineKeyboardButton(KeyboardTexts.POST_LISTING, callback_data=CallbackPatterns.POST_LISTING)],
            [InlineKeyboardButton(KeyboardTexts.SEARCH_LISTINGS, callback_data=CallbackPatterns.SEARCH_LISTINGS)],
            [InlineKeyboardButton(KeyboardTexts.MY_LISTINGS, callback_data=CallbackPatterns.MY_LISTINGS)],
            [
                InlineKeyboardButton(KeyboardTexts.SETTINGS, callback_data=CallbackPatterns.SETTINGS),
                InlineKeyboardButton(KeyboardTexts.HELP, callback_data=CallbackPatterns.HELP)
            ]
        ]
        
        # Admin tugmasini qo'shish
        if is_admin:
            keyboard.append([InlineKeyboardButton(KeyboardTexts.ADMIN_PANEL, callback_data=CallbackPatterns.ADMIN_PANEL)])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_back_button() -> InlineKeyboardMarkup:
        """Orqaga tugmasi"""
        return InlineKeyboardMarkup([[
            InlineKeyboardButton(KeyboardTexts.BACK_TO_MAIN, callback_data=CallbackPatterns.MAIN_MENU)
        ]])
    
    @staticmethod
    def create_regions_keyboard(is_search: bool = False) -> InlineKeyboardMarkup:
        """
        Viloyatlar klaviaturasi
        
        Args:
            is_search: Qidiruv uchunmi yoki e'lon joylashtirish uchunmi
        """
        keyboard = []
        
        if is_search:
            # Qidiruv uchun "Barcha viloyatlar" variant
            keyboard.append([InlineKeyboardButton(KeyboardTexts.ALL_REGIONS, callback_data=f"{CallbackPatterns.SEARCH_REGION}:all")])
        
        # Viloyatlarni 2 ta qatorda joylashtirish
        regions = list(REGIONS.items())
        for i in range(0, len(regions), 2):
            row = []
            
            # Birinchi viloyat
            code, name = regions[i]
            callback_prefix = CallbackPatterns.SEARCH_REGION if is_search else CallbackPatterns.LISTING_REGION
            row.append(InlineKeyboardButton(name, callback_data=f"{callback_prefix}:{code}"))
            
            # Ikkinchi viloyat (agar mavjud bo'lsa)
            if i + 1 < len(regions):
                code2, name2 = regions[i + 1]
                row.append(InlineKeyboardButton(name2, callback_data=f"{callback_prefix}:{code2}"))
            
            keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton(KeyboardTexts.BACK_TO_MAIN, callback_data=CallbackPatterns.MAIN_MENU)])
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_currency_keyboard() -> InlineKeyboardMarkup:
        """Valyuta tanlash klaviaturasi"""
        keyboard = []
        
        # Valyutalarni 2 ta qatorda joylashtirish
        currencies = list(CURRENCIES.items())
        for i in range(0, len(currencies), 2):
            row = []
            
            # Birinchi valyuta
            currency_code, currency_name = currencies[i]
            row.append(InlineKeyboardButton(currency_name, callback_data=f"{CallbackPatterns.LISTING_CURRENCY}:{currency_code}"))
            
            # Ikkinchi valyuta (agar mavjud bo'lsa)
            if i + 1 < len(currencies):
                currency_code2, currency_name2 = currencies[i + 1]
                row.append(InlineKeyboardButton(currency_name2, callback_data=f"{CallbackPatterns.LISTING_CURRENCY}:{currency_code2}"))
            
            keyboard.append(row)
        
        # Orqaga tugmasi
        keyboard.append([InlineKeyboardButton(KeyboardTexts.BACK, callback_data=CallbackPatterns.LISTING_ROOMS)])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_property_type_keyboard(is_search: bool = False) -> InlineKeyboardMarkup:
        """Uy turi klaviaturasi"""
        if is_search:
            # Qidiruv uchun
            keyboard = [
                [InlineKeyboardButton("🏢 Kvartira", callback_data=f"{CallbackPatterns.SEARCH_PROPERTY_TYPE}:kvartira")],
                [InlineKeyboardButton("🏠 Uy", callback_data=f"{CallbackPatterns.SEARCH_PROPERTY_TYPE}:uy")],
                [InlineKeyboardButton("🏢 Ofis", callback_data=f"{CallbackPatterns.SEARCH_PROPERTY_TYPE}:ofis")],
                [InlineKeyboardButton("Barcha turlar", callback_data=f"{CallbackPatterns.SEARCH_PROPERTY_TYPE}:all")],
                [InlineKeyboardButton(KeyboardTexts.BACK, callback_data=CallbackPatterns.SEARCH_TYPE)]
            ]
        else:
            # E'lon joylashtirish uchun
            keyboard = [
                [InlineKeyboardButton("🏢 Kvartira", callback_data=f"{CallbackPatterns.LISTING_PROPERTY_TYPE}:kvartira")],
                [InlineKeyboardButton("🏠 Uy", callback_data=f"{CallbackPatterns.LISTING_PROPERTY_TYPE}:uy")],
                [InlineKeyboardButton("🏢 Ofis", callback_data=f"{CallbackPatterns.LISTING_PROPERTY_TYPE}:ofis")],
                [InlineKeyboardButton(KeyboardTexts.BACK, callback_data=CallbackPatterns.LISTING_TYPE)]
            ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_furniture_keyboard(is_search: bool = False) -> InlineKeyboardMarkup:
        """Mebellar tanlash klaviaturasi"""
        if is_search:
            # Qidiruv uchun
            keyboard = [
                [
                    InlineKeyboardButton("✅ Mebellar bilan", callback_data=f"{CallbackPatterns.SEARCH_FURNISHED}:true"),
                    InlineKeyboardButton("❌ Mebellarsiz", callback_data=f"{CallbackPatterns.SEARCH_FURNISHED}:false")
                ]
            ]
        else:
            # E'lon joylashtirish uchun
            keyboard = [
                [
                    InlineKeyboardButton("✅ Mebellar bilan", callback_data=f"{CallbackPatterns.LISTING_FURNISHED}:true"),
                    InlineKeyboardButton("❌ Mebellarsiz", callback_data=f"{CallbackPatterns.LISTING_FURNISHED}:false")
                ]
            ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_pets_keyboard(is_search: bool = False) -> InlineKeyboardMarkup:
        """Hayvonlar tanlash klaviaturasi"""
        if is_search:
            # Qidiruv uchun
            keyboard = [
                [
                    InlineKeyboardButton("✅ Hayvonlar ruxsat", callback_data=f"{CallbackPatterns.SEARCH_PETS}:true"),
                    InlineKeyboardButton("❌ Hayvonlar taqiq", callback_data=f"{CallbackPatterns.SEARCH_PETS}:false")
                ]
            ]
        else:
            # E'lon joylashtirish uchun
            keyboard = [
                [
                    InlineKeyboardButton("✅ Hayvonlar ruxsat", callback_data=f"{CallbackPatterns.LISTING_PETS}:true"),
                    InlineKeyboardButton("❌ Hayvonlar taqiq", callback_data=f"{CallbackPatterns.LISTING_PETS}:false")
                ]
            ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_search_execute_keyboard() -> InlineKeyboardMarkup:
        """Qidiruvni bajarish klaviaturasi"""
        keyboard = [
            [InlineKeyboardButton(KeyboardTexts.EXECUTE_SEARCH, callback_data=CallbackPatterns.SEARCH_EXECUTE)],
            [InlineKeyboardButton(KeyboardTexts.BACK_TO_MAIN, callback_data=CallbackPatterns.MAIN_MENU)]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_search_options_keyboard() -> InlineKeyboardMarkup:
        """Qidiruv variantlari klaviaturasi"""
        keyboard = [
            [InlineKeyboardButton("🔍 Qidirish", callback_data=CallbackPatterns.SEARCH_EXECUTE)],
            [InlineKeyboardButton("💰 Narx oralig'i", callback_data=f"{CallbackPatterns.SEARCH_PRICE}:custom")],
            [InlineKeyboardButton("🪑 Mebellar", callback_data=f"{CallbackPatterns.SEARCH_FURNISHED}:filter")],
            [InlineKeyboardButton("🐕 Hayvonlar", callback_data=f"{CallbackPatterns.SEARCH_PETS}:filter")],
            [InlineKeyboardButton(KeyboardTexts.BACK_TO_MAIN, callback_data=CallbackPatterns.MAIN_MENU)]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_cities_keyboard(region_code: str, is_search: bool = False) -> InlineKeyboardMarkup:
        """
        Shahar/tumanlar klaviaturasi
        
        Args:
            region_code: Viloyat kodi
            is_search: Qidiruv uchunmi yoki e'lon joylashtirish uchunmi
        """
        keyboard = []
        
        if is_search:
            # Qidiruv uchun "Barcha shaharlar" variant
            keyboard.append([InlineKeyboardButton(KeyboardTexts.ALL_CITIES, callback_data=f"{CallbackPatterns.SEARCH_CITY}:{region_code}:all")])
        
        # Shaharlarni olish
        if region_code == "all":
            # "Barcha viloyatlar" tanlanganida maxsus ishlov
            cities = ["Barcha shaharlar"]
        else:
            # Barcha viloyatlar uchun to'liq shaharlar ro'yxati
            cities = CITIES_BY_REGION.get(region_code, [
                f"{REGIONS.get(region_code, 'Noma\'lum')} markazi",
                "Boshqa shahar/tuman"
            ])
        
        # Shaharlarni 2 ta qatorda joylashtirish
        for i in range(0, len(cities), 2):
            row = []
            
            # Birinchi shahar
            city = cities[i]
            callback_prefix = CallbackPatterns.SEARCH_CITY if is_search else CallbackPatterns.LISTING_CITY
            row.append(InlineKeyboardButton(city, callback_data=f"{callback_prefix}:{region_code}:{city}"))
            
            # Ikkinchi shahar (agar mavjud bo'lsa)
            if i + 1 < len(cities):
                city2 = cities[i + 1]
                row.append(InlineKeyboardButton(city2, callback_data=f"{callback_prefix}:{region_code}:{city2}"))
            
            keyboard.append(row)
        
        # Orqaga tugmasi
        back_callback = CallbackPatterns.SEARCH_LISTINGS if is_search else CallbackPatterns.POST_LISTING
        keyboard.append([InlineKeyboardButton(KeyboardTexts.BACK, callback_data=back_callback)])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_type_keyboard(is_search: bool = False) -> InlineKeyboardMarkup:
        """E'lon turi klaviaturasi"""
        if is_search:
            # Qidiruv uchun
            keyboard = [
                [InlineKeyboardButton(KeyboardTexts.RENT, callback_data=f"{CallbackPatterns.SEARCH_TYPE}:ijara")],
                [InlineKeyboardButton(KeyboardTexts.SALE, callback_data=f"{CallbackPatterns.SEARCH_TYPE}:sotuv")],
                [InlineKeyboardButton(KeyboardTexts.ALL_TYPES, callback_data=f"{CallbackPatterns.SEARCH_TYPE}:all")]
            ]
        else:
            # E'lon joylashtirish uchun
            keyboard = [
                [InlineKeyboardButton(KeyboardTexts.RENT, callback_data=f"{CallbackPatterns.LISTING_TYPE}:ijara")],
                [InlineKeyboardButton(KeyboardTexts.SALE, callback_data=f"{CallbackPatterns.LISTING_TYPE}:sotuv")]
            ]
        
        keyboard.append([InlineKeyboardButton(KeyboardTexts.BACK_TO_MAIN, callback_data=CallbackPatterns.MAIN_MENU)])
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_rooms_keyboard(is_search: bool = False) -> InlineKeyboardMarkup:
        """Xonalar soni klaviaturasi"""
        if is_search:
            # Qidiruv uchun
            keyboard = [
                [
                    InlineKeyboardButton("1", callback_data=f"{CallbackPatterns.SEARCH_ROOMS}:1"),
                    InlineKeyboardButton("2", callback_data=f"{CallbackPatterns.SEARCH_ROOMS}:2"),
                    InlineKeyboardButton("3", callback_data=f"{CallbackPatterns.SEARCH_ROOMS}:3")
                ],
                [
                    InlineKeyboardButton("4", callback_data=f"{CallbackPatterns.SEARCH_ROOMS}:4"),
                    InlineKeyboardButton("5", callback_data=f"{CallbackPatterns.SEARCH_ROOMS}:5"),
                    InlineKeyboardButton("6+", callback_data=f"{CallbackPatterns.SEARCH_ROOMS}:6")
                ],
                [InlineKeyboardButton(KeyboardTexts.ALL_ROOMS, callback_data=f"{CallbackPatterns.SEARCH_ROOMS}:all")]
            ]
        else:
            # E'lon joylashtirish uchun
            keyboard = [
                [
                    InlineKeyboardButton("1", callback_data=f"{CallbackPatterns.LISTING_ROOMS}:1"),
                    InlineKeyboardButton("2", callback_data=f"{CallbackPatterns.LISTING_ROOMS}:2"),
                    InlineKeyboardButton("3", callback_data=f"{CallbackPatterns.LISTING_ROOMS}:3")
                ],
                [
                    InlineKeyboardButton("4", callback_data=f"{CallbackPatterns.LISTING_ROOMS}:4"),
                    InlineKeyboardButton("5", callback_data=f"{CallbackPatterns.LISTING_ROOMS}:5"),
                    InlineKeyboardButton("6+", callback_data=f"{CallbackPatterns.LISTING_ROOMS}:6")
                ]
            ]
        
        keyboard.append([InlineKeyboardButton(KeyboardTexts.BACK_TO_MAIN, callback_data=CallbackPatterns.MAIN_MENU)])
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_yes_no_keyboard(feature: str, is_search: bool = False) -> InlineKeyboardMarkup:
        """Ha/Yo'q klaviaturasi"""
        callback_prefix = CallbackPatterns.SEARCH_FURNISHED if is_search else CallbackPatterns.LISTING_FURNISHED
        if feature == "pets":
            callback_prefix = CallbackPatterns.SEARCH_PETS if is_search else CallbackPatterns.LISTING_PETS
        
        keyboard = [
            [
                InlineKeyboardButton("✅ Ha", callback_data=f"{callback_prefix}:yes"),
                InlineKeyboardButton("❌ Yo'q", callback_data=f"{callback_prefix}:no")
            ],
            [InlineKeyboardButton(KeyboardTexts.BACK_TO_MAIN, callback_data=CallbackPatterns.MAIN_MENU)]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_price_keyboard(is_search: bool = False) -> InlineKeyboardMarkup:
        """Narx klaviaturasi"""
        if is_search:
            # Qidiruv uchun klaviatura
            keyboard = [
                [InlineKeyboardButton(KeyboardTexts.CUSTOM_PRICE, callback_data=f"{CallbackPatterns.SEARCH_PRICE}:custom")],
                [InlineKeyboardButton(KeyboardTexts.BACK_TO_MAIN, callback_data=CallbackPatterns.MAIN_MENU)]
            ]
        else:
            # E'lon joylashtirish uchun klaviatura - valyuta tanlash
            keyboard = [
                [InlineKeyboardButton("🇺🇸 USD", callback_data=f"{CallbackPatterns.LISTING_CURRENCY}:USD")],
                [InlineKeyboardButton("🇺🇿 UZS", callback_data=f"{CallbackPatterns.LISTING_CURRENCY}:UZS")],
                [InlineKeyboardButton(KeyboardTexts.BACK, callback_data=CallbackPatterns.LISTING_ROOMS)]
            ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_search_filters_keyboard() -> InlineKeyboardMarkup:
        """Qidiruv filtrlari klaviaturasi"""
        keyboard = [
            [InlineKeyboardButton(KeyboardTexts.FURNISHED, callback_data=f"{CallbackPatterns.SEARCH_FURNISHED}:filter")],
            [InlineKeyboardButton(KeyboardTexts.PETS_ALLOWED, callback_data=f"{CallbackPatterns.SEARCH_PETS}:filter")],
            [InlineKeyboardButton(KeyboardTexts.EXECUTE_SEARCH, callback_data=CallbackPatterns.SEARCH_EXECUTE)],
            [InlineKeyboardButton(KeyboardTexts.BACK_TO_MAIN, callback_data=CallbackPatterns.MAIN_MENU)]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_pagination_keyboard(
        current_page: int, 
        total_pages: int, 
        callback_prefix: str = CallbackPatterns.SEARCH_PAGE
    ) -> InlineKeyboardMarkup:
        """Pagination klaviaturasi"""
        keyboard = []
        
        if total_pages > 1:
            nav_row = []
            
            if current_page > 0:
                nav_row.append(InlineKeyboardButton(KeyboardTexts.PREV_PAGE, callback_data=f"{callback_prefix}:{current_page - 1}"))
            
            nav_row.append(InlineKeyboardButton(f"{current_page + 1}/{total_pages}", callback_data="PAGE_INFO"))
            
            if current_page < total_pages - 1:
                nav_row.append(InlineKeyboardButton(KeyboardTexts.NEXT_PAGE, callback_data=f"{callback_prefix}:{current_page + 1}"))
            
            keyboard.append(nav_row)
        
        # Boshqa tugmalar
        keyboard.append([
            InlineKeyboardButton(KeyboardTexts.REFRESH_SEARCH, callback_data=CallbackPatterns.SEARCH_LISTINGS),
            InlineKeyboardButton(KeyboardTexts.BACK_TO_MAIN, callback_data=CallbackPatterns.MAIN_MENU)
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_listing_preview_keyboard() -> InlineKeyboardMarkup:
        """E'lon preview klaviaturasi"""
        keyboard = [
            [
                InlineKeyboardButton("✅ Yuborish", callback_data=CallbackPatterns.LISTING_SUBMIT),
                InlineKeyboardButton(KeyboardTexts.CANCEL, callback_data=CallbackPatterns.LISTING_CANCEL)
            ]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def create_description_skip_keyboard() -> InlineKeyboardMarkup:
        """Tavsif o'tkazish klaviaturasi"""
        keyboard = [
            [InlineKeyboardButton(KeyboardTexts.SKIP_DESCRIPTION, callback_data=CallbackPatterns.LISTING_SKIP_DESCRIPTION)],
            [InlineKeyboardButton(KeyboardTexts.BACK_TO_MAIN, callback_data=CallbackPatterns.MAIN_MENU)]
        ]
        return InlineKeyboardMarkup(keyboard)
