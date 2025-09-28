from __future__ import annotations

import datetime as dt

import streamlit as st

from src.db import health_check
from src.finance_queries import (
    get_finance_summary,
    get_finance_monthly_trends,
    get_finance_kpis,
    get_account_analysis,
    get_cost_center_analysis,
    get_budget_vs_actual,
    get_pending_transactions,
    get_vendor_analysis
)
from src.finance_charts import (
    budget_vs_actual_chart,
    budget_utilization_gauge,
    monthly_trends_chart,
    account_analysis_pie,
    cost_center_analysis_chart,
    vendor_spending_chart,
    cash_flow_chart
)
from src.ui import empty_state

st.set_page_config(page_title="Finance Dashboard", layout="wide")

# Professional CSS for Finance Dashboard
st.markdown("""
<style>
    .finance-header {
        background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
        padding: 2rem 1rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
        border: 1px solid #34495e;
    }
    
    .finance-header h1 {
        margin: 0;
        font-size: 2.2rem;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    .finance-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1rem;
        opacity: 0.9;
        font-weight: 300;
    }
    
    /* Dark mode compatibility */
    .stApp[data-theme="dark"] .finance-header {
        background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .finance-header h1 {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .finance-header p {
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
    <div class="finance-header">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
            <img src="data:image/png;base64,{logo_base64}" alt="Reflexta Data Intelligence" class="company-logo" style="height: 60px; margin-right: 25px; vertical-align: middle;">
            <div style="text-align: left;">
                <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700; line-height: 1.2;">Finance Dashboard</h1>
                <p style="margin: 0.3rem 0 0 0; font-size: 1.1rem; opacity: 0.9; font-weight: 300;">Reflexta Data Intelligence</p>
            </div>
        </div>
        <p style="margin: 0; text-align: center; font-size: 1rem; opacity: 0.9;">Comprehensive financial analytics and budget management</p>
    </div>
    """, unsafe_allow_html=True)
