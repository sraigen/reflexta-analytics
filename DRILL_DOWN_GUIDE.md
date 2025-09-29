# 🔍 Plotly Drill-Down Capabilities Guide

## 📋 **Overview**

Plotly drill-down capabilities allow users to interact with charts by clicking on elements to see more detailed information or navigate to different levels of data granularity. This guide explains how to implement and use these features in the Reflexta Analytics Platform.

---

## 🎯 **What is Drill-Down?**

**Drill-down** is an interactive feature that allows users to:
- **Click on chart elements** (bars, pie slices, data points) to see detailed information
- **Navigate through data hierarchies** (department → sub-department → individual transactions)
- **Filter related charts** by clicking on one chart element
- **Explore data at different levels** of granularity

---

## 🚀 **Types of Drill-Down Features**

### **1. Hierarchical Drill-Down**
Click on a high-level element to see its components:

**Example: Department → Sub-Department → Transactions**
```
🏢 Finance Department
  ├── 💰 Budget Management
  │   ├── Transaction 1: $5,000
  │   ├── Transaction 2: $3,200
  │   └── Transaction 3: $1,800
  ├── 📊 Financial Reporting
  │   ├── Transaction 4: $2,100
  │   └── Transaction 5: $1,500
  └── 💳 Accounts Payable
      ├── Transaction 6: $4,200
      └── Transaction 7: $2,800
```

### **2. Temporal Drill-Down**
Click on a time period to see more detailed time breakdowns:

**Example: Year → Quarter → Month → Day**
```
📅 2024
  ├── Q1 (Jan-Mar)
  │   ├── January: $50,000
  │   ├── February: $45,000
  │   └── March: $55,000
  ├── Q2 (Apr-Jun)
  │   ├── April: $60,000
  │   ├── May: $65,000
  │   └── June: $70,000
  └── Q3 (Jul-Sep)
      ├── July: $75,000
      ├── August: $80,000
      └── September: $85,000
```

### **3. Cross-Chart Filtering**
Click on one chart to filter all other charts on the same page:

**Example: Click on "Finance" department**
- Department chart shows Finance selected
- Monthly trend chart filters to Finance data only
- Vendor chart shows only Finance vendors
- Category chart shows only Finance categories

---

## 🛠️ **Implementation Examples**

### **Example 1: Department Spending Drill-Down**

```python
def create_department_drill_down(data: pd.DataFrame) -> None:
    """Create department chart with drill-down to sub-departments."""
    
    # Prepare department data
    dept_data = data.groupby('department')['amount'].sum().reset_index()
    dept_data = dept_data.sort_values('amount', ascending=False)
    
    # Create the main chart
    fig = px.bar(
        dept_data,
        x='department',
        y='amount',
        title="Department Spending Overview",
        color='amount',
        color_continuous_scale='Blues'
    )
    
    # Add click functionality
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Total: $%{y:,.0f}<br><extra></extra>",
        customdata=dept_data['department'].tolist()
    )
    
    # Configure layout for interactivity
    fig.update_layout(
        hovermode='closest',
        clickmode='event+select',
        height=500
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True, key="dept_chart")
    
    # Handle drill-down
    if st.session_state.get('dept_chart_click'):
        clicked_data = st.session_state['dept_chart_click']
        if clicked_data and 'points' in clicked_data:
            point = clicked_data['points'][0]
            selected_dept = point.get('x', '')
            
            # Show sub-department breakdown
            filtered_data = data[data['department'] == selected_dept]
            sub_dept_data = filtered_data.groupby('sub_department')['amount'].sum().reset_index()
            
            # Create sub-department chart
            sub_fig = px.bar(
                sub_dept_data,
                x='sub_department',
                y='amount',
                title=f"Sub-Departments in {selected_dept}",
                color='amount',
                color_continuous_scale='Greens'
            )
            
            st.plotly_chart(sub_fig, use_container_width=True)
```

### **Example 2: Monthly Trends Drill-Down**

