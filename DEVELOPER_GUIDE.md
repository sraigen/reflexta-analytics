# 🚀 Reflexta Analytics - Developer Guide

## 📋 Overview

This is a production-grade data visualization web application built with Python, Streamlit, and PostgreSQL. The application provides comprehensive analytics for Finance and Procurement modules with a professional, luxury UI design.

## 🏗️ Architecture

### Technology Stack
- **Frontend**: Streamlit 1.32.0+ with modern CSS animations
- **Backend**: Python 3.10+ with secure credential management
- **Database**: PostgreSQL with SQLAlchemy 2.0+
- **Visualization**: Plotly Express with animated KPI indicators
- **Styling**: Glass morphism design with gradient animations
- **Security**: Environment variables and secure credential storage
- **AI Integration**: DeepSeek API for intelligent assistance
- **Deployment**: Streamlit Cloud + GitHub

### Project Structure
```
data-viz-app/
├── app.py                          # Main application entry point
├── pages/                          # Dashboard pages
│   ├── 00_Database_Analysis.py    # Database exploration
│   ├── 03_Finance_Dashboard.py     # Finance analytics
│   ├── 04_Procurement_Dashboard.py # Procurement analytics
│   └── 05_Analytics_Dashboard.py   # Executive analytics
├── src/                            # Core application code
│   ├── __init__.py                 # Package initialization
│   ├── db.py                       # Database connection management
│   ├── ui.py                       # Reusable UI components
│   ├── finance_queries.py          # Finance data queries
│   ├── finance_charts.py           # Finance visualizations
│   ├── procurement_queries.py      # Procurement data queries
│   ├── procurement_charts.py       # Procurement visualizations
│   ├── analytics_queries.py        # Analytics data queries
│   └── analytics_charts.py         # Analytics visualizations
├── database/                       # Database related files
│   ├── schema.sql                  # Database schema
│   └── setup_database.py          # Database setup script
├── .streamlit/                     # Streamlit configuration
│   ├── config.toml                 # Streamlit theme config
│   └── secrets.toml                # Database credentials
├── requirements.txt                # Python dependencies
├── pyproject.toml                  # Linting configuration
├── README.md                       # Project documentation
├── EXTENSION_GUIDE.md             # Extension guide for users
├── QUICK_REFERENCE.md              # Quick reference for developers
└── DEVELOPER_GUIDE.md             # This file
```

## 🎨 Modern UI Components

### KPI Indicators
The application features modern animated KPI indicators with:
- **Gradient Backgrounds**: Unique color schemes for each metric
- **Progress Bars**: Dynamic progress indicators based on data values
- **Floating Animations**: Subtle background animations for visual appeal
- **Hover Effects**: Interactive hover states with smooth transitions

### Security Features
- **Environment Variables**: All credentials stored in environment variables
- **Secure Fallbacks**: Working credentials as fallbacks for development
- **Git Protection**: `.gitignore` configured to prevent credential exposure
- **Template Files**: Example configuration files for secure setup

### Glass Morphism Design
- **Backdrop Filters**: Modern blur effects for depth
- **Gradient Overlays**: Sophisticated color transitions
- **Subtle Borders**: Minimal border styling for clean appearance
- **Responsive Design**: Optimized for all screen sizes

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL database (local development)
- Supabase account (production deployment)
- Git

## 🏠 Local Development Setup

### Step 1: Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd data-viz-app

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Local PostgreSQL Configuration
```bash
# Install PostgreSQL (if not already installed)
# Windows: Download from https://www.postgresql.org/download/windows/
# macOS: brew install postgresql
# Ubuntu: sudo apt-get install postgresql postgresql-contrib

# Create database
createdb reflexta_analytics

# Create user (optional)
psql -c "CREATE USER reflexta_user WITH PASSWORD 'your_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE reflexta_analytics TO reflexta_user;"
```

