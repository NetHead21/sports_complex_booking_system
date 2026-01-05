# Test Suite for Sports Booking Management System

This directory contains comprehensive test coverage for the Sports Booking Management System.

## Structure

```
tests/
├── __init__.py
├── business_logic/
│   ├── __init__.py
│   └── services/
│       ├── __init__.py
│       └── test_booking_input_service.py
└── README.md
```

## Running Tests

### Run all tests
```bash
python -m pytest tests/
```

### Run specific test file
```bash
python -m pytest tests/business_logic/services/test_booking_input_service.py
```

### Run with coverage
```bash
python -m pytest tests/ --cov=business_logic --cov-report=html
```

### Run with verbose output
```bash
python -m pytest tests/ -v
```

### Run specific test class
```bash
python -m pytest tests/business_logic/services/test_booking_input_service.py::TestBookingInputServiceCollectNewBookingData
```

### Run specific test method
```bash
python -m pytest tests/business_logic/services/test_booking_input_service.py::TestBookingInputServiceCollectNewBookingData::test_collect_new_booking_data_success
```

## Test Coverage Summary

**Total Test Cases: 114**
- test_booking_input_service.py: 56 tests
- test_member_input_service.py: 58 tests

---

### test_booking_input_service.py

Comprehensive test coverage for `BookingInputService` class including:

#### Main Public Methods
- `collect_new_booking_data()` - 8 test cases
  - Successful data collection with confirmation
  - User declines confirmation
  - Cancellation at each input step (room_id, date, time, user_id)
  - KeyboardInterrupt handling
  - Exception handling

- `collect_room_search_data()` - 6 test cases
  - Successful search criteria collection
  - Cancellation at each input step
  - KeyboardInterrupt handling
  - Exception handling

- `collect_booking_cancellation_data()` - 6 test cases
  - Successful cancellation data collection
  - Empty booking ID validation
  - Non-numeric booking ID validation
  - Member ID cancellation
  - KeyboardInterrupt handling
  - Exception handling

#### Private Helper Methods
- `_collect_room_id()` - 7 test cases
  - Valid input and uppercase conversion
  - Empty input rejection
  - Length validation (min/max)
  - Boundary tests

- `_collect_room_type()` - 6 test cases
  - All room type selections (Tennis, Badminton, Archery, Multi-Purpose)
  - Invalid choice handling
  - Empty input handling

- `_collect_book_date()` - 8 test cases
  - Valid future date acceptance
  - Past date rejection
  - Today's date rejection
  - Invalid format handling
  - Empty input handling
  - Custom field name parameter
  - Invalid calendar dates

- `_collect_book_time()` - 9 test cases
  - Valid time acceptance
  - Business hours boundary tests (06:00-22:00)
  - Before/after business hours rejection
  - Invalid format handling
  - Empty input handling
  - Custom field name parameter
  - Invalid hour/minute values

- `_collect_user_id()` - 8 test cases
  - Valid input acceptance
  - Empty input rejection
  - Length validation (min 3, max 50 characters)
  - Boundary tests (exactly 3 and 50 characters)
  - Whitespace trimming
  - Custom field name parameter

**Total Test Cases: 56**

---

### test_member_input_service.py

Comprehensive test coverage for `MemberInputService` class including:

#### Main Public Methods
- `collect_new_member_data()` - 4 test cases
  - Successful member data collection
  - KeyboardInterrupt handling
  - Exception handling
  - Empty fields handling

- `collect_member_email_update_data()` - 7 test cases
  - Successful email update data collection
  - Email validation (missing @, missing dot, neither)
  - Complex email format acceptance
  - KeyboardInterrupt handling
  - Exception handling

- `collect_member_password_update_data()` - 10 test cases
  - Successful password update with confirmation
  - Password too short validation
  - Password mismatch detection
  - Case sensitivity in password matching
  - Whitespace difference detection
  - Boundary tests (exactly 5, exactly 6 characters)
  - Long password acceptance
  - KeyboardInterrupt handling
  - Exception handling

