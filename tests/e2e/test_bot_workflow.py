"""
End-to-End Tests - Bot Workflow
"""
import pytest
from unittest.mock import AsyncMock, MagicMock
from telegram import Update, User, Chat, Message, CallbackQuery
from telegram.ext import ContextTypes

from src.bot.handlers.listing_handlers import ListingHandlers
from src.services.listing_service import ListingService


@pytest.mark.asyncio
class TestBotWorkflowE2E:
    """End-to-end bot workflow tests"""
    
    async def test_listing_creation_workflow(self, test_db, mock_update, mock_context):
        """Test complete listing creation workflow"""
        # Setup
        listing_service = ListingService(test_db)
        handlers = ListingHandlers(listing_service)
        
        # Mock user data
        user_id = 123456789
        mock_update.effective_user.id = user_id
        mock_context.user_data = {}
        
        # Step 1: Start listing creation
        await handlers.handle_post_listing(mock_update, mock_context)
        
        # Verify user data is initialized
        assert user_id in handlers.user_data
        assert handlers.user_data[user_id] == {}
        
        # Step 2: Select region
        await handlers.handle_region_selection(mock_update, mock_context, "14")
        
        # Verify region data is stored
        assert handlers.user_data[user_id]['region_code'] == "14"
        assert handlers.user_data[user_id]['region_name'] == "Toshkent shahri"
        
        # Step 3: Select city
        await handlers.handle_city_selection(mock_update, mock_context, "14", "Chilonzor")
        
        # Verify city data is stored
        assert handlers.user_data[user_id]['city_name'] == "Chilonzor"
        
        # Step 4: Select type
        await handlers.handle_type_selection(mock_update, mock_context, "ijara")
        
        # Verify type data is stored
        assert handlers.user_data[user_id]['type'] == "ijara"
        
        # Step 5: Select rooms
        await handlers.handle_rooms_selection(mock_update, mock_context, "3")
        
        # Verify rooms data is stored
        assert handlers.user_data[user_id]['rooms'] == 3
        
        # Step 6: Input price
        mock_update.message.text = "500"
        await handlers.handle_price_input(mock_update, mock_context)
        
        # Verify price data is stored
        assert handlers.user_data[user_id]['price'] == 500.0
        
        # Step 7: Input title
        mock_update.message.text = "Yangi kvartira"
        await handlers.handle_title_input(mock_update, mock_context)
        
        # Verify title data is stored
        assert handlers.user_data[user_id]['title'] == "Yangi kvartira"
        
        # Step 8: Input description
        mock_update.message.text = "Juda yaxshi kvartira"
        await handlers.handle_description_input(mock_update, mock_context)
        
        # Verify description data is stored
        assert handlers.user_data[user_id]['description'] == "Juda yaxshi kvartira"
        
        # Step 9: Submit listing
        await handlers.handle_listing_submit(mock_update, mock_context)
        
        # Verify user data is cleared after submission
        assert user_id not in handlers.user_data
    
    async def test_search_workflow(self, test_db, mock_update, mock_context):
        """Test complete search workflow"""
        # Setup
        listing_service = ListingService(test_db)
        handlers = ListingHandlers(listing_service)
        
        # Mock user data
        user_id = 123456789
        mock_update.effective_user.id = user_id
        mock_context.user_data = {}
        
        # Step 1: Start search
        await handlers.handle_search_listings(mock_update, mock_context)
        
        # Verify search data is initialized
        assert user_id in handlers.search_data
        assert handlers.search_data[user_id] == {}
        
        # Step 2: Select region
        await handlers.handle_search_region_selection(mock_update, mock_context, "14")
        
        # Verify region data is stored
        assert handlers.search_data[user_id]['region_code'] == "14"
        assert handlers.search_data[user_id]['region_name'] == "Toshkent shahri"
        
        # Step 3: Select city
        await handlers.handle_search_city_selection(mock_update, mock_context, "14", "Chilonzor")
        
        # Verify city data is stored
        assert handlers.search_data[user_id]['city_name'] == "Chilonzor"
        
        # Step 4: Select type
        await handlers.handle_search_type_selection(mock_update, mock_context, "ijara")
        
        # Verify type data is stored
        assert handlers.search_data[user_id]['type'] == "ijara"
        
        # Step 5: Select rooms
        await handlers.handle_search_rooms_selection(mock_update, mock_context, "3")
        
        # Verify rooms data is stored
        assert handlers.search_data[user_id]['rooms'] == "3"
        
        # Step 6: Input custom price
        await handlers.handle_search_price_custom(mock_update, mock_context)
        
        # Verify waiting state is set
        assert mock_context.user_data['waiting_for_price_range'] is True
        
        # Step 7: Input price range
        mock_update.message.text = "300-600"
        await handlers.handle_search_price_input(mock_update, mock_context)
        
        # Verify price data is stored
        assert handlers.search_data[user_id]['min_price'] == 300.0
        assert handlers.search_data[user_id]['max_price'] == 600.0
        
        # Verify waiting state is cleared
        assert mock_context.user_data['waiting_for_price_range'] is False
        
        # Step 8: Execute search
        await handlers.handle_search_execute(mock_update, mock_context)
        
        # Verify search results are stored in context
        assert f'search_results_{user_id}' in mock_context.user_data
        assert f'search_page_{user_id}' in mock_context.user_data
    
    async def test_error_handling_workflow(self, test_db, mock_update, mock_context):
        """Test error handling in workflow"""
        # Setup
        listing_service = ListingService(test_db)
        handlers = ListingHandlers(listing_service)
        
        # Mock user data
        user_id = 123456789
        mock_update.effective_user.id = user_id
        mock_context.user_data = {}
        
        # Test invalid region code
        await handlers.handle_region_selection(mock_update, mock_context, "99")
        
        # Verify error handling - should not crash
        assert user_id in handlers.user_data
        
        # Test invalid price input
        mock_update.message.text = "invalid_price"
        await handlers.handle_price_input(mock_update, mock_context)
        
        # Verify error handling - should not crash
        assert user_id in handlers.user_data
        
        # Test invalid title input
        mock_update.message.text = "Hi"  # Too short
        await handlers.handle_title_input(mock_update, mock_context)
        
        # Verify error handling - should not crash
        assert user_id in handlers.user_data
    
    async def test_cancel_workflow(self, test_db, mock_update, mock_context):
        """Test cancel workflow"""
        # Setup
        listing_service = ListingService(test_db)
        handlers = ListingHandlers(listing_service)
        
        # Mock user data
        user_id = 123456789
        mock_update.effective_user.id = user_id
        mock_context.user_data = {}
        
        # Start listing creation
        await handlers.handle_post_listing(mock_update, mock_context)
        
        # Add some data
        handlers.user_data[user_id] = {
            'region_code': '14',
            'city_name': 'Toshkent',
            'type': 'ijara'
        }
        
        # Cancel listing
        await handlers.handle_listing_cancel(mock_update, mock_context)
        
        # Verify user data is cleared
        assert user_id not in handlers.user_data
    
    async def test_search_pagination_workflow(self, test_db, mock_update, mock_context):
        """Test search pagination workflow"""
        # Setup
        listing_service = ListingService(test_db)
        handlers = ListingHandlers(listing_service)
        
        # Mock user data
        user_id = 123456789
        mock_update.effective_user.id = user_id
        mock_context.user_data = {}
        
        # Mock search results
        mock_listings = [MagicMock() for _ in range(10)]
        mock_context.user_data[f'search_results_{user_id}'] = mock_listings
        mock_context.user_data[f'search_page_{user_id}'] = 0
        
        # Test pagination
        await handlers._show_search_page(mock_update, mock_context, mock_listings, 0)
        
        # Verify pagination works
        assert f'search_results_{user_id}' in mock_context.user_data
        assert f'search_page_{user_id}' in mock_context.user_data
    
    async def test_workflow_state_management(self, test_db, mock_update, mock_context):
        """Test workflow state management"""
        # Setup
        listing_service = ListingService(test_db)
        handlers = ListingHandlers(listing_service)
        
        # Mock user data
        user_id = 123456789
        mock_update.effective_user.id = user_id
        mock_context.user_data = {}
        
        # Test listing creation state
        await handlers.handle_post_listing(mock_update, mock_context)
        assert user_id in handlers.user_data
        assert user_id not in handlers.search_data
        
        # Test search state
        await handlers.handle_search_listings(mock_update, mock_context)
        assert user_id in handlers.search_data
        assert user_id in handlers.user_data  # Should still be there
        
        # Test state isolation
        handlers.user_data[user_id]['test'] = 'value'
        handlers.search_data[user_id]['test'] = 'different_value'
        
        assert handlers.user_data[user_id]['test'] == 'value'
        assert handlers.search_data[user_id]['test'] == 'different_value'
    
    async def test_concurrent_user_workflows(self, test_db, mock_update, mock_context):
        """Test concurrent user workflows"""
        # Setup
        listing_service = ListingService(test_db)
        handlers = ListingHandlers(listing_service)
        
        # Mock multiple users
        user1_id = 111111111
        user2_id = 222222222
        
        # User 1 starts listing creation
        mock_update.effective_user.id = user1_id
        await handlers.handle_post_listing(mock_update, mock_context)
        handlers.user_data[user1_id]['region_code'] = '14'
        
        # User 2 starts search
        mock_update.effective_user.id = user2_id
        await handlers.handle_search_listings(mock_update, mock_context)
        handlers.search_data[user2_id]['region_code'] = '01'
        
        # Verify data isolation
        assert handlers.user_data[user1_id]['region_code'] == '14'
        assert handlers.search_data[user2_id]['region_code'] == '01'
        assert user1_id not in handlers.search_data
        assert user2_id not in handlers.user_data
    
    async def test_workflow_data_validation(self, test_db, mock_update, mock_context):
        """Test workflow data validation"""
        # Setup
        listing_service = ListingService(test_db)
        handlers = ListingHandlers(listing_service)
        
        # Mock user data
        user_id = 123456789
        mock_update.effective_user.id = user_id
        mock_context.user_data = {}
        
        # Test invalid data handling
        await handlers.handle_post_listing(mock_update, mock_context)
        
        # Try to submit with incomplete data
        await handlers.handle_listing_submit(mock_update, mock_context)
        
        # Verify error handling - should not crash
        assert user_id in handlers.user_data
        
        # Test with complete but invalid data
        handlers.user_data[user_id] = {
            'region_code': '99',  # Invalid
            'city_name': 'Test',
            'type': 'invalid',    # Invalid
            'rooms': 0,           # Invalid
            'price': -100,        # Invalid
            'title': ''           # Invalid
        }
        
        await handlers.handle_listing_submit(mock_update, mock_context)
        
        # Verify error handling - should not crash
        assert user_id in handlers.user_data
