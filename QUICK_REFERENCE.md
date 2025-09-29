# 🚀 Quick Reference Card

## 📋 Common Tasks

### Creating a New Dashboard
1. **Create file**: `pages/06_YourModule_Dashboard.py`
2. **Copy template** from existing dashboard
3. **Update header** with your module name
4. **Add navigation** in `app.py` sidebar
5. **Test** by running the application

### Adding New KPIs
1. **Create query function** in `src/your_module_queries.py`
2. **Add KPI display** in dashboard using `st.metric()`
3. **Include growth calculations** for delta values
4. **Test** with sample data

### Building New Reports
1. **Create report query** in `src/your_module_queries.py`
2. **Add report section** in dashboard using `st.dataframe()`
3. **Configure columns** with proper formatting
4. **Test** data display

### Adding New Modules
1. **Create database tables** in `database/schema.sql`
2. **Create query file** `src/your_module_queries.py`
3. **Create chart file** `src/your_module_charts.py`
4. **Create dashboard file** `pages/06_YourModule_Dashboard.py`
5. **Add sample data** with population script
6. **Update navigation** in `app.py`

## 🔧 Essential Code Patterns

### Query Function Template
```python
@st.cache_data(ttl=60, show_spinner=False)
def get_your_data(from_dt: dt.date, to_dt: dt.date, dept_id: Optional[int] = None) -> pd.DataFrame:
    """Get data for your module."""
    
    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if dept_id:
        where_dept = " AND dept_id = :dept_id"
        params["dept_id"] = dept_id
    
    sql = f"""
    SELECT column1, column2, column3
    FROM your_table
    WHERE date_column BETWEEN :from_dt AND :to_dt
        {where_dept}
    ORDER BY date_column DESC
    """
    
    conn = get_conn()
    return conn.query(sql, params=params)
```

### Chart Function Template
```python
def your_chart(df: pd.DataFrame) -> go.Figure:
    """Create a chart for your data."""
    
    if df.empty:
        return go.Figure()
    
    fig = px.bar(
        df,
        x='category',
        y='amount',
        title="Your Chart Title",
        labels={'amount': 'Amount ($)', 'category': 'Category'}
    )
    
    fig.update_layout(height=500)
    return fig
```

### KPI Display Template
```python
# Display KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Items", 
        value=f"{row['total_items']:,.0f}", 
        delta=f"{row['item_growth']:,.0f}"
    )
```

### Report Display Template
```python
# Display report
st.dataframe(
    data,
    hide_index=True,
    use_container_width=True,
    column_config={
        "amount": st.column_config.NumberColumn("Amount", format="$%.2f"),
        "date": "Date",
        "status": "Status"
    }
)
```

## 🎨 CSS Classes Reference

### Header Styling
```css
.your-module-header {
    background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
    color: white;
    padding: 2.5rem 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    border: 1px solid rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
}
```

### Section Header
```css
.section-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1.2rem 2rem;
    border-radius: 10px;
    margin: 2rem 0 1.5rem 0;
    font-size: 1.4rem;
    font-weight: 600;
}
```

## 🐛 Common Issues & Solutions

### Import Errors
- **Issue**: `ModuleNotFoundError: No module named 'src'`
- **Solution**: Run from `data-viz-app/` directory

### Database Connection
- **Issue**: `Database connection failed`
- **Solution**: Check `.streamlit/secrets.toml` file

### SQL Errors
- **Issue**: `syntax error at or near "WHERE"`
- **Solution**: Use Cursor to debug SQL, check for missing commas

### Chart Issues
- **Issue**: `'x' is not the name of a column`
- **Solution**: Verify column names match your data

### Caching Issues
- **Issue**: Data not updating
- **Solution**: Press 'C' in app or restart application

## 📚 File Structure Reminder

```
data-viz-app/
├── app.py                          # Main application
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

## 🎯 Development Checklist

### Before Starting
- [ ] Plan your module purpose and data needs
- [ ] Identify required KPIs and reports
- [ ] Design database tables and relationships
- [ ] Create sample data for testing

### During Development
- [ ] Create query functions with proper error handling
- [ ] Add chart functions with consistent styling
- [ ] Create dashboard with professional UI
- [ ] Test each component individually
- [ ] Add proper documentation and comments

### Before Deployment
- [ ] Test all functionality thoroughly
- [ ] Verify data accuracy and performance
- [ ] Check for any console errors
- [ ] Ensure responsive design works
- [ ] Update navigation and documentation

## 🚀 Quick Start Commands

### Run Application
```bash
cd data-viz-app
streamlit run app.py
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Clear Cache
- Press 'C' in the Streamlit app
- Or restart the application

### Check Database Connection
- Look for "Database connection failed" errors
- Check `.streamlit/secrets.toml` file
- Verify database credentials

---

**Remember**: Start small, test frequently, and use Cursor's AI assistance! 🎉
