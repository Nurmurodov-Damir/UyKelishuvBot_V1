"""
UyKelishuv Telegram Bot Client
"""
import logging
from typing import Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, 
    CommandHandler, 
    CallbackQueryHandler, 
    MessageHandler, 
    filters, 
    ContextTypes
)

from src.config import settings
from src.services.keyboard_builder import KeyboardBuilder
from src.services.message_builder import MessageBuilder
from src.services.validation_service import ErrorHandler
from src.database.database import AsyncSessionLocal
from src.services.user_service import UserService
from src.services.listing_service import ListingService
from src.services.admin_service import AdminService
from src.bot.handlers.listing_handlers import ListingHandlers
from src.bot.handlers.admin_handlers import AdminHandlers
from src.utils.constants import CallbackPatterns

logger = logging.getLogger(__name__)


class UyKelishuvBot:
    """UyKelishuv Bot asosiy klassi"""
    
    def __init__(self):
        self.application = Application.builder().token(settings.bot_token).build()
        self.keyboard_builder = KeyboardBuilder()
        self.message_builder = MessageBuilder()
        self.user_service = UserService()
        self.listing_service = ListingService()
        self.admin_service = AdminService()
        self.listing_handlers = ListingHandlers(self.listing_service)
        self.admin_handlers = AdminHandlers(self.admin_service)
        logger.info("Bot ishga tushirilmoqda...")
        
    async def start(self):
        """Botni ishga tushirish"""
        try:
            self._register_handlers()
            logger.info("Bot muvaffaqiyatli ishga tushdi")
        except Exception as e:
            logger.error(f"Bot ishga tushishda xatolik: {e}")
            raise
    
    def _register_handlers(self):
        """Handlerlarni ro'yxatdan o'tkazish"""
        try:
            logger.info("Handlerlarni ro'yxatdan o'tkazish boshlandi...")
            
            self.application.add_handler(CommandHandler("start", self._handle_start))
            logger.info("✅ Start handler qo'shildi")
            
            self.application.add_handler(CommandHandler("help", self._handle_help))
            logger.info("✅ Help handler qo'shildi")
            
            self.application.add_handler(CommandHandler("admin", self._handle_admin))
            logger.info("✅ Admin handler qo'shildi")
            
            self.application.add_handler(CallbackQueryHandler(self._handle_callback))
            logger.info("✅ Callback handler qo'shildi")
            
            self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self._handle_message))
            logger.info("✅ Message handler qo'shildi")
            
            logger.info("Handlerlar muvaffaqiyatli ro'yxatdan o'tkazildi")
            
        except Exception as e:
            logger.error(f"Handlerlarni ro'yxatdan o'tkazishda xatolik: {e}")
            raise
    
    async def _handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start komandasi handler"""
        try:
            user = update.effective_user
            if not user:
                return
            
            async with AsyncSessionLocal() as db:
                self.user_service.db = db
                self.listing_service.db = db
                
                # Foydalanuvchini olish yoki yaratish
                user_db = await self.user_service.get_user_by_telegram_id(user.id)
                if not user_db:
                    user_db = await self.user_service.create_user(
                        telegram_user_id=user.id,
                        name=user.first_name or 'User'
                    )
                
                # Xush kelibsiz xabari
                welcome_text = self._get_welcome_message(user.first_name or 'User')
                keyboard = self.keyboard_builder.create_main_menu()
                
                await update.message.reply_text(
                    welcome_text,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
                
        except Exception as e:
            logger.error(f"Start handler xatoligi: {e}")
            await update.message.reply_text("❌ Xatolik yuz berdi")
    
    async def _handle_help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help komandasi handler"""
        help_text = """
📖 **Yordam**

Bu bot uy-joy kelishuvi uchun yaratilgan.

**Asosiy funksiyalar:**
• 📝 E'lon joylashtirish
• 🔍 Uy qidirish
• 👤 Profil boshqarish
• 💬 Ega bilan aloqa

**Komandalar:**
/start - Botni ishga tushirish
/help - Yordam olish
        """
        
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 Asosiy menyu", callback_data='MAIN_MENU')
        ]])
        
        await update.message.reply_text(
            help_text,
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
    
    async def _handle_admin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Admin komandasi handler"""
        try:
            user_id = update.effective_user.id
            
            # Admin huquqini tekshirish
            if not self.admin_service.is_admin(user_id):
                await update.message.reply_text(
                    "❌ Sizda admin huquqi yo'q!",
                    reply_markup=self.keyboard_builder.create_back_button()
                )
                return
            
            # Admin panelni ochish
            async with AsyncSessionLocal() as db:
                self.admin_service.db = db
                stats = await self.admin_service.get_statistics()
                
                message = self.admin_handlers._create_admin_panel_message(stats)
                keyboard = self.admin_handlers._create_admin_panel_keyboard()
                
                await update.message.reply_text(
                    message,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
            
        except Exception as e:
            ErrorHandler.log_error(e, "_handle_admin")
            await update.message.reply_text(self.message_builder.create_error_message("generic"))
    
    async def _handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Callback query handler"""
        try:
            query = update.callback_query
            await query.answer()
            
            data = query.data
            
            if data == CallbackPatterns.MAIN_MENU:
                # Admin ekanligini tekshirish
                is_admin = self.admin_service.is_admin(update.effective_user.id)
                keyboard = self.keyboard_builder.create_main_menu(is_admin=is_admin)
                await query.edit_message_text(
                    "🏠 Asosiy menyu",
                    reply_markup=keyboard
                )
            
            elif data == CallbackPatterns.POST_LISTING:
                await self.listing_handlers.handle_post_listing(update, context)
            
            # E'lon joylashtirish callback handlerlari
            elif data.startswith(f'{CallbackPatterns.LISTING_REGION}:'):
                region_code = data.split(':')[1]
                await self.listing_handlers.handle_region_selection(update, context, region_code)
            
            elif data.startswith(f'{CallbackPatterns.LISTING_CITY}:'):
                parts = data.split(':')
                region_code = parts[1]
                city_name = ':'.join(parts[2:])  # Shahar nomida ':' bo'lishi mumkin
                await self.listing_handlers.handle_city_selection(update, context, region_code, city_name)
            
            elif data.startswith(f'{CallbackPatterns.LISTING_TYPE}:'):
                listing_type = data.split(':')[1]
                await self.listing_handlers.handle_type_selection(update, context, listing_type)
            
            elif data.startswith(f'{CallbackPatterns.LISTING_PROPERTY_TYPE}:'):
                property_type = data.split(':')[1]
                await self.listing_handlers.handle_property_type_selection(update, context, property_type)
            
            elif data.startswith(f'{CallbackPatterns.LISTING_ROOMS}:'):
                rooms = data.split(':')[1]
                await self.listing_handlers.handle_rooms_selection(update, context, rooms)
            
            elif data.startswith(f'{CallbackPatterns.LISTING_CURRENCY}:'):
                currency_code = data.split(':')[1]
                await self.listing_handlers.handle_currency_selection(update, context, currency_code)
            
            elif data.startswith(f'{CallbackPatterns.LISTING_FURNISHED}:'):
                furnished = data.split(':')[1]
                await self.listing_handlers.handle_furniture_selection(update, context, furnished)
            
            elif data.startswith(f'{CallbackPatterns.LISTING_PETS}:'):
                pets_allowed = data.split(':')[1]
                await self.listing_handlers.handle_pets_selection(update, context, pets_allowed)
            
            elif data == CallbackPatterns.LISTING_SUBMIT:
                await self.listing_handlers.handle_listing_submit(update, context)
            
            elif data == "CONFIRM_LISTING":
                await self.listing_handlers.handle_confirm_listing(update, context)
            
            elif data == CallbackPatterns.LISTING_CANCEL:
                await self.listing_handlers.handle_listing_cancel(update, context)
            
            elif data == CallbackPatterns.SEARCH_LISTINGS:
                await self.listing_handlers.handle_search_listings(update, context)
            
            # Search callback handlers
            elif data.startswith(f'{CallbackPatterns.SEARCH_REGION}:'):
                region_code = data.split(':')[1]
                await self.listing_handlers.handle_search_region_selection(update, context, region_code)
            
            elif data.startswith(f'{CallbackPatterns.SEARCH_CITY}:'):
                parts = data.split(':')
                region_code = parts[1]
                city_name = ':'.join(parts[2:])  # Shahar nomida ':' bo'lishi mumkin
                await self.listing_handlers.handle_search_city_selection(update, context, region_code, city_name)
            
            elif data.startswith(f'{CallbackPatterns.SEARCH_TYPE}:'):
                listing_type = data.split(':')[1]
                await self.listing_handlers.handle_search_type_selection(update, context, listing_type)
            
            elif data.startswith(f'{CallbackPatterns.SEARCH_PROPERTY_TYPE}:'):
                property_type = data.split(':')[1]
                await self.listing_handlers.handle_search_property_type_selection(update, context, property_type)
            
            elif data.startswith(f'{CallbackPatterns.SEARCH_ROOMS}:'):
                rooms = data.split(':')[1]
                await self.listing_handlers.handle_search_rooms_selection(update, context, rooms)
            
            elif data == f'{CallbackPatterns.SEARCH_PRICE}:custom':
                await self.listing_handlers.handle_search_price_custom(update, context)
            
            elif data == CallbackPatterns.SEARCH_EXECUTE:
                await self.listing_handlers.handle_search_execute(update, context)
            
            elif data.startswith(f'{CallbackPatterns.SEARCH_FURNISHED}:'):
                furnished = data.split(':')[1]
                if furnished == 'filter':
                    await self.listing_handlers.handle_search_furniture_filter(update, context)
                else:
                    await self.listing_handlers.handle_search_furniture_selection(update, context, furnished)
            
            elif data.startswith(f'{CallbackPatterns.SEARCH_PETS}:'):
                pets_allowed = data.split(':')[1]
                if pets_allowed == 'filter':
                    await self.listing_handlers.handle_search_pets_filter(update, context)
                else:
                    await self.listing_handlers.handle_search_pets_selection(update, context, pets_allowed)
            
            elif data.startswith(f'{CallbackPatterns.SEARCH_PAGE}:'):
                page = int(data.split(':')[1])
                user_id = update.effective_user.id
                listings = context.user_data.get(f'search_results_{user_id}', [])
                await self.listing_handlers._show_search_page(update, context, listings, page)
            
            elif data == CallbackPatterns.MY_LISTINGS:
                await self.listing_handlers.handle_my_listings(update, context)
            
            elif data == CallbackPatterns.SETTINGS:
                await query.edit_message_text(
                    "⚙️ Sozlamalar funksiyasi hali ishlab chiqilmoqda...",
                    reply_markup=self.keyboard_builder.create_back_button()
                )
            
            elif data == CallbackPatterns.HELP:
                await query.edit_message_text(
                    self.message_builder.create_help_message(),
                    reply_markup=self.keyboard_builder.create_back_button(),
                    parse_mode='Markdown'
                )
            
            # Admin Panel Callbacks
            elif data == CallbackPatterns.ADMIN_PANEL:
                await self.admin_handlers.handle_admin_panel(update, context)
            
            elif data == "ADMIN_NEW_LISTINGS":
                await self.admin_handlers.handle_new_listings(update, context)
            
            elif data == CallbackPatterns.ADMIN_PENDING_LISTINGS:
                await self.admin_handlers.handle_pending_listings(update, context)
            
            elif data == "ADMIN_APPROVED_LISTINGS":
                await self.admin_handlers.handle_approved_listings(update, context)
            
            elif data == CallbackPatterns.ADMIN_USERS_MANAGEMENT:
                await self.admin_handlers.handle_users_management(update, context)
            
            elif data == CallbackPatterns.ADMIN_STATISTICS:
                await self.admin_handlers.handle_statistics(update, context)
            
            elif data == "ADMIN_CREATE_LISTING":
                await self.admin_handlers.handle_admin_create_listing(update, context)
            
            elif data.startswith(f'{CallbackPatterns.ADMIN_APPROVE}:'):
                listing_id = data.split(':')[1]
                await self.admin_handlers.handle_approve_listing(update, context, listing_id)
            
            elif data.startswith(f'{CallbackPatterns.ADMIN_REJECT}:'):
                listing_id = data.split(':')[1]
                await self.admin_handlers.handle_reject_listing(update, context, listing_id)
            
            elif data.startswith(f'{CallbackPatterns.ADMIN_DELETE}:'):
                listing_id = data.split(':')[1]
                await self.admin_handlers.handle_delete_listing(update, context, listing_id)
            
            elif data.startswith("ADMIN_NEXT_APPROVED:"):
                current_index = int(data.split(':')[1])
                await self.admin_handlers.handle_next_approved_listing(update, context, current_index)
            
            elif data.startswith("ADMIN_PREV_APPROVED:"):
                current_index = int(data.split(':')[1])
                await self.admin_handlers.handle_prev_approved_listing(update, context, current_index)
            
            else:
                await query.edit_message_text(
                    "❓ Noma'lum buyruq",
                    reply_markup=self.keyboard_builder.create_back_button()
                )
            
        except Exception as e:
            ErrorHandler.log_error(e, "callback_handler")
            await query.answer(self.message_builder.create_error_message("generic"))
    
    async def _handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Oddiy xabar handler"""
        try:
            if update.message.text.startswith('/'):
                return
            
            # E'lon joylashtirish jarayonida bo'lsa
            if context.user_data.get('waiting_for_price'):
                await self.listing_handlers.handle_price_input(update, context)
                return
            
            if context.user_data.get('waiting_for_title'):
                await self.listing_handlers.handle_title_input(update, context)
                return
            
            # Qidiruv jarayonida narx kiritish
            if context.user_data.get('waiting_for_price_range'):
                await self.listing_handlers.handle_search_price_input(update, context)
                return
            
            if context.user_data.get('waiting_for_description'):
                await self.listing_handlers.handle_description_input(update, context)
                return
            
            # Admin rejection reason input
            if context.user_data.get('waiting_for_rejection_reason'):
                await self.admin_handlers.handle_rejection_reason_input(update, context)
                return
            
            # Oddiy xabarlarga javob
            await update.message.reply_text(
                "Sizning xabaringizni qabul qildim! Asosiy menyu uchun /start buyrug'ini ishlating.",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🏠 Asosiy menyu", callback_data='MAIN_MENU')
                ]])
            )
            
        except Exception as e:
            ErrorHandler.log_error(e, "message_handler")
            await update.message.reply_text(self.message_builder.create_error_message("generic"))
    
    def _get_welcome_message(self, name: str) -> str:
        """Xush kelibsiz xabari"""
        return self.message_builder.create_welcome_message(name)
    
    def _get_back_button(self) -> InlineKeyboardMarkup:
        """Orqaga tugmasi"""
        return self.keyboard_builder.create_back_button()
    
    async def stop(self):
        """Botni to'xtatish"""
        try:
            await self.application.stop()
            logger.info("Bot to'xtatildi")
        except Exception as e:
            logger.error(f"Bot to'xtatishda xatolik: {e}")
    
    async def run_until_disconnected(self):
        """Botni uzilguncha ishlatish"""
        try:
            # Botni ishga tushirish
            await self.application.initialize()
            await self.application.start()
            
            # Polling ni boshlash
            await self.application.updater.start_polling()
            
            # Botni uzilguncha kutish
            import asyncio
            await asyncio.Event().wait()
            
        except Exception as e:
            logger.error(f"Bot ishlashda xatolik: {e}")
            raise
        finally:
            # Botni to'xtatish
            try:
                await self.application.stop()
            except:
                pass
    