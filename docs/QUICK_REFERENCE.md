# UyKelishuv Bot - Senior Developer Quick Reference

## 🚀 Quick Start Commands

### Development Setup
```bash
# Clone and setup
git clone <repo-url>
cd UyKelishuvBot
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp env.example .env
# Edit .env with your values

# Database setup
alembic upgrade head

# Run bot
python start_bot.py
```

### Database Operations
```bash
# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1

# Check migration status
alembic current
alembic history
```

### Railway Deployment
```bash
# Login and link
railway login
railway link

# Deploy
railway up

# Check logs
railway logs

# Run migrations on Railway
railway run alembic upgrade head
```

## 📁 Project Structure Quick Reference

```
src/
├── bot/
│   ├── client_telegram.py      # Main bot class
│   ├── handlers/
│   │   └── listing_handlers.py # Listing creation flow
│   └── keyboards_telegram.py   # Inline keyboards
├── database/
│   ├── models.py              # SQLAlchemy models
│   └── database.py            # Connection management
├── services/
│   ├── user_service.py        # User operations
│   └── listing_service.py    # Listing operations
├── utils/
│   ├── helpers.py            # Utility functions
│   └── validators.py         # Input validation
├── config.py                 # Configuration
└── main.py                   # Entry point
```

## 🔧 Key Classes & Methods

### UyKelishuvBot (Main Bot Class)
```python
class UyKelishuvBot:
    def __init__(self)
    async def start(self)
    async def stop(self)
    async def run_until_disconnected(self)
    def _register_handlers(self)
    async def _handle_start(self, update, context)
    async def _handle_callback(self, update, context)
```

### ListingHandlers (Listing Creation)
```python
class ListingHandlers:
    async def handle_post_listing(self, update, context)
    async def handle_region_selection(self, update, context, region_code)
    async def handle_city_selection(self, update, context, region_code, city_name)
    async def handle_type_selection(self, update, context, listing_type)
    async def handle_rooms_selection(self, update, context, rooms)
    async def handle_price_input(self, update, context)
    async def handle_listing_submit(self, update, context)
```

### UserService (User Operations)
```python
class UserService:
    async def get_user_by_telegram_id(self, telegram_id: int) -> Optional[User]
    async def create_user(self, telegram_user_id: int, name: str) -> User
```

### ListingService (Listing Operations)
```python
class ListingService:
    async def create_listing(self, user_id: str, listing_data: dict) -> Listing
    async def get_listing_by_id(self, listing_id: str) -> Optional[Listing]
    async def get_user_listings(self, user_id: str) -> List[Listing]
    async def search_listings(self, filters: dict) -> List[Listing]
    async def update_listing(self, listing_id: str, update_data: dict) -> Optional[Listing]
    async def delete_listing(self, listing_id: str) -> bool
```

## 🗄️ Database Models

### User Model
```python
class User(Base):
    id = Column(String(36), primary_key=True)  # UUID
    telegram_user_id = Column(BigInteger, unique=True)
    name = Column(String(255))
    phone_number = Column(String(20), unique=True)
    locale = Column(String(10), default="uz")
    verified = Column(Boolean, default=False)
    blocked = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### Listing Model
```python
class Listing(Base):
    id = Column(String(36), primary_key=True)  # UUID
    user_id = Column(String(36), ForeignKey("users.id"))
    
    # Location
    region_code = Column(String(2))
    city_name = Column(String(100))
    address = Column(Text)
    
    # Property details
    type = Column(Enum(ListingType))  # ijara/sotuv
    rooms = Column(Integer)
    area_m2 = Column(Float)
    floor = Column(Integer)
    total_floors = Column(Integer)
    
    # Pricing
    price = Column(Numeric(12, 2))
    currency = Column(String(3), default="USD")
    
    # Features
    furnished = Column(Boolean, default=False)
    pets_allowed = Column(Boolean, default=False)
    
    # Content
    title = Column(String(255))
    description = Column(Text)
    media_urls = Column(Text)
    
    # Status
    status = Column(Enum(ListingStatus))  # pending/approved/rejected/archived