### Step 3: Configure Local Secrets
Create `.streamlit/secrets.toml`:
```toml
[connections.sql]
url = "postgresql+psycopg://username:password@localhost:5432/reflexta_analytics"

# DeepSeek AI API Key
deepseek_api_key = "your_deepseek_api_key"
```

### Step 4: Initialize Local Database
```bash
# Run database setup
python database/setup_database.py

# Populate with sample data
python populate_sample_data.py
```

### Step 5: Run Local Application
```bash
streamlit run app.py
# Access at: http://localhost:8501
```

## ☁️ Streamlit Cloud Deployment

### Step 1: Supabase Setup
1. **Create Supabase Project**
   - Go to https://supabase.com
   - Create new project
   - Note down connection details

2. **Get Supabase Connection String**
   ```
   postgresql://postgres.[project-ref]:[password]@aws-1-ap-south-1.pooler.supabase.com:6543/postgres
   ```

### Step 2: GitHub Repository Setup
```bash
# Push code to GitHub
git add .
git commit -m "Initial commit"
git push origin main
```

### Step 3: Streamlit Cloud Configuration
1. **Connect to Streamlit Cloud**
   - Go to https://share.streamlit.io
   - Connect your GitHub repository

2. **Configure Secrets in Streamlit Cloud**
   ```toml
   # In Streamlit Cloud secrets
   [connections.sql]
   url = "postgresql+psycopg://postgres.[project-ref]:[password]@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
   
   # Environment variables
   SUPABASE_URL = "postgresql://postgres.[project-ref]:[password]@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
   DEEPSEEK_API_KEY = "your_deepseek_api_key"
   ```

3. **Deploy Application**
   - Streamlit Cloud will automatically deploy
   - Access your app at: `https://your-app-name.streamlit.app`

## 🔄 Database Migration (Local to Supabase)

### Step 1: Export Local Data
```bash
# Export schema
pg_dump -h localhost -U username -d reflexta_analytics --schema-only > schema.sql

# Export data
pg_dump -h localhost -U username -d reflexta_analytics --data-only > data.sql
```

### Step 2: Import to Supabase
```bash
# Connect to Supabase and run schema
psql "postgresql://postgres.[project-ref]:[password]@aws-1-ap-south-1.pooler.supabase.com:6543/postgres" -f schema.sql

# Import data
psql "postgresql://postgres.[project-ref]:[password]@aws-1-ap-south-1.pooler.supabase.com:6543/postgres" -f data.sql
```

## 🗄️ Database Architecture

### Dual Database Setup
The application supports two database configurations:

#### 1. **Local Development (PostgreSQL)**
- **Purpose**: Local development and testing
- **Connection**: Direct PostgreSQL connection
- **Credentials**: Stored in `.streamlit/secrets.toml`
- **Setup**: `python database/setup_database.py`

#### 2. **Production Deployment (Supabase)**
- **Purpose**: Streamlit Cloud deployment
- **Connection**: Supabase PostgreSQL instance
- **Credentials**: Environment variables in Streamlit Cloud
- **Setup**: Automatic via environment variables

### Database Connection Logic
```python
# src/db.py - Smart database connection
def get_conn() -> Any:
    """Return appropriate database connection based on environment."""
    
    # Priority 1: Supabase URL for production deployment
    SUPABASE_URL = os.getenv("SUPABASE_URL", "postgresql://username:password@localhost:5432/database_name")
    
    try:
        # Try Supabase connection first (for Streamlit Cloud)
        return st.connection("sql", type="sql", url=SUPABASE_URL)
    except Exception:
        # Fallback to local secrets (for development)
        return st.connection("sql", type="sql")
```

### Core Tables
- **finance_departments**: Department information with budget allocations
- **finance_cost_centers**: Cost center definitions
- **finance_accounts**: Chart of accounts
- **finance_budgets**: Budget allocations and tracking
- **finance_transactions**: Financial transactions (revenue/expenses)
- **procurement_vendors**: Vendor information and ratings
- **procurement_categories**: Procurement categories
- **procurement_orders**: Purchase orders and tracking

