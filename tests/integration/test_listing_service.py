"""
Integration Tests - Listing Service
"""
import pytest
from src.services.listing_service import ListingService
from src.database.models import Listing, ListingType, ListingStatus


@pytest.mark.asyncio
class TestListingServiceIntegration:
    """Listing service integration tests"""
    
    async def test_create_listing(self, test_db, listing_service, test_user, valid_listing_data):
        """Test listing creation"""
        listing = await listing_service.create_listing(test_user.id, valid_listing_data)
        
        assert listing is not None
        assert listing.user_id == test_user.id
        assert listing.region_code == valid_listing_data['region_code']
        assert listing.city_name == valid_listing_data['city_name']
        assert listing.type == ListingType(valid_listing_data['type'])
        assert listing.rooms == valid_listing_data['rooms']
        assert listing.price == valid_listing_data['price']
        assert listing.title == valid_listing_data['title']
        assert listing.status == ListingStatus.pending
    
    async def test_get_listing_by_id(self, test_db, listing_service, test_listing):
        """Test getting listing by ID"""
        listing = await listing_service.get_listing_by_id(test_listing.id)
        
        assert listing is not None
        assert listing.id == test_listing.id
        assert listing.title == test_listing.title
        assert listing.owner is not None
        assert listing.owner.id == test_listing.user_id
    
    async def test_get_listing_by_id_not_found(self, test_db, listing_service):
        """Test getting non-existing listing by ID"""
        listing = await listing_service.get_listing_by_id("non-existing-id")
        
        assert listing is None
    
    async def test_get_user_listings(self, test_db, listing_service, test_user):
        """Test getting user listings"""
        # Create multiple listings for the user
        listings_data = [
            {
                'region_code': '14',
                'city_name': 'Toshkent',
                'type': 'ijara',
                'rooms': 2,
                'price': 300.0,
                'title': 'Listing 1',
                'description': 'Description 1'
            },
            {
                'region_code': '14',
                'city_name': 'Toshkent',
                'type': 'sotuv',
                'rooms': 3,
                'price': 50000.0,
                'title': 'Listing 2',
                'description': 'Description 2'
            }
        ]
        
        created_listings = []
        for listing_data in listings_data:
            listing = await listing_service.create_listing(test_user.id, listing_data)
            created_listings.append(listing)
        
        # Get user listings
        user_listings = await listing_service.get_user_listings(test_user.id)
        
        assert len(user_listings) >= len(created_listings)
        
        # Check that our created listings are in the list
        created_listing_ids = {listing.id for listing in created_listings}
        user_listing_ids = {listing.id for listing in user_listings}
        
        assert created_listing_ids.issubset(user_listing_ids)
    
    async def test_get_user_listings_empty(self, test_db, listing_service, test_user):
        """Test getting listings for user with no listings"""
        listings = await listing_service.get_user_listings(test_user.id)
        
        assert isinstance(listings, list)
        assert len(listings) == 0
    
    async def test_search_listings_by_region(self, test_db, listing_service, test_user):
        """Test searching listings by region"""
        # Create listings in different regions
        listings_data = [
            {
                'region_code': '14',
                'city_name': 'Toshkent',
                'type': 'ijara',
                'rooms': 2,
                'price': 300.0,
                'title': 'Toshkent Listing'
            },
            {
                'region_code': '01',
                'city_name': 'Andijon',
                'type': 'ijara',
                'rooms': 3,
                'price': 200.0,
                'title': 'Andijon Listing'
            }
        ]
        
        for listing_data in listings_data:
            await listing_service.create_listing(test_user.id, listing_data)
        
        # Search by Toshkent region
        filters = {'region_code': '14'}
        results = await listing_service.search_listings(filters)
        
        assert len(results) >= 1
        for listing in results:
            assert listing.region_code == '14'
    
    async def test_search_listings_by_type(self, test_db, listing_service, test_user):
        """Test searching listings by type"""
        # Create listings of different types
        listings_data = [
            {
                'region_code': '14',
                'city_name': 'Toshkent',
                'type': 'ijara',
                'rooms': 2,
                'price': 300.0,
                'title': 'Rental Listing'
            },
            {
                'region_code': '14',
                'city_name': 'Toshkent',
                'type': 'sotuv',
                'rooms': 3,
                'price': 50000.0,
                'title': 'Sale Listing'
            }
        ]
        
        for listing_data in listings_data:
            await listing_service.create_listing(test_user.id, listing_data)
        
        # Search by rental type
        filters = {'type': 'ijara'}
        results = await listing_service.search_listings(filters)
        
        assert len(results) >= 1
        for listing in results:
            assert listing.type == ListingType.ijara
    
    async def test_search_listings_by_rooms(self, test_db, listing_service, test_user):
        """Test searching listings by rooms"""
        # Create listings with different room counts
        listings_data = [
            {
                'region_code': '14',
                'city_name': 'Toshkent',
                'type': 'ijara',
                'rooms': 2,
                'price': 300.0,
                'title': '2 Room Listing'
            },
            {
                'region_code': '14',
                'city_name': 'Toshkent',
                'type': 'ijara',
                'rooms': 3,
                'price': 400.0,
                'title': '3 Room Listing'
            }
        ]
        
        for listing_data in listings_data:
            await listing_service.create_listing(test_user.id, listing_data)
        
        # Search by 2 rooms
        filters = {'rooms': 2}
        results = await listing_service.search_listings(filters)
        
        assert len(results) >= 1
        for listing in results:
            assert listing.rooms == 2
    
    async def test_search_listings_by_price_range(self, test_db, listing_service, test_user):
        """Test searching listings by price range"""
        # Create listings with different prices
        listings_data = [
            {
                'region_code': '14',
                'city_name': 'Toshkent',
                'type': 'ijara',
                'rooms': 2,
                'price': 200.0,
                'title': 'Cheap Listing'
            },
            {
                'region_code': '14',
                'city_name': 'Toshkent',
                'type': 'ijara',
                'rooms': 3,
                'price': 500.0,
                'title': 'Expensive Listing'
            }
        ]
        
        for listing_data in listings_data:
            await listing_service.create_listing(test_user.id, listing_data)
        
        # Search by price range
        filters = {'min_price': 300.0, 'max_price': 600.0}
        results = await listing_service.search_listings(filters)
        
        assert len(results) >= 1
        for listing in results:
            assert 300.0 <= listing.price <= 600.0
    
    async def test_search_listings_by_furnished(self, test_db, listing_service, test_user):
        """Test searching listings by furnished status"""
        # Create listings with different furnished status
        listings_data = [
            {
                'region_code': '14',
                'city_name': 'Toshkent',
                'type': 'ijara',
                'rooms': 2,
                'price': 300.0,
                'title': 'Furnished Listing',
                'furnished': True
            },
            {
                'region_code': '14',
                'city_name': 'Toshkent',
                'type': 'ijara',
                'rooms': 3,
                'price': 400.0,
                'title': 'Unfurnished Listing',
                'furnished': False
            }
        ]
        
        for listing_data in listings_data:
            await listing_service.create_listing(test_user.id, listing_data)
        
        # Search by furnished status
        filters = {'furnished': True}
        results = await listing_service.search_listings(filters)
        
        assert len(results) >= 1
        for listing in results:
            assert listing.furnished is True
    
    async def test_search_listings_by_pets_allowed(self, test_db, listing_service, test_user):
        """Test searching listings by pets allowed status"""
        # Create listings with different pets allowed status
        listings_data = [
            {
                'region_code': '14',
                'city_name': 'Toshkent',
                'type': 'ijara',
                'rooms': 2,
                'price': 300.0,
                'title': 'Pets Allowed Listing',
                'pets_allowed': True
            },
            {
                'region_code': '14',
                'city_name': 'Toshkent',
                'type': 'ijara',
                'rooms': 3,
                'price': 400.0,
                'title': 'No Pets Listing',
                'pets_allowed': False
            }
        ]
        
        for listing_data in listings_data:
            await listing_service.create_listing(test_user.id, listing_data)
        
        # Search by pets allowed status
        filters = {'pets_allowed': True}
        results = await listing_service.search_listings(filters)
        
        assert len(results) >= 1
        for listing in results:
            assert listing.pets_allowed is True
    
    async def test_search_listings_multiple_filters(self, test_db, listing_service, test_user):
        """Test searching listings with multiple filters"""
        # Create listings with different combinations
        listings_data = [
            {
                'region_code': '14',
                'city_name': 'Toshkent',
                'type': 'ijara',
                'rooms': 2,
                'price': 300.0,
                'title': 'Matching Listing',
                'furnished': True,
                'pets_allowed': True
            },
            {
                'region_code': '14',
                'city_name': 'Toshkent',
                'type': 'ijara',
                'rooms': 3,
                'price': 400.0,
                'title': 'Non-matching Listing',
                'furnished': False,
                'pets_allowed': False
            }
        ]
        
        for listing_data in listings_data:
            await listing_service.create_listing(test_user.id, listing_data)
        
        # Search with multiple filters
        filters = {
            'region_code': '14',
            'type': 'ijara',
            'rooms': 2,
            'furnished': True,
            'pets_allowed': True
        }
        results = await listing_service.search_listings(filters)
        
        assert len(results) >= 1
        for listing in results:
            assert listing.region_code == '14'
            assert listing.type == ListingType.ijara
            assert listing.rooms == 2
            assert listing.furnished is True
            assert listing.pets_allowed is True
    
    async def test_search_listings_no_results(self, test_db, listing_service):
        """Test searching listings with no matching results"""
        filters = {
            'region_code': '99',  # Non-existing region
            'type': 'ijara',
            'rooms': 10,  # Non-existing room count
            'min_price': 1000000.0  # Very high price
        }
        results = await listing_service.search_listings(filters)
        
        assert isinstance(results, list)
        assert len(results) == 0
    
    async def test_update_listing(self, test_db, listing_service, test_listing):
        """Test listing update"""
        new_title = "Updated Title"
        new_price = 600.0
        
        updated_listing = await listing_service.update_listing(
            test_listing.id,
            {'title': new_title, 'price': new_price}
        )
        
        assert updated_listing is not None
        assert updated_listing.title == new_title
        assert updated_listing.price == new_price
        assert updated_listing.id == test_listing.id
    
    async def test_update_listing_not_found(self, test_db, listing_service):
        """Test updating non-existing listing"""
        updated_listing = await listing_service.update_listing(
            "non-existing-id",
            {'title': 'New Title'}
        )
        
        assert updated_listing is None
    
    async def test_delete_listing(self, test_db, listing_service, test_listing):
        """Test listing deletion"""
        listing_id = test_listing.id
        
        # Delete listing
        success = await listing_service.delete_listing(listing_id)
        assert success is True
        
        # Verify listing is deleted
        listing = await listing_service.get_listing_by_id(listing_id)
        assert listing is None
    
    async def test_delete_listing_not_found(self, test_db, listing_service):
        """Test deleting non-existing listing"""
        success = await listing_service.delete_listing("non-existing-id")
        assert success is False
    
    async def test_listing_status_management(self, test_db, listing_service, test_listing):
        """Test listing status management"""
        # Approve listing
        updated_listing = await listing_service.update_listing(
            test_listing.id,
            {'status': 'approved'}
        )
        
        assert updated_listing is not None
        assert updated_listing.status == ListingStatus.approved
        
        # Reject listing
        updated_listing = await listing_service.update_listing(
            test_listing.id,
            {'status': 'rejected', 'rejection_reason': 'Invalid information'}
        )
        
        assert updated_listing is not None
        assert updated_listing.status == ListingStatus.rejected
        assert updated_listing.rejection_reason == 'Invalid information'
    
    async def test_listing_statistics(self, test_db, listing_service, test_listing):
        """Test listing statistics"""
        # Update views and contacts count
        updated_listing = await listing_service.update_listing(
            test_listing.id,
            {
                'views_count': 100,
                'contacts_count': 5
            }
        )
        
        assert updated_listing is not None
        assert updated_listing.views_count == 100
        assert updated_listing.contacts_count == 5
