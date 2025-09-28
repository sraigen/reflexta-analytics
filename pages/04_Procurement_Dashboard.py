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

# Professional CSS for Procurement Dashboard
st.markdown("""
<style>
    .procurement-header {
        background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
        padding: 2rem 1rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        border: 1px solid #34495e;
    }
    
    .procurement-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    .procurement-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 300;
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
        color: #ecf0f1 !important;
    }
    
    .stApp[data-theme="dark"] .sidebar-logo {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .sidebar-logo h3 {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .sidebar-logo p {
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    .section-header {
        background: linear-gradient(90deg, #34495e 0%, #2c3e50 100%);
        padding: 0.8rem 1rem;
        border-radius: 6px;
        color: white;
        margin: 1.5rem 0 1rem 0;
        font-weight: 500;
        font-size: 1.1rem;
        border-left: 4px solid #3498db;
    }
</style>
""", unsafe_allow_html=True)

# Professional header with company branding
try:
    import base64
    with open("logo.png", "rb") as logo_file:
        logo_base64 = base64.b64encode(logo_file.read()).decode()
    
    st.markdown(f"""
    <div class="procurement-header">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
            <img src="data:image/png;base64,{logo_base64}" alt="Reflexta Data Intelligence" class="company-logo" style="height: 60px; margin-right: 25px; vertical-align: middle;">
            <div style="text-align: left;">
                <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700; line-height: 1.2;">Procurement Dashboard</h1>
                <p style="margin: 0.3rem 0 0 0; font-size: 1.1rem; opacity: 0.9; font-weight: 300;">Reflexta Data Intelligence</p>
            </div>
        </div>
        <p style="margin: 0; text-align: center; font-size: 1rem; opacity: 0.9;">Comprehensive procurement analytics and vendor management</p>
    </div>
    """, unsafe_allow_html=True)
