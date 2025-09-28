"""
Comprehensive Analytics Dashboard
Advanced business intelligence and reporting with professional visualizations.
"""

from __future__ import annotations

import datetime as dt

import streamlit as st

from src.analytics_queries import (
    get_executive_summary,
    get_department_performance,
    get_vendor_performance_analysis,
    get_financial_trends,
    get_procurement_trends,
    get_budget_vs_actual_analysis,
    get_category_spending_analysis
)
from src.analytics_charts import (
    executive_summary_chart,
    department_performance_chart,
    vendor_performance_radar_chart,
    financial_trends_chart,
    budget_vs_actual_chart,
    category_spending_pie_chart,
    procurement_trends_chart,
    performance_heatmap
)
from src.db import health_check
from src.ui import empty_state

st.set_page_config(page_title="Analytics Dashboard", layout="wide")

# Professional CSS for Analytics Dashboard
st.markdown("""
<style>
    .analytics-header {
        background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
        padding: 2rem 1rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        border: 1px solid #34495e;
    }

    .analytics-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 600;
        letter-spacing: -0.5px;
    }

    .analytics-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Dark mode compatibility */
    .stApp[data-theme="dark"] .analytics-header {
        background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .analytics-header h1 {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .analytics-header p {
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

    .metric-card {
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 6px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        text-align: center;
    }

    .metric-value {
        font-size: 2rem;
        font-weight: 600;
        color: #2c3e50;
        margin: 0.5rem 0;
    }

    .metric-label {
        font-size: 0.9rem;
        color: #6c757d;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Professional header with company branding
try:
    import base64
    with open("logo.png", "rb") as logo_file:
        logo_base64 = base64.b64encode(logo_file.read()).decode()
    
    st.markdown(f"""
    <div class="analytics-header">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
            <img src="data:image/png;base64,{logo_base64}" alt="Reflexta Data Intelligence" class="company-logo" style="height: 60px; margin-right: 25px; vertical-align: middle;">
            <div style="text-align: left;">
                <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700; line-height: 1.2;">Advanced Analytics Dashboard</h1>
                <p style="margin: 0.3rem 0 0 0; font-size: 1.1rem; opacity: 0.9; font-weight: 300;">Reflexta Data Intelligence</p>
            </div>
        </div>
        <p style="margin: 0; text-align: center; font-size: 1rem; opacity: 0.9;">Comprehensive Business Intelligence • Executive Insights • Performance Analytics</p>
    </div>
    """, unsafe_allow_html=True)
except FileNotFoundError:
    st.markdown("""
    <div class="analytics-header">
        <h1>Advanced Analytics Dashboard</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9; font-weight: 300;">Reflexta Data Intelligence</p>
        <p>Comprehensive Business Intelligence • Executive Insights • Performance Analytics</p>
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
            <p>Advanced Analytics</p>
        </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown("""
        <div class="sidebar-logo">
            <h3>Reflexta Data Intelligence</h3>
            <p>Advanced Analytics</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### Analytics Filters")
    st.markdown("---")

    today = dt.date.today()
    default_from = today - dt.timedelta(days=90)

    st.markdown("**Date Range**")
    from_dt = st.date_input("From Date", value=default_from, key="analytics_from")
    to_dt = st.date_input("To Date", value=today, key="analytics_to")

    st.markdown("**Department**")
    dept_options = ["All", "Finance", "Procurement", "IT", "HR", "Operations", "Marketing", "Sales", "Legal"]
    selected_dept = st.selectbox("Select Department", dept_options, key="analytics_dept")

    st.markdown("**Analysis Type**")
    analysis_type = st.selectbox(
        "Select Analysis Type",
        options=["Executive Summary", "Department Performance", "Vendor Analysis", "Financial Trends", "Budget Analysis", "Category Analysis"],
        key="analytics_type"
    )

    st.markdown("**Time Period**")
    time_period = st.selectbox(
        "Select Time Period",
        options=["Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year"],
        key="analytics_period"
    )

    st.markdown("**Metric Focus**")
    metric_focus = st.selectbox(
        "Select Metric Focus",
        options=["Financial Performance", "Operational Efficiency", "Vendor Performance", "Budget Utilization", "Trend Analysis"],
        key="analytics_metric"
    )

    st.markdown("**Comparison Period**")
    comparison_period = st.selectbox(
        "Compare With",
        options=["Previous Period", "Same Period Last Year", "Year to Date", "No Comparison"],
        key="analytics_comparison"
    )

    st.markdown("**Performance Threshold**")
    performance_threshold = st.slider(
        "Performance Threshold (%)",
        min_value=0,
        max_value=100,
        value=80,
        step=5,
        key="analytics_threshold"
    )

    st.markdown("---")
    st.markdown("### Quick Actions")
    if st.button("Refresh Analytics", use_container_width=True, key="analytics_refresh"):
        st.rerun()

    if st.button("Export Report", use_container_width=True, key="analytics_export"):
        st.success("Analytics report export feature coming soon!")

    st.markdown("---")
    st.markdown("### Analytics Info")
    st.info("Use filters to customize your analytics view. All charts and metrics will update automatically.")

if not health_check():
    st.error("Database connection failed. Please check your connection settings.")
    st.stop()

try:
    # Executive Summary Section
    st.markdown('<div class="section-header">Executive Summary</div>', unsafe_allow_html=True)
    
    exec_summary = get_executive_summary()
    if not empty_state(exec_summary):
        row = exec_summary.iloc[0]
        
        # KPI Grid
        st.markdown('<div class="kpi-grid">', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Revenue",
                f"${float(row['total_revenue']):,.0f}",
                help="Total revenue generated in the period"
            )
        
        with col2:
            st.metric(
                "Total Expenses",
                f"${float(row['total_expenses']):,.0f}",
                help="Total expenses incurred in the period"
            )
        
        with col3:
            st.metric(
                "Net Profit",
                f"${float(row['net_profit']):,.0f}",
                help="Net profit (Revenue - Expenses)"
            )
        
        with col4:
            st.metric(
                "Budget Utilization",
                f"{float(row['budget_utilization_pct']):.1f}%",
                help="Percentage of budget utilized"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Executive Summary Chart
        st.plotly_chart(executive_summary_chart(exec_summary), use_container_width=True)
    else:
        st.info("No executive summary data available for the selected filters.")

    # Department Performance Section
    st.markdown('<div class="section-header">Department Performance Analysis</div>', unsafe_allow_html=True)
    
    dept_performance = get_department_performance()
    if not empty_state(dept_performance):
        st.plotly_chart(department_performance_chart(dept_performance), use_container_width=True)
        
        # Department Performance Table
        st.markdown("#### Detailed Department Metrics")
        st.dataframe(
            dept_performance,
            use_container_width=True,
            hide_index=True,
            column_config={
                "dept_name": "Department",
                "dept_code": "Code",
                "budget_allocation": st.column_config.NumberColumn("Budget ($)", format="$%.2f"),
                "revenue": st.column_config.NumberColumn("Revenue ($)", format="$%.2f"),
                "expenses": st.column_config.NumberColumn("Expenses ($)", format="$%.2f"),
                "procurement_value": st.column_config.NumberColumn("Procurement ($)", format="$%.2f"),
                "budget_utilization_pct": st.column_config.NumberColumn("Budget Util %", format="%.1f%%"),
                "order_completion_rate": st.column_config.NumberColumn("Completion %", format="%.1f%%")
            }
        )
    else:
        st.info("No department performance data available for the selected filters.")

    # Vendor Performance Section
    st.markdown('<div class="section-header">Vendor Performance Analysis</div>', unsafe_allow_html=True)
    
    vendor_performance = get_vendor_performance_analysis()
    if not empty_state(vendor_performance):
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(vendor_performance_radar_chart(vendor_performance), use_container_width=True)
        
        with col2:
            st.markdown("#### Top Performing Vendors")
            top_vendors = vendor_performance.head(10)
            st.dataframe(
                top_vendors,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "vendor_name": "Vendor",
                    "vendor_code": "Code",
                    "rating": st.column_config.NumberColumn("Rating", format="%.1f"),
                    "total_orders": "Orders",
                    "total_value": st.column_config.NumberColumn("Total Value ($)", format="$%.2f"),
                    "completion_rate": st.column_config.NumberColumn("Completion %", format="%.1f%%"),
                    "delivery_performance": "Delivery Performance"
                }
            )
    else:
        st.info("No vendor performance data available for the selected filters.")

    # Financial Trends Section
    st.markdown('<div class="section-header">Financial Trends Analysis</div>', unsafe_allow_html=True)
    
    financial_trends = get_financial_trends()
    if not empty_state(financial_trends):
        st.plotly_chart(financial_trends_chart(financial_trends), use_container_width=True)
    else:
        st.info("No financial trends data available for the selected filters.")

    # Budget vs Actual Section
    st.markdown('<div class="section-header">Budget vs Actual Analysis</div>', unsafe_allow_html=True)
    
    budget_analysis = get_budget_vs_actual_analysis()
    if not empty_state(budget_analysis):
        st.plotly_chart(budget_vs_actual_chart(budget_analysis), use_container_width=True)
        
        # Budget Analysis Table
        st.markdown("#### Budget Performance Details")
        st.dataframe(
            budget_analysis,
            use_container_width=True,
            hide_index=True,
            column_config={
                "budget_name": "Budget",
                "dept_name": "Department",
                "cost_center_name": "Cost Center",
                "account_name": "Account",
                "budget_amount": st.column_config.NumberColumn("Budget ($)", format="$%.2f"),
                "spent_amount": st.column_config.NumberColumn("Spent ($)", format="$%.2f"),
                "remaining_amount": st.column_config.NumberColumn("Remaining ($)", format="$%.2f"),
                "budget_utilization_pct": st.column_config.NumberColumn("Utilization %", format="%.1f%%"),
                "budget_status": "Status"
            }
        )
    else:
        st.info("No budget analysis data available for the selected filters.")

    # Category Spending Section
    st.markdown('<div class="section-header">Category Spending Analysis</div>', unsafe_allow_html=True)
    
    category_spending = get_category_spending_analysis()
    if not empty_state(category_spending):
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(category_spending_pie_chart(category_spending), use_container_width=True)
        
        with col2:
            st.markdown("#### Category Performance Metrics")
            st.dataframe(
                category_spending,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "category_name": "Category",
                    "category_code": "Code",
                    "total_orders": "Orders",
                    "total_spending": st.column_config.NumberColumn("Spending ($)", format="$%.2f"),
                    "avg_order_value": st.column_config.NumberColumn("Avg Order ($)", format="$%.2f"),
                    "completion_rate": st.column_config.NumberColumn("Completion %", format="%.1f%%"),
                    "unique_vendors": "Vendors"
                }
            )
    else:
        st.info("No category spending data available for the selected filters.")

    # Procurement Trends Section
    st.markdown('<div class="section-header">Procurement Trends Analysis</div>', unsafe_allow_html=True)
    
    procurement_trends = get_procurement_trends()
    if not empty_state(procurement_trends):
        st.plotly_chart(procurement_trends_chart(procurement_trends), use_container_width=True)
    else:
        st.info("No procurement trends data available for the selected filters.")

except Exception as e:
    st.error(f"❌ Analytics Dashboard Error: Failed to load data: {e}")
    st.info("Please check your database connection and ensure all required tables exist with the proper data.")
