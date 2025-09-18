"""
Unit Tests - Message Builder Service
"""
import pytest
from src.services.message_builder import MessageBuilder


class TestMessageBuilder:
    """Message builder service unit tests"""
    
    def test_create_welcome_message(self):
        """Test welcome message creation"""
        builder = MessageBuilder()
        
        name = "Test User"
        message = builder.create_welcome_message(name)
        
        assert isinstance(message, str)
        assert name in message
        assert "UyKelishuv" in message
        assert "xush kelibsiz" in message
    
    def test_create_help_message(self):
        """Test help message creation"""
        builder = MessageBuilder()
        
        message = builder.create_help_message()
        
        assert isinstance(message, str)
        assert "Yordam" in message
        assert "funksiyalar" in message
        assert "Komandalar" in message
    
    def test_create_search_start_message(self):
        """Test search start message creation"""
        builder = MessageBuilder()
        
        message = builder.create_search_start_message()
        
        assert isinstance(message, str)
        assert "E'lon qidirish" in message
        assert "viloyatni tanlang" in message
    
    def test_create_listing_start_message(self):
        """Test listing start message creation"""
        builder = MessageBuilder()
        
        message = builder.create_listing_start_message()
        
        assert isinstance(message, str)
        assert "E'lon joylashtirish" in message
        assert "viloyatni tanlang" in message
    
    def test_create_region_selection_message(self):
        """Test region selection message creation"""
        builder = MessageBuilder()
        
        region_name = "Toshkent"
        message = builder.create_region_selection_message(region_name)
        
        assert isinstance(message, str)
        assert region_name in message
        assert "shahar/tumanni tanlang" in message
    
    def test_create_city_selection_message(self):
        """Test city selection message creation"""
        builder = MessageBuilder()
        
        region_name = "Toshkent"
        city_name = "Chilonzor"
        message = builder.create_city_selection_message(region_name, city_name)
        
        assert isinstance(message, str)
        assert region_name in message
        assert city_name in message
        assert "e'lon turini tanlang" in message
    
    def test_create_type_selection_message(self):
        """Test type selection message creation"""
        builder = MessageBuilder()
        
        type_name = "Ijara"
        message = builder.create_type_selection_message(type_name)
        
        assert isinstance(message, str)
        assert type_name in message
        assert "uy turini tanlang" in message
    
    def test_create_rooms_selection_message(self):
        """Test rooms selection message creation"""
        builder = MessageBuilder()
        
        rooms_text = "3 xona"
        message = builder.create_rooms_selection_message(rooms_text)
        
        assert isinstance(message, str)
        assert rooms_text in message
        assert "Narx oralig'ini belgilang" in message
    
    def test_create_price_input_message(self):
        """Test price input message creation"""
        builder = MessageBuilder()
        
        message = builder.create_price_input_message()
        
        assert isinstance(message, str)
        assert "Narx oralig'ini kiriting" in message
        assert "Masalan" in message
    
    def test_create_price_confirmation_message(self):
        """Test price confirmation message creation"""
        builder = MessageBuilder()
        
        min_price = 100.0
        max_price = 500.0
        message = builder.create_price_confirmation_message(min_price, max_price)
        
        assert isinstance(message, str)
        assert "100.0-500.0 USD" in message
        assert "filtrlarni tanlang" in message
    
    def test_create_price_confirmation_message_min_only(self):
        """Test price confirmation message with min price only"""
        builder = MessageBuilder()
        
        min_price = 500.0
        max_price = None
        message = builder.create_price_confirmation_message(min_price, max_price)
        
        assert isinstance(message, str)
        assert "500.0+ USD" in message
    
    def test_create_price_confirmation_message_exact(self):
        """Test price confirmation message with exact price"""
        builder = MessageBuilder()
        
        min_price = 500.0
        max_price = 500.0
        message = builder.create_price_confirmation_message(min_price, max_price)
        
        assert isinstance(message, str)
        assert "500.0 USD" in message
    
    def test_create_search_filters_message(self):
        """Test search filters message creation"""
        builder = MessageBuilder()
        
        message = builder.create_search_filters_message()
        
        assert isinstance(message, str)
        assert "filtrlarni tanlang" in message
    
    def test_create_no_search_results_message(self):
        """Test no search results message creation"""
        builder = MessageBuilder()
        
        message = builder.create_no_search_results_message()
        
        assert isinstance(message, str)
        assert "topilmadi" in message
        assert "qaytadan urinib ko'ring" in message
    
    def test_create_listing_preview_message(self, valid_listing_data):
        """Test listing preview message creation"""
        builder = MessageBuilder()
        
        message = builder.create_listing_preview_message(valid_listing_data)
        
        assert isinstance(message, str)
        assert valid_listing_data['title'] in message
        assert valid_listing_data['city_name'] in message
        assert "E'loni yuborishni tasdiqlaysizmi?" in message
    
    def test_create_success_message(self):
        """Test success message creation"""
        builder = MessageBuilder()
        
        message = builder.create_success_message("listing_created")
        
        assert isinstance(message, str)
        assert "muvaffaqiyatli yuborildi" in message
        assert "tekshirish jarayonida" in message
    
    def test_create_error_message_generic(self):
        """Test generic error message creation"""
        builder = MessageBuilder()
        
        message = builder.create_error_message("generic")
        
        assert isinstance(message, str)
        assert "Xatolik yuz berdi" in message
    
    def test_create_error_message_custom(self):
        """Test custom error message creation"""
        builder = MessageBuilder()
        
        custom_message = "Custom error message"
        message = builder.create_error_message("generic", custom_message)
        
        assert isinstance(message, str)
        assert custom_message in message
        assert message.startswith("❌")
    
    def test_create_validation_error_message(self):
        """Test validation error message creation"""
        builder = MessageBuilder()
        
        field = "title"
        error = "Title is too short"
        message = builder.create_validation_error_message(field, error)
        
        assert isinstance(message, str)
        assert field in message
        assert error in message
        assert message.startswith("❌")
    
    def test_create_price_input_error_message(self):
        """Test price input error message creation"""
        builder = MessageBuilder()
        
        message = builder.create_price_input_error_message()
        
        assert isinstance(message, str)
        assert "Noto'g'ri narx format" in message
        assert "To'g'ri formatlar" in message
    
    def test_create_title_input_error_message(self):
        """Test title input error message creation"""
        builder = MessageBuilder()
        
        message = builder.create_title_input_error_message()
        
        assert isinstance(message, str)
        assert "Sarlavha noto'g'ri" in message
        assert "Kamida" in message
        assert "maksimum" in message
    
    def test_create_rooms_input_error_message(self):
        """Test rooms input error message creation"""
        builder = MessageBuilder()
        
        message = builder.create_rooms_input_error_message()
        
        assert isinstance(message, str)
        assert "Xonalar soni noto'g'ri" in message
        assert "dan" in message
        assert "gacha" in message
    
    def test_format_price_range(self):
        """Test price range formatting"""
        builder = MessageBuilder()
        
        # Test range
        result = builder._format_price_range(100.0, 500.0)
        assert result == "100.0-500.0 USD"
        
        # Test min only
        result = builder._format_price_range(500.0, None)
        assert result == "500.0+ USD"
        
        # Test exact
        result = builder._format_price_range(500.0, 500.0)
        assert result == "500.0 USD"
        
        # Test unlimited
        result = builder._format_price_range(None, None)
        assert result == "Cheklanmagan"
