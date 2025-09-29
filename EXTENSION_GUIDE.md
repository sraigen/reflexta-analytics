# 🚀 Reflexta Analytics - Extension Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Understanding the Application Structure](#understanding-the-application-structure)
3. [Creating New Dashboards](#creating-new-dashboards)
4. [Adding New KPIs](#adding-new-kpis)
5. [Building New Reports](#building-new-reports)
6. [Adding New Modules](#adding-new-modules)
7. [Best Practices](#best-practices)
8. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Knowledge
- **Basic SQL**: Understanding SELECT, WHERE, GROUP BY, JOIN statements
- **Cursor IDE**: Familiarity with Cursor's AI assistance features
- **File Management**: Basic understanding of folders and files

### Required Tools
- Cursor IDE (already installed)
- Python 3.10+ (already installed)
- PostgreSQL database access
- Git for version control

---

## Understanding the Application Structure

### 📁 Project Structure
```
data-viz-app/
├── app.py                          # Main application entry point
├── pages/                          # Dashboard pages
│   ├── 00_Database_Analysis.py    # Database exploration
│   ├── 03_Finance_Dashboard.py     # Finance analytics
│   ├── 04_Procurement_Dashboard.py # Procurement analytics
│   └── 05_Analytics_Dashboard.py   # Executive analytics
├── src/                            # Core application code
│   ├── db.py                       # Database connection
│   ├── ui.py                       # UI components
│   ├── finance_queries.py         # Finance data queries
│   ├── finance_charts.py           # Finance visualizations
│   ├── procurement_queries.py      # Procurement data queries
│   ├── procurement_charts.py       # Procurement visualizations
│   ├── analytics_queries.py        # Analytics data queries
│   └── analytics_charts.py         # Analytics visualizations
├── database/
│   └── schema.sql                  # Database schema
└── requirements.txt                # Python dependencies
```

### 🔧 Key Components

**1. Database Layer (`src/db.py`)**
- Handles database connections
- Provides health check functionality
- Used by all query functions

**2. Query Layer (`src/*_queries.py`)**
- Contains SQL queries for data retrieval
- Implements caching for performance
- Handles parameterized queries for security

**3. Visualization Layer (`src/*_charts.py`)**
- Creates interactive charts using Plotly
- Handles data formatting and styling
- Provides consistent chart themes

**4. UI Layer (`src/ui.py` & `pages/*.py`)**
- Reusable UI components
- Dashboard layouts and styling
- Filter controls and navigation

---

## Creating New Dashboards

### Step 1: Plan Your Dashboard

**Before coding, define:**
- **Purpose**: What business questions will it answer?
- **Data Sources**: Which database tables will you use?
- **KPIs**: What key metrics will you display?
- **Filters**: What filtering options do users need?
- **Charts**: What visualizations will be most effective?

### Step 2: Create the Dashboard File

**1. Navigate to the `pages/` folder**
**2. Create a new file following the naming convention:**
```
pages/06_YourModule_Dashboard.py
```

**3. Use this template as your starting point:**

```python
from __future__ import annotations

import datetime as dt
from typing import Optional

import streamlit as st

from src.db import health_check
from src.your_module_queries import get_your_kpis, get_your_summary
from src.your_module_charts import your_chart_function
from src.ui import empty_state

st.set_page_config(page_title="Your Module Dashboard", layout="wide")

# Professional CSS for Your Module Dashboard
st.markdown("""
<style>
    .your-module-header {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .your-module-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .your-module-header h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -2px;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
        position: relative;
        z-index: 1;
        background: linear-gradient(45deg, #ffffff, #e2e8f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .your-module-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="your-module-header">
    <h1>🎯 Your Module Dashboard</h1>
    <p>Comprehensive Analytics & Performance Metrics</p>
</div>
""", unsafe_allow_html=True)

if not health_check():
    st.error("Database connection failed. Please check your connection settings.")
    st.stop()

# Dashboard Filters - Sidebar Approach
with st.sidebar:
    st.markdown("### 🔧 Your Module Filters")
    
    from_date = st.date_input(
        "From Date", 
        value=dt.date.today() - dt.timedelta(days=30),
        help="Select start date for analysis"
    )

    to_date = st.date_input(
        "To Date", 
        value=dt.date.today(),
        help="Select end date for analysis"
    )

    # Add your specific filters here
    department = st.selectbox(
        "Department",
        options=["All", "Finance", "Procurement", "IT", "HR", "Operations", "Marketing", "Sales", "Legal"],
        help="Filter by specific department"
    )

    # Get department ID if specific department is selected
    dept_id = None
    if department != "All":
        dept_mapping = {
            "Finance": 1, "Procurement": 2, "IT": 3, "HR": 4, "Operations": 5,
            "Marketing": 6, "Sales": 7, "Legal": 8
        }
        dept_id = dept_mapping.get(department)

    st.markdown("---")
    st.markdown("### Quick Actions")
    if st.button("Refresh Data", use_container_width=True):
        st.rerun()
    
    if st.button("Export Report", use_container_width=True):
        st.success("Report export feature coming soon!")

try:
    # Your Module KPIs
    st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)
    
    kpis = get_your_kpis(from_date, to_date, dept_id)
    if not kpis.empty:
        row = kpis.iloc[0]
        
        # Display your KPIs using st.metric
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Items", 
                value=f"{row['total_items']:,.0f}", 
                delta=f"{row['item_growth']:,.0f}"
            )
        
        with col2:
            st.metric(
                label="Total Value", 
                value=f"${row['total_value']:,.2f}", 
                delta=f"${row['value_growth']:,.2f}"
            )
        
        with col3:
            st.metric(
                label="Average Value", 
                value=f"${row['avg_value']:,.2f}", 
                delta=f"${row['avg_growth']:,.2f}"
            )
        
        with col4:
            st.metric(
                label="Success Rate", 
                value=f"{row['success_rate']:,.1f}%", 
                delta=f"{row['rate_growth']:,.1f}%"
            )
    else:
        st.info("No KPI data available for the selected period.")

    # Your Module Charts
    st.markdown('<div class="section-header">Analytics & Trends</div>', unsafe_allow_html=True)
    
    # Add your charts here
    chart_data = get_your_summary(from_date, to_date, dept_id)
    if not empty_state(chart_data):
        st.plotly_chart(your_chart_function(chart_data), use_container_width=True)
    else:
        st.info("No chart data available for the selected period.")

except Exception as e:
    st.error(f"Error loading your module data: {str(e)}")
    st.info("Please check your database connection and try again.")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p>🎯 Your Module Dashboard - Reflexta Data Intelligence</p>
    <p>Comprehensive Analytics & Performance Metrics</p>
</div>
""", unsafe_allow_html=True)
```

### Step 3: Add Navigation

**1. Open `app.py`**
**2. Find the sidebar navigation section**
**3. Add your new dashboard to the navigation:**

```python
# In the sidebar section of app.py
st.markdown("### Navigation")
st.info("Navigate to specific dashboards for detailed analytics and filtering options.")

# Add your new dashboard
if st.button("🎯 Your Module Dashboard", use_container_width=True):
    st.switch_page("pages/06_YourModule_Dashboard.py")
```

---

## Adding New KPIs

### Step 1: Create Query Functions

**1. Create a new query file: `src/your_module_queries.py`**

```python
from __future__ import annotations

import datetime as dt
from typing import Optional

import pandas as pd
import streamlit as st

from src.db import get_conn

@st.cache_data(ttl=60, show_spinner=False)
def get_your_kpis(from_dt: dt.date, to_dt: dt.date, dept_id: Optional[int] = None) -> pd.DataFrame:
    """Get key performance indicators for your module."""
    
    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if dept_id:
        where_dept = " AND dept_id = :dept_id"
        params["dept_id"] = dept_id
    
    # Calculate previous period for growth comparison
    from datetime import timedelta
    period_days = (to_dt - from_dt).days
    prev_from_dt = from_dt - timedelta(days=period_days)
    prev_to_dt = from_dt - timedelta(days=1)
    
    sql = f"""
    WITH current_period AS (
        SELECT 
            COUNT(*) as total_items,
            COALESCE(SUM(amount), 0) as total_value,
            COALESCE(AVG(amount), 0) as avg_value,
            COUNT(CASE WHEN status = 'Completed' THEN 1 END) as completed_items,
            COUNT(CASE WHEN status = 'Completed' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0) as success_rate
        FROM your_table
        WHERE created_date BETWEEN :from_dt AND :to_dt
            {where_dept}
    ),
    previous_period AS (
        SELECT 
            COUNT(*) as prev_total_items,
            COALESCE(SUM(amount), 0) as prev_total_value,
            COALESCE(AVG(amount), 0) as prev_avg_value,
            COUNT(CASE WHEN status = 'Completed' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0) as prev_success_rate
        FROM your_table
        WHERE created_date BETWEEN :prev_from_dt AND :prev_to_dt
            {where_dept}
    )
    SELECT 
        c.*,
        COALESCE(c.total_items - p.prev_total_items, 0) as item_growth,
        COALESCE(c.total_value - p.prev_total_value, 0) as value_growth,
        COALESCE(c.avg_value - p.prev_avg_value, 0) as avg_growth,
        COALESCE(c.success_rate - p.prev_success_rate, 0) as rate_growth
    FROM current_period c
    CROSS JOIN previous_period p
    """
    
    params["prev_from_dt"] = prev_from_dt
    params["prev_to_dt"] = prev_to_dt
    
    conn = get_conn()
    return conn.query(sql, params=params)

@st.cache_data(ttl=60, show_spinner=False)
def get_your_summary(from_dt: dt.date, to_dt: dt.date, dept_id: Optional[int] = None) -> pd.DataFrame:
    """Get summary data for your module."""
    
    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if dept_id:
        where_dept = " AND dept_id = :dept_id"
        params["dept_id"] = dept_id
    
    sql = f"""
    SELECT 
        category,
        COUNT(*) as item_count,
        SUM(amount) as total_amount,
        AVG(amount) as avg_amount,
        COUNT(CASE WHEN status = 'Completed' THEN 1 END) as completed_count
    FROM your_table
    WHERE created_date BETWEEN :from_dt AND :to_dt
        {where_dept}
    GROUP BY category
    ORDER BY total_amount DESC
    """
    
    conn = get_conn()
    return conn.query(sql, params=params)
```

### Step 2: Create Chart Functions

**1. Create a new chart file: `src/your_module_charts.py`**

```python
from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def your_chart_function(df: pd.DataFrame) -> go.Figure:
    """Create a chart for your module data."""
    
    if df.empty:
        return go.Figure()
    
    fig = px.bar(
        df,
        x='category',
        y='total_amount',
        title="Your Module Analysis by Category",
        labels={'total_amount': 'Total Amount ($)', 'category': 'Category'},
        color='total_amount',
        color_continuous_scale='Viridis'
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Category",
        yaxis_title="Total Amount ($)",
        showlegend=False
    )
    
    return fig

def your_trend_chart(df: pd.DataFrame) -> go.Figure:
    """Create a trend chart for your module data."""
    
    if df.empty:
        return go.Figure()
    
    fig = px.line(
        df,
        x='date',
        y='amount',
        title="Your Module Trends Over Time",
        labels={'amount': 'Amount ($)', 'date': 'Date'},
        markers=True
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Date",
        yaxis_title="Amount ($)"
    )
    
    return fig
```

### Step 3: Display KPIs in Dashboard

**In your dashboard file, add the KPI display:**

```python
# Your Module KPIs
st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)

kpis = get_your_kpis(from_date, to_date, dept_id)
if not kpis.empty:
    row = kpis.iloc[0]
    
    # Display your KPIs using st.metric
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Items", 
            value=f"{row['total_items']:,.0f}", 
            delta=f"{row['item_growth']:,.0f}"
        )
    
    with col2:
        st.metric(
            label="Total Value", 
            value=f"${row['total_value']:,.2f}", 
            delta=f"${row['value_growth']:,.2f}"
        )
    
    with col3:
        st.metric(
            label="Average Value", 
            value=f"${row['avg_value']:,.2f}", 
            delta=f"${row['avg_growth']:,.2f}"
        )
    
    with col4:
        st.metric(
            label="Success Rate", 
            value=f"{row['success_rate']:,.1f}%", 
            delta=f"{row['rate_growth']:,.1f}%"
        )
else:
    st.info("No KPI data available for the selected period.")
```

---

## Building New Reports

### Step 1: Create Report Query Functions

**Add to your `src/your_module_queries.py`:**

```python
@st.cache_data(ttl=60, show_spinner=False)
def get_detailed_report(from_dt: dt.date, to_dt: dt.date, dept_id: Optional[int] = None) -> pd.DataFrame:
    """Get detailed report data for your module."""
    
    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if dept_id:
        where_dept = " AND dept_id = :dept_id"
        params["dept_id"] = dept_id
    
    sql = f"""
    SELECT 
        item_id,
        item_name,
        category,
        amount,
        status,
        created_date,
        completed_date,
        dept_name,
        created_by
    FROM your_table t
    JOIN finance_departments d ON t.dept_id = d.dept_id
    WHERE t.created_date BETWEEN :from_dt AND :to_dt
        {where_dept}
    ORDER BY t.created_date DESC
    """
    
    conn = get_conn()
    return conn.query(sql, params=params)

@st.cache_data(ttl=60, show_spinner=False)
def get_summary_report(from_dt: dt.date, to_dt: dt.date, dept_id: Optional[int] = None) -> pd.DataFrame:
    """Get summary report data for your module."""
    
    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if dept_id:
        where_dept = " AND dept_id = :dept_id"
        params["dept_id"] = dept_id
    
    sql = f"""
    SELECT 
        d.dept_name,
        COUNT(*) as total_items,
        SUM(amount) as total_amount,
        AVG(amount) as avg_amount,
        COUNT(CASE WHEN status = 'Completed' THEN 1 END) as completed_items,
        COUNT(CASE WHEN status = 'Completed' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0) as completion_rate
    FROM your_table t
    JOIN finance_departments d ON t.dept_id = d.dept_id
    WHERE t.created_date BETWEEN :from_dt AND :to_dt
        {where_dept}
    GROUP BY d.dept_id, d.dept_name
    ORDER BY total_amount DESC
    """
    
    conn = get_conn()
    return conn.query(sql, params=params)
```

### Step 2: Add Report Sections to Dashboard

**In your dashboard file, add report sections:**

```python
# Detailed Report
st.markdown('<div class="section-header">Detailed Report</div>', unsafe_allow_html=True)

detailed_data = get_detailed_report(from_date, to_date, dept_id)
if not empty_state(detailed_data):
    st.dataframe(
        detailed_data,
        hide_index=True,
        use_container_width=True,
        column_config={
            "item_id": "ID",
            "item_name": "Item Name",
            "category": "Category",
            "amount": st.column_config.NumberColumn("Amount", format="$%.2f"),
            "status": "Status",
            "created_date": "Created Date",
            "completed_date": "Completed Date",
            "dept_name": "Department",
            "created_by": "Created By"
        }
    )
else:
    st.info("No detailed report data available for the selected period.")

# Summary Report
st.markdown('<div class="section-header">Summary Report</div>', unsafe_allow_html=True)

summary_data = get_summary_report(from_date, to_date, dept_id)
if not empty_state(summary_data):
    st.dataframe(
        summary_data,
        hide_index=True,
        use_container_width=True,
        column_config={
            "dept_name": "Department",
            "total_items": "Total Items",
            "total_amount": st.column_config.NumberColumn("Total Amount", format="$%.2f"),
            "avg_amount": st.column_config.NumberColumn("Average Amount", format="$%.2f"),
            "completed_items": "Completed Items",
            "completion_rate": st.column_config.NumberColumn("Completion Rate", format="%.1f%%")
        }
    )
else:
    st.info("No summary report data available for the selected period.")
```

---

## Adding New Modules

### Step 1: Plan Your Module

**Define your module:**
- **Purpose**: What business process will it track?
- **Data Model**: What tables and relationships do you need?
- **KPIs**: What key metrics are important?
- **Reports**: What reports will users need?

### Step 2: Create Database Schema

**1. Open `database/schema.sql`**
**2. Add your module tables:**

```sql
-- Your Module Tables
CREATE TABLE your_module_items (
    item_id SERIAL PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    category_id INTEGER REFERENCES your_module_categories(category_id),
    dept_id INTEGER REFERENCES finance_departments(dept_id),
    amount DECIMAL(12,2) NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('Draft', 'Submitted', 'Approved', 'Completed', 'Cancelled')),
    priority VARCHAR(20) NOT NULL CHECK (priority IN ('Low', 'Medium', 'High', 'Urgent')),
    created_date DATE NOT NULL DEFAULT CURRENT_DATE,
    completed_date DATE,
    created_by VARCHAR(100),
    notes TEXT
);

CREATE TABLE your_module_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL,
    category_code VARCHAR(20) UNIQUE NOT NULL,
    description TEXT
);

-- Add indexes for performance
CREATE INDEX idx_your_module_items_dept ON your_module_items(dept_id);
CREATE INDEX idx_your_module_items_category ON your_module_items(category_id);
CREATE INDEX idx_your_module_items_status ON your_module_items(status);
CREATE INDEX idx_your_module_items_created_date ON your_module_items(created_date);
```

### Step 3: Create Module Files

**1. Create query file: `src/your_module_queries.py`**
**2. Create chart file: `src/your_module_charts.py`**
**3. Create dashboard file: `pages/06_YourModule_Dashboard.py`**

**Use the templates provided in the previous sections.**

### Step 4: Add Sample Data

**Create a data population script: `populate_your_module_data.py`**

```python
import random
import datetime as dt
from src.db import get_conn

def populate_your_module_data():
    """Populate your module with sample data."""
    
    conn = get_conn()
    
    # Clear existing data
    conn.execute("DELETE FROM your_module_items")
    conn.execute("DELETE FROM your_module_categories")
    
    # Insert categories
    categories = [
        ("Category 1", "CAT001", "Description for Category 1"),
        ("Category 2", "CAT002", "Description for Category 2"),
        ("Category 3", "CAT003", "Description for Category 3"),
        ("Category 4", "CAT004", "Description for Category 4"),
        ("Category 5", "CAT005", "Description for Category 5")
    ]
    
    for cat_name, cat_code, description in categories:
        conn.execute(
            "INSERT INTO your_module_categories (category_name, category_code, description) VALUES (?, ?, ?)",
            (cat_name, cat_code, description)
        )
    
    # Insert sample items
    statuses = ['Draft', 'Submitted', 'Approved', 'Completed', 'Cancelled']
    priorities = ['Low', 'Medium', 'High', 'Urgent']
    departments = [1, 2, 3, 4, 5, 6, 7, 8]  # Department IDs
    
    for i in range(100):
        item_name = f"Item {i+1}"
        category_id = random.randint(1, 5)
        dept_id = random.choice(departments)
        amount = round(random.uniform(100, 5000), 2)
        status = random.choice(statuses)
        priority = random.choice(priorities)
        
        created_date = dt.date.today() - dt.timedelta(days=random.randint(0, 90))
        completed_date = None
        if status == 'Completed':
            completed_date = created_date + dt.timedelta(days=random.randint(1, 30))
        
        conn.execute(
            """INSERT INTO your_module_items 
               (item_name, category_id, dept_id, amount, status, priority, created_date, completed_date, created_by, notes) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (item_name, category_id, dept_id, amount, status, priority, created_date, completed_date, f"User{i+1}", f"Notes for item {i+1}")
        )
    
    print("Your module data populated successfully!")

if __name__ == "__main__":
    populate_your_module_data()
```

### Step 5: Update Navigation

**Add your module to the main navigation in `app.py`:**

```python
# In the sidebar section
st.markdown("### Navigation")
st.info("Navigate to specific dashboards for detailed analytics and filtering options.")

# Add your new module
if st.button("🎯 Your Module Dashboard", use_container_width=True):
    st.switch_page("pages/06_YourModule_Dashboard.py")
```

---

## Best Practices

### 🎯 Development Workflow

**1. Start Small**
- Begin with basic KPIs
- Add one chart at a time
- Test each component before moving to the next

**2. Use Cursor's AI Assistance**
- Ask Cursor to help with SQL queries
- Use Cursor to generate chart code
- Let Cursor help with error debugging

**3. Test Frequently**
- Run the application after each change
- Check that data displays correctly
- Verify that filters work properly

### 🔧 Code Organization

**1. Follow Naming Conventions**
- Use descriptive function names
- Use consistent variable naming
- Follow the existing file structure

**2. Add Documentation**
- Include docstrings for all functions
- Add comments for complex logic
- Document any custom SQL queries

**3. Handle Errors Gracefully**
- Use try-catch blocks
- Provide meaningful error messages
- Show fallback content when data is unavailable

### 📊 SQL Best Practices

**1. Use Parameterized Queries**
```python
# Good - prevents SQL injection
sql = "SELECT * FROM table WHERE date BETWEEN :start_date AND :end_date"
conn.query(sql, params={"start_date": start_date, "end_date": end_date})

# Bad - vulnerable to SQL injection
sql = f"SELECT * FROM table WHERE date BETWEEN '{start_date}' AND '{end_date}'"
```

**2. Add Proper Indexing**
```sql
-- Add indexes for commonly queried columns
CREATE INDEX idx_table_date ON your_table(created_date);
CREATE INDEX idx_table_dept ON your_table(dept_id);
```

**3. Use COALESCE for Null Handling**
```sql
-- Handle null values gracefully
SELECT COALESCE(SUM(amount), 0) as total_amount
FROM your_table
```

### 🎨 UI Best Practices

**1. Consistent Styling**
- Use the same CSS classes across all dashboards
- Follow the established color scheme
- Maintain consistent spacing and typography

**2. Responsive Design**
- Use `use_container_width=True` for charts
- Test on different screen sizes
- Ensure mobile compatibility

**3. User Experience**
- Provide clear filter labels
- Show loading states for data fetching
- Display helpful error messages

---

## Troubleshooting

### Common Issues and Solutions

**1. Import Errors**
```
Error: ModuleNotFoundError: No module named 'src'
```
**Solution:** Ensure you're running from the correct directory (`data-viz-app/`)

**2. Database Connection Issues**
```
Error: Database connection failed
```
**Solution:** Check your `.streamlit/secrets.toml` file and database credentials

**3. SQL Syntax Errors**
```
Error: syntax error at or near "WHERE"
```
**Solution:** Use Cursor to help debug SQL queries, check for missing commas or quotes

**4. Chart Display Issues**
```
Error: 'x' is not the name of a column
```
**Solution:** Verify that the column names in your data match what you're using in the chart

**5. Caching Issues**
```
Error: Data not updating after changes
```
**Solution:** Clear Streamlit cache by pressing 'C' in the app or restart the application

### Getting Help

**1. Use Cursor's AI**
- Ask Cursor to explain error messages
- Use Cursor to generate code templates
- Let Cursor help debug issues

**2. Check Existing Code**
- Look at similar functions in existing files
- Copy patterns from working dashboards
- Follow the established code structure

**3. Test Incrementally**
- Add one feature at a time
- Test each change before adding the next
- Use print statements to debug data flow

---

## 🎉 Conclusion

This guide provides a comprehensive framework for extending the Reflexta Analytics application. By following these steps and best practices, you can:

- ✅ **Create new dashboards** with professional styling
- ✅ **Add new KPIs** with growth calculations
- ✅ **Build new reports** with detailed data views
- ✅ **Add new modules** with complete functionality
- ✅ **Maintain code quality** and consistency
- ✅ **Troubleshoot issues** effectively

Remember to:
- 🎯 **Start small** and build incrementally
- 🤖 **Use Cursor's AI** for assistance
- 🧪 **Test frequently** to catch issues early
- 📚 **Follow existing patterns** for consistency
- 🔧 **Ask for help** when needed

Happy coding! 🚀
