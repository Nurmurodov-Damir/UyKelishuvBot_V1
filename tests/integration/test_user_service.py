"""
Integration Tests - User Service
"""
import pytest
from src.services.user_service import UserService
from src.database.models import User


@pytest.mark.asyncio
class TestUserServiceIntegration:
    """User service integration tests"""
    
    async def test_create_user(self, test_db, user_service):
        """Test user creation"""
        telegram_id = 987654321
        name = "Integration Test User"
        
        user = await user_service.create_user(telegram_id, name)
        
        assert user is not None
        assert user.telegram_user_id == telegram_id
        assert user.name == name
        assert user.verified is False
        assert user.blocked is False
        assert user.locale == "uz"
    
    async def test_get_user_by_telegram_id_existing(self, test_db, user_service, test_user):
        """Test getting existing user by telegram ID"""
        user = await user_service.get_user_by_telegram_id(test_user.telegram_user_id)
        
        assert user is not None
        assert user.id == test_user.id
        assert user.telegram_user_id == test_user.telegram_user_id
        assert user.name == test_user.name
    
    async def test_get_user_by_telegram_id_not_found(self, test_db, user_service):
        """Test getting non-existing user by telegram ID"""
        user = await user_service.get_user_by_telegram_id(999999999)
        
        assert user is None
    
    async def test_get_user_by_id_existing(self, test_db, user_service, test_user):
        """Test getting existing user by ID"""
        user = await user_service.get_user_by_id(test_user.id)
        
        assert user is not None
        assert user.id == test_user.id
        assert user.telegram_user_id == test_user.telegram_user_id
        assert user.name == test_user.name
    
    async def test_get_user_by_id_not_found(self, test_db, user_service):
        """Test getting non-existing user by ID"""
        user = await user_service.get_user_by_id("non-existing-id")
        
        assert user is None
    
    async def test_update_user(self, test_db, user_service, test_user):
        """Test user update"""
        new_name = "Updated Name"
        new_phone = "+998901234567"
        
        updated_user = await user_service.update_user(
            test_user.id,
            name=new_name,
            phone_number=new_phone,
            verified=True
        )
        
        assert updated_user is not None
        assert updated_user.name == new_name
        assert updated_user.phone_number == new_phone
        assert updated_user.verified is True
    
    async def test_update_user_not_found(self, test_db, user_service):
        """Test updating non-existing user"""
        updated_user = await user_service.update_user(
            "non-existing-id",
            name="New Name"
        )
        
        assert updated_user is None
    
    async def test_delete_user(self, test_db, user_service, test_user):
        """Test user deletion"""
        user_id = test_user.id
        
        # Delete user
        success = await user_service.delete_user(user_id)
        assert success is True
        
        # Verify user is deleted
        user = await user_service.get_user_by_id(user_id)
        assert user is None
    
    async def test_delete_user_not_found(self, test_db, user_service):
        """Test deleting non-existing user"""
        success = await user_service.delete_user("non-existing-id")
        assert success is False
    
    async def test_get_all_users(self, test_db, user_service):
        """Test getting all users"""
        # Create multiple users
        users_data = [
            (111111111, "User 1"),
            (222222222, "User 2"),
            (333333333, "User 3")
        ]
        
        created_users = []
        for telegram_id, name in users_data:
            user = await user_service.create_user(telegram_id, name)
            created_users.append(user)
        
        # Get all users
        all_users = await user_service.get_all_users()
        
        assert len(all_users) >= len(created_users)
        
        # Check that our created users are in the list
        created_user_ids = {user.id for user in created_users}
        all_user_ids = {user.id for user in all_users}
        
        assert created_user_ids.issubset(all_user_ids)
    
    async def test_user_phone_verification(self, test_db, user_service, test_user):
        """Test user phone verification"""
        phone_number = "+998901234567"
        
        # Update user with phone number
        updated_user = await user_service.update_user(
            test_user.id,
            phone_number=phone_number,
            verified=True
        )
        
        assert updated_user is not None
        assert updated_user.phone_number == phone_number
        assert updated_user.verified is True
    
    async def test_user_locale_update(self, test_db, user_service, test_user):
        """Test user locale update"""
        new_locale = "ru"
        
        updated_user = await user_service.update_user(
            test_user.id,
            locale=new_locale
        )
        
        assert updated_user is not None
        assert updated_user.locale == new_locale
    
    async def test_user_blocking(self, test_db, user_service, test_user):
        """Test user blocking"""
        # Block user
        updated_user = await user_service.update_user(
            test_user.id,
            blocked=True
        )
        
        assert updated_user is not None
        assert updated_user.blocked is True
        
        # Unblock user
        updated_user = await user_service.update_user(
            test_user.id,
            blocked=False
        )
        
        assert updated_user is not None
        assert updated_user.blocked is False