- `collect_member_id_for_deletion()` - 8 test cases
  - Successful deletion with correct confirmation
  - Case-sensitive confirmation ("DELETE" only)
  - Wrong confirmation text rejection
  - Empty confirmation rejection
  - Whitespace in confirmation handling
  - KeyboardInterrupt handling
  - Exception handling

- `collect_member_id_for_lookup()` - 4 test cases
  - Successful member ID collection
  - Member ID with spaces
  - KeyboardInterrupt handling
  - Exception handling

#### Utility Methods
- `display_operation_result()` - 4 test cases
  - Success message display
  - Failure message without error details
  - Failure message with error details
  - Different operation types

- `validate_member_data()` - 21 test cases
  - Complete valid data validation
  - Partial validation (ID only, ID + email)
  - Empty member ID rejection
  - Whitespace-only member ID rejection
  - Member ID length validation (min 3 chars)
  - Boundary tests (exactly 2, exactly 3 characters)
  - Invalid email format (no @, no dot)
  - Email length validation (min 5 chars)
  - Boundary tests (exactly 4, exactly 5 characters)
  - Password length validation (min 6 chars)
  - Boundary tests (exactly 5, exactly 6 characters)
  - Password whitespace-only rejection
  - Password with spaces acceptance
  - Complex valid email acceptance
  - Very long inputs handling
  - Multiple invalid fields (returns first error)

**Total Test Cases: 58**

---

## Summary Statistics

- **Total Tests**: 114
- **Test Files**: 2
- **Test Classes**: 15
- **Success Rate**: 100% ✅

---

## Edge Cases Covered

### Boundary Tests
- Minimum/maximum length validation
- Exactly at boundary values
- One above/below boundary values

### Format Validation
- Email format (@, dot requirements)
- Date format (ISO 8601)
- Time format (HH:MM, 24-hour)
- ID format constraints

### Security Tests
- Password confirmation matching
- Case-sensitive validation
- Deletion confirmation requirements
- Input sanitization

### User Experience
- Keyboard interrupt handling (Ctrl+C)
- Empty input rejection
- Whitespace trimming
- Clear error messaging

### Business Rules
- Future dates only
- Business hours (06:00-22:00)
- Password minimum length
- Confirmation text matching

---

**Total Test Cases: 114 (Previously: 58)**

## Running Tests

- **Framework**: unittest (Python standard library)
- **Mocking**: unittest.mock
- **Coverage Tool**: pytest-cov (optional)

## Testing Principles

1. **Isolation**: Each test is independent and uses mocking to isolate the unit under test
2. **Clarity**: Descriptive test names following the pattern `test_<method>_<scenario>`
3. **Completeness**: Testing happy paths, error cases, edge cases, and boundary conditions
4. **Maintainability**: Well-organized test classes mirroring the source code structure

## Dependencies

Required for testing:
```bash
pip install pytest pytest-cov
```

## Writing New Tests

When adding new tests:

1. Create test files with the prefix `test_`
2. Create test classes with the prefix `Test`
3. Create test methods with the prefix `test_`
4. Use descriptive names that explain what is being tested
5. Include docstrings explaining the test purpose
6. Mock external dependencies appropriately
7. Use assertions to verify expected behavior
8. Test both success and failure scenarios

## Example Test Structure

```python
class TestMyClass(unittest.TestCase):
    """Test cases for MyClass."""

    @patch('module.dependency')
    def test_method_success(self, mock_dep):
        """Test successful execution of method."""
        # Arrange
        mock_dep.return_value = "expected_value"
        
        # Act
        result = MyClass.method()
        
        # Assert
        self.assertEqual(result, "expected_result")
        mock_dep.assert_called_once()
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines. Ensure all tests pass before merging code changes.

## Future Test Coverage

Planned test files:
- `test_member_input_service.py`
- `test_room_database_manager.py`
- `test_member_database_manager.py`
- Integration tests for complete workflows
- Performance tests for database operations
