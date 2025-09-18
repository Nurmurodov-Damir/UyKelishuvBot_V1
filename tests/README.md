# 🧪 UyKelishuv Bot - Testing Documentation

## 📋 Test Overview

Bu loyiha uchun comprehensive testing suite yaratilgan. Testlar 3 ta kategoriyaga bo'lingan:

- **Unit Tests** - Individual service'lar va metodlar
- **Integration Tests** - Service'lar o'rtasidagi integration
- **End-to-End Tests** - To'liq bot workflow'lari

## 🏗️ Test Structure

```
tests/
├── conftest.py                 # Test fixtures va setup
├── unit/                       # Unit tests
│   ├── test_validation_service.py
│   ├── test_message_builder.py
│   └── test_keyboard_builder.py
├── integration/                # Integration tests
│   ├── test_user_service.py
│   └── test_listing_service.py
├── e2e/                       # End-to-end tests
│   └── test_bot_workflow.py
└── fixtures/                   # Test data fixtures
```

## 🚀 Test Running

### Quick Start
```bash
# Barcha testlarni ishga tushirish
python run_tests.py

# Yoki pytest bilan
pytest tests/ -v
```

### Individual Test Categories
```bash
# Unit tests
pytest tests/unit/ -v

# Integration tests
pytest tests/integration/ -v

# E2E tests
pytest tests/e2e/ -v
```

### Coverage Reports
```bash
# Terminal coverage
pytest tests/ --cov=src --cov-report=term-missing

# HTML coverage report
pytest tests/ --cov=src --cov-report=html:htmlcov
```

## 📊 Test Coverage

### Target Coverage: 80%+

| Module | Coverage | Status |
|--------|----------|--------|
| Validation Service | 95%+ | ✅ |
| Message Builder | 90%+ | ✅ |
| Keyboard Builder | 90%+ | ✅ |
| User Service | 85%+ | ✅ |
| Listing Service | 85%+ | ✅ |
| Bot Handlers | 80%+ | ✅ |

## 🧪 Test Types

### Unit Tests
- **Validation Service**: Input validation, error handling
- **Message Builder**: Message formatting, text generation
- **Keyboard Builder**: Keyboard creation, button layouts

### Integration Tests
- **User Service**: Database operations, user management
- **Listing Service**: CRUD operations, search functionality

### E2E Tests
- **Listing Creation Workflow**: Complete listing creation process
- **Search Workflow**: Complete search process
- **Error Handling**: Error scenarios and recovery
- **State Management**: User state isolation

## 🔧 Test Configuration

### pytest.ini
```ini
[tool:pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts = 
    -v
    --tb=short
    --strict-markers
    --disable-warnings
    --cov=src
    --cov-report=term-missing
    --cov-report=html:htmlcov
    --cov-fail-under=80
markers =
    unit: Unit tests
    integration: Integration tests
    e2e: End-to-end tests
    slow: Slow tests
    database: Database tests
asyncio_mode = auto
```

### Test Dependencies
```txt
pytest>=7.4.0
pytest-asyncio>=0.21.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0
httpx>=0.24.0
```

## 🎯 Test Fixtures

### Database Fixtures
- `test_db`: In-memory SQLite database
- `test_user`: Sample database user
- `test_listing`: Sample database listing

### Telegram Fixtures
- `mock_user`: Mock Telegram user
- `mock_chat`: Mock Telegram chat
- `mock_message`: Mock Telegram message
- `mock_callback_query`: Mock callback query
- `mock_update`: Mock Telegram update
- `mock_context`: Mock bot context

### Service Fixtures
- `user_service`: User service instance
- `listing_service`: Listing service instance
- `validation_service`: Validation service instance
- `keyboard_builder`: Keyboard builder instance
- `message_builder`: Message builder instance
- `listing_handlers`: Listing handlers instance

### Data Fixtures
- `valid_listing_data`: Valid listing data for testing
- `invalid_listing_data`: Invalid listing data for testing
- `search_filters`: Search filters for testing

## 📝 Test Examples

### Unit Test Example
```python
def test_validate_price_valid(self):
    """Test valid price validation"""
    validator = ValidationService()
    
    is_valid, price_value, error = validator.validate_price("500")
    
    assert is_valid is True
    assert price_value == 500.0
    assert error is None
```

### Integration Test Example
```python
async def test_create_user(self, test_db, user_service):
    """Test user creation"""
    telegram_id = 987654321
    name = "Test User"
    
    user = await user_service.create_user(telegram_id, name)
    
    assert user is not None
    assert user.telegram_user_id == telegram_id
    assert user.name == name
```

### E2E Test Example
```python
async def test_listing_creation_workflow(self, test_db, mock_update, mock_context):
    """Test complete listing creation workflow"""
    handlers = ListingHandlers(ListingService(test_db))
    
    # Start listing creation
    await handlers.handle_post_listing(mock_update, mock_context)
    
    # Select region
    await handlers.handle_region_selection(mock_update, mock_context, "14")
    
    # Verify data is stored
    assert handlers.user_data[user_id]['region_code'] == "14"
```

## 🐛 Debugging Tests

### Verbose Output
```bash
pytest tests/ -v -s
```

### Specific Test
```bash
pytest tests/unit/test_validation_service.py::TestValidationService::test_validate_price_valid -v
```

### Debug Mode
```bash
pytest tests/ --pdb
```

### Logging
```bash
pytest tests/ --log-cli-level=DEBUG
```

## 🔄 Continuous Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.11
    - name: Install dependencies
      run: pip install -r requirements.txt
    - name: Run tests
      run: pytest tests/ --cov=src --cov-report=xml
    - name: Upload coverage
      uses: codecov/codecov-action@v1
```

## 📈 Performance Testing

### Load Testing
```bash
# Install locust
pip install locust

# Run load tests
locust -f tests/performance/locustfile.py
```

### Benchmark Testing
```bash
# Install pytest-benchmark
pip install pytest-benchmark

# Run benchmarks
pytest tests/ --benchmark-only
```

## 🎯 Best Practices

### Test Naming
- Test files: `test_*.py`
- Test classes: `Test*`
- Test methods: `test_*`

### Test Structure
- **Arrange**: Setup test data
- **Act**: Execute the code
- **Assert**: Verify results

### Test Isolation
- Each test is independent
- Use fixtures for setup/teardown
- Mock external dependencies

### Test Data
- Use realistic test data
- Test edge cases
- Test error scenarios

## 🚨 Common Issues

### Database Issues
- Use in-memory SQLite for tests
- Clean up after each test
- Use transactions for isolation

### Async Issues
- Use `@pytest.mark.asyncio`
- Proper async/await usage
- Mock async dependencies

### Mock Issues
- Mock external API calls
- Use proper mock types
- Verify mock calls

## 📚 Additional Resources

- [pytest Documentation](https://docs.pytest.org/)
- [pytest-asyncio](https://pytest-asyncio.readthedocs.io/)
- [pytest-cov](https://pytest-cov.readthedocs.io/)
- [Testing Best Practices](https://docs.python.org/3/library/unittest.html)

---

**🎉 Happy Testing!**