### Key Relationships
- Departments → Transactions (1:many)
- Vendors → Orders (1:many)
- Categories → Orders (1:many)
- Accounts → Transactions (1:many)

## 🔧 Core Components

### Database Layer (`src/db.py`)
```python
def get_conn() -> Any:
    """Return a Streamlit SQL connection."""
    return st.connection("sql", type="sql")

def health_check() -> bool:
    """Verify database connectivity."""
    # Implementation with error handling
```

### Query Layer (`src/*_queries.py`)
- **Caching**: All queries use `@st.cache_data(ttl=60)`
- **Parameterization**: SQL injection prevention
- **Error Handling**: Graceful failure with user feedback
- **Performance**: Optimized queries with proper indexing

### Visualization Layer (`src/*_charts.py`)
- **Plotly Integration**: Interactive charts
- **Consistent Theming**: Professional color schemes
- **Responsive Design**: Mobile-friendly layouts
- **Data Validation**: Empty state handling

### UI Layer (`src/ui.py`)
- **Reusable Components**: KPI cards, section headers
- **Luxury Styling**: Professional gradients and shadows
- **Dark Mode**: Full theme compatibility
- **Accessibility**: Screen reader friendly

## 📊 Dashboard Architecture

### Main Application (`app.py`)
- **Entry Point**: Application initialization
- **Navigation**: Sidebar with company branding
- **Overview**: Executive summary with key metrics
- **Styling**: Global CSS and theme management

### Dashboard Pages (`pages/*.py`)
- **Finance Dashboard**: Financial analytics and reporting
- **Procurement Dashboard**: Vendor and order management
- **Analytics Dashboard**: Executive business intelligence
- **Database Analysis**: Schema exploration and health checks

### Common Patterns
```python
# Standard dashboard structure
st.set_page_config(page_title="Dashboard Name", layout="wide")

# Professional CSS
st.markdown("""<style>...</style>""", unsafe_allow_html=True)

# Header with luxury styling
st.markdown("""<div class="dashboard-header">...</div>""", unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    # Filter controls

# Main content
try:
    # Data loading and display
except Exception as e:
    st.error(f"Error: {str(e)}")
```

## 🎨 Design System

### Color Palette
- **Primary**: Dark navy gradients (`#0f0f23` → `#533483`)
- **Accents**: Indigo (`#6366f1`), Emerald (`#10b981`), Amber (`#f59e0b`)
- **Text**: Slate grays (`#1e293b`, `#64748b`)
- **Backgrounds**: Light grays with subtle gradients

### Typography
- **Headers**: 3rem, font-weight 800, gradient text
- **Body**: 1rem, font-weight 500
- **Labels**: 0.9rem, font-weight 600, uppercase
- **Metrics**: 2.5rem, font-weight 800

### Components
- **Cards**: 16px border-radius, luxury shadows
- **Buttons**: Rounded corners, hover effects
- **Charts**: Consistent theming, responsive sizing
- **Tables**: Professional styling, column formatting

## 🔒 Security Considerations

### Database Security
- **Parameterized Queries**: All SQL uses parameter binding
- **Connection Security**: Encrypted connections
- **Credential Management**: Streamlit secrets
- **Access Control**: Database user permissions

### Application Security
- **Input Validation**: All user inputs validated
- **Error Handling**: No sensitive data in error messages
- **Caching**: Secure data caching with TTL
- **Deployment**: HTTPS in production

## 🗃️ Adding Other Database Connections

### Oracle Database Integration

#### Step 1: Install Oracle Dependencies
```bash
# Install Oracle Instant Client
# Windows: Download from Oracle website
# macOS: brew install instantclient-basic
# Ubuntu: Download from Oracle website

# Install Python Oracle driver
pip install cx_Oracle
# OR for newer versions
pip install oracledb
```