except FileNotFoundError:
    st.markdown("""
    <div class="finance-header">
        <div style="text-align: center; margin-bottom: 1rem;">
            <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700; line-height: 1.2;">Finance Dashboard</h1>
            <p style="margin: 0.3rem 0 0 0; font-size: 1.1rem; opacity: 0.9; font-weight: 300;">Reflexta Data Intelligence</p>
        </div>
        <p style="margin: 0; text-align: center; font-size: 1rem; opacity: 0.9;">Comprehensive financial analytics and budget management</p>
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
            <p>Finance Analytics</p>
        </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown("""
        <div class="sidebar-logo">
            <h3>Reflexta Data Intelligence</h3>
            <p>Finance Analytics</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("### Finance Filters")
    st.markdown("---")
    
    today = dt.date.today()
    default_from = today - dt.timedelta(days=90)
    
    st.markdown("**Date Range**")
    from_dt = st.date_input("From Date", value=default_from, key="finance_from")
    to_dt = st.date_input("To Date", value=today, key="finance_to")
    
    st.markdown("**Department**")
    dept_options = ["All", "Finance", "Procurement", "IT", "HR", "Operations", "Marketing", "Sales", "Legal"]
    selected_dept = st.selectbox("Select Department", dept_options, key="finance_dept")
    
    st.markdown("**Transaction Type**")
    transaction_types = ["All", "Revenue", "Expense", "Asset", "Liability", "Equity"]
    selected_type = st.selectbox("Transaction Type", transaction_types, key="finance_type")
    
    st.markdown("**Account Type**")
    account_types = ["All", "Income", "Expense", "Asset", "Liability", "Equity"]
    selected_account_type = st.selectbox("Account Type", account_types, key="finance_account_type")
    
    st.markdown("**Transaction Status**")
    status_options = ["All", "Pending", "Approved", "Rejected", "Completed"]
    selected_status = st.selectbox("Transaction Status", status_options, key="finance_status")
    
    st.markdown("**Amount Range**")
    amount_range = st.slider(
        "Transaction Amount Range ($)",
        min_value=0,
        max_value=100000,
        value=(0, 100000),
        step=1000,
        key="finance_amount_range"
    )
    
    st.markdown("**Budget Status**")
    budget_status = st.selectbox(
        "Budget Status",
        ["All", "Under Budget", "Near Limit", "Over Budget"],
        key="finance_budget_status"
    )
    
    st.markdown("---")
    st.markdown("### Quick Actions")
    if st.button("Refresh Data", use_container_width=True, key="finance_refresh"):
        st.rerun()
    
    if st.button("Export Report", use_container_width=True, key="finance_export"):
        st.success("Finance report export feature coming soon!")
    
    st.markdown("---")
    st.markdown("### Finance Info")
    st.info("Use the filters above to analyze specific departments, time periods, or transaction types.")

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
    transaction_type = selected_type if selected_type != "All" else None
    account_type = selected_account_type if selected_account_type != "All" else None
    status = selected_status if selected_status != "All" else None
    min_amount, max_amount = amount_range
    
    # Finance KPIs
    st.markdown('<div class="section-header">Key Financial Metrics</div>', unsafe_allow_html=True)
    
    kpis = get_finance_kpis(from_dt, to_dt, dept_id)
    if not kpis.empty:
        row = kpis.iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Total Transactions", 
                f"{int(row['total_transactions']) if row['total_transactions'] is not None else 0:,}",
                help="Total number of financial transactions"
            )
        
        with col2:
            st.metric(
                "Total Revenue", 
                f"${float(row['total_revenue']) if row['total_revenue'] is not None else 0:,.0f}",
                help="Total revenue generated"
            )
        
        with col3:
            st.metric(
                "Total Expenses", 
                f"${float(row['total_expenses']) if row['total_expenses'] is not None else 0:,.0f}",
                help="Total expenses incurred"
            )
        
        with col4:
            st.metric(
                "Net Income", 
                f"${float(row['net_income']) if row['net_income'] is not None else 0:,.0f}",
                help="Net income (Revenue - Expenses)"
            )
    else:
        st.info("No financial data available for the selected filters.")
    
    # Budget vs Actual Analysis
    st.markdown('<div class="section-header">Budget vs Actual Analysis</div>', unsafe_allow_html=True)
    
    budget_data = get_budget_vs_actual(from_dt, to_dt, dept_id)
    if not empty_state(budget_data):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### Budget vs Actual Spending")
            fig = budget_vs_actual_chart(budget_data)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Budget Utilization")
            fig = budget_utilization_gauge(budget_data)
            st.plotly_chart(fig, use_container_width=True)
        
        # Budget details table
        st.markdown("#### Budget Details")
        st.dataframe(
            budget_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "budget_amount": st.column_config.NumberColumn("Budget ($)", format="$%.2f"),
                "actual_spent": st.column_config.NumberColumn("Actual ($)", format="$%.2f"),
                "variance": st.column_config.NumberColumn("Variance ($)", format="$%.2f"),
                "utilization_pct": st.column_config.NumberColumn("Utilization %", format="%.1f%%")
            }
        )
    else:
        st.info("No budget data available for the selected filters.")
    
    # Monthly Trends
    st.markdown('<div class="section-header">Financial Trends</div>', unsafe_allow_html=True)
    
    trends_data = get_finance_monthly_trends(from_dt, to_dt, selected_type)
    if not empty_state(trends_data):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### Monthly Financial Trends")
            fig = monthly_trends_chart(trends_data)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Cash Flow Analysis")
            fig = cash_flow_chart(trends_data)
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No trend data available for the selected filters.")
    
    # Account Analysis
    st.markdown('<div class="section-header">Account Analysis</div>', unsafe_allow_html=True)
    
    account_data = get_account_analysis(from_dt, to_dt)
    if not empty_state(account_data):
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.markdown("#### Spending by Account")
            fig = account_analysis_pie(account_data)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Cost Center Analysis")
            cost_center_data = get_cost_center_analysis(from_dt, to_dt)
            if not empty_state(cost_center_data):
                fig = cost_center_analysis_chart(cost_center_data)
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No cost center data available.")
    
    # Vendor Analysis
    st.markdown('<div class="section-header">Vendor Analysis</div>', unsafe_allow_html=True)
    
    vendor_data = get_vendor_analysis(from_dt, to_dt)
    if not empty_state(vendor_data):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("#### Top Vendors by Spending")
            fig = vendor_spending_chart(vendor_data)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("#### Vendor Summary")
            st.dataframe(
                vendor_data,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "total_amount": st.column_config.NumberColumn("Total ($)", format="$%.2f"),
                    "avg_amount": st.column_config.NumberColumn("Avg ($)", format="$%.2f")
                }
            )
    
    # Pending Transactions
    st.markdown('<div class="section-header">Pending Transactions</div>', unsafe_allow_html=True)
    
    pending_data = get_pending_transactions()
    if not empty_state(pending_data):
        st.markdown("#### Transactions Requiring Approval")
        st.dataframe(
            pending_data,
            use_container_width=True,
            hide_index=True,
            column_config={
                "amount": st.column_config.NumberColumn("Amount ($)", format="$%.2f"),
                "transaction_date": "Date"
            }
        )
    else:
        st.success("No pending transactions!")
        
except Exception as exc:
    st.error(f"Finance Dashboard Error: Failed to load data: {exc}")
    st.info("Please check your database connection and ensure the Finance tables exist with the required columns.")