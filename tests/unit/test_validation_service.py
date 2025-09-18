"""
Unit Tests - Validation Service
"""
import pytest
from src.services.validation_service import ValidationService


class TestValidationService:
    """Validation service unit tests"""
    
    def test_validate_price_valid(self):
        """Test valid price validation"""
        validator = ValidationService()
        
        # Valid prices
        valid_prices = ["100", "500.50", "1000.99", "0.01"]
        
        for price in valid_prices:
            is_valid, price_value, error = validator.validate_price(price)
            assert is_valid is True
            assert price_value is not None
            assert error is None
            assert price_value > 0
    
    def test_validate_price_invalid(self):
        """Test invalid price validation"""
        validator = ValidationService()
        
        # Invalid prices
        invalid_prices = ["-100", "0", "abc", "1000001", ""]
        
        for price in invalid_prices:
            is_valid, price_value, error = validator.validate_price(price)
            assert is_valid is False
            assert price_value is None
            assert error is not None
    
    def test_validate_price_range_valid(self):
        """Test valid price range validation"""
        validator = ValidationService()
        
        # Valid ranges
        valid_ranges = [
            ("100-500", 100.0, 500.0),
            ("500+", 500.0, None),
            ("500", 500.0, 500.0),
            ("100.5-500.99", 100.5, 500.99)
        ]
        
        for price_text, expected_min, expected_max in valid_ranges:
            is_valid, min_price, max_price, error = validator.validate_price_range(price_text)
            assert is_valid is True
            assert min_price == expected_min
            assert max_price == expected_max
            assert error is None
    
    def test_validate_price_range_invalid(self):
        """Test invalid price range validation"""
        validator = ValidationService()
        
        # Invalid ranges
        invalid_ranges = ["500-100", "abc", "100-", "-500", ""]
        
        for price_text in invalid_ranges:
            is_valid, min_price, max_price, error = validator.validate_price_range(price_text)
            assert is_valid is False
            assert min_price is None
            assert max_price is None
            assert error is not None
    
    def test_validate_title_valid(self):
        """Test valid title validation"""
        validator = ValidationService()
        
        # Valid titles
        valid_titles = [
            "Test Listing",
            "Yangi kvartira",
            "A" * 255,  # Max length
            "A" * 5     # Min length
        ]
        
        for title in valid_titles:
            is_valid, cleaned_title, error = validator.validate_title(title)
            assert is_valid is True
            assert cleaned_title is not None
            assert error is None
            assert len(cleaned_title) >= 5
            assert len(cleaned_title) <= 255
    
    def test_validate_title_invalid(self):
        """Test invalid title validation"""
        validator = ValidationService()
        
        # Invalid titles
        invalid_titles = [
            "",           # Empty
            "Test",       # Too short
            "A" * 256,    # Too long
            "   ",        # Only spaces
            None          # None
        ]
        
        for title in invalid_titles:
            is_valid, cleaned_title, error = validator.validate_title(title)
            assert is_valid is False
            assert cleaned_title is None
            assert error is not None
    
    def test_validate_description_valid(self):
        """Test valid description validation"""
        validator = ValidationService()
        
        # Valid descriptions
        valid_descriptions = [
            "Test description",
            "A" * 2000,  # Max length
            None,        # Optional
            ""           # Empty (optional)
        ]
        
        for description in valid_descriptions:
            is_valid, cleaned_description, error = validator.validate_description(description)
            assert is_valid is True
            assert error is None
    
    def test_validate_description_invalid(self):
        """Test invalid description validation"""
        validator = ValidationService()
        
        # Invalid descriptions
        invalid_descriptions = [
            "A" * 2001,  # Too long
        ]
        
        for description in invalid_descriptions:
            is_valid, cleaned_description, error = validator.validate_description(description)
            assert is_valid is False
            assert cleaned_description is None
            assert error is not None
    
    def test_validate_rooms_valid(self):
        """Test valid rooms validation"""
        validator = ValidationService()
        
        # Valid rooms
        valid_rooms = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        
        for rooms in valid_rooms:
            is_valid, error = validator.validate_rooms(rooms)
            assert is_valid is True
            assert error is None
    
    def test_validate_rooms_invalid(self):
        """Test invalid rooms validation"""
        validator = ValidationService()
        
        # Invalid rooms
        invalid_rooms = [0, -1, 11, 100, "abc", None]
        
        for rooms in invalid_rooms:
            is_valid, error = validator.validate_rooms(rooms)
            assert is_valid is False
            assert error is not None
    
    def test_validate_region_code_valid(self):
        """Test valid region code validation"""
        validator = ValidationService()
        
        # Valid region codes
        valid_regions = ["01", "14", "09"]
        
        for region_code in valid_regions:
            is_valid, error = validator.validate_region_code(region_code)
            assert is_valid is True
            assert error is None
    
    def test_validate_region_code_invalid(self):
        """Test invalid region code validation"""
        validator = ValidationService()
        
        # Invalid region codes
        invalid_regions = ["99", "1", "abc", "", None]
        
        for region_code in invalid_regions:
            is_valid, error = validator.validate_region_code(region_code)
            assert is_valid is False
            assert error is not None
    
    def test_validate_listing_data_valid(self, valid_listing_data):
        """Test valid listing data validation"""
        validator = ValidationService()
        
        is_valid, error = validator.validate_listing_data(valid_listing_data)
        assert is_valid is True
        assert error is None
    
    def test_validate_listing_data_invalid(self, invalid_listing_data):
        """Test invalid listing data validation"""
        validator = ValidationService()
        
        is_valid, error = validator.validate_listing_data(invalid_listing_data)
        assert is_valid is False
        assert error is not None
    
    def test_validate_listing_data_missing_fields(self):
        """Test listing data with missing required fields"""
        validator = ValidationService()
        
        # Missing required fields
        incomplete_data = {
            'region_code': '14',
            'city_name': 'Toshkent'
            # Missing: type, rooms, price, title
        }
        
        is_valid, error = validator.validate_listing_data(incomplete_data)
        assert is_valid is False
        assert error is not None
        assert "Kerakli maydon topilmadi" in error
