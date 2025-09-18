# 🏠 UyKelishuv Bot

UyKelishuv Bot - O'zbekiston uchun uy ijara va sotuv e'lonlari boti. Bu bot foydalanuvchilarga uy/kvartira e'lonlarini joylashtirish, qidirish va boshqa foydalanuvchilar bilan aloqa qilish imkoniyatini beradi.

## ✨ Asosiy Funksiyalar

- 📝 **E'lon joylashtirish** - Uy/kvartira e'lonlarini joylashtirish
- 🔍 **E'lon qidirish** - Filtrlar bilan qidirish
- 👤 **Profil boshqaruvi** - Shaxsiy ma'lumotlar va e'lonlar
- 📱 **Telefon verifikatsiyasi** - SMS orqali tasdiqlash
- 🚨 **Shikoyat tizimi** - Noto'g'ri e'lonlarga shikoyat
- 👨‍💼 **Admin panel** - Moderatsiya va boshqaruv
- 🌐 **Ko'p til** - O'zbek, Rus, Ingliz tillari

## 🛠️ Texnologiyalar

- **Python 3.11+**
- **python-telegram-bot** - Telegram Bot API
- **SQLAlchemy** - ORM
- **Alembic** - Database migrations
- **Pydantic** - Data validation
- **AsyncIO** - Asynchronous programming
- **PostgreSQL** - Production database
- **SQLite** - Development database

## 📋 Talablar

- Python 3.11 yoki undan yuqori
- PostgreSQL (production) yoki SQLite (development)
- Telegram Bot Token
- Railway.com account (production deployment uchun)

## 🚀 O'rnatish

### 1. Repository ni klonlash

```bash
git clone <repository-url>
cd UyKelishuvBot
```

### 2. Virtual environment yaratish

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# yoki
venv\\Scripts\\activate  # Windows
```

### 3. Dependencies o'rnatish

```bash
pip install -r requirements.txt
```

### 4. Environment variables sozlash

`env.example` faylini `.env` nomiga nusxalang va kerakli qiymatlarni kiriting:

```env
# Telegram Bot Token (majburiy)
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here

# Database Configuration
# Development uchun SQLite:
DATABASE_URL=sqlite:///uykelishuv.db
# Production uchun PostgreSQL:
# DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/uykelishuv

# Security Keys
SECRET_KEY=your_secret_key_here_change_this_in_production
JWT_SECRET_KEY=your_jwt_secret_key_here_change_this_in_production

# Debug Mode (true/false)
DEBUG=true

# Admin Telegram IDs (vergul bilan ajratilgan)
ADMIN_IDS=123456789,987654321

# Bot Name
BOT_NAME=UyKelishuv Bot
```

### 5. Database ni ishga tushirish

```bash
# Migration yaratish (agar kerak bo'lsa)
alembic revision --autogenerate -m "Initial migration"

# Migration ni ishga tushirish
alembic upgrade head
```

### 6. Bot ni ishga tushirish

```bash
python start_bot.py
```

## 🚀 Railway.com da Deployment

### 1. Railway.com da account yaratish

1. [Railway.com](https://railway.app) ga kiring
2. GitHub account bilan ro'yxatdan o'ting
3. "New Project" tugmasini bosing

### 2. PostgreSQL Database qo'shish

1. Project dashboard da "New" tugmasini bosing
2. "Database" ni tanlang
3. "PostgreSQL" ni tanlang
4. Database yaratilgandan keyin, "Connect" tugmasini bosing
5. Connection string ni nusxalang

### 3. Bot ni deploy qilish

1. Project dashboard da "New" tugmasini bosing
2. "GitHub Repo" ni tanlang
3. UyKelishuvBot repository ni tanlang
4. "Deploy" tugmasini bosing

### 4. Environment Variables o'rnatish

Railway dashboard da "Variables" bo'limiga o'ting va quyidagi o'zgaruvchilarni qo'shing:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
DATABASE_URL=postgresql+asyncpg://username:password@hostname:port/database_name
SECRET_KEY=your_secret_key_here_change_this_in_production
JWT_SECRET_KEY=your_jwt_secret_key_here_change_this_in_production
DEBUG=false
ADMIN_IDS=123456789,987654321
BOT_NAME=UyKelishuv Bot
```

### 5. Database Migration

Railway terminal orqali migration ni ishga tushiring:

```bash
alembic upgrade head
```

### 6. Bot ni ishga tushirish

Railway avtomatik ravishda bot ni ishga tushiradi. Logs bo'limida bot ishlayotganini ko'rishingiz mumkin.

## 🧪 Test qilish

Botning barcha funksiyalarini test qilish uchun:

```bash
python test_bot_functionality.py
```

## 📁 Loyiha tuzilishi

