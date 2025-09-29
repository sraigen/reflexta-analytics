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

# Finance Dashboard Filters - Sidebar Approach
with st.sidebar:
    st.markdown("### 🔧 Finance Filters")
    
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

    transaction_type = st.selectbox(
        "Transaction Type",
        options=["All", "Revenue", "Expense"],
        help="Filter by transaction type"
    )

    # Get department ID if specific department is selected
    dept_id = None
    if department != "All":
        dept_mapping = {
            "Finance": 1, "Procurement": 2, "IT": 3, "HR": 4, "Operations": 5,
            "Marketing": 6, "Sales": 7, "Legal": 8
        }
        dept_id = dept_mapping.get(department)


# Professional CSS for Finance Dashboard
st.markdown("""
<style>
    .finance-header {
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
    
    .finance-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .finance-header h1 {
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
    
    .finance-header p {
        margin: 0.5rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.9;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    .section-header {
        background: linear-gradient(90deg, #3498db 0%, #2980b9 100%);
        color: white;
        padding: 0.8rem 1.2rem;
        margin: 1.5rem 0 1rem 0;
        border-radius: 6px;
        font-weight: 500;
        font-size: 1.1rem;
        border-left: 4px solid #3498db;
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
    .stApp[data-theme="dark"] .finance-header {
        background: linear-gradient(90deg, #2c3e50 0%, #34495e 100%);
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .finance-header h1 {
        color: white !important;
    }
    
    .stApp[data-theme="dark"] .finance-header p {
        color: rgba(255, 255, 255, 0.9) !important;
    }
    
    .stApp[data-theme="dark"] .section-header {
        background: linear-gradient(90deg, #3498db 0%, #2980b9 100%);
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
<div class="finance-header">
    <h1>💰 Finance Dashboard</h1>
    <p>Comprehensive Financial Analytics & Performance Metrics</p>
</div>
""", unsafe_allow_html=True)

if not health_check():
    st.error("Database connection failed. Please check your connection settings.")
    st.stop()

try:
    # Finance KPIs
    st.markdown('<div class="section-header">Key Financial Metrics</div>', unsafe_allow_html=True)
    
    kpis = get_finance_kpis(from_date, to_date, dept_id)
    if not kpis.empty:
        row = kpis.iloc[0]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Revenue",
                value=f"${row['total_revenue']:,.2f}" if row['total_revenue'] else "$0.00",
                delta=f"${row['revenue_growth']:,.2f}" if row['revenue_growth'] else None
            )
        
        with col2:
            st.metric(
                label="Total Expenses",
                value=f"${row['total_expenses']:,.2f}" if row['total_expenses'] else "$0.00",
                delta=f"${row['expense_growth']:,.2f}" if row['expense_growth'] else None
            )
        
        with col3:
            st.metric(
                label="Net Income",
                value=f"${row['net_income']:,.2f}" if row['net_income'] else "$0.00",
                delta=f"${row['net_income_growth']:,.2f}" if row['net_income_growth'] else None
            )
        
        with col4:
            st.metric(
                label="Transaction Count",
                value=f"{row['total_transactions']:,}" if row['total_transactions'] else "0",
                delta=f"{row['transaction_growth']:,}" if row['transaction_growth'] else None
            )
    else:
        st.warning("No financial data available for the selected period.")
    
    # Budget vs Actual Analysis
    st.markdown('<div class="section-header">Budget vs Actual Analysis</div>', unsafe_allow_html=True)
    
    budget_data = get_budget_vs_actual(from_date, to_date, dept_id)
    if not empty_state(budget_data):
        col1, col2 = st.columns(2)
        
        with col1:
            st.plotly_chart(
                budget_vs_actual_chart(budget_data),
                use_container_width=True
            )
        
        with col2:
            st.plotly_chart(
                budget_utilization_gauge(budget_data),
                use_container_width=True
            )
    else:
        st.info("No budget data available for the selected period.")
    
    # Monthly Trends
    st.markdown('<div class="section-header">Financial Trends</div>', unsafe_allow_html=True)
    
    trends_data = get_finance_monthly_trends(from_date, to_date, transaction_type)
    if not empty_state(trends_data):
        st.plotly_chart(
            monthly_trends_chart(trends_data),
            use_container_width=True
        )
    else:
        st.info("No trend data available for the selected period.")
    
    # Account Analysis
    st.markdown('<div class="section-header">Account Analysis</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### Account Distribution")
        account_data = get_account_analysis(from_date, to_date)
        if not empty_state(account_data):
            st.plotly_chart(
                account_analysis_pie(account_data),
                use_container_width=True
            )
        else:
            st.info("No account data available.")
    
    with col2:
        st.markdown("#### Cost Center Analysis")
        cost_center_data = get_cost_center_analysis(from_date, to_date)
        if not empty_state(cost_center_data):
            st.plotly_chart(
                cost_center_analysis_chart(cost_center_data),
                use_container_width=True
            )
        else:
            st.info("No cost center data available.")
    
    # Vendor Analysis
    st.markdown('<div class="section-header">Vendor Spending Analysis</div>', unsafe_allow_html=True)
    
    vendor_data = get_vendor_analysis(from_date, to_date, dept_id)
    if not empty_state(vendor_data):
        st.plotly_chart(
            vendor_spending_chart(vendor_data),
            use_container_width=True
        )
    else:
        st.info("No vendor data available for the selected period.")
    
    # Cash Flow Analysis
    st.markdown('<div class="section-header">Cash Flow Analysis</div>', unsafe_allow_html=True)
    
    cash_flow_data = get_finance_summary(from_date, to_date, dept_id)
    if not empty_state(cash_flow_data):
        st.plotly_chart(
            cash_flow_chart(cash_flow_data),
            use_container_width=True
        )
    else:
        st.info("No cash flow data available for the selected period.")
    
    # Pending Transactions
    st.markdown('<div class="section-header">Pending Transactions</div>', unsafe_allow_html=True)
    
    pending_data = get_pending_transactions(from_date, to_date, dept_id)
    if not empty_state(pending_data):
        st.dataframe(
            pending_data,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No pending transactions for the selected period.")

except Exception as e:
    st.error(f"Error loading finance data: {str(e)}")
    st.info("Please check your database connection and try again.")

# Render simple AI chat
from src.simple_ai_chat import render_simple_ai_chat
render_simple_ai_chat()