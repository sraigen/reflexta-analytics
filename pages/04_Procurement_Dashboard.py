from __future__ import annotations

import datetime as dt

import streamlit as st

from src.db import health_check
from src.procurement_queries import (
    get_procurement_summary,
    get_procurement_kpis,
    get_vendor_performance,
    get_category_analysis,
    get_procurement_trends,
    get_pending_orders,
    get_delivery_performance,
    get_spend_analysis
)
from src.procurement_charts import (
    vendor_performance_chart,
    procurement_trends_chart,
    category_spending_pie,
    department_procurement_chart,
    delivery_performance_chart,
    procurement_kpi_gauge,
    procurement_heatmap,
    order_status_distribution,
    priority_analysis_chart
)
from src.ui import empty_state

st.set_page_config(page_title="Procurement Dashboard", layout="wide")

# Procurement Dashboard Filters - Sidebar Approach
with st.sidebar:
    st.markdown("### 🔧 Procurement Filters")
    
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

    department = st.selectbox(
        "Department",
        options=["All", "Finance", "Procurement", "IT", "HR", "Operations", "Marketing", "Sales", "Legal"],
        help="Filter by specific department"
    )

    order_status = st.selectbox(
        "Order Status",
        options=["All", "Pending", "Approved", "In Progress", "Completed", "Cancelled"],
        help="Filter by order status"
    )

    # Additional filters
    st.markdown("**Additional Filters**")
    
    vendor = st.selectbox(
        "Vendor",
        options=["All"] + [f"Vendor {i}" for i in range(1, 11)],
        help="Filter by specific vendor"
    )

    category = st.selectbox(
        "Category",
        options=["All", "Office Supplies", "IT Equipment", "Marketing", "Travel", "Utilities", "Professional Services", "Equipment", "Software", "Consulting", "Training"],
        help="Filter by category"
    )

    priority = st.selectbox(
        "Priority",
        options=["All", "Low", "Medium", "High", "Urgent"],
        help="Filter by priority level"
    )

    # Get department ID if specific department is selected
    dept_id = None
    if department != "All":
        dept_mapping = {
            "Finance": 1, "Procurement": 2, "IT": 3, "HR": 4, "Operations": 5,
            "Marketing": 6, "Sales": 7, "Legal": 8
        }
        dept_id = dept_mapping.get(department)


# Professional CSS for Procurement Dashboard
st.markdown("""
<style>
    .procurement-header {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .procurement-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .procurement-header h1 {
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
    
    .procurement-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    .section-header {
        background: linear-gradient(90deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        padding: 0.8rem 1.2rem;
        margin: 1.5rem 0 1rem 0;
        border-radius: 6px;
        font-weight: 500;
        font-size: 1.1rem;
        border-left: 4px solid #e74c3c;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid #dee2e6;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 0.5rem;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-change {
        font-size: 0.8rem;
        margin-top: 0.5rem;
        padding: 0.2rem 0.5rem;
        border-radius: 4px;
        font-weight: 500;
    }
    
    .metric-change.positive {
        background-color: #d4edda;
        color: #155724;
    }
    
    .metric-change.negative {
        background-color: #f8d7da;
        color: #721c24;
    }
    
    /* Dark mode compatibility */
    .stApp[data-theme="dark"] .procurement-header {
        background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .procurement-header h1 {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .procurement-header p {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    .stApp[data-theme="dark"] .section-header {
        background: linear-gradient(90deg, #e74c3c 0%, #c0392b 100%);
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .metric-card {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
        border: 1px solid #4a5568;
        color: white;
    }
    
    .stApp[data-theme="dark"] .metric-value {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .metric-label {
        color: rgba(255, 255, 255, 0.8) !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="procurement-header">
    <h1>🛒 Procurement Dashboard</h1>
    <p>Comprehensive Procurement Analytics & Vendor Performance</p>
</div>
""", unsafe_allow_html=True)

if not health_check():
    st.error("Database connection failed. Please check your connection settings.")
    st.stop()