except FileNotFoundError:
    st.markdown("""
    <div class="procurement-header">
        <h1>Procurement Dashboard</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9; font-weight: 300;">Reflexta Data Intelligence</p>
        <p>Comprehensive procurement analytics and vendor management</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar filters
with st.sidebar:
    # Company logo in sidebar
    try:
        with open("logo.png", "rb") as logo_file:
            logo_base64 = base64.b64encode(logo_file.read()).decode()
        
        st.markdown(f"""
        <div class="sidebar-logo">
            <img src="data:image/png;base64,{logo_base64}" alt="Reflexta Data Intelligence" style="height: 40px; margin-bottom: 0.5rem;">
            <h3>Reflexta Data Intelligence</h3>
            <p>Procurement Analytics</p>
        </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown("""
        <div class="sidebar-logo">
            <h3>Reflexta Data Intelligence</h3>
            <p>Procurement Analytics</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### Procurement Filters")
    st.markdown("---")
    
    today = dt.date.today()
    default_from = today - dt.timedelta(days=90)
    
    st.markdown("**Date Range**")
    from_dt = st.date_input("From Date", value=default_from, key="proc_from")
    to_dt = st.date_input("To Date", value=today, key="proc_to")
    
    st.markdown("**Department**")
    dept_options = ["All", "Finance", "Procurement", "IT", "HR", "Operations", "Marketing", "Sales", "Legal"]
    selected_dept = st.selectbox("Select Department", dept_options, key="proc_dept")
    
    st.markdown("**Vendor**")
    vendor_options = ["All", "TechCorp Solutions", "Office Supplies Inc", "Consulting Partners", 
                     "Software Systems Ltd", "Logistics Pro", "Marketing Agency", "Legal Associates", 
                     "HR Services Co", "Equipment Rentals", "Security Solutions"]
    selected_vendor = st.selectbox("Select Vendor", vendor_options, key="proc_vendor")
    
    st.markdown("**Category**")
    category_options = ["All", "Software", "Hardware", "Services", "Office Supplies", "Raw Materials",
                       "Equipment", "Marketing", "Travel", "Training", "Maintenance"]
    selected_category = st.selectbox("Select Category", category_options, key="proc_category")
    
    st.markdown("**Order Status**")
    status_options = ["All", "Draft", "Submitted", "Approved", "Rejected", "Ordered", "Received", "Closed", "Cancelled"]
    selected_status = st.selectbox("Order Status", status_options, key="proc_status")
    
    st.markdown("**Priority**")
    priority_options = ["All", "Low", "Medium", "High", "Urgent"]
    selected_priority = st.selectbox("Order Priority", priority_options, key="proc_priority")
    
    st.markdown("**Order Value Range**")
    value_range = st.slider(
        "Order Value Range ($)",
        min_value=0,
        max_value=200000,
        value=(0, 200000),
        step=5000,
        key="proc_value_range"
    )
    
    st.markdown("**Vendor Rating**")
    rating_range = st.slider(
        "Minimum Vendor Rating",
        min_value=1.0,
        max_value=5.0,
        value=1.0,
        step=0.1,
        key="proc_rating"
    )
    
    st.markdown("**Group By**")
    group_by = st.selectbox("Trend Grouping", ["month", "quarter", "week"], key="proc_group")
    
    st.markdown("---")
    st.markdown("### Quick Actions")
    if st.button("Refresh Data", use_container_width=True, key="proc_refresh"):
        st.rerun()
    
    if st.button("Export Report", use_container_width=True, key="proc_export"):
        st.success("Procurement report export feature coming soon!")
    
    st.markdown("---")
    st.markdown("### Procurement Info")
    st.info("Analyze vendor performance, category spending, and delivery metrics.")

if not health_check():
    st.error("Database connection failed. Please check your connection settings.")
    st.stop()

try:
    # Get department ID if specific department is selected
    dept_id = None
    if selected_dept != "All":
        dept_mapping = {
            "Finance": 1, "Procurement": 2, "IT": 3, "HR": 4, "Operations": 5,
            "Marketing": 6, "Sales": 7, "Legal": 8
        }
        dept_id = dept_mapping.get(selected_dept)
    
    # Process other filters
    vendor_id = None
    if selected_vendor != "All":
        vendor_mapping = {
            "TechCorp Solutions": 1, "Office Supplies Inc": 2, "Consulting Partners": 3,
            "Software Systems Ltd": 4, "Logistics Pro": 5, "Marketing Agency": 6,
            "Legal Associates": 7, "HR Services Co": 8, "Equipment Rentals": 9, "Security Solutions": 10
        }
        vendor_id = vendor_mapping.get(selected_vendor)
    
    category_id = None
    if selected_category != "All":
        category_mapping = {
            "Software": 1, "Hardware": 2, "Services": 3, "Office Supplies": 4, "Raw Materials": 5,
            "Equipment": 6, "Marketing": 7, "Travel": 8, "Training": 9, "Maintenance": 10
        }
        category_id = category_mapping.get(selected_category)
    
    status = selected_status if selected_status != "All" else None
    priority = selected_priority if selected_priority != "All" else None
    min_value, max_value = value_range
    min_rating = rating_range
    
    # Procurement KPIs
    st.markdown('<div class="section-header">Key Procurement Metrics</div>', unsafe_allow_html=True)
    
    kpis = get_procurement_kpis(from_dt, to_dt, dept_id)
    if not kpis.empty:
        row = kpis.iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Orders", 
                f"{int(row['total_orders']) if row['total_orders'] is not None else 0:,}",
                help="Total number of procurement orders"
            )
        
        with col2:
            st.metric(
                "Total Value", 
                f"${float(row['total_value']) if row['total_value'] is not None else 0:,.0f}",
                help="Total value of all orders"
            )
        
        with col3:
            st.metric(
                "Unique Vendors", 
                f"{int(row['unique_vendors']) if row['unique_vendors'] is not None else 0:,}",
                help="Number of unique vendors used"
            )
        
        with col4:
            st.metric(
                "Completed Orders", 
                f"{int(row['completed_orders']) if row['completed_orders'] is not None else 0:,}",
                help="Number of completed orders"
            )
    else:
        st.info("No procurement data available for the selected filters.")
    
    # Department Performance
    st.markdown('<div class="section-header">Department Performance</div>', unsafe_allow_html=True)
    
    dept_data = get_procurement_summary(from_dt, to_dt, dept_id)
    if not empty_state(dept_data):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### Department Procurement Performance")
            fig = department_procurement_chart(dept_data)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Department Summary")
            st.dataframe(
                dept_data,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "total_value": st.column_config.NumberColumn("Total Value ($)", format="$%.2f"),
                    "avg_order_value": st.column_config.NumberColumn("Avg Order ($)", format="$%.2f"),
                    "completion_rate": st.column_config.NumberColumn("Completion %", format="%.1f%%")
                }
            )
    else:
        st.info("No department data available for the selected filters.")
    
    # Vendor Performance
    st.markdown('<div class="section-header">Vendor Performance</div>', unsafe_allow_html=True)
    
    vendor_data = get_vendor_performance(from_dt, to_dt)
    if not empty_state(vendor_data):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### Vendor Performance Analysis")
            fig = vendor_performance_chart(vendor_data)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Top Vendors")
            top_vendors = vendor_data.head(10)
            st.dataframe(
                top_vendors,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "total_value": st.column_config.NumberColumn("Total Value ($)", format="$%.2f"),
                    "completion_rate": st.column_config.NumberColumn("Completion %", format="%.1f%%"),
                    "rating": st.column_config.NumberColumn("Rating", format="%.1f")
                }
            )
    else:
        st.info("No vendor data available for the selected filters.")
    
    # Category Analysis
    st.markdown('<div class="section-header">Category Analysis</div>', unsafe_allow_html=True)
    
    category_data = get_category_analysis(from_dt, to_dt)
    if not empty_state(category_data):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Spending by Category")
            fig = category_spending_pie(category_data)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Category Performance")
            st.dataframe(
                category_data,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "total_value": st.column_config.NumberColumn("Total Value ($)", format="$%.2f"),
                    "avg_order_value": st.column_config.NumberColumn("Avg Order ($)", format="$%.2f"),
                    "completion_rate": st.column_config.NumberColumn("Completion %", format="%.1f%%")
                }
            )
    else:
        st.info("No category data available for the selected filters.")
    
    # Procurement Trends
    st.markdown('<div class="section-header">Procurement Trends</div>', unsafe_allow_html=True)
    
    trends_data = get_procurement_trends(from_dt, to_dt, group_by)
    if not empty_state(trends_data):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"#### {group_by.title()} Procurement Trends")
            fig = procurement_trends_chart(trends_data, group_by)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Trend Summary")
            st.dataframe(
                trends_data,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "total_value": st.column_config.NumberColumn("Total Value ($)", format="$%.2f"),
                    "avg_order_value": st.column_config.NumberColumn("Avg Order ($)", format="$%.2f"),
                    "completion_rate": st.column_config.NumberColumn("Completion %", format="%.1f%%")
                }
            )
    else:
        st.info("No trend data available for the selected filters.")
    
    # Delivery Performance
    st.markdown('<div class="section-header">Delivery Performance</div>', unsafe_allow_html=True)
    
    delivery_data = get_delivery_performance(from_dt, to_dt)
    if not empty_state(delivery_data):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### Delivery Performance by Vendor")
            fig = delivery_performance_chart(delivery_data)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Delivery Metrics")
            st.dataframe(
                delivery_data,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "on_time_percentage": st.column_config.NumberColumn("On Time %", format="%.1f%%"),
                    "avg_delivery_delay_days": st.column_config.NumberColumn("Avg Delay (days)", format="%.1f")
                }
            )
    else:
        st.info("No delivery data available for the selected filters.")
    
    # Pending Orders
    st.markdown('<div class="section-header">Pending Orders</div>', unsafe_allow_html=True)
    
    pending_data = get_pending_orders()
    if not empty_state(pending_data):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Order Status Distribution")
            fig = order_status_distribution(pending_data)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Priority Analysis")
            fig = priority_analysis_chart(pending_data)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("#### Pending Orders Details")
        st.dataframe(
            pending_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "grand_total": st.column_config.NumberColumn("Total ($)", format="$%.2f"),
                "order_date": "Order Date",
                "expected_delivery_date": "Expected Delivery"
            }
        )
    else:
        st.success("No pending orders!")
    
    # Detailed Spend Analysis
    st.markdown('<div class="section-header">Detailed Spend Analysis</div>', unsafe_allow_html=True)
    
    spend_data = get_spend_analysis(from_dt, to_dt, dept_id)
    if not empty_state(spend_data):
        st.markdown("#### All Procurement Orders")
        st.dataframe(
            spend_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "grand_total": st.column_config.NumberColumn("Total ($)", format="$%.2f"),
                "order_date": "Order Date",
                "expected_delivery_date": "Expected Delivery",
                "actual_delivery_date": "Actual Delivery"
            }
        )
    else:
        st.info("No spend data available for the selected filters.")
        
except Exception as exc:
    st.error(f"Procurement Dashboard Error: Failed to load data: {exc}")
    st.info("Please check your database connection and ensure the Procurement tables exist with the required columns.")