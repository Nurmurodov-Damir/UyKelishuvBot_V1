"""
Listing Handlers - E'lon joylashtirish va qidirish handlerlari (Clean Code)
"""
import logging
from typing import Dict, Any, List, Optional
from telegram import Update
from telegram.ext import ContextTypes
from src.services.listing_service import ListingService
from src.services.validation_service import ValidationService, ErrorHandler
from src.services.keyboard_builder import KeyboardBuilder
from src.services.message_builder import MessageBuilder
from src.utils.constants import CallbackPatterns, BotConstants
from src.config import REGIONS
from src.database.database import AsyncSessionLocal
from src.database.models import Listing, ListingStatus

logger = logging.getLogger(__name__)


class ListingHandlers:
    """E'lon joylashtirish va qidirish handlerlari"""
    
    def __init__(self, listing_service: ListingService):
        self.listing_service = listing_service
        self.user_data: Dict[int, Dict[str, Any]] = {}
        self.search_data: Dict[int, Dict[str, Any]] = {}
        self.keyboard_builder = KeyboardBuilder()
        self.message_builder = MessageBuilder()
        self.validator = ValidationService()
    
    # ==================== LISTING CREATION HANDLERS ====================
    
    async def handle_post_listing(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """E'lon joylashtirishni boshlash"""
        try:
            user_id = update.effective_user.id
            self.user_data[user_id] = {}
            
            await update.callback_query.edit_message_text(
                self.message_builder.create_listing_start_message(),
                reply_markup=self.keyboard_builder.create_regions_keyboard(is_search=False),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_post_listing")
            await update.callback_query.answer(self.message_builder.create_error_message("generic"))
    
    async def handle_region_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE, region_code: str) -> None:
        """Viloyat tanlash"""
        try:
            user_id = update.effective_user.id
            
            # Viloyat kodini tekshirish
            is_valid, error = self.validator.validate_region_code(region_code)
            if not is_valid:
                await update.callback_query.edit_message_text(
                    self.message_builder.create_error_message("generic", error),
                    reply_markup=self.keyboard_builder.create_regions_keyboard(is_search=False)
                )
                return
            
            # Viloyat ma'lumotlarini saqlash
            self.user_data[user_id]['region_code'] = region_code
            self.user_data[user_id]['region_name'] = REGIONS[region_code]
            
            await update.callback_query.edit_message_text(
                self.message_builder.create_region_selection_message(REGIONS[region_code], is_search=False),
                reply_markup=self.keyboard_builder.create_cities_keyboard(region_code, is_search=False),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_region_selection")
            await update.callback_query.answer(self.message_builder.create_error_message("generic"))
    
    async def handle_city_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE, region_code: str, city_name: str) -> None:
        """Shahar tanlash"""
        try:
            user_id = update.effective_user.id
            
            # Shahar nomini saqlash
            self.user_data[user_id]['city_name'] = city_name
            
            region_name = REGIONS.get(region_code, 'Noma\'lum')
            
            await update.callback_query.edit_message_text(
                self.message_builder.create_city_selection_message(region_name, city_name, is_search=False),
                reply_markup=self.keyboard_builder.create_type_keyboard(is_search=False),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_city_selection")
            await update.callback_query.answer(self.message_builder.create_error_message("generic"))
    
    async def handle_type_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE, listing_type: str) -> None:
        """E'lon turi tanlash"""
        try:
            user_id = update.effective_user.id
            
            # E'lon turini saqlash
            self.user_data[user_id]['type'] = listing_type
            
            type_name = "Ijara" if listing_type == "ijara" else "Sotuv"
            
            await update.callback_query.edit_message_text(
                self.message_builder.create_type_selection_message(type_name, is_search=False),
                reply_markup=self.keyboard_builder.create_rooms_keyboard(is_search=False),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_type_selection")
            await update.callback_query.answer(self.message_builder.create_error_message("generic"))
    
    async def handle_rooms_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE, rooms: str) -> None:
        """Xonalar soni tanlash"""
        try:
            user_id = update.effective_user.id
            
            # Xonalar sonini tekshirish va saqlash
            rooms_int = int(rooms) if rooms.isdigit() else 6
            is_valid, error = self.validator.validate_rooms(rooms_int)
            
            if not is_valid:
                await update.callback_query.edit_message_text(
                    self.message_builder.create_error_message("generic", error),
                    reply_markup=self.keyboard_builder.create_rooms_keyboard(is_search=False)
                )
                return
            
            self.user_data[user_id]['rooms'] = rooms_int
            
            rooms_text = "6+" if rooms == "6" else f"{rooms_int} xona"
            
            await update.callback_query.edit_message_text(
                self.message_builder.create_rooms_selection_message(rooms_text, is_search=False),
                reply_markup=self.keyboard_builder.create_price_keyboard(is_search=False),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_rooms_selection")
            await update.callback_query.answer(self.message_builder.create_error_message("generic"))
    
    async def handle_price_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Narx kiritish"""
        try:
            user_id = update.effective_user.id
            price_text = update.message.text.strip()
            
            # Narxni tekshirish
            is_valid, price, error = self.validator.validate_price(price_text)
            
            if not is_valid:
                await update.message.reply_text(
                    self.message_builder.create_error_message("generic", error),
                    reply_markup=self.keyboard_builder.create_back_button()
                )
                return
            
            # Narxni saqlash
            self.user_data[user_id]['price'] = price
            context.user_data['waiting_for_price'] = False
            
            # Keyingi qadamga o'tish
            await update.message.reply_text(
                f"Narx: {price} USD\n\nE'lon sarlavhasini kiriting:",
                reply_markup=self.keyboard_builder.create_back_button()
            )
            
            # Sarlavha kiritish uchun kutish
            context.user_data['waiting_for_title'] = True
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_price_input")
            await update.message.reply_text(self.message_builder.create_error_message("generic"))
    
    async def handle_title_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Sarlavha kiritish"""
        try:
            user_id = update.effective_user.id
            title = update.message.text.strip()
            
            # Sarlavhani tekshirish
            is_valid, cleaned_title, error = self.validator.validate_title(title)
            
            if not is_valid:
                await update.message.reply_text(
                    self.message_builder.create_error_message("generic", error),
                    reply_markup=self.keyboard_builder.create_back_button()
                )
                return
            
            # Sarlavhani saqlash
            self.user_data[user_id]['title'] = cleaned_title
            context.user_data['waiting_for_title'] = False
            
            # Tavsif kiritish uchun kutish
            await update.message.reply_text(
                f"Sarlavha: {cleaned_title}\n\nE'lon tavsifini kiriting (ixtiyoriy):",
                reply_markup=self.keyboard_builder.create_description_skip_keyboard()
            )
            
            context.user_data['waiting_for_description'] = True
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_title_input")
            await update.message.reply_text(self.message_builder.create_error_message("generic"))
    
    async def handle_description_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Tavsif kiritish"""
        try:
            user_id = update.effective_user.id
            description = update.message.text.strip()
            
            # Tavsifni tekshirish
            is_valid, cleaned_description, error = self.validator.validate_description(description)
            
            if not is_valid:
                await update.message.reply_text(
                    self.message_builder.create_error_message("generic", error),
                    reply_markup=self.keyboard_builder.create_back_button()
                )
                return
            
            # Tavsifni saqlash
            self.user_data[user_id]['description'] = cleaned_description
            context.user_data['waiting_for_description'] = False
            
            # E'lon preview ko'rsatish
            await self.show_listing_preview(update, context)
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_description_input")
            await update.message.reply_text(self.message_builder.create_error_message("generic"))
    
    async def show_listing_preview(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """E'lon preview ko'rsatish"""
        try:
            user_id = update.effective_user.id
            listing_data = self.user_data.get(user_id, {})
            
            if not listing_data:
                await update.message.reply_text(
                    self.message_builder.create_error_message("missing_data"),
                    reply_markup=self.keyboard_builder.create_back_button()
                )
                return
            
            # E'lon ma'lumotlarini tekshirish
            is_valid, error = self.validator.validate_listing_data(listing_data)
            if not is_valid:
                await update.message.reply_text(
                    self.message_builder.create_error_message("generic", error),
                    reply_markup=self.keyboard_builder.create_back_button()
                )
                return
            
            await update.message.reply_text(
                self.message_builder.create_listing_preview_message(listing_data),
                reply_markup=self.keyboard_builder.create_listing_preview_keyboard(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            ErrorHandler.log_error(e, "show_listing_preview")
            await update.message.reply_text(self.message_builder.create_error_message("generic"))
    
    async def handle_listing_submit(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """E'lonni yuborish"""
        try:
            user_id = update.effective_user.id
            listing_data = self.user_data.get(user_id, {})
            
            if not listing_data:
                await update.callback_query.edit_message_text(
                    self.message_builder.create_error_message("missing_data"),
                    reply_markup=self.keyboard_builder.create_back_button()
                )
                return
            
            # Database operatsiyasi
            async with AsyncSessionLocal() as db:
                from src.services.user_service import UserService
                user_service = UserService(db)
                user_db = await user_service.get_user_by_telegram_id(user_id)
                
                if not user_db:
                    await update.callback_query.edit_message_text(
                        self.message_builder.create_error_message("user_not_found"),
                        reply_markup=self.keyboard_builder.create_back_button()
                    )
                    return
                
                # Listing service ni yangi session bilan ishga tushirish
                self.listing_service.db = db
                
                # E'lonni database ga saqlash
                listing = await self.listing_service.create_listing(user_db.id, listing_data)
                
                if listing:
                    # Muvaffaqiyat
                    del self.user_data[user_id]
                    await update.callback_query.edit_message_text(
                        self.message_builder.create_success_message("listing_created"),
                        reply_markup=self.keyboard_builder.create_back_button(),
                        parse_mode='Markdown'
                    )
                else:
                    await update.callback_query.edit_message_text(
                        self.message_builder.create_error_message("generic", "E'lon yuborishda xatolik yuz berdi"),
                        reply_markup=self.keyboard_builder.create_back_button()
                    )
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_listing_submit")
            await update.callback_query.answer(self.message_builder.create_error_message("generic"))
    
    async def handle_listing_cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """E'lonni bekor qilish"""
        try:
            user_id = update.effective_user.id
            
            # Foydalanuvchi ma'lumotlarini tozalash
            if user_id in self.user_data:
                del self.user_data[user_id]
            
            await update.callback_query.edit_message_text(
                "❌ E'lon joylashtirish bekor qilindi.",
                reply_markup=self.keyboard_builder.create_back_button()
            )
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_listing_cancel")
            await update.callback_query.answer(self.message_builder.create_error_message("generic"))
    
    # ==================== SEARCH HANDLERS ====================
    
    async def handle_search_listings(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """E'lon qidirishni boshlash"""
        try:
            user_id = update.effective_user.id
            self.search_data[user_id] = {}
            
            await update.callback_query.edit_message_text(
                self.message_builder.create_search_start_message(),
                reply_markup=self.keyboard_builder.create_regions_keyboard(is_search=True),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_search_listings")
            await update.callback_query.answer(self.message_builder.create_error_message("generic"))
    
    async def handle_search_region_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE, region_code: str) -> None:
        """Qidiruv uchun viloyat tanlash"""
        try:
            user_id = update.effective_user.id
            
            # Viloyat kodini saqlash
            self.search_data[user_id]['region_code'] = region_code
            if region_code != 'all':
                self.search_data[user_id]['region_name'] = REGIONS[region_code]
            
            region_text = "Barcha viloyatlar" if region_code == 'all' else REGIONS[region_code]
            
            await update.callback_query.edit_message_text(
                self.message_builder.create_region_selection_message(region_text, is_search=True),
                reply_markup=self.keyboard_builder.create_cities_keyboard(region_code, is_search=True),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_search_region_selection")
            await update.callback_query.answer(self.message_builder.create_error_message("generic"))
    
    async def handle_search_city_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE, region_code: str, city_name: str) -> None:
        """Qidiruv uchun shahar tanlash"""
        try:
            user_id = update.effective_user.id
            
            # Shahar nomini saqlash
            self.search_data[user_id]['city_name'] = city_name
            
            region_text = "Barcha viloyatlar" if region_code == 'all' else REGIONS[region_code]
            city_text = "Barcha shaharlar" if city_name == 'all' else city_name
            
            await update.callback_query.edit_message_text(
                self.message_builder.create_city_selection_message(region_text, city_text, is_search=True),
                reply_markup=self.keyboard_builder.create_type_keyboard(is_search=True),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_search_city_selection")
            await update.callback_query.answer(self.message_builder.create_error_message("generic"))
    
    async def handle_search_type_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE, listing_type: str) -> None:
        """Qidiruv uchun e'lon turi tanlash"""
        try:
            user_id = update.effective_user.id
            
            # E'lon turini saqlash
            self.search_data[user_id]['type'] = listing_type
            
            type_name = "Ijara" if listing_type == "ijara" else "Sotuv" if listing_type == "sotuv" else "Barcha turlar"
            
            await update.callback_query.edit_message_text(
                self.message_builder.create_type_selection_message(type_name, is_search=True),
                reply_markup=self.keyboard_builder.create_rooms_keyboard(is_search=True),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_search_type_selection")
            await update.callback_query.answer(self.message_builder.create_error_message("generic"))
    
    async def handle_search_rooms_selection(self, update: Update, context: ContextTypes.DEFAULT_TYPE, rooms: str) -> None:
        """Qidiruv uchun xonalar soni tanlash"""
        try:
            user_id = update.effective_user.id
            
            # Xonalar sonini saqlash
            self.search_data[user_id]['rooms'] = rooms
            
            rooms_text = "Barcha" if rooms == 'all' else f"{rooms} xona"
            
            await update.callback_query.edit_message_text(
                self.message_builder.create_rooms_selection_message(rooms_text, is_search=True),
                reply_markup=self.keyboard_builder.create_price_keyboard(is_search=True),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_search_rooms_selection")
            await update.callback_query.answer(self.message_builder.create_error_message("generic"))
    
    async def handle_search_price_custom(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Qidiruv uchun narx oralig'ini kiritish"""
        try:
            await update.callback_query.edit_message_text(
                self.message_builder.create_price_input_message(),
                reply_markup=self.keyboard_builder.create_back_button()
            )
            
            # Narx kiritish uchun kutish
            context.user_data['waiting_for_price_range'] = True
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_search_price_custom")
            await update.callback_query.answer(self.message_builder.create_error_message("generic"))
    
    async def handle_search_price_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Qidiruv uchun narx kiritish"""
        try:
            user_id = update.effective_user.id
            price_text = update.message.text.strip()
            
            # Narx formatini tekshirish va parse qilish
            is_valid, min_price, max_price, error = self.validator.validate_price_range(price_text)
            
            if not is_valid:
                await update.message.reply_text(
                    self.message_builder.create_error_message("generic", error),
                    reply_markup=self.keyboard_builder.create_back_button()
                )
                return
            
            # Narxni saqlash
            if min_price is not None:
                self.search_data[user_id]['min_price'] = min_price
            if max_price is not None:
                self.search_data[user_id]['max_price'] = max_price
            
            # Narx kiritishni to'xtatish
            context.user_data['waiting_for_price_range'] = False
            
            # Qidiruv filtrlari sahifasiga o'tish
            await update.message.reply_text(
                self.message_builder.create_price_confirmation_message(min_price, max_price),
                reply_markup=self.keyboard_builder.create_search_filters_keyboard(),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_search_price_input")
            await update.message.reply_text(self.message_builder.create_error_message("generic"))
    
    async def handle_search_execute(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Qidiruvni bajarish"""
        try:
            user_id = update.effective_user.id
            search_filters = self.search_data.get(user_id, {})
            
            if not search_filters:
                await update.callback_query.edit_message_text(
                    self.message_builder.create_error_message("missing_data"),
                    reply_markup=self.keyboard_builder.create_back_button()
                )
                return
            
            # Database dan qidiruv
            async with AsyncSessionLocal() as db:
                self.listing_service.db = db
                
                # Filtrlarni tozalash
                clean_filters = self._clean_search_filters(search_filters)
                
                # Qidiruvni bajarish
                listings = await self.listing_service.search_listings(clean_filters)
                
                if listings:
                    # Natijalarni ko'rsatish
                    await self._show_search_results(update, context, listings)
                else:
                    await update.callback_query.edit_message_text(
                        self.message_builder.create_no_search_results_message(),
                        reply_markup=self.keyboard_builder.create_search_filters_keyboard()
                    )
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_search_execute")
            await update.callback_query.answer(self.message_builder.create_error_message("generic"))
    
    async def _show_search_results(self, update: Update, context: ContextTypes.DEFAULT_TYPE, listings: List[Listing]) -> None:
        """Qidiruv natijalarini ko'rsatish"""
        try:
            user_id = update.effective_user.id
            
            # Natijalarni saqlash (pagination uchun)
            context.user_data[f'search_results_{user_id}'] = listings
            context.user_data[f'search_page_{user_id}'] = 0
            
            # Birinchi sahifani ko'rsatish
            await self._show_search_page(update, context, listings, 0)
            
        except Exception as e:
            ErrorHandler.log_error(e, "_show_search_results")
            await update.callback_query.answer(self.message_builder.create_error_message("generic"))
    
    async def _show_search_page(self, update: Update, context: ContextTypes.DEFAULT_TYPE, listings: List[Listing], page: int) -> None:
        """Qidiruv sahifasini ko'rsatish"""
        try:
            await update.callback_query.edit_message_text(
                self.message_builder.create_search_results_message(listings, page),
                reply_markup=self.keyboard_builder.create_pagination_keyboard(page, len(listings) // BotConstants.ITEMS_PER_PAGE + 1),
                parse_mode='Markdown'
            )
            
        except Exception as e:
            ErrorHandler.log_error(e, "_show_search_page")
            await update.callback_query.answer(self.message_builder.create_error_message("generic"))
    
    def _clean_search_filters(self, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Qidiruv filtrlarini tozalash"""
        clean_filters = {}
        
        # Faqat None bo'lmagan va 'all' bo'lmagan qiymatlarni qo'shish
        for key, value in filters.items():
            if value is not None and value != 'all':
                clean_filters[key] = value
        
        return clean_filters