try:
    # Procurement KPIs
    st.markdown('<div class="section-header">Key Procurement Metrics</div>', unsafe_allow_html=True)
    
    kpis = get_procurement_kpis(from_date, to_date, dept_id)
    if not kpis.empty:
        row = kpis.iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Orders",
                value=f"{row['total_orders']:,}" if row['total_orders'] else "0",
                delta=f"{row['order_growth']:,}" if row['order_growth'] else None
            )
        
        with col2:
            st.metric(
                label="Total Spend",
                value=f"${row['total_spend']:,.2f}" if row['total_spend'] else "$0.00",
                delta=f"${row['spend_growth']:,.2f}" if row['spend_growth'] else None
            )
        
        with col3:
            st.metric(
                label="Average Order Value",
                value=f"${row['avg_order_value']:,.2f}" if row['avg_order_value'] else "$0.00",
                delta=f"${row['aov_growth']:,.2f}" if row['aov_growth'] else None
            )
        
        with col4:
            st.metric(
                label="Active Vendors",
                value=f"{row['active_vendors']:,}" if row['active_vendors'] else "0",
                delta=f"{row['vendor_growth']:,}" if row['vendor_growth'] else None
            )
    else:
        st.warning("No procurement data available for the selected period.")
    
    # Interactive Charts with Drill-Down
    st.markdown('<div class="section-header">Interactive Analytics</div>', unsafe_allow_html=True)
    
    if not procurement_data.empty:
        # Create tabs for different chart types
        tab1, tab2, tab3 = st.tabs([
            "🏪 Vendor Analysis", 
            "📅 Order Trends", 
            "📊 Category Breakdown"
        ])
        
        with tab1:
            st.markdown("### Vendor Performance with Drill-Down")
            st.markdown("**Click on any vendor bar to see their order history**")
            
            # Prepare vendor data
            vendor_data = procurement_data.groupby('vendor_name').agg({
                'amount': 'sum',
                'order_id': 'count'
            }).reset_index()
            vendor_data.columns = ['vendor', 'total_spend', 'order_count']
            vendor_data = vendor_data.sort_values('total_spend', ascending=False).head(10)
            
            # Create vendor chart with drill-down
            import plotly.express as px
            import plotly.graph_objects as go
            from plotly.subplots import make_subplots
            
            # Create subplot with dual y-axes
            fig = make_subplots(
                rows=1, cols=1,
                specs=[[{"secondary_y": True}]]
            )
            
            # Add spending bars
            fig.add_trace(
                go.Bar(
                    name="Total Spend",
                    x=vendor_data['vendor'],
                    y=vendor_data['total_spend'],
                    marker_color='#e74c3c',
                    hovertemplate="<b>%{x}</b><br>Spend: $%{y:,.0f}<br><extra></extra>",
                    customdata=vendor_data['vendor'].tolist()
                ),
                secondary_y=False
            )
            
            # Add order count line
            fig.add_trace(
                go.Scatter(
                    name="Order Count",
                    x=vendor_data['vendor'],
                    y=vendor_data['order_count'],
                    mode='lines+markers',
                    line=dict(color='#27ae60', width=3),
                    marker=dict(size=8),
                    hovertemplate="<b>%{x}</b><br>Orders: %{y}<br><extra></extra>",
                    customdata=vendor_data['vendor'].tolist()
                ),
                secondary_y=True
            )
            
            # Configure layout
            fig.update_layout(
                title={
                    'text': "Top Vendors by Performance",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#1e293b'}
                },
                hovermode='closest',
                clickmode='event+select',
                height=500,
                showlegend=True
            )
            
            # Configure axes
            fig.update_xaxes(title_text="Vendor")
            fig.update_yaxes(title_text="Total Spend ($)", secondary_y=False)
            fig.update_yaxes(title_text="Order Count", secondary_y=True)
            
            # Display the chart
            st.plotly_chart(fig, use_container_width=True, key="vendor_chart")
            
            # Handle drill-down
            if st.session_state.get('vendor_chart_click'):
                clicked_data = st.session_state['vendor_chart_click']
                if clicked_data and 'points' in clicked_data:
                    point = clicked_data['points'][0]
                    selected_vendor = point.get('x', '')
                    
                    st.markdown(f"#### 🔍 Drill-Down: {selected_vendor}")
                    
                    # Filter data for selected vendor
                    vendor_orders = procurement_data[procurement_data['vendor_name'] == selected_vendor]
                    
                    if not vendor_orders.empty:
                        # Show vendor performance metrics
                        col1, col2, col3, col4 = st.columns(4)
                        
                        with col1:
                            st.metric(
                                "Total Orders",
                                len(vendor_orders),
                                delta=None
                            )
                        
                        with col2:
                            st.metric(
                                "Total Spend",
                                f"${vendor_orders['amount'].sum():,.0f}",
                                delta=None
                            )
                        
                        with col3:
                            st.metric(
                                "Average Order",
                                f"${vendor_orders['amount'].mean():,.0f}",
                                delta=None
                            )
                        
                        with col4:
                            st.metric(
                                "Largest Order",
                                f"${vendor_orders['amount'].max():,.0f}",
                                delta=None
                            )
                        
                        # Show detailed orders
                        st.markdown("#### 📋 Order Details")
                        st.dataframe(
                            vendor_orders[['date', 'order_id', 'amount', 'category', 'status']],
                            use_container_width=True
                        )
        
        with tab2:
            st.markdown("### Order Trends with Drill-Down")
            st.markdown("**Click on any month point to see daily breakdown**")
            
            # Prepare monthly data
            procurement_data['month'] = pd.to_datetime(procurement_data['date']).dt.to_period('M')
            monthly_data = procurement_data.groupby('month')['amount'].sum().reset_index()
            monthly_data['month_str'] = monthly_data['month'].astype(str)
            
            # Create monthly trend chart
            trend_fig = px.line(
                monthly_data,
                x='month_str',
                y='amount',
                title="Monthly Procurement Trends",
                markers=True,
                line_shape='spline',
                color_discrete_sequence=['#e74c3c']
            )
            
            # Add click functionality
            trend_fig.update_traces(
                hovertemplate="<b>%{x}</b><br>Total: $%{y:,.0f}<br><extra></extra>",
                customdata=monthly_data['month'].tolist()
            )
            
            # Configure layout
            trend_fig.update_layout(
                title={
                    'text': "Monthly Procurement Trends",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#1e293b'}
                },
                xaxis_title="Month",
                yaxis_title="Total Spending ($)",
                hovermode='closest',
                clickmode='event+select',
                height=500
            )
            
            # Display the chart
            st.plotly_chart(trend_fig, use_container_width=True, key="proc_trend_chart")
            
            # Handle drill-down
            if st.session_state.get('proc_trend_chart_click'):
                clicked_data = st.session_state['proc_trend_chart_click']
                if clicked_data and 'points' in clicked_data:
                    point = clicked_data['points'][0]
                    selected_month = point.get('x', '')
                    
                    st.markdown(f"#### 🔍 Drill-Down: {selected_month}")
                    
                    # Filter data for selected month
                    month_data = procurement_data[pd.to_datetime(procurement_data['date']).dt.to_period('M').astype(str) == selected_month]
                    
                    if not month_data.empty:
                        # Show daily breakdown
                        daily_data = month_data.groupby(pd.to_datetime(month_data['date']).dt.date)['amount'].sum().reset_index()
                        daily_data.columns = ['date', 'amount']
                        daily_data = daily_data.sort_values('date')
                        
                        # Create daily chart
                        daily_fig = px.bar(
                            daily_data,
                            x='date',
                            y='amount',
                            title=f"Daily Procurement for {selected_month}",
                            color='amount',
                            color_continuous_scale='Reds'
                        )
                        
                        daily_fig.update_layout(
                            height=400,
                            showlegend=False,
                            title={
                                'text': f"Daily Procurement for {selected_month}",
                                'x': 0.5,
                                'xanchor': 'center'
                            }
                        )
                        
                        st.plotly_chart(daily_fig, use_container_width=True)
        
        with tab3:
            st.markdown("### Category Breakdown with Drill-Down")
            st.markdown("**Click on any category slice to see detailed breakdown**")
            
            # Prepare category data
            category_data = procurement_data.groupby('category')['amount'].sum().reset_index()
            category_data = category_data.sort_values('amount', ascending=False)
            
            # Create category pie chart
            category_fig = px.pie(
                category_data,
                values='amount',
                names='category',
                title="Procurement by Category",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            
            # Add click functionality
            category_fig.update_traces(
                hovertemplate="<b>%{label}</b><br>Amount: $%{value:,.0f}<br>Percentage: %{percent}<br><extra></extra>",
                customdata=category_data['category'].tolist()
            )
            
            # Configure layout
            category_fig.update_layout(
                title={
                    'text': "Procurement by Category",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#1e293b'}
                },
                hovermode='closest',
                clickmode='event+select',
                height=500
            )
            
            # Display the chart
            st.plotly_chart(category_fig, use_container_width=True, key="proc_category_chart")
            
            # Handle drill-down
            if st.session_state.get('proc_category_chart_click'):
                clicked_data = st.session_state['proc_category_chart_click']
                if clicked_data and 'points' in clicked_data:
                    point = clicked_data['points'][0]
                    selected_category = point.get('label', '')
                    
                    st.markdown(f"#### 🔍 Drill-Down: {selected_category}")
                    
                    # Filter data for selected category
                    category_items = procurement_data[procurement_data['category'] == selected_category]
                    
                    if not category_items.empty:
                        # Show category summary
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric(
                                "Total Orders",
                                len(category_items),
                                delta=None
                            )
                        
                        with col2:
                            st.metric(
                                "Total Amount",
                                f"${category_items['amount'].sum():,.0f}",
                                delta=None
                            )
                        
                        with col3:
                            st.metric(
                                "Average Order",
                                f"${category_items['amount'].mean():,.0f}",
                                delta=None
                            )
                        
                        # Show detailed items
                        st.markdown("#### 📋 Order Details")
                        st.dataframe(
                            category_items[['date', 'order_id', 'amount', 'vendor_name', 'status']],
                            use_container_width=True
                        )

    # Vendor Performance Analysis
    st.markdown('<div class="section-header">Vendor Performance Analysis</div>', unsafe_allow_html=True)
    
    vendor_data = get_vendor_performance(from_date, to_date, dept_id)
    if not empty_state(vendor_data):
        st.plotly_chart(
            vendor_performance_chart(vendor_data),
            use_container_width=True
        )
    else:
        st.info("No vendor performance data available for the selected period.")
    
    # Procurement Trends
    st.markdown('<div class="section-header">Procurement Trends</div>', unsafe_allow_html=True)
    
    trends_data = get_procurement_trends(from_date, to_date, dept_id)
    if not empty_state(trends_data):
        st.plotly_chart(
            procurement_trends_chart(trends_data),
            use_container_width=True
        )
    else:
        st.info("No trend data available for the selected period.")
    
    # Category Analysis
    st.markdown('<div class="section-header">Spending by Category</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Category Distribution")
        category_data = get_category_analysis(from_date, to_date, dept_id)
        if not empty_state(category_data):
            st.plotly_chart(
                category_spending_pie(category_data),
                use_container_width=True
            )
        else:
            st.info("No category data available.")
    
    with col2:
        st.markdown("#### Department Procurement")
        dept_data = get_spend_analysis(from_date, to_date, dept_id)
        if not empty_state(dept_data):
            st.plotly_chart(
                department_procurement_chart(dept_data),
                use_container_width=True
            )
        else:
            st.info("No department data available.")
    
    # Delivery Performance
    st.markdown('<div class="section-header">Delivery Performance</div>', unsafe_allow_html=True)
    
    delivery_data = get_delivery_performance(from_date, to_date, dept_id)
    if not empty_state(delivery_data):
        st.plotly_chart(
            delivery_performance_chart(delivery_data),
            use_container_width=True
        )
    else:
        st.info("No delivery performance data available for the selected period.")
    
    # Order Status Distribution
    st.markdown('<div class="section-header">Order Status Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Order Status Distribution")
        status_data = get_pending_orders(from_date, to_date, dept_id)
        if not empty_state(status_data):
            st.plotly_chart(
                order_status_distribution(status_data),
                use_container_width=True
            )
        else:
            st.info("No order status data available.")
    
    with col2:
        st.markdown("#### Priority Analysis")
        priority_data = get_pending_orders(from_date, to_date, dept_id)
        if not empty_state(priority_data):
            st.plotly_chart(
                priority_analysis_chart(priority_data),
                use_container_width=True
            )
        else:
            st.info("No priority data available.")
    
    # Procurement Summary Table
    st.markdown('<div class="section-header">Procurement Summary</div>', unsafe_allow_html=True)
    
    summary_data = get_procurement_summary(from_date, to_date, dept_id)
    if not empty_state(summary_data):
        st.dataframe(
            summary_data,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No summary data available for the selected period.")

except Exception as e:
    st.error(f"Error loading procurement data: {str(e)}")
    st.info("Please check your database connection and try again.")

# Render sidebar AI chat
from src.sidebar_ai_chat import render_sidebar_ai_chat
render_sidebar_ai_chat()