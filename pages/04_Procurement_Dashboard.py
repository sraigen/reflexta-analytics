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

# Render global AI chat
from src.global_ai_chat import render_global_ai_chat
render_global_ai_chat()