```

## 🌍 Regional Data Structure

### Regions (14 total)
```python
REGIONS = {
    "01": "Andijon", "02": "Buxoro", "03": "Farg'ona",
    "04": "Jizzax", "05": "Xorazm", "06": "Namangan",
    "07": "Navoiy", "08": "Qashqadaryo", "09": "Qoraqalpog'iston",
    "10": "Samarqand", "11": "Sirdaryo", "12": "Surxondaryo",
    "13": "Toshkent viloyati", "14": "Toshkent shahri"
}
```

### Special Cases
- **Tashkent City (14)**: 11 districts
- **Karakalpakstan (09)**: 14 cities
- **Other Regions**: Central city + "Other city/district"

## 🔑 Environment Variables

### Required
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_here
```

### Optional
```env
DEBUG=false
ADMIN_IDS=123456789,987654321
BOT_NAME=UyKelishuv Bot
```

## 🎯 Callback Data Patterns

### Listing Creation Flow
```
POST_LISTING                    # Start listing creation
LISTING_REGION:XX              # Select region (01-14)
LISTING_CITY:XX:CityName      # Select city
LISTING_TYPE:ijara|sotuv      # Select type
LISTING_ROOMS:1-6             # Select rooms
LISTING_FURNISHED:yes|no      # Furnished option
LISTING_PETS:yes|no           # Pets allowed
LISTING_SUBMIT                # Submit listing
LISTING_CANCEL                # Cancel listing
```

### Navigation
```
MAIN_MENU                     # Return to main menu
HELP                          # Show help
SETTINGS                      # User settings
SEARCH_LISTINGS               # Search functionality
MY_LISTINGS                   # User's listings
```

## 🚨 Common Issues & Solutions

### Database Connection Issues
```bash
# Check database URL format
DATABASE_URL=postgresql+asyncpg://user:pass@host:port/db

# For SQLite
DATABASE_URL=sqlite+aiosqlite:///uykelishuv.db

# Run migrations
alembic upgrade head
```

### Bot Token Issues
```bash
# Verify token format
TELEGRAM_BOT_TOKEN=123456789:ABCdefGHIjklMNOpqrsTUVwxyz

# Test bot with curl
curl "https://api.telegram.org/bot<TOKEN>/getMe"
```

### Import Errors
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt

# Check Python path
python -c "import sys; print(sys.path)"
```

## 📊 Performance Monitoring

### Key Metrics to Track
- **Response Time**: Handler execution time
- **Database Queries**: Query execution time
- **Memory Usage**: Heap usage
- **Error Rate**: Exception frequency
- **User Activity**: Daily active users

### Logging Levels
- **DEBUG**: Development debugging
- **INFO**: General information
- **WARNING**: Potential issues
- **ERROR**: Error conditions
- **CRITICAL**: System failures

## 🔒 Security Checklist

### Input Validation
- [ ] Phone number format validation
- [ ] Text input sanitization
- [ ] Numeric input validation
- [ ] File upload restrictions

### Access Control
- [ ] Admin ID validation
- [ ] User permission checks
- [ ] Rate limiting implementation
- [ ] Session management

### Data Protection
- [ ] Sensitive data encryption
- [ ] Secure database connections
- [ ] Environment variable security
- [ ] Audit logging

## 🧪 Testing Strategy

### Test Types
```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# End-to-end tests
pytest tests/e2e/

# Coverage report
pytest --cov=src tests/
```

### Test Structure
```
tests/
├── unit/
│   ├── test_services/
│   └── test_utils/
├── integration/
│   ├── test_handlers/
│   └── test_database/
└── e2e/
    └── test_workflows/
```

## 🚀 Deployment Checklist

### Pre-deployment
- [ ] Run all tests
- [ ] Update environment variables
- [ ] Run database migrations
- [ ] Check security settings
- [ ] Verify bot token

### Post-deployment
- [ ] Health check
- [ ] Monitor logs
- [ ] Test bot functionality
- [ ] Check database connections
- [ ] Verify admin access

---

**Remember**: This is a production system handling real estate transactions. Always test changes thoroughly and maintain high code quality standards.
