"""
Unit Tests - Keyboard Builder Service
"""
import pytest
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from src.services.keyboard_builder import KeyboardBuilder
from src.utils.constants import CallbackPatterns, KeyboardTexts


class TestKeyboardBuilder:
    """Keyboard builder service unit tests"""
    
    def test_create_main_menu(self):
        """Test main menu keyboard creation"""
        builder = KeyboardBuilder()
        
        keyboard = builder.create_main_menu()
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 4  # 4 rows
        
        # Check first row (POST_LISTING)
        assert keyboard.inline_keyboard[0][0].text == KeyboardTexts.POST_LISTING
        assert keyboard.inline_keyboard[0][0].callback_data == CallbackPatterns.POST_LISTING
        
        # Check second row (SEARCH_LISTINGS)
        assert keyboard.inline_keyboard[1][0].text == KeyboardTexts.SEARCH_LISTINGS
        assert keyboard.inline_keyboard[1][0].callback_data == CallbackPatterns.SEARCH_LISTINGS
        
        # Check third row (MY_LISTINGS)
        assert keyboard.inline_keyboard[2][0].text == KeyboardTexts.MY_LISTINGS
        assert keyboard.inline_keyboard[2][0].callback_data == CallbackPatterns.MY_LISTINGS
        
        # Check fourth row (SETTINGS and HELP)
        assert keyboard.inline_keyboard[3][0].text == KeyboardTexts.SETTINGS
        assert keyboard.inline_keyboard[3][0].callback_data == CallbackPatterns.SETTINGS
        assert keyboard.inline_keyboard[3][1].text == KeyboardTexts.HELP
        assert keyboard.inline_keyboard[3][1].callback_data == CallbackPatterns.HELP
    
    def test_create_back_button(self):
        """Test back button keyboard creation"""
        builder = KeyboardBuilder()
        
        keyboard = builder.create_back_button()
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 1
        assert len(keyboard.inline_keyboard[0]) == 1
        
        button = keyboard.inline_keyboard[0][0]
        assert button.text == KeyboardTexts.BACK_TO_MAIN
        assert button.callback_data == CallbackPatterns.MAIN_MENU
    
    def test_create_regions_keyboard_listing(self):
        """Test regions keyboard for listing creation"""
        builder = KeyboardBuilder()
        
        keyboard = builder.create_regions_keyboard(is_search=False)
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) > 0
        
        # Check that all buttons have correct callback pattern
        for row in keyboard.inline_keyboard:
            for button in row:
                if button.callback_data != CallbackPatterns.MAIN_MENU:
                    assert button.callback_data.startswith(f"{CallbackPatterns.LISTING_REGION}:")
    
    def test_create_regions_keyboard_search(self):
        """Test regions keyboard for search"""
        builder = KeyboardBuilder()
        
        keyboard = builder.create_regions_keyboard(is_search=True)
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) > 0
        
        # Check first button is "All regions"
        first_button = keyboard.inline_keyboard[0][0]
        assert first_button.text == KeyboardTexts.ALL_REGIONS
        assert first_button.callback_data == f"{CallbackPatterns.SEARCH_REGION}:all"
        
        # Check that other buttons have correct callback pattern
        for row in keyboard.inline_keyboard[1:]:
            for button in row:
                if button.callback_data != CallbackPatterns.MAIN_MENU:
                    assert button.callback_data.startswith(f"{CallbackPatterns.SEARCH_REGION}:")
    
    def test_create_cities_keyboard_listing(self):
        """Test cities keyboard for listing creation"""
        builder = KeyboardBuilder()
        
        region_code = "14"  # Toshkent
        keyboard = builder.create_cities_keyboard(region_code, is_search=False)
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) > 0
        
        # Check that all buttons have correct callback pattern
        for row in keyboard.inline_keyboard:
            for button in row:
                if button.callback_data != CallbackPatterns.POST_LISTING:
                    assert button.callback_data.startswith(f"{CallbackPatterns.LISTING_CITY}:{region_code}:")
    
    def test_create_cities_keyboard_search(self):
        """Test cities keyboard for search"""
        builder = KeyboardBuilder()
        
        region_code = "14"  # Toshkent
        keyboard = builder.create_cities_keyboard(region_code, is_search=True)
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) > 0
        
        # Check first button is "All cities"
        first_button = keyboard.inline_keyboard[0][0]
        assert first_button.text == KeyboardTexts.ALL_CITIES
        assert first_button.callback_data == f"{CallbackPatterns.SEARCH_CITY}:{region_code}:all"
    
    def test_create_type_keyboard_listing(self):
        """Test type keyboard for listing creation"""
        builder = KeyboardBuilder()
        
        keyboard = builder.create_type_keyboard(is_search=False)
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 3  # 2 type buttons + back button
        
        # Check rent button
        rent_button = keyboard.inline_keyboard[0][0]
        assert rent_button.text == KeyboardTexts.RENT
        assert rent_button.callback_data == f"{CallbackPatterns.LISTING_TYPE}:ijara"
        
        # Check sale button
        sale_button = keyboard.inline_keyboard[1][0]
        assert sale_button.text == KeyboardTexts.SALE
        assert sale_button.callback_data == f"{CallbackPatterns.LISTING_TYPE}:sotuv"
    
    def test_create_type_keyboard_search(self):
        """Test type keyboard for search"""
        builder = KeyboardBuilder()
        
        keyboard = builder.create_type_keyboard(is_search=True)
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 4  # 3 type buttons + back button
        
        # Check all types button
        all_types_button = keyboard.inline_keyboard[2][0]
        assert all_types_button.text == KeyboardTexts.ALL_TYPES
        assert all_types_button.callback_data == f"{CallbackPatterns.SEARCH_TYPE}:all"
    
    def test_create_rooms_keyboard_listing(self):
        """Test rooms keyboard for listing creation"""
        builder = KeyboardBuilder()
        
        keyboard = builder.create_rooms_keyboard(is_search=False)
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 3  # 2 room rows + back button
        
        # Check first row (1, 2, 3)
        assert keyboard.inline_keyboard[0][0].text == "1"
        assert keyboard.inline_keyboard[0][0].callback_data == f"{CallbackPatterns.LISTING_ROOMS}:1"
        assert keyboard.inline_keyboard[0][1].text == "2"
        assert keyboard.inline_keyboard[0][1].callback_data == f"{CallbackPatterns.LISTING_ROOMS}:2"
        assert keyboard.inline_keyboard[0][2].text == "3"
        assert keyboard.inline_keyboard[0][2].callback_data == f"{CallbackPatterns.LISTING_ROOMS}:3"
        
        # Check second row (4, 5, 6+)
        assert keyboard.inline_keyboard[1][0].text == "4"
        assert keyboard.inline_keyboard[1][0].callback_data == f"{CallbackPatterns.LISTING_ROOMS}:4"
        assert keyboard.inline_keyboard[1][1].text == "5"
        assert keyboard.inline_keyboard[1][1].callback_data == f"{CallbackPatterns.LISTING_ROOMS}:5"
        assert keyboard.inline_keyboard[1][2].text == "6+"
        assert keyboard.inline_keyboard[1][2].callback_data == f"{CallbackPatterns.LISTING_ROOMS}:6"
    
    def test_create_rooms_keyboard_search(self):
        """Test rooms keyboard for search"""
        builder = KeyboardBuilder()
        
        keyboard = builder.create_rooms_keyboard(is_search=True)
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 4  # 3 room rows + back button
        
        # Check all rooms button
        all_rooms_button = keyboard.inline_keyboard[2][0]
        assert all_rooms_button.text == KeyboardTexts.ALL_ROOMS
        assert all_rooms_button.callback_data == f"{CallbackPatterns.SEARCH_ROOMS}:all"
    
    def test_create_yes_no_keyboard_furnished(self):
        """Test yes/no keyboard for furnished option"""
        builder = KeyboardBuilder()
        
        keyboard = builder.create_yes_no_keyboard("furnished", is_search=False)
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 2  # Yes/No + back button
        
        # Check yes button
        yes_button = keyboard.inline_keyboard[0][0]
        assert yes_button.text == "✅ Ha"
        assert yes_button.callback_data == f"{CallbackPatterns.LISTING_FURNISHED}:yes"
        
        # Check no button
        no_button = keyboard.inline_keyboard[0][1]
        assert no_button.text == "❌ Yo'q"
        assert no_button.callback_data == f"{CallbackPatterns.LISTING_FURNISHED}:no"
    
    def test_create_yes_no_keyboard_pets(self):
        """Test yes/no keyboard for pets option"""
        builder = KeyboardBuilder()
        
        keyboard = builder.create_yes_no_keyboard("pets", is_search=False)
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        
        # Check yes button
        yes_button = keyboard.inline_keyboard[0][0]
        assert yes_button.text == "✅ Ha"
        assert yes_button.callback_data == f"{CallbackPatterns.LISTING_PETS}:yes"
    
    def test_create_price_keyboard(self):
        """Test price keyboard creation"""
        builder = KeyboardBuilder()
        
        keyboard = builder.create_price_keyboard(is_search=True)
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 2  # Custom price + back button
        
        # Check custom price button
        custom_button = keyboard.inline_keyboard[0][0]
        assert custom_button.text == KeyboardTexts.CUSTOM_PRICE
        assert custom_button.callback_data == f"{CallbackPatterns.SEARCH_PRICE}:custom"
    
    def test_create_search_filters_keyboard(self):
        """Test search filters keyboard creation"""
        builder = KeyboardBuilder()
        
        keyboard = builder.create_search_filters_keyboard()
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 4  # 4 rows
        
        # Check furnished button
        furnished_button = keyboard.inline_keyboard[0][0]
        assert furnished_button.text == KeyboardTexts.FURNISHED
        assert furnished_button.callback_data == f"{CallbackPatterns.SEARCH_FURNISHED}:filter"
        
        # Check pets button
        pets_button = keyboard.inline_keyboard[1][0]
        assert pets_button.text == KeyboardTexts.PETS_ALLOWED
        assert pets_button.callback_data == f"{CallbackPatterns.SEARCH_PETS}:filter"
        
        # Check execute search button
        execute_button = keyboard.inline_keyboard[2][0]
        assert execute_button.text == KeyboardTexts.EXECUTE_SEARCH
        assert execute_button.callback_data == CallbackPatterns.SEARCH_EXECUTE
    
    def test_create_pagination_keyboard(self):
        """Test pagination keyboard creation"""
        builder = KeyboardBuilder()
        
        current_page = 1
        total_pages = 5
        keyboard = builder.create_pagination_keyboard(current_page, total_pages)
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 2  # Navigation + other buttons
        
        # Check navigation row
        nav_row = keyboard.inline_keyboard[0]
        assert len(nav_row) == 3  # Prev, Page info, Next
        
        # Check prev button
        prev_button = nav_row[0]
        assert prev_button.text == KeyboardTexts.PREV_PAGE
        assert prev_button.callback_data == f"{CallbackPatterns.SEARCH_PAGE}:0"
        
        # Check page info button
        page_info_button = nav_row[1]
        assert page_info_button.text == "2/5"
        assert page_info_button.callback_data == "PAGE_INFO"
        
        # Check next button
        next_button = nav_row[2]
        assert next_button.text == KeyboardTexts.NEXT_PAGE
        assert next_button.callback_data == f"{CallbackPatterns.SEARCH_PAGE}:2"
    
    def test_create_pagination_keyboard_first_page(self):
        """Test pagination keyboard for first page"""
        builder = KeyboardBuilder()
        
        current_page = 0
        total_pages = 3
        keyboard = builder.create_pagination_keyboard(current_page, total_pages)
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        
        # Check navigation row (no prev button)
        nav_row = keyboard.inline_keyboard[0]
        assert len(nav_row) == 2  # Page info, Next
        
        # Check page info button
        page_info_button = nav_row[0]
        assert page_info_button.text == "1/3"
        
        # Check next button
        next_button = nav_row[1]
        assert next_button.text == KeyboardTexts.NEXT_PAGE
        assert next_button.callback_data == f"{CallbackPatterns.SEARCH_PAGE}:1"
    
    def test_create_pagination_keyboard_last_page(self):
        """Test pagination keyboard for last page"""
        builder = KeyboardBuilder()
        
        current_page = 2
        total_pages = 3
        keyboard = builder.create_pagination_keyboard(current_page, total_pages)
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        
        # Check navigation row (no next button)
        nav_row = keyboard.inline_keyboard[0]
        assert len(nav_row) == 2  # Prev, Page info
        
        # Check prev button
        prev_button = nav_row[0]
        assert prev_button.text == KeyboardTexts.PREV_PAGE
        assert prev_button.callback_data == f"{CallbackPatterns.SEARCH_PAGE}:1"
        
        # Check page info button
        page_info_button = nav_row[1]
        assert page_info_button.text == "3/3"
    
    def test_create_pagination_keyboard_single_page(self):
        """Test pagination keyboard for single page"""
        builder = KeyboardBuilder()
        
        current_page = 0
        total_pages = 1
        keyboard = builder.create_pagination_keyboard(current_page, total_pages)
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 1  # Only other buttons row
        
        # Check other buttons row
        other_row = keyboard.inline_keyboard[0]
        assert len(other_row) == 2  # Refresh search, Back to main
        
        # Check refresh search button
        refresh_button = other_row[0]
        assert refresh_button.text == KeyboardTexts.REFRESH_SEARCH
        assert refresh_button.callback_data == CallbackPatterns.SEARCH_LISTINGS
        
        # Check back to main button
        back_button = other_row[1]
        assert back_button.text == KeyboardTexts.BACK_TO_MAIN
        assert back_button.callback_data == CallbackPatterns.MAIN_MENU
    
    def test_create_listing_preview_keyboard(self):
        """Test listing preview keyboard creation"""
        builder = KeyboardBuilder()
        
        keyboard = builder.create_listing_preview_keyboard()
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 1
        assert len(keyboard.inline_keyboard[0]) == 2
        
        # Check submit button
        submit_button = keyboard.inline_keyboard[0][0]
        assert submit_button.text == "✅ Yuborish"
        assert submit_button.callback_data == CallbackPatterns.LISTING_SUBMIT
        
        # Check cancel button
        cancel_button = keyboard.inline_keyboard[0][1]
        assert cancel_button.text == KeyboardTexts.CANCEL
        assert cancel_button.callback_data == CallbackPatterns.LISTING_CANCEL
    
    def test_create_description_skip_keyboard(self):
        """Test description skip keyboard creation"""
        builder = KeyboardBuilder()
        
        keyboard = builder.create_description_skip_keyboard()
        
        assert isinstance(keyboard, InlineKeyboardMarkup)
        assert len(keyboard.inline_keyboard) == 2
        
        # Check skip description button
        skip_button = keyboard.inline_keyboard[0][0]
        assert skip_button.text == KeyboardTexts.SKIP_DESCRIPTION
        assert skip_button.callback_data == CallbackPatterns.LISTING_SKIP_DESCRIPTION
        
        # Check back to main button
        back_button = keyboard.inline_keyboard[1][0]
        assert back_button.text == KeyboardTexts.BACK_TO_MAIN
        assert back_button.callback_data == CallbackPatterns.MAIN_MENU