```
UyKelishuvBot/
├── src/
│   ├── bot/
│   │   ├── handlers/          # Bot handlerlari
│   │   │   ├── admin.py      # Admin panel
│   │   │   ├── listing.py    # E'lon joylash
│   │   │   ├── profile.py    # Profil boshqaruvi
│   │   │   ├── search.py     # Qidiruv
│   │   │   ├── verification.py # Verifikatsiya
│   │   │   └── reports.py    # Shikoyatlar
│   │   ├── keyboards.py      # Klaviaturalar
│   │   └── client.py         # Asosiy bot klassi
│   ├── database/
│   │   ├── models.py         # Database modellari
│   │   └── database.py       # Database ulanishi
│   ├── services/
│   │   ├── user_service.py   # Foydalanuvchi xizmatlari
│   │   ├── listing_service.py # E'lon xizmatlari
│   │   ├── auth_service.py   # Autentifikatsiya
│   │   └── report_service.py # Shikoyat xizmatlari
│   ├── utils/
│   │   ├── helpers.py        # Yordamchi funksiyalar
│   │   └── validators.py     # Validatsiya funksiyalari
│   ├── config.py             # Konfiguratsiya
│   └── main.py              # Asosiy fayl
├── alembic/                  # Database migrations
├── requirements.txt          # Dependencies
├── test_bot_functionality.py # Test script
└── README.md                # Bu fayl
```

## 🎮 Bot Komandalari

- `/start` - Bot ni ishga tushirish
- `/help` - Yordam ma'lumotlari
- `/verify` - Telefon verifikatsiyasi
- `/profile` - Profil ko'rish
- `/admin` - Admin panel (faqat adminlar uchun)

## ⌨️ Inline Keyboard Tugmalari

Bot barcha tugmalar uchun inline keyboard ishlatadi:

- **Asosiy menyu**: E'lon joylash, qidirish, profil, sozlamalar
- **Viloyatlar**: O'zbekiston viloyatlari
- **Shaharlar**: Viloyat bo'yicha shaharlar
- **E'lon turi**: Ijara/Sotuv
- **Xonalar**: Xonalar soni
- **Filtrlar**: Qidiruv filtrlari
- **Amallar**: Tahrirlash, o'chirish, tasdiqlash

## 🔧 Konfiguratsiya

### Database

SQLite (development):
```env
DATABASE_URL=sqlite:///uykelishuv.db
```

PostgreSQL (production):
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/uykelishuv
```

Railway PostgreSQL:
```env
DATABASE_URL=postgresql+asyncpg://username:password@hostname:port/database_name
```

### Admin Panel

Admin ID larni `.env` faylida belgilang:
```env
ADMIN_IDS=123456789,987654321
```

### Debug Rejimi

Development uchun:
```env
DEBUG=True
```

Production uchun:
```env
DEBUG=False
```

## 🚨 Xavfsizlik

- Barcha foydalanuvchi ma'lumotlari shifrlangan
- Telefon raqamlar SMS orqali tasdiqlanadi
- Admin panel faqat ruxsat berilgan foydalanuvchilar uchun
- Spam va noto'g'ri kontent uchun shikoyat tizimi

## 📊 Statistika

Bot quyidagi statistikalar to'playdi:

- Foydalanuvchilar soni
- E'lonlar soni
- Ko'rishlar soni
- Kontaktlar soni
- Shikoyatlar soni

## 🔄 Yangilanishlar

Bot yangilanishlari:

- ✅ To'liq inline keyboard qo'llab-quvvatlash
- ✅ Ko'p til qo'llab-quvvatlash
- ✅ Telefon verifikatsiyasi
- ✅ Admin panel
- ✅ Shikoyat tizimi
- ✅ Filtrlar bilan qidiruv
- ✅ Profil boshqaruvi

## 🐛 Xatoliklarni tuzatish

### Umumiy muammolar

1. **Database ulanishi xatoligi**
   ```bash
   # Database faylini tekshiring
   ls -la uykelishuv.db
   
   # Migration ni qayta ishga tushiring
   alembic upgrade head
   ```

2. **Telegram API xatoligi**
   ```bash
   # API ID va Hash ni tekshiring
   # https://my.telegram.org/apps dan oling
   ```

3. **Import xatoligi**
   ```bash
   # Virtual environment ni faollashtiring
   source venv/bin/activate
   
   # Dependencies ni qayta o'rnating
   pip install -r requirements.txt
   ```

### Log fayllar

Bot loglari `bot.log` faylida saqlanadi:
```bash
tail -f bot.log
```

## 🤝 Hissa qo'shish

1. Repository ni fork qiling
2. Yangi branch yarating (`git checkout -b feature/amazing-feature`)
3. O'zgarishlarni commit qiling (`git commit -m 'Add amazing feature'`)
4. Branch ga push qiling (`git push origin feature/amazing-feature`)
5. Pull Request yarating

## 📄 Litsenziya

Bu loyiha MIT litsenziyasi ostida tarqatiladi. Batafsil ma'lumot uchun `LICENSE` faylini ko'ring.

## 📞 Aloqa

Savollar yoki takliflar uchun:

- 📧 Email: support@uykelishuv.uz
- 💬 Telegram: @uykelishuv_support
- 🌐 Website: https://uykelishuv.uz

## 🙏 Minnatdorchilik

- [Telethon](https://github.com/LonamiWebs/Telethon) - Telegram Bot API
- [SQLAlchemy](https://www.sqlalchemy.org/) - Python ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation

---

**"Ijaradan sotuvgacha, egadan bevosita"** 🏠