```python
def create_monthly_drill_down(data: pd.DataFrame) -> None:
    """Create monthly chart with drill-down to daily data."""
    
    # Prepare monthly data
    data['month'] = pd.to_datetime(data['date']).dt.to_period('M')
    monthly_data = data.groupby('month')['amount'].sum().reset_index()
    monthly_data['month_str'] = monthly_data['month'].astype(str)
    
    # Create the main chart
    fig = px.line(
        monthly_data,
        x='month_str',
        y='amount',
        title="Monthly Spending Trends",
        markers=True,
        line_shape='spline'
    )
    
    # Add click functionality
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Total: $%{y:,.0f}<br><extra></extra>",
        customdata=monthly_data['month'].tolist()
    )
    
    # Configure layout
    fig.update_layout(
        hovermode='closest',
        clickmode='event+select',
        height=500
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True, key="monthly_chart")
    
    # Handle drill-down
    if st.session_state.get('monthly_chart_click'):
        clicked_data = st.session_state['monthly_chart_click']
        if clicked_data and 'points' in clicked_data:
            point = clicked_data['points'][0]
            selected_month = point.get('x', '')
            
            # Show daily breakdown
            month_data = data[pd.to_datetime(data['date']).dt.to_period('M').astype(str) == selected_month]
            daily_data = month_data.groupby(pd.to_datetime(month_data['date']).dt.date)['amount'].sum().reset_index()
            
            # Create daily chart
            daily_fig = px.bar(
                daily_data,
                x='date',
                y='amount',
                title=f"Daily Spending for {selected_month}",
                color='amount',
                color_continuous_scale='Oranges'
            )
            
            st.plotly_chart(daily_fig, use_container_width=True)
```

### **Example 3: Cross-Chart Filtering**

```python
def create_cross_chart_filtering(data: pd.DataFrame) -> None:
    """Create multiple charts that filter each other."""
    
    # Initialize session state for filters
    if 'cross_filter' not in st.session_state:
        st.session_state['cross_filter'] = {}
    
    # Create filter controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏢 Filter by Department"):
            st.session_state['cross_filter']['type'] = 'department'
    
    with col2:
        if st.button("📅 Filter by Month"):
            st.session_state['cross_filter']['type'] = 'month'
    
    with col3:
        if st.button("🔄 Clear Filters"):
            st.session_state['cross_filter'] = {}
            st.rerun()
    
    # Apply filters to data
    filtered_data = data.copy()
    
    if st.session_state['cross_filter'].get('type') == 'department':
        selected_dept = st.selectbox(
            "Select Department",
            data['department'].unique(),
            key="dept_filter"
        )
        filtered_data = filtered_data[filtered_data['department'] == selected_dept]
    
    # Show filtered charts
    if not filtered_data.empty:
        # Department chart
        dept_data = filtered_data.groupby('department')['amount'].sum().reset_index()
        dept_fig = px.bar(dept_data, x='department', y='amount', title="Department Spending (Filtered)")
        st.plotly_chart(dept_fig, use_container_width=True)
        
        # Category chart
        category_data = filtered_data.groupby('category')['amount'].sum().reset_index()
        category_fig = px.pie(category_data, values='amount', names='category', title="Category Breakdown (Filtered)")
        st.plotly_chart(category_fig, use_container_width=True)
```

---

## 🎨 **Visual Design for Drill-Down**

### **Color Coding**
- **Main Chart**: Use primary colors (blues, purples)
- **Drill-Down Chart**: Use secondary colors (greens, oranges, reds)
- **Selected Element**: Use accent colors to highlight selection

### **Hover Effects**
```python
# Add professional hover effects
fig.update_traces(
    hovertemplate="<b>%{x}</b><br>Total: $%{y:,.0f}<br><extra></extra>",
    customdata=data['department'].tolist()
)
```

### **Click Indicators**
```python
# Add click functionality
fig.update_layout(
    hovermode='closest',
    clickmode='event+select',
    height=500
)
```

