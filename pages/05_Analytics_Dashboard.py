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

# Analytics Dashboard Filters - Sidebar Approach
with st.sidebar:
    st.markdown("### 🔧 Analytics Filters")
    
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

    analysis_type = st.selectbox(
        "Analysis Type",
        options=["Comprehensive", "Financial Only", "Procurement Only", "Performance Only"],
        help="Select type of analysis"
    )

    # Additional filters
    st.markdown("**Additional Filters**")
    
    time_period = st.selectbox(
        "Time Period",
        options=["Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year", "Custom"],
        help="Select time period for analysis"
    )

    metric_focus = st.selectbox(
        "Metric Focus",
        options=["All Metrics", "Financial KPIs", "Operational KPIs", "Vendor KPIs"],
        help="Focus on specific metrics"
    )

    data_quality = st.selectbox(
        "Data Quality",
        options=["All Data", "Complete Records", "Validated Data"],
        help="Filter by data quality"
    )

    # Get department ID if specific department is selected
    dept_id = None
    if department != "All":
        dept_mapping = {
            "Finance": 1, "Procurement": 2, "IT": 3, "HR": 4, "Operations": 5,
            "Marketing": 6, "Sales": 7, "Legal": 8
        }
        dept_id = dept_mapping.get(department)


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
        font-size: 1.1rem;
        opacity: 0.9;
        font-weight: 300;
    }

    .section-header {
        background: linear-gradient(90deg, #9b59b6 0%, #8e44ad 100%);
        color: white;
        padding: 0.8rem 1.2rem;
        margin: 1.5rem 0 1rem 0;
        border-radius: 6px;
        font-weight: 500;
        font-size: 1.1rem;
        border-left: 4px solid #9b59b6;
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
    .stApp[data-theme="dark"] .analytics-header {
        background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
        color: white !important;
    }

    .stApp[data-theme="dark"] .analytics-header h1 {
        color: white !important;
    }

    .stApp[data-theme="dark"] .analytics-header p {
        color: rgba(255, 255, 255, 0.9) !important;
    }

    .stApp[data-theme="dark"] .section-header {
        background: linear-gradient(90deg, #9b59b6 0%, #8e44ad 100%);
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
    
    /* Fix excessive spacing and scrolling issues */
    .stApp {
        overflow-x: hidden;
    }
    
    .stPlotlyChart {
        max-height: 600px !important;
    }
    
    .stDataFrame {
        max-height: 400px !important;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="analytics-header">
    <h1>📊 Analytics Dashboard</h1>
    <p>Advanced Business Intelligence & Comprehensive Reporting</p>
</div>
""", unsafe_allow_html=True)

if not health_check():
    st.error("Database connection failed. Please check your connection settings.")
    st.stop()

try:
    # Executive Summary
    st.markdown('<div class="section-header">Executive Summary</div>', unsafe_allow_html=True)
    
    summary_data = get_executive_summary(from_date, to_date, dept_id)
    if not empty_state(summary_data):
        st.plotly_chart(
            executive_summary_chart(summary_data),
            use_container_width=True
        )
    else:
        st.info("No executive summary data available for the selected period.")
    
    # Department Performance
    st.markdown('<div class="section-header">Department Performance Analysis</div>', unsafe_allow_html=True)
    
    dept_data = get_department_performance(from_date, to_date, dept_id)
    if not empty_state(dept_data):
        st.plotly_chart(
            department_performance_chart(dept_data),
            use_container_width=True
        )
    else:
        st.info("No department performance data available for the selected period.")
    
    # Vendor Performance Analysis
    st.markdown('<div class="section-header">Vendor Performance Analysis</div>', unsafe_allow_html=True)
    
    vendor_data = get_vendor_performance_analysis(from_date, to_date, dept_id)
    if not empty_state(vendor_data):
        st.plotly_chart(
            vendor_performance_radar_chart(vendor_data),
            use_container_width=True
        )
    else:
        st.info("No vendor performance data available for the selected period.")
    
    # Financial Trends
    st.markdown('<div class="section-header">Financial Trends Analysis</div>', unsafe_allow_html=True)
    
    financial_data = get_financial_trends(from_date, to_date, dept_id)
    if not empty_state(financial_data):
        st.plotly_chart(
            financial_trends_chart(financial_data),
            use_container_width=True
        )
    else:
        st.info("No financial trends data available for the selected period.")
    
    # Procurement Trends
    st.markdown('<div class="section-header">Procurement Trends Analysis</div>', unsafe_allow_html=True)
    
    procurement_data = get_procurement_trends(from_date, to_date, dept_id)
    if not empty_state(procurement_data):
        st.plotly_chart(
            procurement_trends_chart(procurement_data),
            use_container_width=True
        )
    else:
        st.info("No procurement trends data available for the selected period.")
    
    # Budget vs Actual Analysis
    st.markdown('<div class="section-header">Budget vs Actual Analysis</div>', unsafe_allow_html=True)
    
    budget_data = get_budget_vs_actual_analysis(from_date, to_date, dept_id)
    if not empty_state(budget_data):
        st.plotly_chart(
            budget_vs_actual_chart(budget_data),
            use_container_width=True
        )
    else:
        st.info("No budget analysis data available for the selected period.")
    
    # Category Spending Analysis
    st.markdown('<div class="section-header">Category Spending Analysis</div>', unsafe_allow_html=True)
    
    category_data = get_category_spending_analysis(from_date, to_date, dept_id)
    if not empty_state(category_data):
        st.plotly_chart(
            category_spending_pie_chart(category_data),
            use_container_width=True
        )
    else:
        st.info("No category spending data available for the selected period.")
    
    # Performance Heatmap
    st.markdown('<div class="section-header">Performance Heatmap</div>', unsafe_allow_html=True)
    
    heatmap_data = get_department_performance(from_date, to_date, dept_id)
    if not empty_state(heatmap_data):
        st.plotly_chart(
            performance_heatmap(heatmap_data),
            use_container_width=True
        )
    else:
        st.info("No performance heatmap data available for the selected period.")

except Exception as e:
    st.error(f"Error loading analytics data: {str(e)}")
    st.info("Please check your database connection and try again.")

# Footer to prevent excessive scrolling
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p>📊 Analytics Dashboard - Reflexta Data Intelligence</p>
    <p>Advanced Business Intelligence & Comprehensive Reporting</p>
</div>
""", unsafe_allow_html=True)