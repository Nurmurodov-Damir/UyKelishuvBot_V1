"""
Admin Handlers - Admin panel handlerlari
"""
import logging
from typing import Dict, Any, List, Optional
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from src.services.admin_service import AdminService
from src.services.keyboard_builder import KeyboardBuilder
from src.services.message_builder import MessageBuilder
from src.services.validation_service import ErrorHandler
from src.services.notification_service import NotificationService
from src.utils.constants import CallbackPatterns, BotConstants
from src.config import REGIONS
from src.database.database import AsyncSessionLocal
from src.database.models import Listing, ListingStatus, User

logger = logging.getLogger(__name__)


class AdminHandlers:
    """Admin panel handlerlari"""
    
    def __init__(self, admin_service: AdminService):
        self.admin_service = admin_service
        self.keyboard_builder = KeyboardBuilder()
        self.message_builder = MessageBuilder()
        self.notification_service = NotificationService()
        self.admin_data: Dict[int, Dict[str, Any]] = {}
    
    async def handle_admin_panel(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Admin panelni ochish"""
        try:
            user_id = update.effective_user.id
            
            # Admin huquqini tekshirish
            async with AsyncSessionLocal() as db:
                self.admin_service.db = db
                
                if not self.admin_service.is_admin(user_id):
                    await update.callback_query.edit_message_text(
                        "❌ Sizda admin huquqi yo'q!",
                        reply_markup=self.keyboard_builder.create_back_button()
                    )
                    return
                
                # Statistika olish
                stats = await self.admin_service.get_statistics()
                
                message = self._create_admin_panel_message(stats)
                keyboard = self._create_admin_panel_keyboard()
                
                await update.callback_query.edit_message_text(
                    message,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_admin_panel")
            await update.callback_query.answer("❌ Xatolik yuz berdi")
    
    async def handle_pending_listings(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Tasdiqlanmagan e'lonlarni ko'rsatish"""
        try:
            user_id = update.effective_user.id
            
            async with AsyncSessionLocal() as db:
                self.admin_service.db = db
                
                if not self.admin_service.is_admin(user_id):
                    await update.callback_query.answer("❌ Ruxsat yo'q")
                    return
                
                # Pending e'lonlarni olish
                pending_listings = await self.admin_service.get_pending_listings()
                
                if not pending_listings:
                    await update.callback_query.edit_message_text(
                        "📋 **Tasdiqlanmagan e'lonlar**\n\n"
                        "Hozirda tasdiqlanmagan e'lonlar yo'q.",
                        reply_markup=self._create_back_to_admin_keyboard(),
                        parse_mode='Markdown'
                    )
                    return
                
                # Birinchi e'lonni ko'rsatish
                self.admin_data[user_id] = {
                    'pending_listings': pending_listings,
                    'current_index': 0
                }
                
                await self._show_listing_for_moderation(update, context, pending_listings[0], 0, len(pending_listings))
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_pending_listings")
            await update.callback_query.answer("❌ Xatolik yuz berdi")
    
    async def handle_approve_listing(self, update: Update, context: ContextTypes.DEFAULT_TYPE, listing_id: str) -> None:
        """E'lonni tasdiqlash"""
        try:
            user_id = update.effective_user.id
            
            async with AsyncSessionLocal() as db:
                self.admin_service.db = db
                
                if not self.admin_service.is_admin(user_id):
                    await update.callback_query.answer("❌ Ruxsat yo'q")
                    return
                
                # E'lonni tasdiqlash
                success = await self.admin_service.approve_listing(listing_id, user_id)
                
                if success:
                    await update.callback_query.answer("✅ E'lon tasdiqlandi")
                    
                    # Keyingi e'lonni ko'rsatish
                    await self._show_next_pending_listing(update, context)
                else:
                    await update.callback_query.answer("❌ E'lonni tasdiqlashda xatolik")
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_approve_listing")
            await update.callback_query.answer("❌ Xatolik yuz berdi")
    
    async def handle_reject_listing(self, update: Update, context: ContextTypes.DEFAULT_TYPE, listing_id: str) -> None:
        """E'lonni rad etish"""
        try:
            user_id = update.effective_user.id
            
            # Rad etish sababi so'rash
            await update.callback_query.edit_message_text(
                "❌ **E'lonni rad etish**\n\n"
                "Rad etish sababini kiriting:",
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton("🔙 Orqaga", callback_data=f"ADMIN_LISTING_DETAIL:{listing_id}")
                ]]),
                parse_mode='Markdown'
            )
            
            # Sabab kiritish uchun kutish
            context.user_data['waiting_for_rejection_reason'] = True
            context.user_data['rejecting_listing_id'] = listing_id
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_reject_listing")
            await update.callback_query.answer("❌ Xatolik yuz berdi")
    
    async def handle_rejection_reason_input(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Rad etish sababini qabul qilish"""
        try:
            user_id = update.effective_user.id
            reason = update.message.text.strip()
            listing_id = context.user_data.get('rejecting_listing_id')
            
            if not listing_id:
                await update.message.reply_text("❌ E'lon ID topilmadi")
                return
            
            async with AsyncSessionLocal() as db:
                self.admin_service.db = db
                
                if not self.admin_service.is_admin(user_id):
                    await update.message.reply_text("❌ Ruxsat yo'q")
                    return
                
                # E'lonni rad etish
                success = await self.admin_service.reject_listing(listing_id, user_id, reason)
                
                if success:
                    await update.message.reply_text("✅ E'lon rad etildi")
                    
                    # Keyingi e'lonni ko'rsatish
                    await self._show_next_pending_listing_after_message(update, context)
                else:
                    await update.message.reply_text("❌ E'lonni rad etishda xatolik")
            
            # Kutish holatini tozalash
            context.user_data['waiting_for_rejection_reason'] = False
            context.user_data['rejecting_listing_id'] = None
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_rejection_reason_input")
            await update.message.reply_text("❌ Xatolik yuz berdi")
    
    async def handle_delete_listing(self, update: Update, context: ContextTypes.DEFAULT_TYPE, listing_id: str) -> None:
        """E'lonni o'chirish"""
        try:
            user_id = update.effective_user.id
            
            async with AsyncSessionLocal() as db:
                self.admin_service.db = db
                
                if not self.admin_service.is_admin(user_id):
                    await update.callback_query.answer("❌ Ruxsat yo'q")
                    return
                
                # E'lonni o'chirish
                success = await self.admin_service.delete_listing(listing_id, user_id)
                
                if success:
                    await update.callback_query.answer("🗑️ E'lon o'chirildi")
                    
                    # Keyingi e'lonni ko'rsatish
                    await self._show_next_pending_listing(update, context)
                else:
                    await update.callback_query.answer("❌ E'lonni o'chirishda xatolik")
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_delete_listing")
            await update.callback_query.answer("❌ Xatolik yuz berdi")
    
    async def handle_users_management(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Foydalanuvchilar boshqaruvi"""
        try:
            user_id = update.effective_user.id
            
            async with AsyncSessionLocal() as db:
                self.admin_service.db = db
                
                if not self.admin_service.is_admin(user_id):
                    await update.callback_query.answer("❌ Ruxsat yo'q")
                    return
                
                # Foydalanuvchilar ro'yxati
                users = await self.admin_service.get_all_users()
                
                message = self._create_users_management_message(users)
                keyboard = self._create_users_management_keyboard()
                
                await update.callback_query.edit_message_text(
                    message,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_users_management")
            await update.callback_query.answer("❌ Xatolik yuz berdi")
    
    async def handle_statistics(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Statistika ko'rsatish"""
        try:
            user_id = update.effective_user.id
            
            async with AsyncSessionLocal() as db:
                self.admin_service.db = db
                
                if not self.admin_service.is_admin(user_id):
                    await update.callback_query.answer("❌ Ruxsat yo'q")
                    return
                
                # Statistika olish
                stats = await self.admin_service.get_statistics()
                
                message = self._create_detailed_statistics_message(stats)
                keyboard = self._create_back_to_admin_keyboard()
                
                await update.callback_query.edit_message_text(
                    message,
                    reply_markup=keyboard,
                    parse_mode='Markdown'
                )
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_statistics")
            await update.callback_query.answer("❌ Xatolik yuz berdi")
    
    async def handle_new_listings(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Yangi e'lonlarni ko'rsatish"""
        try:
            await update.callback_query.answer()
            
            async with AsyncSessionLocal() as db:
                admin_service = AdminService(db)
                pending_listings = await admin_service.get_pending_listings()
                
                if not pending_listings:
                    await update.callback_query.edit_message_text(
                        "📋 **Yangi e'lonlar yo'q**\n\nHozircha tekshirish kutayotgan e'lonlar mavjud emas.",
                        reply_markup=self._create_admin_panel_keyboard(),
                        parse_mode='Markdown'
                    )
                    return
                
                # Birinchi e'lonni ko'rsatish
                await self._show_pending_listing(update, context, pending_listings[0], 0, len(pending_listings))
                
        except Exception as e:
            ErrorHandler.log_error(e, "handle_new_listings")
            await update.callback_query.answer("❌ Xatolik yuz berdi")
    
    async def _show_pending_listing(self, update: Update, context: ContextTypes.DEFAULT_TYPE, listing: Listing, index: int, total: int) -> None:
        """Tekshirish kutayotgan e'lonni ko'rsatish"""
        try:
            # E'lon ma'lumotlarini tayyorlash
            property_type_text = ""
            if listing.property_type:
                property_type_names = {
                    'kvartira': 'Kvartira',
                    'uy': 'Uy', 
                    'ofis': 'Ofis'
                }
                property_type_text = f"\n🏠 Uy turi: {property_type_names.get(listing.property_type.value, listing.property_type.value)}"
            
            message_text = (
                f"📋 **Yangi e'lon** ({index + 1}/{total})\n\n"
                f"👤 **Muallif:** {listing.owner.name}\n"
                f"📱 **Telefon:** {listing.owner.phone_number or 'Ko\'rsatilmagan'}\n"
                f"📍 **Manzil:** {REGIONS.get(listing.region_code, 'Noma\'lum')} - {listing.city_name}\n"
                f"🏠 **E'lon turi:** {'Ijara' if listing.type.value == 'ijara' else 'Sotuv'}{property_type_text}\n"
                f"🚪 **Xonalar:** {listing.rooms}\n"
                f"💰 **Narx:** {listing.price} {listing.currency}\n"
                f"🛋️ **Mebellar:** {'Ha' if listing.furnished else 'Yo\'q'}\n"
                f"🐕 **Hayvonlar:** {'Ruxsat etilgan' if listing.pets_allowed else 'Ruxsat etilmagan'}\n"
                f"📝 **Sarlavha:** {listing.title}\n"
                f"📄 **Tavsif:** {listing.description or 'Tavsif yo\'q'}\n"
                f"📅 **Yaratilgan:** {listing.created_at.strftime('%d.%m.%Y %H:%M')}"
            )
            
            keyboard = self._create_pending_listing_keyboard(listing.id, index, total)
            
            await update.callback_query.edit_message_text(
                message_text,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            ErrorHandler.log_error(e, "_show_pending_listing")
            await update.callback_query.answer("❌ Xatolik yuz berdi")
    
    def _create_pending_listing_keyboard(self, listing_id: str, index: int, total: int) -> InlineKeyboardMarkup:
        """Tekshirish kutayotgan e'lon uchun klaviatura"""
        keyboard = []
        
        # Tasdiqlash va rad etish tugmalari
        keyboard.append([
            InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"ADMIN_APPROVE:{listing_id}"),
            InlineKeyboardButton("❌ Rad etish", callback_data=f"ADMIN_REJECT:{listing_id}")
        ])
        
        # Navigatsiya tugmalari
        nav_buttons = []
        if index > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"ADMIN_PREV_PENDING:{index-1}"))
        if index < total - 1:
            nav_buttons.append(InlineKeyboardButton("Keyingi ➡️", callback_data=f"ADMIN_NEXT_PENDING:{index+1}"))
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        # Admin panelga qaytish
        keyboard.append([InlineKeyboardButton("🔙 Admin Panel", callback_data="ADMIN_PANEL")])
        
        return InlineKeyboardMarkup(keyboard)
    
    async def handle_admin_create_listing(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Admin e'lon qo'shish"""
        try:
            user_id = update.effective_user.id
            
            async with AsyncSessionLocal() as db:
                self.admin_service.db = db
                
                if not self.admin_service.is_admin(user_id):
                    await update.callback_query.answer("❌ Ruxsat yo'q")
                    return
                
                # Admin e'lon qo'shish jarayonini boshlash
                await update.callback_query.edit_message_text(
                    "📝 **Admin E'lon Qo'shish**\n\n"
                    "Siz admin sifatida e'lon qo'sha olasiz. E'lon avtomatik tasdiqlangan holatda bo'ladi.\n\n"
                    "E'lon qo'shish jarayonini boshlash uchun tugmani bosing:",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("📝 E'lon qo'shish", callback_data=CallbackPatterns.POST_LISTING)],
                        [InlineKeyboardButton("🔙 Admin Panel", callback_data="ADMIN_PANEL")]
                    ]),
                    parse_mode='Markdown'
                )
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_admin_create_listing")
            await update.callback_query.answer("❌ Xatolik yuz berdi")
    
    async def handle_approved_listings(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Tasdiqlangan e'lonlarni ko'rsatish"""
        try:
            user_id = update.effective_user.id
            
            async with AsyncSessionLocal() as db:
                self.admin_service.db = db
                
                if not self.admin_service.is_admin(user_id):
                    await update.callback_query.answer("❌ Ruxsat yo'q")
                    return
                
                # Tasdiqlangan e'lonlarni olish
                approved_listings = await self.admin_service.get_approved_listings()
                
                if not approved_listings:
                    await update.callback_query.edit_message_text(
                        "✅ **Tasdiqlangan e'lonlar**\n\n"
                        "Hozirda tasdiqlangan e'lonlar yo'q.",
                        reply_markup=self._create_back_to_admin_keyboard(),
                        parse_mode='Markdown'
                    )
                    return
                
                # Birinchi e'lonni ko'rsatish
                self.admin_data[user_id] = {
                    'approved_listings': approved_listings,
                    'current_index': 0
                }
                
                await self._show_approved_listing(update, context, approved_listings[0], 0, len(approved_listings))
            
        except Exception as e:
            ErrorHandler.log_error(e, "handle_approved_listings")
            await update.callback_query.answer("❌ Xatolik yuz berdi")
    
    async def handle_next_approved_listing(self, update: Update, context: ContextTypes.DEFAULT_TYPE, current_index: int) -> None:
        """Tasdiqlangan e'lonlarda keyingi e'lonni ko'rsatish"""
        try:
            user_id = update.effective_user.id
            
            # Admin huquqini tekshirish
            async with AsyncSessionLocal() as db:
                self.admin_service.db = db
                
                if not self.admin_service.is_admin(user_id):
                    await update.callback_query.edit_message_text(
                        "❌ Sizda admin huquqi yo'q!",
                        reply_markup=self.keyboard_builder.create_back_button()
                    )
                    return
                
                # Tasdiqlangan e'lonlarni olish
                listings = await self.admin_service.get_approved_listings()
                
                if not listings:
                    await update.callback_query.edit_message_text(
                        "✅ Tasdiqlangan e'lonlar yo'q",
                        reply_markup=self.keyboard_builder.create_back_button()
                    )
                    return
                
                # Keyingi e'lonni ko'rsatish
                next_index = current_index + 1
                if next_index < len(listings):
                    await self._show_approved_listing(update, context, listings[next_index], next_index, len(listings))
                else:
                    await update.callback_query.answer("Bu oxirgi e'lon!")
                    
        except Exception as e:
            ErrorHandler.log_error(e, "handle_next_approved_listing")
            await update.callback_query.answer("❌ Xatolik yuz berdi")
    
    async def handle_prev_approved_listing(self, update: Update, context: ContextTypes.DEFAULT_TYPE, current_index: int) -> None:
        """Tasdiqlangan e'lonlarda oldingi e'lonni ko'rsatish"""
        try:
            user_id = update.effective_user.id
            
            # Admin huquqini tekshirish
            async with AsyncSessionLocal() as db:
                self.admin_service.db = db
                
                if not self.admin_service.is_admin(user_id):
                    await update.callback_query.edit_message_text(
                        "❌ Sizda admin huquqi yo'q!",
                        reply_markup=self.keyboard_builder.create_back_button()
                    )
                    return
                
                # Tasdiqlangan e'lonlarni olish
                listings = await self.admin_service.get_approved_listings()
                
                if not listings:
                    await update.callback_query.edit_message_text(
                        "✅ Tasdiqlangan e'lonlar yo'q",
                        reply_markup=self.keyboard_builder.create_back_button()
                    )
                    return
                
                # Oldingi e'lonni ko'rsatish
                prev_index = current_index - 1
                if prev_index >= 0:
                    await self._show_approved_listing(update, context, listings[prev_index], prev_index, len(listings))
                else:
                    await update.callback_query.answer("Bu birinchi e'lon!")
                    
        except Exception as e:
            ErrorHandler.log_error(e, "handle_prev_approved_listing")
            await update.callback_query.answer("❌ Xatolik yuz berdi")
    
    # Helper methods
    
    def _create_admin_panel_message(self, stats: Dict[str, Any]) -> str:
        """Admin panel xabari"""
        users_stats = stats['users']
        listings_stats = stats['listings']
        
        return f"""🛡️ **Admin Panel**

📊 **Tezkor Statistika:**

👥 **Foydalanuvchilar:**
• Jami: {users_stats['total']}
• Tasdiqlangan: {users_stats['verified']}
• Bloklangan: {users_stats['blocked']}

📋 **E'lonlar:**
• Jami: {listings_stats['total']}
• Kutayotgan: {listings_stats['pending']}
• Tasdiqlangan: {listings_stats['approved']}
• Rad etilgan: {listings_stats['rejected']}

Kerakli amalni tanlang:"""
    
    def _create_admin_panel_keyboard(self) -> InlineKeyboardMarkup:
        """Admin panel klaviaturasi"""
        keyboard = [
            [InlineKeyboardButton("📋 Yangi e'lonlar", callback_data="ADMIN_NEW_LISTINGS")],
            [InlineKeyboardButton("📋 Tasdiqlanmagan e'lonlar", callback_data="ADMIN_PENDING_LISTINGS")],
            [InlineKeyboardButton("✅ Tasdiqlangan e'lonlar", callback_data="ADMIN_APPROVED_LISTINGS")],
            [InlineKeyboardButton("📝 E'lon qo'shish", callback_data="ADMIN_CREATE_LISTING")],
            [InlineKeyboardButton("👥 Foydalanuvchilar", callback_data="ADMIN_USERS_MANAGEMENT")],
            [InlineKeyboardButton("📊 Batafsil statistika", callback_data="ADMIN_STATISTICS")],
            [InlineKeyboardButton("🔙 Asosiy menyu", callback_data=CallbackPatterns.MAIN_MENU)]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def _create_back_to_admin_keyboard(self) -> InlineKeyboardMarkup:
        """Admin panelga qaytish klaviaturasi"""
        return InlineKeyboardMarkup([[
            InlineKeyboardButton("🔙 Admin Panel", callback_data="ADMIN_PANEL")
        ]])
    
    async def _show_listing_for_moderation(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                         listing: Listing, current_index: int, total_count: int) -> None:
        """Moderatsiya uchun e'lon ko'rsatish"""
        try:
            region_name = REGIONS.get(listing.region_code, listing.region_code)
            type_name = "Ijara" if listing.type.value == "ijara" else "Sotuv"
            furnished_text = "✅" if listing.furnished else "❌"
            pets_text = "✅" if listing.pets_allowed else "❌"
            
            message = f"""📋 **E'lon Moderatsiyasi** ({current_index + 1}/{total_count})

**Sarlavha:** {listing.title}
**Joylashuv:** {region_name} - {listing.city_name}
**Turi:** {type_name}
**Xonalar:** {listing.rooms} xona
**Narx:** {listing.price} {listing.currency}
**Mebellar:** {furnished_text}
**Hayvonlar:** {pets_text}

**Tavsif:** {listing.description or 'Tavsif yo\'q'}

**Egasi:** {listing.owner.name}
**Telefon:** {listing.owner.phone_number or 'Ko\'rsatilmagan'}
**Yaratilgan:** {listing.created_at.strftime('%d.%m.%Y %H:%M')}

Ushbu e'lon bilan nima qilasiz?"""
            
            keyboard = self._create_listing_moderation_keyboard(listing.id, current_index, total_count)
            
            await update.callback_query.edit_message_text(
                message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            ErrorHandler.log_error(e, "_show_listing_for_moderation")
            await update.callback_query.answer("❌ Xatolik yuz berdi")
    
    def _create_listing_moderation_keyboard(self, listing_id: str, current_index: int, total_count: int) -> InlineKeyboardMarkup:
        """E'lon moderatsiya klaviaturasi"""
        keyboard = [
            [
                InlineKeyboardButton("✅ Tasdiqlash", callback_data=f"ADMIN_APPROVE:{listing_id}"),
                InlineKeyboardButton("❌ Rad etish", callback_data=f"ADMIN_REJECT:{listing_id}")
            ],
            [InlineKeyboardButton("🗑️ O'chirish", callback_data=f"ADMIN_DELETE:{listing_id}")],
        ]
        
        # Navigation buttons
        nav_row = []
        if current_index > 0:
            nav_row.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"ADMIN_PREV_LISTING:{current_index}"))
        if current_index < total_count - 1:
            nav_row.append(InlineKeyboardButton("➡️ Keyingi", callback_data=f"ADMIN_NEXT_LISTING:{current_index}"))
        
        if nav_row:
            keyboard.append(nav_row)
        
        keyboard.append([InlineKeyboardButton("🔙 Admin Panel", callback_data="ADMIN_PANEL")])
        
        return InlineKeyboardMarkup(keyboard)
    
    async def _show_next_pending_listing(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Keyingi tasdiqlanmagan e'lonni ko'rsatish"""
        try:
            user_id = update.effective_user.id
            
            if user_id not in self.admin_data:
                # Qaytadan pending listings ni olish
                await self.handle_pending_listings(update, context)
                return
            
            admin_data = self.admin_data[user_id]
            pending_listings = admin_data['pending_listings']
            current_index = admin_data['current_index']
            
            # Keyingi e'lonni topish
            next_index = current_index + 1
            
            if next_index >= len(pending_listings):
                # Barcha e'lonlar ko'rib chiqildi
                await update.callback_query.edit_message_text(
                    "✅ **Barcha e'lonlar ko'rib chiqildi!**\n\n"
                    "Tasdiqlanmagan e'lonlar qolmadi.",
                    reply_markup=self._create_back_to_admin_keyboard(),
                    parse_mode='Markdown'
                )
                del self.admin_data[user_id]
                return
            
            # Keyingi e'lonni ko'rsatish
            self.admin_data[user_id]['current_index'] = next_index
            await self._show_listing_for_moderation(update, context, pending_listings[next_index], next_index, len(pending_listings))
            
        except Exception as e:
            ErrorHandler.log_error(e, "_show_next_pending_listing")
            await update.callback_query.answer("❌ Xatolik yuz berdi")
    
    async def _show_next_pending_listing_after_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Message dan keyin keyingi e'lonni ko'rsatish"""
        try:
            # Message update ni callback query update ga o'zgartirish
            from unittest.mock import MagicMock
            
            mock_callback_query = MagicMock()
            mock_callback_query.edit_message_text = update.message.reply_text
            mock_callback_query.answer = lambda text: None
            
            mock_update = MagicMock()
            mock_update.callback_query = mock_callback_query
            mock_update.effective_user = update.effective_user
            
            await self._show_next_pending_listing(mock_update, context)
            
        except Exception as e:
            ErrorHandler.log_error(e, "_show_next_pending_listing_after_message")
            await update.message.reply_text("❌ Xatolik yuz berdi")
    
    def _create_users_management_message(self, users: List[User]) -> str:
        """Foydalanuvchilar boshqaruvi xabari"""
        total_users = len(users)
        verified_users = sum(1 for user in users if user.verified)
        blocked_users = sum(1 for user in users if user.blocked)
        
        return f"""👥 **Foydalanuvchilar Boshqaruvi**

📊 **Statistika:**
• Jami foydalanuvchilar: {total_users}
• Tasdiqlangan: {verified_users}
• Bloklangan: {blocked_users}

**Oxirgi 10 foydalanuvchi:**
"""
    
    def _create_users_management_keyboard(self) -> InlineKeyboardMarkup:
        """Foydalanuvchilar boshqaruvi klaviaturasi"""
        keyboard = [
            [InlineKeyboardButton("🔍 Foydalanuvchi qidirish", callback_data="ADMIN_SEARCH_USER")],
            [InlineKeyboardButton("📋 Barcha foydalanuvchilar", callback_data="ADMIN_ALL_USERS")],
            [InlineKeyboardButton("🚫 Bloklangan foydalanuvchilar", callback_data="ADMIN_BLOCKED_USERS")],
            [InlineKeyboardButton("🔙 Admin Panel", callback_data="ADMIN_PANEL")]
        ]
        return InlineKeyboardMarkup(keyboard)
    
    def _create_detailed_statistics_message(self, stats: Dict[str, Any]) -> str:
        """Batafsil statistika xabari"""
        users_stats = stats['users']
        listings_stats = stats['listings']
        
        return f"""📊 **Batafsil Statistika**

👥 **Foydalanuvchilar:**
• Jami: {users_stats['total']}
• Tasdiqlangan: {users_stats['verified']}
• Tasdiqlanmagan: {users_stats['total'] - users_stats['verified']}
• Bloklangan: {users_stats['blocked']}
• Faol: {users_stats['total'] - users_stats['blocked']}

📋 **E'lonlar:**
• Jami: {listings_stats['total']}
• Kutayotgan: {listings_stats['pending']}
• Tasdiqlangan: {listings_stats['approved']}
• Rad etilgan: {listings_stats['rejected']}

📈 **E'lon turlari:**
• Ijara: {listings_stats['rental']}
• Sotuv: {listings_stats['sale']}

📊 **Tasdiqlanish foizi:** {(listings_stats['approved'] / max(listings_stats['total'], 1) * 100):.1f}%
📊 **Rad etilish foizi:** {(listings_stats['rejected'] / max(listings_stats['total'], 1) * 100):.1f}%"""
    
    async def _show_approved_listing(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                   listing: Listing, current_index: int, total_count: int) -> None:
        """Tasdiqlangan e'lonni ko'rsatish"""
        try:
            region_name = REGIONS.get(listing.region_code, listing.region_code)
            type_name = "Ijara" if listing.type.value == "ijara" else "Sotuv"
            furnished_text = "✅" if listing.furnished else "❌"
            pets_text = "✅" if listing.pets_allowed else "❌"
            
            message = f"""✅ **Tasdiqlangan E'lon** ({current_index + 1}/{total_count})

**Sarlavha:** {listing.title}
**Joylashuv:** {region_name} - {listing.city_name}
**Turi:** {type_name}
**Xonalar:** {listing.rooms} xona
**Narx:** {listing.price} {listing.currency}
**Mebellar:** {furnished_text}
**Hayvonlar:** {pets_text}

**Tavsif:** {listing.description or 'Tavsif yo\'q'}

**Egasi:** {listing.owner.name}
**Telefon:** {listing.owner.phone_number or 'Ko\'rsatilmagan'}
**Yaratilgan:** {listing.created_at.strftime('%d.%m.%Y %H:%M')}
**Tasdiqlangan:** {listing.approved_at.strftime('%d.%m.%Y %H:%M') if listing.approved_at else 'Noma\'lum'}

Bu e'lon tasdiqlangan va foydalanuvchilar ko'ra oladi."""
            
            keyboard = self._create_approved_listing_keyboard(listing.id, current_index, total_count)
            
            await update.callback_query.edit_message_text(
                message,
                reply_markup=keyboard,
                parse_mode='Markdown'
            )
            
        except Exception as e:
            ErrorHandler.log_error(e, "_show_approved_listing")
            await update.callback_query.answer("❌ Xatolik yuz berdi")
    
    def _create_approved_listing_keyboard(self, listing_id: str, current_index: int, total_count: int) -> InlineKeyboardMarkup:
        """Tasdiqlangan e'lon klaviaturasi"""
        keyboard = [
            [InlineKeyboardButton("🗑️ O'chirish", callback_data=f"ADMIN_DELETE:{listing_id}")],
        ]
        
        # Navigation buttons
        nav_row = []
        if current_index > 0:
            nav_row.append(InlineKeyboardButton("⬅️ Oldingi", callback_data=f"ADMIN_PREV_APPROVED:{current_index}"))
        if current_index < total_count - 1:
            nav_row.append(InlineKeyboardButton("➡️ Keyingi", callback_data=f"ADMIN_NEXT_APPROVED:{current_index}"))
        
        if nav_row:
            keyboard.append(nav_row)
        
        keyboard.append([InlineKeyboardButton("🔙 Admin Panel", callback_data="ADMIN_PANEL")])
        
        return InlineKeyboardMarkup(keyboard)