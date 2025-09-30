# 🚀 Reflexta Analytics Platform

A production-grade data visualization platform built with Python, Streamlit, and PostgreSQL. Features comprehensive Finance and Procurement analytics with luxury professional UI, executive insights, and interactive visualizations.

## 🎯 Key Features

- **💼 Enterprise-Grade**: Production-ready with professional luxury UI
- **📊 Modern KPI Indicators**: Animated progress bars and gradient cards
- **🎨 Contemporary Design**: Glass morphism effects and modern styling
- **⚡ High Performance**: Optimized queries with intelligent caching
- **🔒 Secure**: Environment variables and secure credential management
- **📱 Responsive**: Works seamlessly across all devices
- **🤖 AI Assistant**: Intelligent chatbot with DeepSeek integration

## 🚀 Features

### Core Modules
- **📊 Executive Dashboard**: High-level KPIs and business metrics
- **💰 Finance Module**: Budget management, transaction tracking, cost center analysis
- **🛒 Procurement Module**: Vendor management, order tracking, category analysis
- **📈 Analytics Dashboard**: Advanced business intelligence and reporting
- **🗄️ Database Analysis**: Schema exploration and data quality checks

### Professional Features
- **🎨 Modern UI**: Glass morphism design with animated KPI indicators
- **⚡ Real-time Data**: Live database connections with intelligent caching
- **📊 Interactive Charts**: Plotly-powered visualizations with professional styling
- **🔍 Advanced Analytics**: Executive summaries, performance heatmaps, trend analysis
- **🤖 AI Assistant**: Intelligent chatbot powered by DeepSeek API for dashboard help
- **📱 Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **🔒 Security**: Environment variables and secure credential management

## 🏗️ Architecture

### Technology Stack
- **Frontend**: Streamlit with custom CSS styling
- **Backend**: Python with SQLAlchemy 2.0
- **Database**: PostgreSQL with comprehensive schema
- **Visualization**: Plotly Express and Graph Objects
- **Caching**: Streamlit's built-in caching for performance
- **Deployment**: Docker and Docker Compose ready

### Database Schema
- **Finance Tables**: 8 core tables with relationships
- **Procurement Tables**: 3 core tables with vendor management
- **Analytical Views**: 15+ views for business intelligence
- **Indexes**: Optimized for performance
- **Triggers**: Automatic budget and status updates

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- PostgreSQL 12+
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

4. **Configure database connection and AI assistant**
   ```bash
   cp .streamlit/secrets_template.toml .streamlit/secrets.toml
   # Edit .streamlit/secrets.toml with your database credentials and DeepSeek API key
   ```

5. **Set up database schema and sample data**
   ```bash
   python setup_db.py
   python populate_sample_data.py
   ```

6. **Run the application**
   ```bash
   streamlit run app.py
   ```

7. **Access the dashboard**
   ```
   http://localhost:8501
   ```

## 📊 Dashboard Features

### Main Dashboard
- **Executive Summary**: Key business metrics and KPIs
- **Department Analytics**: Performance comparison across departments
- **Quick Navigation**: Access to specialized dashboards
- **Real-time Filters**: Date range and department filtering

### Finance Dashboard
- **Financial KPIs**: Revenue, expenses, profit metrics with trend analysis
- **Budget vs Actual**: Comprehensive budget analysis with utilization rates
- **Account Analysis**: Detailed account performance and categorization
- **Cost Center Analysis**: Spending patterns by cost center
- **Vendor Spending**: Financial transactions by vendor
- **Cash Flow Analysis**: Revenue and expense trends over time

### Procurement Dashboard
- **Procurement KPIs**: Order metrics, completion rates, vendor performance
- **Vendor Performance**: Comprehensive vendor analysis with ratings
- **Category Spending**: Spending analysis by procurement category
- **Department Spending**: Procurement patterns by department
- **Delivery Performance**: On-time delivery metrics and analysis
- **Order Management**: Order status tracking and completion rates

### Analytics Dashboard
- **Executive Summary**: High-level business intelligence
- **Department Performance**: Multi-dimensional performance analysis
- **Vendor Performance**: Advanced vendor analytics with radar charts
- **Financial Trends**: Time-series analysis of financial metrics
- **Budget Analysis**: Detailed budget vs actual performance
- **Category Analysis**: Spending distribution and trends
- **Performance Heatmaps**: Visual performance comparison

### Database Analysis
- **Schema Explorer**: Browse all tables, views, and relationships
- **Data Quality**: Sample data and statistical analysis
- **Table Information**: Column details and constraints
- **Sample Data**: Preview of actual data in tables

