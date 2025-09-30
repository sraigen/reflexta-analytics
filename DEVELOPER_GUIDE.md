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
- PostgreSQL database
- Git

### Installation
1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd data-viz-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**
   - Update `.streamlit/secrets.toml` with your database credentials
   - Run database setup: `python database/setup_database.py`

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

## 🗄️ Database Schema

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

## 🚀 Deployment

### Streamlit Cloud
1. **Connect GitHub repository**
2. **Configure secrets** in Streamlit Cloud dashboard
3. **Set environment variables**
4. **Deploy automatically** on push

### Local Development
1. **Database setup**: Run `python database/setup_database.py`
2. **Environment**: Configure `.streamlit/secrets.toml`
3. **Run**: `streamlit run app.py`
4. **Debug**: Use Cursor IDE with AI assistance

### Production Considerations
- **Database**: Use production PostgreSQL instance
- **Caching**: Configure appropriate TTL values
- **Monitoring**: Set up error tracking
- **Backup**: Regular database backups

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

### Common Issues
1. **Database Connection**: Check credentials in secrets.toml
2. **Import Errors**: Ensure all dependencies installed
3. **Chart Display**: Verify data format and column names
4. **Styling Issues**: Check CSS class names and selectors
5. **Performance**: Monitor database query execution times

### Debug Tools
- **Streamlit Debug**: Use `st.write()` for data inspection
- **Database Logs**: Check PostgreSQL logs
- **Browser DevTools**: Inspect CSS and JavaScript
- **Cursor AI**: Use AI assistance for debugging

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
