"""
Message Builder Service - Xabar yaratish xizmati
"""
from typing import List, Optional
from src.utils.constants import UIMessages, SuccessMessages, ErrorMessages
from src.config import REGIONS
from src.database.models import Listing

class MessageBuilder:
    """Xabar yaratish xizmati"""
    
    @staticmethod
    def create_welcome_message(name: str) -> str:
        """Xush kelibsiz xabari"""
        return UIMessages.WELCOME.format(name=name)
    
    @staticmethod
    def create_help_message() -> str:
        """Yordam xabari"""
        return UIMessages.HELP_TEXT
    
    @staticmethod
    def create_search_start_message() -> str:
        """Qidiruv boshlash xabari"""
        return UIMessages.SEARCH_START
    
    @staticmethod
    def create_listing_start_message() -> str:
        """E'lon joylashtirish boshlash xabari"""
        return UIMessages.LISTING_START
    
    @staticmethod
    def create_region_selection_message(region_name: str, is_search: bool = False) -> str:
        """Viloyat tanlash xabari"""
        action = "qidirish" if is_search else "joylashtirish"
        return f"🔍 **E'lon {action}**\n\nViloyat: {region_name}\n\nEndi shahar/tumanni tanlang:"
    
    @staticmethod
    def create_city_selection_message(region_name: str, city_name: str, is_search: bool = False) -> str:
        """Shahar tanlash xabari"""
        action = "qidirish" if is_search else "joylashtirish"
        return f"🔍 **E'lon {action}**\n\nViloyat: {region_name}\nShahar: {city_name}\n\nEndi e'lon turini tanlang:"
    
    @staticmethod
    def create_type_selection_message(type_name: str, is_search: bool = False) -> str:
        """E'lon turi tanlash xabari"""
        action = "qidirish" if is_search else "joylashtirish"
        if type_name == "Ijara":
            return f"🔍 **E'lon {action}**\n\nE'lon turi: {type_name}\n\nEndi uy turini tanlang:"
        else:
            return f"🔍 **E'lon {action}**\n\nE'lon turi: {type_name}\n\nEndi xonalar sonini tanlang:"
    
    @staticmethod
    def create_property_type_selection_message(property_type_name: str) -> str:
        """Uy turi tanlash xabari"""
        return f"🔍 **E'lon joylashtirish**\n\nUy turi: {property_type_name}\n\nEndi xonalar sonini tanlang:"
    
    @staticmethod
    def create_rooms_selection_message(rooms_text: str, is_search: bool = False) -> str:
        """Xonalar soni tanlash xabari"""
        action = "qidirish" if is_search else "joylashtirish"
        return f"🔍 **E'lon {action}**\n\nXonalar soni: {rooms_text}\n\nNarx oralig'ini belgilang:"
    
    @staticmethod
    def create_price_input_message() -> str:
        """Narx kiritish xabari"""
        return """🔍 **E'lon qidirish**

Narx oralig'ini kiriting:

Masalan: 100-500
yoki: 500+ (500 dan yuqori)
yoki: 500 (aniq narx)"""
    
    @staticmethod
    def create_price_confirmation_message(min_price: Optional[float], max_price: Optional[float]) -> str:
        """Narx tasdiqlash xabari"""
        price_text = MessageBuilder._format_price_range(min_price, max_price)
        return f"🔍 **E'lon qidirish**\n\nNarx: {price_text}\n\nQo'shimcha filtrlarni tanlang:"
    
    @staticmethod
    def create_search_filters_message() -> str:
        """Qidiruv filtrlari xabari"""
        return "🔍 **E'lon qidirish**\n\nQo'shimcha filtrlarni tanlang:"
    
    @staticmethod
    def create_search_results_message(listings: List[Listing], current_page: int) -> str:
        """Qidiruv natijalari xabari"""
        if not listings:
            return "🔍 **Qidiruv natijalari**\n\nBu sahifada e'lonlar yo'q."
        
        text = f"🔍 **Qidiruv natijalari** ({len(listings)} ta e'lon topildi)\n\n"
        
        items_per_page = 5
        start_idx = current_page * items_per_page
        
        for i, listing in enumerate(listings[start_idx:start_idx + items_per_page], start_idx + 1):
            text += MessageBuilder._format_listing_item(listing, i)
        
        return text
    
    @staticmethod
    def create_no_search_results_message() -> str:
        """Qidiruv natijalari yo'q xabari"""
        return """🔍 **Qidiruv natijalari**

Sizning qidiruv mezonlaringizga mos e'lonlar topilmadi.

Qidiruv mezonlarini o'zgartirib qaytadan urinib ko'ring."""
    
    @staticmethod
    def create_listing_preview_message(listing_data: dict) -> str:
        """E'lon preview xabari"""
        region_name = REGIONS.get(listing_data.get('region_code', ''), 'Noma\'lum')
        type_name = "Ijara" if listing_data.get('type') == 'ijara' else "Sotuv"
        furnished_text = "✅" if listing_data.get('furnished') else "❌"
        pets_text = "✅" if listing_data.get('pets_allowed') else "❌"
        
        text = "📋 **E'lon ko'rinishi**\n\n"
        text += f"**Sarlavha:** {listing_data.get('title', 'Noma\'lum')}\n"
        text += f"**Joylashuv:** {region_name} - {listing_data.get('city_name', 'Noma\'lum')}\n"
        text += f"**Turi:** {type_name}\n"
        text += f"**Xonalar:** {listing_data.get('rooms', 'Noma\'lum')} xona\n"
        text += f"**Narx:** {listing_data.get('price', 'Noma\'lum')} {listing_data.get('currency', 'USD')}\n"
        text += f"**Mebellar:** {furnished_text}\n"
        text += f"**Hayvonlar:** {pets_text}\n"
        
        if listing_data.get('description'):
            text += f"**Tavsif:** {listing_data.get('description')}\n"
        
        text += "\nE'loni yuborishni tasdiqlaysizmi?"
        
        return text
    
    @staticmethod
    def create_success_message(message_type: str) -> str:
        """Muvaffaqiyat xabari"""
        if message_type == "listing_created":
            return SuccessMessages.LISTING_CREATED
        elif message_type == "listing_updated":
            return SuccessMessages.LISTING_UPDATED
        elif message_type == "listing_deleted":
            return SuccessMessages.LISTING_DELETED
        else:
            return "✅ Amal muvaffaqiyatli bajarildi!"
    
    @staticmethod
    def create_error_message(error_type: str, custom_message: Optional[str] = None) -> str:
        """Xatolik xabari"""
        if custom_message:
            return f"❌ {custom_message}"
        
        error_messages = {
            "invalid_price": ErrorMessages.INVALID_PRICE,
            "invalid_title": ErrorMessages.INVALID_TITLE,
            "invalid_rooms": ErrorMessages.INVALID_ROOMS,
            "missing_data": ErrorMessages.MISSING_DATA,
            "user_not_found": ErrorMessages.USER_NOT_FOUND,
            "listing_not_found": ErrorMessages.LISTING_NOT_FOUND,
            "no_search_results": ErrorMessages.NO_SEARCH_RESULTS,
            "generic": ErrorMessages.GENERIC_ERROR
        }
        
        return error_messages.get(error_type, ErrorMessages.GENERIC_ERROR)
    
    @staticmethod
    def create_validation_error_message(field: str, error: str) -> str:
        """Validatsiya xatolik xabari"""
        return f"❌ **{field}** maydonida xatolik:\n\n{error}"
    
    @staticmethod
    def create_price_input_error_message() -> str:
        """Narx kiritish xatolik xabari"""
        return """❌ Noto'g'ri narx format!

To'g'ri formatlar:
• 100-500 (oralik)
• 500+ (500 dan yuqori)
• 500 (aniq narx)"""
    
    @staticmethod
    def create_title_input_error_message(min_length: int = 5, max_length: int = 255) -> str:
        """Sarlavha kiritish xatolik xabari"""
        return f"""❌ Sarlavha noto'g'ri!

Kamida {min_length} ta, maksimum {max_length} ta belgi kiriting."""
    
    @staticmethod
    def create_rooms_input_error_message(min_rooms: int = 1, max_rooms: int = 10) -> str:
        """Xonalar soni kiritish xatolik xabari"""
        return f"""❌ Xonalar soni noto'g'ri!

{min_rooms} dan {max_rooms} gacha raqam kiriting."""
    
    # Private helper methods
    @staticmethod
    def _format_price_range(min_price: Optional[float], max_price: Optional[float]) -> str:
        """Narx oralig'ini formatlash"""
        if min_price is not None and max_price is not None:
            if min_price == max_price:
                return f"{min_price} USD"
            else:
                return f"{min_price}-{max_price} USD"
        elif min_price is not None:
            return f"{min_price}+ USD"
        else:
            return "Cheklanmagan"
    
    @staticmethod
    def _format_listing_item(listing: Listing, index: int) -> str:
        """E'lon elementini formatlash"""
        type_name = "Ijara" if listing.type.value == "ijara" else "Sotuv"
        furnished_text = "✅" if listing.furnished else "❌"
        pets_text = "✅" if listing.pets_allowed else "❌"
        region_name = REGIONS.get(listing.region_code, listing.region_code)
        
        text = f"**{index}. {listing.title}**\n"
        text += f"📍 {region_name} - {listing.city_name}\n"
        text += f"🏠 {type_name} • {listing.rooms} xona • {listing.price} {listing.currency}\n"
        text += f"🪑 Mebellar: {furnished_text} • 🐕 Hayvonlar: {pets_text}\n"
        text += f"👤 {listing.owner.name}\n\n"
        
        return text