## 🛠️ Configuration

### Database Setup

The application requires a PostgreSQL database. The setup process includes:

1. **Schema Creation**: All tables, views, indexes, and triggers
2. **Sample Data**: Comprehensive realistic business data
3. **Performance Optimization**: Proper indexing and constraints
4. **Data Integrity**: Foreign keys and check constraints

### Environment Configuration

Create a `.streamlit/secrets.toml` file:

```toml
[connections.sql]
url = "postgresql+psycopg://username:password@localhost:5432/database_name"
```

### Customization

- **Colors**: Modify `PROFESSIONAL_COLORS` in chart modules
- **Styling**: Update CSS in dashboard pages
- **Queries**: Add new analytics in `src/analytics_queries.py`
- **Charts**: Create new visualizations in `src/analytics_charts.py`

## 📁 Project Structure

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
│   ├── procurement_charts.py        # Procurement visualizations
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
├── populate_sample_data.py         # Sample data population
├── README.md                       # Project documentation
├── DEVELOPER_GUIDE.md             # Developer documentation
├── EXTENSION_GUIDE.md             # Extension guide for users
├── QUICK_REFERENCE.md              # Quick reference for developers
├── Dockerfile                      # Docker configuration
├── docker-compose.yml              # Docker Compose setup
└── logo.png                        # Company logo
```

## 🔧 Development

### Adding New Modules

1. **Create query functions** in `src/` directory
2. **Create chart functions** for visualizations
3. **Create dashboard page** in `pages/` directory
4. **Update navigation** in `app.py`
5. **Add sample data** if needed

### Database Schema Details

#### Finance Module
- `finance_departments`: Department information and budgets
- `finance_cost_centers`: Cost center management
- `finance_accounts`: Chart of accounts
- `finance_budgets`: Budget allocation and tracking
- `finance_transactions`: Financial transactions

#### Procurement Module
- `procurement_vendors`: Vendor information and ratings
- `procurement_categories`: Product/service categories
- `procurement_orders`: Purchase orders and tracking

#### Analytical Views
- Budget utilization analysis
- Vendor performance metrics
- Department spending patterns
- Financial trend analysis
- Procurement efficiency metrics

## 🚀 Deployment

### Docker Deployment

1. **Build the image**
   ```bash
   docker build -t enterprise-analytics .
   ```

2. **Run with Docker Compose**
   ```bash
   docker-compose up -d
   ```

### Production Considerations

- **Security**: Configure proper database credentials and SSL
- **Performance**: Set up database connection pooling
- **Monitoring**: Implement logging and health checks
- **Backup**: Configure automated database backups
- **Scaling**: Consider load balancing for high traffic

## 📊 Sample Data

The platform includes comprehensive sample data:

- **8 Departments**: Finance, Procurement, IT, HR, Operations, Marketing, Sales, Legal
- **10 Cost Centers**: Detailed cost center structure
- **10 Account Types**: Complete chart of accounts
- **200+ Transactions**: Realistic financial transactions over 6 months
- **10 Vendors**: Diverse vendor base with ratings and performance data
- **10 Categories**: Comprehensive procurement categories
- **150+ Orders**: Realistic procurement orders with various statuses

## 🎯 Use Cases

### Executive Management
- High-level business metrics and KPIs
- Department performance comparison
- Budget utilization and financial health
- Strategic decision support

### Finance Teams
- Budget planning and tracking
- Expense analysis and categorization
- Financial reporting and compliance
- Cost center performance

### Procurement Teams
- Vendor performance management
- Order tracking and fulfillment
- Category spending analysis
- Supplier relationship management

### Operations Teams
- Department efficiency metrics
- Resource utilization analysis
- Performance benchmarking
- Process optimization insights

## 🔮 Roadmap

### Short Term
- [ ] Real-time notifications and alerts
- [ ] Advanced filtering and search capabilities
- [ ] Export functionality for reports
- [ ] Mobile app integration

### Medium Term
- [ ] Machine learning integration for predictions
- [ ] Advanced analytics with statistical models
- [ ] API endpoints for external integrations
- [ ] Multi-tenant architecture

### Long Term
- [ ] AI-powered insights and recommendations
- [ ] Advanced workflow automation
- [ ] Integration with ERP systems
- [ ] Cloud-native deployment options

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- 📧 Create an issue in the repository
- 📚 Check the documentation and examples
- 💬 Join our community discussions
- 🔧 Review the troubleshooting guide

## 🙏 Acknowledgments

- Streamlit team for the amazing framework
- Plotly for powerful visualization capabilities
- PostgreSQL community for robust database features
- Open source contributors and the community