---

## 🔧 **Technical Implementation**

### **1. Chart Configuration**
```python
# Configure chart for interactivity
fig.update_layout(
    hovermode='closest',        # Show closest point on hover
    clickmode='event+select',   # Enable click events
    height=500,                 # Set chart height
    showlegend=False            # Hide legend if not needed
)
```

### **2. Click Event Handling**
```python
# Handle click events
if st.session_state.get('chart_click'):
    clicked_data = st.session_state['chart_click']
    if clicked_data and 'points' in clicked_data:
        point = clicked_data['points'][0]
        selected_value = point.get('x', point.get('label', ''))
        selected_amount = point.get('y', 0)
        
        # Process the click event
        process_drill_down(selected_value, selected_amount)
```

### **3. Data Filtering**
```python
# Filter data based on selection
def filter_data_by_selection(data: pd.DataFrame, selection: str, filter_type: str) -> pd.DataFrame:
    """Filter data based on user selection."""
    
    if filter_type == 'department':
        return data[data['department'] == selection]
    elif filter_type == 'month':
        return data[pd.to_datetime(data['date']).dt.to_period('M').astype(str) == selection]
    elif filter_type == 'vendor':
        return data[data['vendor_name'] == selection]
    elif filter_type == 'category':
        return data[data['category'] == selection]
    
    return data
```

---

## 📊 **Use Cases in Reflexta Platform**

### **1. Finance Dashboard**
- **Department Drill-Down**: Click on Finance → see Finance sub-departments
- **Monthly Drill-Down**: Click on January → see daily transactions
- **Category Drill-Down**: Click on "Office Supplies" → see specific items

### **2. Procurement Dashboard**
- **Vendor Drill-Down**: Click on a vendor → see their order history
- **Category Drill-Down**: Click on "IT Equipment" → see specific purchases
- **Order Drill-Down**: Click on an order → see order details

### **3. Analytics Dashboard**
- **Cross-Chart Filtering**: Click on a department → filter all charts
- **Temporal Analysis**: Click on a quarter → see monthly breakdown
- **Performance Metrics**: Click on a KPI → see contributing factors

---

## 🎯 **Best Practices**

### **1. User Experience**
- **Clear Visual Cues**: Use colors and animations to indicate clickable elements
- **Consistent Behavior**: All drill-down features should work similarly
- **Easy Navigation**: Provide "Back" buttons and clear hierarchy
- **Loading States**: Show spinners during data processing

### **2. Performance**
- **Data Caching**: Cache drill-down data to improve performance
- **Lazy Loading**: Load detailed data only when needed
- **Efficient Queries**: Optimize database queries for drill-down data
- **Memory Management**: Clear unused data from session state

### **3. Error Handling**
- **Empty States**: Handle cases where no data is available
- **Error Messages**: Show helpful error messages for failed drill-downs
- **Fallback Options**: Provide alternative views when drill-down fails
- **Data Validation**: Validate data before processing drill-downs

---

## 🚀 **Advanced Features**

### **1. Multi-Level Drill-Down**
```python
def create_multi_level_drill_down(data: pd.DataFrame) -> None:
    """Create drill-down with multiple levels."""
    
    # Level 1: Department
    dept_data = data.groupby('department')['amount'].sum().reset_index()
    dept_fig = px.bar(dept_data, x='department', y='amount')
    st.plotly_chart(dept_fig, use_container_width=True, key="level1")
    
    # Level 2: Sub-Department (if department selected)
    if st.session_state.get('level1_click'):
        selected_dept = get_selected_department()
        sub_dept_data = data[data['department'] == selected_dept].groupby('sub_department')['amount'].sum().reset_index()
        sub_dept_fig = px.bar(sub_dept_data, x='sub_department', y='amount')
        st.plotly_chart(sub_dept_fig, use_container_width=True, key="level2")
        
        # Level 3: Individual Transactions (if sub-department selected)
        if st.session_state.get('level2_click'):
            selected_sub_dept = get_selected_sub_department()
            transaction_data = data[(data['department'] == selected_dept) & 
                                  (data['sub_department'] == selected_sub_dept)]
            st.dataframe(transaction_data)
```

