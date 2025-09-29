from __future__ import annotations

import datetime as dt

import pandas as pd
import streamlit as st

from src.db import health_check
from src.finance_queries import get_finance_kpis, get_finance_summary
from src.procurement_queries import get_procurement_kpis, get_procurement_summary
from src.ui import kpi_row, section_header, empty_state

# Professional CSS for enterprise UI
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #2c3e50 100%);
        padding: 1.5rem 1.5rem;
        border-radius: 8px;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
        border: 1px solid #34495e;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        position: relative;
        overflow: hidden;
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .main-header h1 {
        margin: 0;
        font-size: 2.5rem;
        font-weight: 700;
        letter-spacing: -1px;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        position: relative;
        z-index: 1;
    }
    
    .main-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 300;
        position: relative;
        z-index: 1;
    }
    
    .company-logo {
        filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.3));
        transition: transform 0.3s ease;
    }
    
    .company-logo:hover {
        transform: scale(1.05);
    }
    
    .company-footer {
        background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 3rem;
        color: white;
        text-align: center;
        border: 1px solid #34495e;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    
    .company-footer h3 {
        margin: 0 0 0.5rem 0;
        font-size: 1.2rem;
        font-weight: 600;
    }
    
    .company-footer p {
        margin: 0;
        font-size: 0.9rem;
        opacity: 0.8;
    }
    
    .brand-highlight {
        background: linear-gradient(45deg, #3498db, #2ecc71);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 700;
    }
    
    .pulse-animation {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.02); }
        100% { transform: scale(1); }
    }
    
    .gradient-text {
        background: linear-gradient(45deg, #3498db, #2ecc71, #e74c3c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-weight: 600;
    }
    
    /* Dark mode compatibility */
    .stApp[data-theme="dark"] .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #2c3e50 100%) !important;
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .main-header h1 {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .main-header p {
        color: #ecf0f1 !important;
    }
    
    /* Force dark mode styling for main app */
    .stApp[data-theme="dark"] .main-header * {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .main-header .gradient-text {
        background: linear-gradient(45deg, #3498db, #2ecc71, #e74c3c) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }
    
    /* Override inline styles for dark mode */
    .stApp[data-theme="dark"] .main-header h1 {
        color: white !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5) !important;
    }
    
    .stApp[data-theme="dark"] .main-header p {
        color: #ecf0f1 !important;
    }
    
    /* Force all text in main header to be visible in dark mode */
    .stApp[data-theme="dark"] .main-header div {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .main-header div p {
        color: #ecf0f1 !important;
    }
    
    .stApp[data-theme="dark"] .main-header div h1 {
        color: white !important;
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
    
    /* Force white text in headers for dark mode */
    .stApp[data-theme="dark"] .finance-header,
    .stApp[data-theme="dark"] .procurement-header,
    .stApp[data-theme="dark"] .analytics-header,
    .stApp[data-theme="dark"] .db-header {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .finance-header h1,
    .stApp[data-theme="dark"] .procurement-header h1,
    .stApp[data-theme="dark"] .analytics-header h1,
    .stApp[data-theme="dark"] .db-header h1 {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .finance-header p,
    .stApp[data-theme="dark"] .procurement-header p,
    .stApp[data-theme="dark"] .analytics-header p,
    .stApp[data-theme="dark"] .db-header p {
        color: #ecf0f1 !important;
    }
    
    /* Dark mode for main app KPI sections */
    .stApp[data-theme="dark"] .section-header {
        background: linear-gradient(90deg, #34495e 0%, #2c3e50 100%) !important;
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .section-header h3 {
        color: white !important;
    }
    
    /* Dark mode for metric containers */
    .stApp[data-theme="dark"] .metric-container {
        background: #2c3e50 !important;
        border: 1px solid #34495e !important;
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .metric-value {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .metric-label {
        color: #bdc3c7 !important;
    }
    
    /* Dark mode for company footer */
    .stApp[data-theme="dark"] .company-footer {
        background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%) !important;
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .company-footer h3 {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .company-footer p {
        color: rgba(255, 255, 255, 0.8) !important;
    }
    
    /* Dark mode for Streamlit metric components */
    .stApp[data-theme="dark"] .metric {
        background: #2c3e50 !important;
        border: 1px solid #34495e !important;
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .metric .metric-value {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .metric .metric-label {
        color: #bdc3c7 !important;
    }
    
    /* Dark mode for Streamlit columns */
    .stApp[data-theme="dark"] .stColumn {
        background: transparent !important;
    }
    
    /* Dark mode for Streamlit containers */
    .stApp[data-theme="dark"] .stContainer {
        background: transparent !important;
    }
    
    /* Additional dark mode fixes for main app */
    .stApp[data-theme="dark"] .main-header {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #2c3e50 100%) !important;
    }
    
    .stApp[data-theme="dark"] .main-header img {
        filter: brightness(1.2) !important;
    }
    
    /* Header content styling */
    .header-content {
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 1.5rem;
    }
    
    .company-logo {
        height: 80px;
        margin-right: 30px;
        vertical-align: middle;
    }
    
    .header-text {
        text-align: left;
    }
    
    .header-text h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1.1;
        text-shadow: 0 2px 4px rgba(0,0,0,0.3);
    }
    
    .header-subtitle {
        margin: 0.5rem 0 0 0;
        font-size: 1.1rem;
        color: #ecf0f1;
        font-weight: 400;
    }
    
    .header-description {
        margin: 0;
        text-align: center;
        font-size: 1rem;
        color: #bdc3c7;
        font-weight: 300;
    }
    
    /* Dark mode for new header structure */
    .stApp[data-theme="dark"] .header-text h1 {
        color: white !important;
        text-shadow: 0 2px 4px rgba(0,0,0,0.5) !important;
    }
    
    .stApp[data-theme="dark"] .header-subtitle {
        color: #ecf0f1 !important;
    }
    
    .stApp[data-theme="dark"] .header-description {
        color: #bdc3c7 !important;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    .sidebar .sidebar-content .block-container {
        padding-top: 1rem;
    }
    
    .sidebar-logo {
        text-align: center;
        margin-bottom: 1.5rem;
        padding: 1rem;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 8px;
        margin: 0 0.5rem 1.5rem 0.5rem;
    }
    
    .sidebar-logo img {
        height: 40px;
        margin-bottom: 0.5rem;
    }
    
    .sidebar-logo h3 {
        color: white;
        margin: 0;
        font-size: 1rem;
        font-weight: 600;
    }
    
    .sidebar-logo p {
        color: rgba(255, 255, 255, 0.8);
        margin: 0;
        font-size: 0.8rem;
    }
    
    /* Navigation links styling */
    .sidebar .sidebar-content .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 6px;
        color: white;
    }
    
    .sidebar .sidebar-content .stSelectbox > div > div:hover {
        background-color: rgba(255, 255, 255, 0.2);
        border-color: #3498db;
    }
    
    /* Dark mode for sidebar filters */
    .stApp[data-theme="dark"] .sidebar .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .sidebar .stSelectbox > div > div:hover {
        background-color: rgba(255, 255, 255, 0.2) !important;
        border-color: #3498db !important;
    }
    
    /* Dark mode for sidebar input fields */
    .stApp[data-theme="dark"] .sidebar .stTextInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .sidebar .stTextInput > div > div > input:focus {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border-color: #3498db !important;
        color: white !important;
    }
    
    /* Dark mode for sidebar date inputs */
    .stApp[data-theme="dark"] .sidebar .stDateInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .sidebar .stDateInput > div > div > input:focus {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border-color: #3498db !important;
        color: white !important;
    }
    
    /* Dark mode for sidebar labels */
    .stApp[data-theme="dark"] .sidebar label {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .sidebar .stMarkdown {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .sidebar .stMarkdown p {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .sidebar .stMarkdown strong {
        color: white !important;
    }
    
    /* Dark mode for sidebar buttons */
    .stApp[data-theme="dark"] .sidebar .stButton > button {
        background-color: #3498db !important;
        color: white !important;
        border: 1px solid #2980b9 !important;
    }
    
    .stApp[data-theme="dark"] .sidebar .stButton > button:hover {
        background-color: #2980b9 !important;
        color: white !important;
    }
    
    /* Dark mode for sidebar sliders */
    .stApp[data-theme="dark"] .sidebar .stSlider > div > div > div {
        background-color: rgba(255, 255, 255, 0.2) !important;
    }
    
    .stApp[data-theme="dark"] .sidebar .stSlider > div > div > div > div {
        background-color: #3498db !important;
    }
    
    /* Dark mode for sidebar number inputs */
    .stApp[data-theme="dark"] .sidebar .stNumberInput > div > div > input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .sidebar .stNumberInput > div > div > input:focus {
        background-color: rgba(255, 255, 255, 0.15) !important;
        border-color: #3498db !important;
        color: white !important;
    }
    
    /* Dark mode for sidebar checkboxes */
    .stApp[data-theme="dark"] .sidebar .stCheckbox > div > label {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .sidebar .stCheckbox > div > label > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
    }
    
    /* Dark mode for sidebar radio buttons */
    .stApp[data-theme="dark"] .sidebar .stRadio > div > label {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .sidebar .stRadio > div > label > div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        border: 1px solid rgba(255, 255, 255, 0.3) !important;
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
    
    .sidebar .sidebar-content {
        background: #f8f9fa;
        border-right: 1px solid #dee2e6;
    }
    
    .stSelectbox > div > div {
        background-color: white;
        border: 1px solid #ced4da;
        border-radius: 4px;
    }
    
    .stDateInput > div > div {
        background-color: white;
        border: 1px solid #ced4da;
        border-radius: 4px;
    }
    
    .stButton > button {
        background: #007bff;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.2s ease;
    }
    
    .stButton > button:hover {
        background: #0056b3;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0, 123, 255, 0.3);
    }
    
    .metric-container {
        background: white;
        border: 1px solid #dee2e6;
        border-radius: 6px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
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
</style>
""", unsafe_allow_html=True)

st.set_page_config(
    page_title="Enterprise Analytics Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io',
        'Report a bug': "https://github.com/streamlit/streamlit/issues",
        'About': "# Enterprise Analytics Dashboard\nBuilt with Streamlit, PostgreSQL, and Plotly"
    }
)

# Professional header with company branding
try:
    import base64
    with open("logo.png", "rb") as logo_file:
        logo_base64 = base64.b64encode(logo_file.read()).decode()
    
    st.markdown(f"""
    <div class="main-header">
        <div class="header-content">
            <img src="data:image/png;base64,{logo_base64}" alt="Reflexta Data Intelligence" class="company-logo">
            <div class="header-text">
                <h1 class="gradient-text">Reflexta Data Intelligence</h1>
                <p class="header-subtitle">Enterprise Analytics Platform</p>
            </div>
        </div>
        <p class="header-description">Comprehensive Finance & Procurement Analytics • Real-time Business Intelligence</p>
    </div>
    """, unsafe_allow_html=True)
except FileNotFoundError:
    # Fallback if logo is not found
    st.markdown("""
    <div class="main-header">
        <h1 class="gradient-text">Reflexta Data Intelligence</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9; font-weight: 300;">Enterprise Analytics Platform</p>
        <p>Comprehensive Finance & Procurement Analytics • Real-time Business Intelligence</p>
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
            <p>Enterprise Analytics Platform</p>
        </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown("""
        <div class="sidebar-logo">
            <h3>Reflexta Data Intelligence</h3>
            <p>Enterprise Analytics Platform</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### Filters & Controls")
    st.markdown("---")
    
    today = dt.date.today()
    default_from = today - dt.timedelta(days=30)

    st.markdown("**Date Range**")
    from_dt = st.date_input("From Date", value=default_from, help="Select start date for analysis")
    to_dt = st.date_input("To Date", value=today, help="Select end date for analysis")

    st.markdown("**Department**")
    department = st.selectbox(
        "Select Department", 
        options=["All", "Finance", "Procurement", "IT", "HR", "Operations", "Marketing", "Sales", "Legal"],
        help="Filter data by specific department"
    )
    
    st.markdown("**Module Focus**")
    module_focus = st.selectbox(
        "Select Module Focus",
        options=["All Modules", "Finance Only", "Procurement Only", "Analytics Only"],
        help="Focus on specific business modules"
    )
    
    st.markdown("**Time Period**")
    time_period = st.selectbox(
        "Select Time Period",
        options=["Last 30 Days", "Last 90 Days", "Last 6 Months", "Last Year", "Custom Range"],
        help="Quick time period selection"
    )
    
    st.markdown("**Data Quality**")
    data_quality = st.selectbox(
        "Data Quality Filter",
        options=["All Data", "Complete Records Only", "Validated Data Only"],
        help="Filter based on data completeness"
    )
    
    st.markdown("---")
    st.markdown("### Quick Actions")
    if st.button("Refresh Data", use_container_width=True):
        st.rerun()
    
    if st.button("Export Report", use_container_width=True):
        st.success("Report export feature coming soon!")
    
    st.markdown("---")
    st.markdown("### Navigation")
    st.info("Use the filters above to customize your dashboard view. All charts and KPIs will update automatically.")

if not health_check():
    st.error("Database connection failed. Please check your connection settings.")
    st.stop()

try:
    # Process time period selection
    if time_period != "Custom Range":
        if time_period == "Last 30 Days":
            from_dt = today - dt.timedelta(days=30)
        elif time_period == "Last 90 Days":
            from_dt = today - dt.timedelta(days=90)
        elif time_period == "Last 6 Months":
            from_dt = today - dt.timedelta(days=180)
        elif time_period == "Last Year":
            from_dt = today - dt.timedelta(days=365)
    
    # Get department ID if specific department is selected
    dept_id = None
    if department != "All":
        dept_mapping = {
            "Finance": 1, "Procurement": 2, "IT": 3, "HR": 4, "Operations": 5,
            "Marketing": 6, "Sales": 7, "Legal": 8
        }
        dept_id = dept_mapping.get(department)
    
    # KPI Section with professional styling
    st.markdown('<div class="section-header">Key Performance Indicators</div>', unsafe_allow_html=True)
    
    # Finance KPIs
    finance_kpis = get_finance_kpis(from_dt, to_dt, dept_id)
    if not finance_kpis.empty:
        row = finance_kpis.iloc[0]
        st.markdown("#### Finance Metrics")
        # Handle None values safely
        total_transactions = int(row["total_transactions"]) if row["total_transactions"] is not None else 0
        total_revenue = float(row["total_revenue"]) if row["total_revenue"] is not None else 0.0
        total_expenses = float(row["total_expenses"]) if row["total_expenses"] is not None else 0.0
        kpi_row(total_transactions, total_revenue, total_expenses)
    
    # Procurement KPIs
    procurement_kpis = get_procurement_kpis(from_dt, to_dt, dept_id)
    if not procurement_kpis.empty:
        row = procurement_kpis.iloc[0]
        st.markdown("#### Procurement Metrics")
        # Handle None values safely
        total_orders = int(row["total_orders"]) if row["total_orders"] is not None else 0
        total_value = float(row["total_value"]) if row["total_value"] is not None else 0.0
        avg_order_value = float(row["avg_order_value"]) if row["avg_order_value"] is not None else 0.0
        kpi_row(total_orders, total_value, avg_order_value)

    # Department Summary
    st.markdown('<div class="section-header">Department Analytics</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Finance Summary")
        finance_summary = get_finance_summary(from_dt, to_dt, dept_id)
        if not empty_state(finance_summary):
            st.dataframe(
                finance_summary,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "dept_name": "Department",
                    "dept_code": "Code",
                    "budget_allocation": st.column_config.NumberColumn("Budget ($)", format="$%.2f"),
                    "total_spent": st.column_config.NumberColumn("Spent ($)", format="$%.2f"),
                    "remaining_budget": st.column_config.NumberColumn("Remaining ($)", format="$%.2f"),
                    "budget_utilization_pct": st.column_config.NumberColumn("Utilization %", format="%.1f%%")
                }
            )
        else:
            st.info("No finance data available for the selected filters.")
    
    with col2:
        st.markdown("#### Procurement Summary")
        procurement_summary = get_procurement_summary(from_dt, to_dt, dept_id)
        if not empty_state(procurement_summary):
            st.dataframe(
                procurement_summary,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "dept_name": "Department",
                    "dept_code": "Code",
                    "total_orders": "Orders",
                    "total_value": st.column_config.NumberColumn("Total Value ($)", format="$%.2f"),
                    "avg_order_value": st.column_config.NumberColumn("Avg Order ($)", format="$%.2f"),
                    "completion_rate": st.column_config.NumberColumn("Completion %", format="%.1f%%")
                }
            )
        else:
            st.info("No procurement data available for the selected filters.")

    # Quick Navigation
    st.markdown('<div class="section-header">Quick Navigation</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("Finance Dashboard", use_container_width=True):
            st.switch_page("pages/03_Finance_Dashboard.py")
    
    with col2:
        if st.button("Procurement Dashboard", use_container_width=True):
            st.switch_page("pages/04_Procurement_Dashboard.py")
    
    with col3:
        if st.button("Analytics Dashboard", use_container_width=True):
            st.switch_page("pages/05_Analytics_Dashboard.py")
    
    with col4:
        if st.button("Database Analysis", use_container_width=True):
            st.switch_page("pages/00_Database_Analysis.py")

    # Professional footer
    st.markdown("""
    <div class="company-footer">
        <h3>Reflexta Data Intelligence</h3>
        <p>Empowering businesses with intelligent data analytics and insights</p>
        <p style="margin-top: 0.5rem; font-size: 0.8rem; opacity: 0.7;">
            Enterprise Analytics Platform • Real-time Business Intelligence • Advanced Data Visualization
        </p>
    </div>
    """, unsafe_allow_html=True)
        
except Exception as exc:  # noqa: BLE001
    st.error(f"Database Error: Failed to load data: {exc}")
    st.info("Please check your database connection and ensure the Finance and Procurement tables exist.")