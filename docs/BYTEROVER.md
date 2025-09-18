# UyKelishuv Bot - Byterover Handbook

## Project Overview

**UyKelishuv Bot** is a comprehensive Telegram bot for real estate listings in Uzbekistan. It facilitates property rental and sales announcements with multi-language support (Uzbek, Russian, English) and includes features like user verification, admin moderation, and complaint systems.

### Core Functionality
- 📝 **Property Listing Creation** - Users can post rental/sale announcements
- 🔍 **Advanced Search** - Filter-based property search
- 👤 **Profile Management** - User profiles and personal listings
- 📱 **Phone Verification** - SMS-based verification system
- 🚨 **Complaint System** - Report inappropriate listings
- 👨‍💼 **Admin Panel** - Moderation and management tools
- 🌐 **Multi-language** - Uzbek, Russian, English support

## Technical Architecture

### Technology Stack
- **Backend**: Python 3.11+
- **Bot Framework**: python-telegram-bot 20.0
- **Database ORM**: SQLAlchemy 2.0+
- **Migrations**: Alembic 1.12+
- **Validation**: Pydantic 2.0+
- **Async Support**: AsyncIO
- **Database**: PostgreSQL (production) / SQLite (development)
- **Deployment**: Railway.com

### Project Structure
```
src/
├── bot/
│   ├── handlers/          # Bot handlers
│   │   └── listing_handlers.py
│   ├── keyboards_telegram.py  # Inline keyboards
│   └── client_telegram.py     # Main bot client
├── database/
│   ├── models.py         # Database models
│   └── database.py       # Database connection
├── services/
│   ├── user_service.py   # User operations
│   └── listing_service.py # Listing operations
├── utils/
│   ├── helpers.py        # Helper functions
│   └── validators.py     # Validation functions
├── config.py             # Configuration
└── main.py              # Entry point
```

## Database Schema

### Core Models

#### User Model
- `id`: UUID primary key
- `telegram_user_id`: Unique Telegram user ID
- `name`: User display name
- `phone_number`: Verified phone number
- `locale`: Language preference (uz/ru/en)
- `verified`: Verification status
- `blocked`: Block status
- `created_at`: Registration timestamp

#### Listing Model
- `id`: UUID primary key
- `user_id`: Foreign key to User
- **Location**: `region_code`, `city_name`, `address`
- **Property Details**: `type` (ijara/sotuv), `rooms`, `area_m2`, `floor`, `total_floors`
- **Pricing**: `price`, `currency` (default USD)
- **Features**: `furnished`, `pets_allowed`
- **Content**: `title`, `description`, `media_urls`
- **Statistics**: `views_count`, `contacts_count`
- **Status**: `status` (pending/approved/rejected/archived)
- **Timestamps**: `created_at`, `updated_at`, `approved_at`

## Key Features Implementation

### 1. Listing Creation Flow
1. **Region Selection** - Choose from 14 Uzbekistan regions
2. **City Selection** - Region-specific cities/districts
3. **Property Type** - Rental (ijara) or Sale (sotuv)
4. **Room Count** - 1-6+ rooms
5. **Price Input** - USD currency
6. **Features** - Furnished, pets allowed
7. **Content** - Title and description
8. **Preview & Submit** - Review before submission

### 2. Regional Data Structure
- **14 Regions** with 2-digit codes (01-14)
- **Tashkent City** (14) - 11 districts
- **Karakalpakstan** (09) - 14 cities
- **Other Regions** - Central city + "Other city/district"

### 3. Bot Architecture
- **UyKelishuvBot** - Main bot class
- **ListingHandlers** - Listing creation handlers
- **MainKeyboard** - Inline keyboard management
- **UserService** - User operations
- **ListingService** - Listing operations

## Configuration Management

### Environment Variables
```env
TELEGRAM_BOT_TOKEN=your_bot_token
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db
SECRET_KEY=your_secret_key
JWT_SECRET_KEY=your_jwt_secret
DEBUG=false
ADMIN_IDS=123456789,987654321
BOT_NAME=UyKelishuv Bot
```

### Database Configuration
- **Development**: SQLite with aiosqlite
- **Production**: PostgreSQL with asyncpg
- **Railway**: Automatic PostgreSQL provisioning

## Development Guidelines

### Code Organization
- **Handlers**: Separate files for different functionalities
- **Services**: Business logic separation
- **Models**: Database schema definition
- **Utils**: Reusable helper functions

### Error Handling
- Comprehensive try-catch blocks
- User-friendly error messages
- Logging for debugging
- Graceful fallbacks

### Security Considerations
- User data encryption
- Phone number verification
- Admin-only access controls
- Spam prevention

## Deployment Strategy

### Railway.com Deployment
1. **Database Setup** - PostgreSQL service
2. **Environment Variables** - Production configuration
3. **Migration Execution** - Alembic migrations
4. **Bot Startup** - Automatic deployment

### Local Development
1. **Virtual Environment** - Python venv
2. **Dependencies** - pip install -r requirements.txt
3. **Environment File** - .env configuration
4. **Database Migration** - alembic upgrade head
5. **Bot Execution** - python start_bot.py

## Future Enhancements

### Planned Features
- Advanced search filters
- User profile management
- Phone verification system
- Admin moderation panel
- Complaint handling system
- Multi-language support
- Media upload support

### Technical Improvements
- Caching implementation
- Rate limiting
- Performance optimization
- Monitoring and analytics
- Automated testing

## Troubleshooting

### Common Issues
1. **Database Connection** - Check DATABASE_URL format
2. **Telegram API** - Verify bot token
3. **Import Errors** - Activate virtual environment
4. **Migration Issues** - Run alembic upgrade head

### Logging
- Bot logs: `bot.log`
- Database logs: SQLAlchemy echo mode
- Error tracking: Comprehensive exception handling

## Contributing Guidelines

### Development Workflow
1. Fork repository
2. Create feature branch
3. Implement changes
4. Test functionality
5. Submit pull request

### Code Standards
- Follow PEP 8
- Use type hints
- Document functions
- Write tests
- Handle errors gracefully

---

**"Ijaradan sotuvgacha, egadan bevosita"** 🏠