#### Step 2: Configure Oracle Connection
Update `src/db.py`:
```python
import oracledb
from sqlalchemy import create_engine

def get_oracle_conn():
    """Return Oracle database connection."""
    oracle_url = os.getenv("ORACLE_URL", "oracle+cx_oracle://username:password@localhost:1521/XE")
    
    try:
        engine = create_engine(oracle_url)
        return engine
    except Exception as e:
        st.error(f"Oracle connection failed: {e}")
        return None
```

#### Step 3: Update Connection Logic
```python
# src/db.py - Enhanced database connection
def get_conn() -> Any:
    """Return appropriate database connection based on environment."""
    
    # Check for Oracle connection
    if os.getenv("USE_ORACLE", "false").lower() == "true":
        return get_oracle_conn()
    
    # Default PostgreSQL logic
    SUPABASE_URL = os.getenv("SUPABASE_URL", "postgresql://username:password@localhost:5432/database_name")
    
    try:
        return st.connection("sql", type="sql", url=SUPABASE_URL)
    except Exception:
        return st.connection("sql", type="sql")
```

#### Step 4: Oracle Configuration
```toml
# .streamlit/secrets.toml
[connections.oracle]
url = "oracle+cx_oracle://username:password@localhost:1521/XE"

# Environment variables
USE_ORACLE = "true"
ORACLE_URL = "oracle+cx_oracle://username:password@localhost:1521/XE"
```

### MySQL Database Integration

#### Step 1: Install MySQL Dependencies
```bash
pip install pymysql
# OR
pip install mysql-connector-python
```

#### Step 2: Configure MySQL Connection
```python
# src/db.py - MySQL connection
def get_mysql_conn():
    """Return MySQL database connection."""
    mysql_url = os.getenv("MYSQL_URL", "mysql+pymysql://username:password@localhost:3306/database_name")
    
    try:
        engine = create_engine(mysql_url)
        return engine
    except Exception as e:
        st.error(f"MySQL connection failed: {e}")
        return None
```

### SQL Server Integration

#### Step 1: Install SQL Server Dependencies
```bash
pip install pyodbc
# OR
pip install mssql+pyodbc
```

#### Step 2: Configure SQL Server Connection
```python
# src/db.py - SQL Server connection
def get_sqlserver_conn():
    """Return SQL Server database connection."""
    sqlserver_url = os.getenv("SQLSERVER_URL", "mssql+pyodbc://username:password@localhost:1433/database_name?driver=ODBC+Driver+17+for+SQL+Server")
    
    try:
        engine = create_engine(sqlserver_url)
        return engine
    except Exception as e:
        st.error(f"SQL Server connection failed: {e}")
        return None
```

### Multi-Database Support

#### Enhanced Connection Manager
```python
# src/db.py - Multi-database support
class DatabaseManager:
    def __init__(self):
        self.db_type = os.getenv("DATABASE_TYPE", "postgresql")
        self.connections = {}
    
    def get_connection(self):
        """Get appropriate database connection."""
        if self.db_type == "oracle":
            return self._get_oracle_conn()
        elif self.db_type == "mysql":
            return self._get_mysql_conn()
        elif self.db_type == "sqlserver":
            return self._get_sqlserver_conn()
        else:
            return self._get_postgresql_conn()
    
    def _get_oracle_conn(self):
        """Oracle connection."""
        oracle_url = os.getenv("ORACLE_URL")
        return create_engine(oracle_url)
    
    def _get_mysql_conn(self):
        """MySQL connection."""
        mysql_url = os.getenv("MYSQL_URL")
        return create_engine(mysql_url)
    
    def _get_sqlserver_conn(self):
        """SQL Server connection."""
        sqlserver_url = os.getenv("SQLSERVER_URL")
        return create_engine(sqlserver_url)
    
    def _get_postgresql_conn(self):
        """PostgreSQL connection."""
        SUPABASE_URL = os.getenv("SUPABASE_URL", "postgresql://username:password@localhost:5432/database_name")
        try:
            return st.connection("sql", type="sql", url=SUPABASE_URL)
        except Exception:
            return st.connection("sql", type="sql")
```

### Database-Specific Schema Adaptations

