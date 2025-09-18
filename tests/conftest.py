"""
Test Fixtures - Test uchun ma'lumotlar
"""
import pytest
import pytest_asyncio
import asyncio
from typing import AsyncGenerator, Generator
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from telegram import Update, User, Chat, Message, CallbackQuery, InlineKeyboardButton
from telegram.ext import ContextTypes

from src.database.database import AsyncSessionLocal
from src.database.models import Base, User as DBUser, Listing, ListingType, ListingStatus
from src.services.user_service import UserService
from src.services.listing_service import ListingService
from src.services.validation_service import ValidationService
from src.services.keyboard_builder import KeyboardBuilder
from src.services.message_builder import MessageBuilder
from src.bot.handlers.listing_handlers import ListingHandlers


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Event loop fixture"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """Test database session"""
    # Test uchun SQLite in-memory database
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Create session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    
    async with async_session() as session:
        yield session
    
    await engine.dispose()


@pytest.fixture
def mock_user() -> User:
    """Mock Telegram user"""
    return User(
        id=123456789,
        is_bot=False,
        first_name="Test",
        last_name="User",
        username="testuser",
        language_code="uz"
    )


@pytest.fixture
def mock_chat() -> Chat:
    """Mock Telegram chat"""
    return Chat(
        id=123456789,
        type="private"
    )


@pytest.fixture
def mock_message(mock_user: User, mock_chat: Chat) -> Message:
    """Mock Telegram message"""
    return Message(
        message_id=1,
        from_user=mock_user,
        chat=mock_chat,
        date=1234567890,
        text="Test message"
    )


@pytest.fixture
def mock_callback_query(mock_user: User, mock_chat: Chat) -> CallbackQuery:
    """Mock Telegram callback query"""
    return CallbackQuery(
        id="test_callback_id",
        from_user=mock_user,
        chat_instance="test_chat_instance",
        data="TEST_CALLBACK"
    )


@pytest.fixture
def mock_update(mock_message: Message, mock_callback_query: CallbackQuery) -> Update:
    """Mock Telegram update"""
    update = Update(update_id=1)
    update.message = mock_message
    update.callback_query = mock_callback_query
    return update


@pytest.fixture
def mock_context() -> ContextTypes.DEFAULT_TYPE:
    """Mock Telegram context"""
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.user_data = {}
    context.bot_data = {}
    context.application = MagicMock()
    return context


@pytest_asyncio.fixture
async def test_user(test_db: AsyncSession) -> DBUser:
    """Test database user"""
    user = DBUser(
        telegram_user_id=123456789,
        name="Test User",
        phone_number="+998901234567",
        locale="uz",
        verified=True
    )
    test_db.add(user)
    await test_db.commit()
    await test_db.refresh(user)
    return user


@pytest_asyncio.fixture
async def test_listing(test_db: AsyncSession, test_user: DBUser) -> Listing:
    """Test database listing"""
    listing = Listing(
        user_id=test_user.id,
        region_code="14",
        city_name="Toshkent",
        type=ListingType.ijara,
        rooms=3,
        price=500.0,
        currency="USD",
        title="Test Listing",
        description="Test description",
        furnished=True,
        pets_allowed=False,
        status=ListingStatus.approved
    )
    test_db.add(listing)
    await test_db.commit()
    await test_db.refresh(listing)
    return listing


@pytest.fixture
def user_service(test_db: AsyncSession) -> UserService:
    """User service fixture"""
    return UserService(test_db)


@pytest.fixture
def listing_service(test_db: AsyncSession) -> ListingService:
    """Listing service fixture"""
    return ListingService(test_db)


@pytest.fixture
def validation_service() -> ValidationService:
    """Validation service fixture"""
    return ValidationService()


@pytest.fixture
def keyboard_builder() -> KeyboardBuilder:
    """Keyboard builder fixture"""
    return KeyboardBuilder()


@pytest.fixture
def message_builder() -> MessageBuilder:
    """Message builder fixture"""
    return MessageBuilder()


@pytest.fixture
def listing_handlers(listing_service: ListingService) -> ListingHandlers:
    """Listing handlers fixture"""
    return ListingHandlers(listing_service)


# Test data fixtures
@pytest.fixture
def valid_listing_data() -> dict:
    """Valid listing data for testing"""
    return {
        'region_code': '14',
        'city_name': 'Toshkent',
        'type': 'ijara',
        'rooms': 3,
        'price': 500.0,
        'currency': 'USD',
        'title': 'Test Listing',
        'description': 'Test description',
        'furnished': True,
        'pets_allowed': False
    }


@pytest.fixture
def invalid_listing_data() -> dict:
    """Invalid listing data for testing"""
    return {
        'region_code': '99',  # Invalid region
        'city_name': '',      # Empty city
        'type': 'invalid',    # Invalid type
        'rooms': 0,           # Invalid rooms
        'price': -100,        # Invalid price
        'title': '',          # Empty title
    }


@pytest.fixture
def search_filters() -> dict:
    """Search filters for testing"""
    return {
        'region_code': '14',
        'city_name': 'Toshkent',
        'type': 'ijara',
        'rooms': 3,
        'min_price': 100.0,
        'max_price': 1000.0,
        'furnished': True,
        'pets_allowed': False
    }
