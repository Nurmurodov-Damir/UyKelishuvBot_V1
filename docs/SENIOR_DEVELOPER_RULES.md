# UyKelishuv Bot - Senior Developer Rules & Guidelines

## 🎯 Project-Specific Development Rules

### 1. Architecture & Code Organization

#### Module Structure Rules
- **ALWAYS** follow the established module separation:
  - `src/bot/` - Telegram bot logic only
  - `src/services/` - Business logic layer
  - `src/database/` - Data access layer
  - `src/utils/` - Shared utilities
- **NEVER** mix database operations in bot handlers
- **ALWAYS** use service layer for business logic
- **MANDATORY** async/await pattern for all database operations

#### Handler Organization
```python
# ✅ CORRECT: Handler delegates to service
async def handle_listing_submit(self, update, context):
    async with AsyncSessionLocal() as db:
        self.listing_service.db = db
        listing = await self.listing_service.create_listing(user_id, data)

# ❌ WRONG: Direct database access in handler
async def handle_listing_submit(self, update, context):
    listing = Listing(user_id=user_id, ...)
    db.add(listing)
```

### 2. Database & Data Management

#### Session Management Rules
- **ALWAYS** use `AsyncSessionLocal()` context manager
- **NEVER** create global database sessions
- **MANDATORY** proper session cleanup in finally blocks
- **ALWAYS** use `await db.commit()` after modifications

#### Model Design Principles
- **UUID primary keys** for all entities
- **Enum types** for status fields (ListingStatus, ListingType)
- **Proper relationships** with back_populates
- **Timestamps** for audit trails (created_at, updated_at)

#### Migration Guidelines
```bash
# ✅ CORRECT: Always create migrations for schema changes
alembic revision --autogenerate -m "Add new field"
alembic upgrade head

# ❌ WRONG: Direct schema modifications
```

### 3. Telegram Bot Development

#### Handler Implementation Rules
- **ALWAYS** use `CallbackQueryHandler` for inline keyboards
- **MANDATORY** `await query.answer()` for callback responses
- **ALWAYS** handle exceptions in handlers
- **NEVER** block the main thread with synchronous operations

#### Keyboard Management
- **ALWAYS** use `InlineKeyboardMarkup` for user interactions
- **CONSISTENT** callback data format: `ACTION:PARAMETER`
- **ALWAYS** provide back/cancel options
- **MANDATORY** keyboard validation before sending

#### User State Management
```python
# ✅ CORRECT: Use context.user_data for state
context.user_data['waiting_for_price'] = True
if context.user_data.get('waiting_for_price'):
    await self.handle_price_input(update, context)

# ❌ WRONG: Global state variables
```

### 4. Error Handling & Logging

#### Exception Handling Standards
- **ALWAYS** wrap handler methods in try-catch
- **MANDATORY** user-friendly error messages
- **ALWAYS** log errors with context
- **NEVER** expose internal errors to users

#### Logging Implementation
```python
# ✅ CORRECT: Structured logging
logger = logging.getLogger(__name__)
logger.error(f"Listing submit handler error: {e}")

# ❌ WRONG: Print statements
print(f"Error: {e}")
```

### 5. Configuration & Environment

#### Environment Variable Rules
- **ALWAYS** use Pydantic Settings for configuration
- **MANDATORY** .env file for local development
- **NEVER** hardcode sensitive values
- **ALWAYS** validate required environment variables

#### Configuration Validation
```python
# ✅ CORRECT: Validate on startup
def create_settings():
    required_vars = ["TELEGRAM_BOT_TOKEN"]
    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"Missing required env var: {var}")
```

### 6. Security & Validation

#### Input Validation Rules
- **ALWAYS** validate user inputs
- **MANDATORY** sanitize text inputs
- **ALWAYS** check user permissions
- **NEVER** trust user-provided data

#### Phone Number Validation
```python
# ✅ CORRECT: Use regex validation
PHONE_REGEX = r"^\+998[0-9]{9}$"
if not re.match(PHONE_REGEX, phone_number):
    raise ValueError("Invalid phone number format")
```

### 7. Performance & Optimization

#### Database Query Optimization
- **ALWAYS** use `selectinload` for relationships
- **MANDATORY** proper indexing on foreign keys
- **ALWAYS** limit query results when possible
- **NEVER** use N+1 queries

#### Async Best Practices
```python
# ✅ CORRECT: Proper async patterns
async def get_user_listings(self, user_id: str) -> List[Listing]:
    result = await self.db.execute(
        select(Listing)
        .options(selectinload(Listing.owner))
        .where(Listing.user_id == user_id)
    )
    return result.scalars().all()
```

### 8. Testing & Quality Assurance

#### Testing Requirements
- **MANDATORY** unit tests for services
- **ALWAYS** test error scenarios
- **REQUIRED** integration tests for handlers
- **NEVER** deploy without testing

#### Code Quality Standards
- **ALWAYS** use type hints
- **MANDATORY** docstrings for public methods
- **ALWAYS** follow PEP 8
- **REQUIRED** code reviews for all changes

### 9. Deployment & Production

#### Railway.com Deployment Rules
- **ALWAYS** use environment variables for production config
- **MANDATORY** run migrations before deployment
- **ALWAYS** test in staging environment first
- **NEVER** deploy directly to production

#### Production Checklist
```bash
# ✅ REQUIRED: Pre-deployment steps
1. alembic upgrade head
2. Verify environment variables
3. Test bot functionality
4. Check database connections
5. Monitor logs
```

### 10. Regional & Localization

#### Multi-language Support
- **ALWAYS** use locale-aware messages
- **MANDATORY** support for uz/ru/en
- **ALWAYS** store user language preference
- **NEVER** hardcode text in handlers

#### Regional Data Management
```python
# ✅ CORRECT: Use configuration constants
REGIONS = {
    "01": "Andijon",
    "02": "Buxoro",
    # ... other regions
}

# ❌ WRONG: Hardcoded region names
```

## 🚨 Critical Development Warnings

### Database Operations
- **NEVER** use synchronous database operations
- **ALWAYS** handle database connection failures
- **MANDATORY** proper transaction management
- **NEVER** commit without proper error handling

### Bot API Limits
- **ALWAYS** respect Telegram API rate limits
- **MANDATORY** handle API errors gracefully
- **ALWAYS** implement retry logic for failed requests
- **NEVER** spam users with messages

### Security Considerations
- **ALWAYS** validate admin permissions
- **MANDATORY** sanitize user inputs
- **ALWAYS** use HTTPS in production
- **NEVER** log sensitive information

## 📋 Development Workflow

### Feature Development Process
1. **Analysis** - Understand requirements
2. **Design** - Plan architecture changes
3. **Implementation** - Follow coding standards
4. **Testing** - Comprehensive test coverage
5. **Review** - Code review process
6. **Deployment** - Staged deployment

### Code Review Checklist
- [ ] Follows project architecture
- [ ] Proper error handling
- [ ] Type hints included
- [ ] Documentation updated
- [ ] Tests written
- [ ] Security considerations
- [ ] Performance impact assessed

## 🎯 Success Metrics

### Code Quality Indicators
- Zero critical security vulnerabilities
- 90%+ test coverage
- All handlers have proper error handling
- Database operations are async
- Configuration is externalized

### Performance Targets
- Handler response time < 2 seconds
- Database query time < 500ms
- Bot uptime > 99%
- Memory usage < 512MB

---

**Remember**: This is a production system handling real estate transactions. Code quality, security, and reliability are paramount.