#### Oracle Schema Changes
```sql
-- Oracle-specific schema modifications
-- Replace SERIAL with NUMBER and SEQUENCE
CREATE SEQUENCE finance_departments_id_seq;
CREATE TABLE finance_departments (
    id NUMBER DEFAULT finance_departments_id_seq.NEXTVAL PRIMARY KEY,
    dept_name VARCHAR2(100) NOT NULL,
    dept_code VARCHAR2(10) UNIQUE NOT NULL,
    budget_allocation NUMBER(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### MySQL Schema Changes
```sql
-- MySQL-specific schema modifications
CREATE TABLE finance_departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL,
    dept_code VARCHAR(10) UNIQUE NOT NULL,
    budget_allocation DECIMAL(15,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;
```

#### SQL Server Schema Changes
```sql
-- SQL Server-specific schema modifications
CREATE TABLE finance_departments (
    id INT IDENTITY(1,1) PRIMARY KEY,
    dept_name NVARCHAR(100) NOT NULL,
    dept_code NVARCHAR(10) UNIQUE NOT NULL,
    budget_allocation DECIMAL(15,2),
    created_at DATETIME2 DEFAULT GETDATE()
);
```

## 🚀 Deployment

### Streamlit Cloud Deployment
1. **Connect GitHub repository**
2. **Configure secrets** in Streamlit Cloud dashboard
3. **Set environment variables** for your chosen database
4. **Deploy automatically** on push

### Local Development
1. **Database setup**: Run `python database/setup_database.py`
2. **Environment**: Configure `.streamlit/secrets.toml`
3. **Run**: `streamlit run app.py`
4. **Debug**: Use Cursor IDE with AI assistance

### Production Considerations
- **Database**: Use production database instance
- **Connection Pooling**: Configure appropriate pool sizes
- **Caching**: Configure appropriate TTL values
- **Monitoring**: Set up error tracking
- **Backup**: Regular database backups
- **Security**: Use encrypted connections

## 🧪 Testing

### Manual Testing
1. **Database Connection**: Verify connectivity
2. **Data Loading**: Check all queries return data
3. **UI Components**: Test all interactive elements
4. **Responsive Design**: Test on different screen sizes
5. **Error Handling**: Test with invalid inputs

### Automated Testing
```python
# Example test structure
def test_database_connection():
    """Test database connectivity."""
    assert health_check() == True

def test_query_functions():
    """Test query functions return data."""
    # Implementation
```

## 📈 Performance Optimization

### Database Optimization
- **Indexing**: Proper indexes on frequently queried columns
- **Query Optimization**: Efficient SQL with proper joins
- **Connection Pooling**: Reuse database connections
- **Caching**: 60-second TTL for query results

### Application Optimization
- **Lazy Loading**: Load data only when needed
- **Component Caching**: Cache expensive operations
- **Image Optimization**: Compressed assets
- **CSS Optimization**: Minified stylesheets

## 🐛 Troubleshooting

### Database Connection Issues

#### PostgreSQL Connection Problems
```bash
# Check PostgreSQL service status
# Windows
net start postgresql-x64-13

# macOS
brew services start postgresql

# Ubuntu
sudo systemctl start postgresql

# Test connection
psql -h localhost -U username -d database_name
```

#### Supabase Connection Issues
```python
# Test Supabase connection
import os
import psycopg2

def test_supabase_connection():
    try:
        conn = psycopg2.connect(
            host="aws-1-ap-south-1.pooler.supabase.com",
            port="6543",
            database="postgres",
            user="postgres.[project-ref]",
            password="your_password"
        )
        print("Supabase connection successful!")
        conn.close()
    except Exception as e:
        print(f"Supabase connection failed: {e}")
```

#### Oracle Connection Issues
```bash
# Check Oracle service
# Windows
net start OracleServiceXE

# Test Oracle connection
sqlplus username/password@localhost:1521/XE
```

#### MySQL Connection Issues
```bash
# Check MySQL service
# Windows
net start mysql

# macOS
brew services start mysql

# Ubuntu
sudo systemctl start mysql

# Test connection
mysql -h localhost -u username -p
```

### Environment Variable Issues

#### Check Environment Variables
```python
# Debug environment variables
import os
import streamlit as st

def debug_environment():
    st.write("Environment Variables:")
    st.write(f"SUPABASE_URL: {os.getenv('SUPABASE_URL', 'Not set')}")
    st.write(f"DATABASE_TYPE: {os.getenv('DATABASE_TYPE', 'Not set')}")
    st.write(f"USE_ORACLE: {os.getenv('USE_ORACLE', 'Not set')}")
```

#### Streamlit Secrets Issues
```python
# Debug Streamlit secrets
import streamlit as st

def debug_secrets():
    try:
        secrets = st.secrets
        st.write("Secrets available:", list(secrets.keys()))
        
        if 'connections' in secrets:
            st.write("Database connections:", secrets['connections'])
    except Exception as e:
        st.error(f"Secrets error: {e}")
```

### Common Issues
1. **Database Connection**: Check credentials in secrets.toml
2. **Import Errors**: Ensure all dependencies installed
3. **Chart Display**: Verify data format and column names
4. **Styling Issues**: Check CSS class names and selectors
5. **Performance**: Monitor database query execution times
6. **Oracle Instant Client**: Ensure Oracle Instant Client is installed
7. **MySQL Driver**: Install correct MySQL Python driver
8. **SQL Server ODBC**: Install Microsoft ODBC Driver for SQL Server

### Debug Tools
- **Streamlit Debug**: Use `st.write()` for data inspection
- **Database Logs**: Check database-specific logs
- **Browser DevTools**: Inspect CSS and JavaScript
- **Cursor AI**: Use AI assistance for debugging
- **Connection Testing**: Use database-specific connection testers

## 🔄 Development Workflow

### Code Standards
- **Python**: PEP 8 compliance with Black formatting
- **SQL**: Proper formatting and commenting
- **CSS**: Consistent naming and organization
- **Documentation**: Comprehensive docstrings

### Git Workflow
1. **Feature Branches**: Create branches for new features
2. **Commit Messages**: Descriptive commit messages
3. **Code Review**: Review all changes before merge
4. **Testing**: Test all changes before deployment

### Extension Guidelines
- **New Dashboards**: Follow existing patterns
- **New KPIs**: Use consistent metric display
- **New Charts**: Follow design system
- **New Modules**: Complete module structure

## 📚 Resources

### Documentation
- **Streamlit**: https://docs.streamlit.io/
- **Plotly**: https://plotly.com/python/
- **SQLAlchemy**: https://docs.sqlalchemy.org/
- **PostgreSQL**: https://www.postgresql.org/docs/

### Development Tools
- **Cursor IDE**: AI-powered development
- **Git**: Version control
- **Docker**: Containerization (optional)
- **Postman**: API testing (if needed)

## 🎯 Future Enhancements

### Planned Features
- **User Authentication**: Role-based access control
- **Real-time Updates**: WebSocket integration
- **Advanced Analytics**: Machine learning insights
- **Mobile App**: React Native companion
- **API Integration**: External data sources

### Technical Debt
- **Test Coverage**: Increase automated testing
- **Documentation**: API documentation
- **Monitoring**: Application performance monitoring
- **Security**: Enhanced security measures

## 📞 Support

### Getting Help
- **Documentation**: Check this guide and README
- **Extension Guide**: Use EXTENSION_GUIDE.md for new features
- **Quick Reference**: Use QUICK_REFERENCE.md for common tasks
- **Issues**: Create GitHub issues for bugs

### Contributing
- **Code Quality**: Follow established patterns
- **Testing**: Test all changes thoroughly
- **Documentation**: Update docs for new features
- **Review**: Submit pull requests for review

---

**Last Updated**: December 2024  
**Version**: 1.0.0  
**Maintainer**: Development Team