### **2. Dynamic Drill-Down**
```python
def create_dynamic_drill_down(data: pd.DataFrame) -> None:
    """Create drill-down that adapts to data structure."""
    
    # Analyze data structure
    available_levels = analyze_data_hierarchy(data)
    
    # Create drill-down based on available levels
    for level in available_levels:
        level_data = data.groupby(level)['amount'].sum().reset_index()
        level_fig = px.bar(level_data, x=level, y='amount')
        st.plotly_chart(level_fig, use_container_width=True, key=f"level_{level}")
```

### **3. Interactive Filters**
```python
def create_interactive_filters(data: pd.DataFrame) -> None:
    """Create interactive filters that work with drill-down."""
    
    # Create filter controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        department_filter = st.selectbox("Department", data['department'].unique())
    
    with col2:
        date_range = st.date_input("Date Range", value=[data['date'].min(), data['date'].max()])
    
    with col3:
        amount_range = st.slider("Amount Range", 
                                float(data['amount'].min()), 
                                float(data['amount'].max()),
                                (float(data['amount'].min()), float(data['amount'].max())))
    
    # Apply filters
    filtered_data = data[
        (data['department'] == department_filter) &
        (data['date'] >= date_range[0]) &
        (data['date'] <= date_range[1]) &
        (data['amount'] >= amount_range[0]) &
        (data['amount'] <= amount_range[1])
    ]
    
    # Create drill-down charts with filtered data
    create_drill_down_charts(filtered_data)
```

---

## 📋 **Implementation Checklist**

### **Before Implementation**
- [ ] Define drill-down hierarchy and levels
- [ ] Identify clickable elements and interactions
- [ ] Plan data filtering and processing logic
- [ ] Design visual feedback and user experience

### **During Implementation**
- [ ] Configure chart interactivity settings
- [ ] Implement click event handling
- [ ] Add data filtering and processing
- [ ] Create visual feedback and animations
- [ ] Test all drill-down scenarios

### **After Implementation**
- [ ] Test performance with large datasets
- [ ] Validate user experience and navigation
- [ ] Check error handling and edge cases
- [ ] Optimize queries and data processing
- [ ] Document usage and maintenance

---

## 🎪 **Demo Scenarios**

### **Scenario 1: Department Analysis**
1. **Start**: Show department spending overview
2. **Click**: Click on "Finance" department
3. **Drill-Down**: Show Finance sub-departments
4. **Click**: Click on "Budget Management"
5. **Details**: Show individual transactions

### **Scenario 2: Monthly Trends**
1. **Start**: Show monthly spending trends
2. **Click**: Click on "January 2024"
3. **Drill-Down**: Show daily spending for January
4. **Click**: Click on a specific day
5. **Details**: Show transactions for that day

### **Scenario 3: Vendor Performance**
1. **Start**: Show top vendors by spend
2. **Click**: Click on a specific vendor
3. **Drill-Down**: Show vendor order history
4. **Click**: Click on a specific order
5. **Details**: Show order line items

---

## 🔧 **Troubleshooting**

### **Common Issues**
1. **Charts not responding to clicks**: Check `clickmode='event+select'` setting
2. **Data not filtering**: Verify session state and data processing logic
3. **Performance issues**: Implement data caching and query optimization
4. **Visual feedback missing**: Add hover effects and click indicators

### **Debug Tips**
1. **Check session state**: Use `st.write(st.session_state)` to debug
2. **Verify data structure**: Ensure data has required columns
3. **Test click events**: Add logging to track click events
4. **Monitor performance**: Use `st.time()` to measure processing time

---

*This guide provides comprehensive information about implementing and using Plotly drill-down capabilities in the Reflexta Analytics Platform. For technical implementation details, refer to the source code examples.*
