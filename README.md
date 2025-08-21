# 🏟️ Sports Complex Booking System

A comprehensive Python-based sports complex management system designed with clean architecture principles, featuring member management, room booking, and administrative operations.

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Usage](#-usage)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [API Documentation](#-api-documentation)
- [Development](#-development)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 👥 Member Management
- **Member Registration**: Create new member accounts with validation
- **Profile Updates**: Update member email addresses and passwords
- **Member Deletion**: Safe member removal with confirmation prompts
- **Member Listing**: View all registered members with payment status
- **Data Validation**: Comprehensive input validation using Pydantic models

### 🏨 Room Management
- **Room Listing**: View all available sports facilities
- **Room Search**: Find specific rooms by type or availability
- **Room Booking**: Reserve facilities for specific time slots
- **Booking Cancellation**: Cancel existing reservations
- **Availability Tracking**: Real-time room availability management

### 🎯 System Features
- **Interactive CLI Menu**: User-friendly command-line interface
- **Professional Table Formatting**: Clean data presentation with alignment
- **Comprehensive Error Handling**: Robust error management and user feedback
- **Database Integration**: MySQL backend with stored procedures
- **Input Validation**: Multi-layer validation for data integrity
- **Audit Logging**: Operation tracking and error logging

## 🏗️ Architecture

This project follows **Clean Architecture** principles with clear separation of concerns:

```
📁 sports_booking/
├── 📁 business_logic/          # Business rules and use cases
│   ├── commands/               # Command pattern implementations
│   └── services/              # Business services and validation
├── 📁 persistence/            # Data access layer
│   ├── database/              # Database operations
│   └── models/                # Data models (Pydantic)
└── 📁 presentation/           # User interface layer
    ├── menu/                  # CLI menu system
    └── formatters/            # Data presentation utilities
```

### Design Patterns Used

- **Command Pattern**: All business operations implemented as commands
- **Single Responsibility Principle**: Each class has one clear purpose
- **Dependency Injection**: Loose coupling between layers
- **Repository Pattern**: Database operations abstracted through repositories
- **Service Layer**: Business logic separated from presentation

## 🚀 Installation

### Why UV?

This project uses **UV** as the recommended package manager for several advantages:

- **⚡ Speed**: 10-100x faster than pip for package installation and resolution
- **🔒 Reliability**: Better dependency resolution and lock file generation
- **🎯 Simplicity**: Single tool for virtual environments, package management, and project setup
- **🔄 Compatibility**: Drop-in replacement for pip with additional features
- **📦 Modern**: Built with Rust for performance and reliability

### Prerequisites

- **Python 3.8+**: Required for type hints and modern Python features
- **MySQL 8.0+**: Database server for data persistence
- **UV**: Modern Python package and project manager (recommended)
- **pip** (alternative): Traditional Python package manager

### Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone https://github.com/NetHead21/sports_complex_booking_system.git
   cd sports_complex_booking_system
   ```

2. **Install UV (if not already installed)**
   ```bash
   # Install UV using pip
   pip install uv
   
   # Or install using the official installer (recommended)
   curl -LsSf https://astral.sh/uv/install.sh | sh  # Unix/macOS
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows
   ```

3. **Create Virtual Environment and Install Dependencies**
   ```bash
   # Using UV (recommended)
   uv venv
   uv pip install -r requirements.txt
   
   # Activate virtual environment
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   ```
   
   **Alternative with traditional pip:**
   ```bash
   python -m venv .venv
   
   # Activate virtual environment
   # Windows
   .venv\Scripts\activate
   # macOS/Linux
   source .venv/bin/activate
   
   pip install -r requirements.txt
   ```

4. **Database Setup**
   ```sql
   -- Create database
   CREATE DATABASE sports_booking;
   
   -- Import schema and stored procedures
   mysql -u username -p sports_booking < database/schema.sql
   mysql -u username -p sports_booking < database/procedures.sql
   ```

5. **Configuration**
   ```python
   # Update database configuration in persistence/database.py
   DATABASE_CONFIG = {
       'host': 'localhost',
       'user': 'your_username',
       'password': 'your_password',
       'database': 'sports_booking'
   }
   ```

## 💻 Usage

### Quick Start with UV

```bash
# Clone and setup with UV (fastest method)
git clone https://github.com/NetHead21/sports_complex_booking_system.git
cd sports_complex_booking_system
uv venv
uv pip install -r requirements.txt
```

### Starting the Application

```bash
python main.py
```

### Main Menu Navigation

```
🏟️  SPORTS COMPLEX BOOKING SYSTEM
==================================================
Main Menu:
  A: Member Management
  B: Room Management
  Q: Quit
--------------------------------------------------
```

### Member Management Operations

- **View All Members**: Display member list with payment status
- **Add New Member**: Register new members with validation
- **Update Member Email**: Change member email addresses
- **Update Member Password**: Change member passwords with confirmation
- **Delete Member**: Remove members with safety confirmations

### Room Management Operations

- **View All Rooms**: Display available facilities
- **Search Rooms**: Find rooms by criteria
- **Book Room**: Reserve facilities for specific times
- **Cancel Booking**: Remove existing reservations

## 📁 Project Structure

```
sports_booking/
├── main.py                           # Application entry point
├── requirements.txt                  # Python dependencies (UV managed)
├── requirements-dev.txt             # Development dependencies
├── pyproject.toml                   # UV project configuration
├── README.md                        # Project documentation
│
├── business_logic/                  # Business layer
│   ├── __init__.py                 # Module exports
│   ├── command.py                  # Base command interface
│   ├── member_input_service.py     # Member input collection service
│   │
│   ├── # Member Commands
│   ├── add_member_command.py       # Member creation
│   ├── delete_member_command.py    # Member deletion
│   ├── update_member_email_command.py    # Email updates
│   ├── update_member_password_command.py # Password updates
│   ├── list_members_commands.py    # Member listing
│   │
│   ├── # Room Commands
│   ├── list_rooms_command.py       # Room listing
│   ├── search_rooms_command.py     # Room search
│   ├── book_rooms_command.py       # Room booking
│   ├── cancel_book_room_command.py # Booking cancellation
│   │
│   └── quit_command.py             # Application termination
│
├── persistence/                     # Data layer
│   ├── __init__.py                 # Module exports
│   ├── database.py                 # Database connection manager
│   ├── models.py                   # Pydantic data models
│   ├── member_booking_database.py  # Member data operations
│   └── room_booking_database.py    # Room data operations
│
└── presentation/                    # Presentation layer
    ├── __init__.py                 # Module exports
    ├── menu.py                     # CLI menu system
    ├── options.py                  # Menu option definitions
    ├── user_input.py              # Input collection utilities
    ├── utils.py                    # Presentation utilities
    └── table_formatter.py         # Data formatting utilities
```

## 🗄️ Database Schema

### Core Tables

#### Members Table
```sql
CREATE TABLE members (
    id VARCHAR(50) PRIMARY KEY,          -- Member username
    password VARCHAR(255) NOT NULL,      -- Hashed password
    email VARCHAR(100) UNIQUE NOT NULL,  -- Contact email
    payment_due DECIMAL(10,2) DEFAULT 0, -- Outstanding balance
    member_since TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Rooms Table
```sql
CREATE TABLE rooms (
    id VARCHAR(10) PRIMARY KEY,          -- Room identifier
    room_type VARCHAR(50) NOT NULL,      -- Facility type
    capacity INT NOT NULL,               -- Maximum occupancy
    hourly_rate DECIMAL(8,2) NOT NULL,   -- Booking cost
    availability_status ENUM('AVAILABLE', 'MAINTENANCE', 'BOOKED')
);
```

#### Bookings Table
```sql
CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    room_id VARCHAR(10),                 -- Foreign key to rooms
    member_id VARCHAR(50),               -- Foreign key to members
    booking_datetime DATETIME NOT NULL,  -- Reservation time
    duration_hours INT DEFAULT 1,        -- Booking duration
    payment_status ENUM('PAID', 'UNPAID') DEFAULT 'UNPAID',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (room_id) REFERENCES rooms(id),
    FOREIGN KEY (member_id) REFERENCES members(id)
);
```

### Stored Procedures

- `insert_new_member(id, password, email)` - Create new member
- `update_member_email(member_id, email)` - Update member email
- `update_member_password(member_id, password)` - Update member password
- `delete_member(member_id)` - Remove member and cleanup
- `book_room(room_id, member_id, datetime, duration)` - Create booking
- `cancel_booking(booking_id, member_id)` - Cancel reservation

### 🔍 Audit Trail System

The system includes comprehensive audit logging that automatically tracks all booking transactions.

#### Audit Table
```sql
CREATE TABLE booking_audit (
    id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,                    -- Reference to booking
    action ENUM('INSERT', 'UPDATE', 'DELETE', 'CANCEL') NOT NULL,
    old_values JSON,                            -- Previous state (UPDATE/DELETE)
    new_values JSON,                            -- New state (INSERT/UPDATE)
    changed_by VARCHAR(50),                     -- Database user
    ip_address VARCHAR(45),                     -- Client IP address
    user_agent VARCHAR(255),                    -- Application identifier
    changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_booking_audit_id (booking_id),
    INDEX idx_booking_audit_date (changed_at),
    INDEX idx_booking_audit_action (action),
    INDEX idx_booking_audit_user (changed_by)
);
```

#### Automatic Triggers
The audit system uses database triggers that fire automatically:

- **INSERT Trigger**: Records new booking creation
- **UPDATE Trigger**: Tracks booking modifications  
- **DELETE Trigger**: Preserves deleted booking data
- **CANCEL Trigger**: Special handling for cancellations

#### Application Integration
To enhance audit logging in your Python application, set session variables before database operations:

```python
# Example: Setting audit context in your application
def set_audit_context(cursor, user_id, ip_address, user_agent):
    """Set audit context for database operations"""
    cursor.execute("SET @audit_ip_address = %s", (ip_address,))
    cursor.execute("SET @audit_user_agent = %s", (user_agent,))
    cursor.execute("SET @audit_user_id = %s", (user_id,))

# Usage example
import mysql.connector

connection = mysql.connector.connect(
    host='localhost',
    database='sports_booking',
    user='your_user',
    password='your_password'
)
cursor = connection.cursor()

# Set audit context
set_audit_context(
    cursor=cursor,
    user_id='john_doe',
    ip_address='192.168.1.100',
    user_agent='Python Sports Booking App v1.0'
)

# Now perform booking operations - they will be automatically audited
cursor.callproc('make_booking', ['T1', '2025-12-25', '10:00:00', 'john_doe'])
```

#### Audit Query Procedure
Use the `get_booking_audit_trail()` procedure to retrieve audit information:

```sql
-- Get all audit records for a specific booking
CALL get_booking_audit_trail(5, NULL, NULL, @status, @message);
SELECT @status, @message;

-- Get all audit records within a date range
CALL get_booking_audit_trail(NULL, '2025-08-01', '2025-08-31', @status, @message);

-- Get audit records for specific booking within date range
CALL get_booking_audit_trail(3, '2025-08-01', '2025-08-31', @status, @message);
```

**Procedure Parameters:**
- `p_booking_id`: Specific booking ID (NULL for all bookings)
- `p_date_from`: Start date filter (NULL for no start limit)  
- `p_date_to`: End date filter (NULL for no end limit)
- `p_status`: OUTPUT - Operation status ('SUCCESS', 'ERROR', 'NO_RECORDS')
- `p_message`: OUTPUT - Descriptive result message

**Query Results Include:**
- Audit record ID and timestamp
- Action performed (INSERT/UPDATE/DELETE/CANCEL)
- Complete before/after values in JSON format
- User information and source tracking
- Human-readable summary descriptions
- Time elapsed since the change

#### Benefits
- **Complete Transparency**: Every booking change is automatically tracked
- **Compliance Ready**: Full audit trail for financial transactions  
- **Security Monitoring**: Track who made changes and from where
- **Data Recovery**: Previous values preserved for rollback scenarios
- **Debugging Aid**: See exactly what happened and when
- **Zero Configuration**: Works automatically with existing procedures

## 📚 API Documentation

### Business Logic Layer

#### Command Interface
All business operations implement the `Command` interface:
```python
class Command:
    def execute(self, data=None) -> None:
        """Execute the business operation"""
        pass
```

#### Member Input Service
Centralized service for member data collection:
```python
class MemberInputService:
    @staticmethod
    def collect_new_member_data() -> Optional[Member]:
        """Collect and validate new member registration data"""
        
    @staticmethod
    def collect_member_email_update_data() -> Optional[Tuple[str, str]]:
        """Collect member ID and new email for updates"""
        
    @staticmethod
    def collect_member_password_update_data() -> Optional[Tuple[str, str]]:
        """Collect member ID and new password with confirmation"""
```

### Data Layer

#### Member Database Operations
```python
class MemberBookingDatabase:
    def create_new_member(self, member: Member) -> None:
        """Create new member record"""
        
    def update_member_email(self, member_id: str, email: str) -> bool:
        """Update member email address"""
        
    def update_member_password(self, member_id: str, password: str) -> bool:
        """Update member password"""
        
    def delete_member(self, member_id: str) -> bool:
        """Delete member record"""
        
    def show_members(self) -> List[Tuple]:
        """Retrieve all member records"""
```

### Presentation Layer

#### Table Formatting
```python
def format_member_table(member_data: List[Tuple], title: str) -> str:
    """Format member data into professional table display"""

def format_booking_table(booking_data: List[Tuple], title: str) -> str:
    """Format booking data with datetime and status formatting"""
```

## 🛠️ Development

### Code Style
- **PEP 8**: Python style guide compliance
- **Type Hints**: Comprehensive type annotations
- **Docstrings**: Detailed documentation for all modules, classes, and methods
- **Error Handling**: Comprehensive exception handling

### Design Principles
- **SOLID Principles**: Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion
- **Clean Architecture**: Clear separation between business logic, data access, and presentation
- **Command Pattern**: Consistent command-based operations
- **Input Validation**: Multi-layer validation with Pydantic models

### Development Setup

1. **Install Development Dependencies**
   ```bash
   # Using UV (recommended)
   uv pip install -r requirements-dev.txt
   
   # Or using traditional pip
   pip install -r requirements-dev.txt
   ```

2. **Package Management with UV**
   ```bash
   # Add new dependency
   uv add package-name
   
   # Add development dependency
   uv add --dev package-name
   
   # Update dependencies
   uv pip compile requirements.in --output-file requirements.txt
   
   # Sync environment with lock file
   uv pip sync requirements.txt
   ```

2. **Package Management with UV**
   ```bash
   # Add new dependency
   uv add package-name
   
   # Add development dependency
   uv add --dev package-name
   
   # Update dependencies
   uv pip compile requirements.in --output-file requirements.txt
   
   # Sync environment with lock file
   uv pip sync requirements.txt
   ```

3. **Code Formatting**
   ```bash
   black sports_booking/
   isort sports_booking/
   ```

4. **Type Checking**
   ```bash
   mypy sports_booking/
   ```

5. **Linting**
   ```bash
   flake8 sports_booking/
   pylint sports_booking/
   ```

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=sports_booking

# Run specific test file
python -m pytest tests/test_member_commands.py
```

### Test Structure
```
tests/
├── unit/                    # Unit tests
│   ├── test_commands/      # Command tests
│   ├── test_services/      # Service tests
│   └── test_database/      # Database tests
├── integration/            # Integration tests
└── fixtures/              # Test data and fixtures
```

### Test Coverage
- **Unit Tests**: Individual component testing
- **Integration Tests**: Cross-layer functionality
- **Database Tests**: Data persistence validation
- **Command Tests**: Business logic verification

## 🤝 Contributing

### Development Workflow

1. **Fork the Repository**
2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```
3. **Make Changes**
   - Follow code style guidelines
   - Add comprehensive tests
   - Update documentation
4. **Commit Changes**
   ```bash
   git commit -m "feat: add your feature description"
   ```
5. **Push and Create Pull Request**

### Contribution Guidelines
- **Code Quality**: Maintain high code quality standards
- **Documentation**: Update README and docstrings
- **Testing**: Include tests for new features
- **Backward Compatibility**: Ensure changes don't break existing functionality

## 📊 Performance Considerations

### Database Optimization
- **Indexed Columns**: Primary keys and foreign keys properly indexed
- **Stored Procedures**: Complex operations handled at database level
- **Connection Pooling**: Efficient database connection management

### Application Performance
- **Lazy Loading**: Database connections established on demand
- **Memory Management**: Efficient data structure usage
- **Error Handling**: Graceful degradation under error conditions

## 🔒 Security Features

### Data Protection
- **Input Validation**: Comprehensive validation at all layers
- **SQL Injection Prevention**: Parameterized queries and stored procedures
- **Password Security**: Secure password handling (hashing handled by database)
- **Data Integrity**: Foreign key constraints and validation rules

### Access Control
- **Member Authentication**: Secure member identification
- **Operation Validation**: Member existence verification for all operations
- **Audit Logging**: Operation tracking for security monitoring

## 🚀 Future Enhancements

### Planned Features
- **Web Interface**: Django/Flask web application
- **API Development**: RESTful API for external integration
- **Payment Integration**: Online payment processing
- **Notification System**: Email/SMS notifications for bookings
- **Reporting Module**: Advanced analytics and reporting
- **Mobile Application**: iOS/Android mobile apps

### Technical Improvements
- **Caching Layer**: Redis integration for performance
- **Microservices**: Service decomposition for scalability
- **Docker Deployment**: Containerization for easy deployment
- **CI/CD Pipeline**: Automated testing and deployment

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Juniven Saavedra**
- GitHub: [@NetHead21](https://github.com/NetHead21)
- Repository: [sports_complex_booking_system](https://github.com/NetHead21/sports_complex_booking_system)

## 🙏 Acknowledgments

- Clean Architecture principles by Robert C. Martin
- Python community for excellent libraries and tools
- MySQL team for robust database features
- Contributors and testers who helped improve the system

---

**Built with ❤️ using Python, MySQL, and Clean Architecture principles**
