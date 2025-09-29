from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime as dt
from typing import Optional, Any

# Import database and query functions
from src.db import get_conn, health_check
from src.finance_queries import get_finance_kpis, get_finance_monthly_trends, get_vendor_analysis
from src.procurement_queries import get_procurement_kpis, get_procurement_trends, get_vendor_performance
from src.ui import empty_state

st.set_page_config(page_title="Analytics Dashboard", layout="wide")

# Professional CSS for Analytics Dashboard
st.markdown("""
<style>
    .analytics-header {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        color: white;
        padding: 2.5rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .analytics-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .analytics-header h1 {
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
    
    .analytics-header p {
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
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 2rem 0 1rem 0;
        font-size: 1.3rem;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3498db;
        margin-bottom: 1rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        color: #7f8c8d;
        margin: 0;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-change {
        font-size: 0.8rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }
    
    .positive {
        color: #27ae60;
    }
    
    .negative {
        color: #e74c3c;
    }
    
    .neutral {
        color: #95a5a6;
    }
</style>
""", unsafe_allow_html=True)

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

    # Get department ID if specific department is selected
    dept_id = None
    if department != "All":
        dept_mapping = {
            "Finance": 1, "Procurement": 2, "IT": 3, "HR": 4, "Operations": 5,
            "Marketing": 6, "Sales": 7, "Legal": 8
        }
        dept_id = dept_mapping.get(department)

# Header
st.markdown("""
<div class="analytics-header">
    <h1>📊 Business Intelligence Dashboard</h1>
    <p>Executive Analytics & Key Performance Indicators</p>
</div>
""", unsafe_allow_html=True)

if not health_check():
    st.error("Database connection failed. Please check your connection settings.")
    st.stop()

try:
    # Executive Summary KPIs
    st.markdown('<div class="section-header">Executive Summary</div>', unsafe_allow_html=True)
    
    # Get finance and procurement KPIs
    finance_kpis = get_finance_kpis(from_date, to_date, dept_id)
    procurement_kpis = get_procurement_kpis(from_date, to_date, dept_id)
    
    if not finance_kpis.empty and not procurement_kpis.empty:
        fin_row = finance_kpis.iloc[0]
        proc_row = procurement_kpis.iloc[0]
        
        # Create KPI columns
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">${fin_row['total_revenue']:,.0f}</div>
                <div class="metric-label">Total Revenue</div>
                <div class="metric-change {'positive' if fin_row['revenue_growth'] > 0 else 'negative' if fin_row['revenue_growth'] < 0 else 'neutral'}">
                    {fin_row['revenue_growth']:+.0f} vs previous period
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">${fin_row['net_income']:,.0f}</div>
                <div class="metric-label">Net Income</div>
                <div class="metric-change {'positive' if fin_row['net_income_growth'] > 0 else 'negative' if fin_row['net_income_growth'] < 0 else 'neutral'}">
                    {fin_row['net_income_growth']:+.0f} vs previous period
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{proc_row['total_orders']:,.0f}</div>
                <div class="metric-label">Total Orders</div>
                <div class="metric-change {'positive' if proc_row['order_growth'] > 0 else 'negative' if proc_row['order_growth'] < 0 else 'neutral'}">
                    {proc_row['order_growth']:+.0f} vs previous period
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">${proc_row['total_spend']:,.0f}</div>
                <div class="metric-label">Total Spend</div>
                <div class="metric-change {'positive' if proc_row['spend_growth'] > 0 else 'negative' if proc_row['spend_growth'] < 0 else 'neutral'}">
                    {proc_row['spend_growth']:+.0f} vs previous period
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Financial Performance Trends
    st.markdown('<div class="section-header">Financial Performance Trends</div>', unsafe_allow_html=True)
    
    trends_data = get_finance_monthly_trends(from_date, to_date)
    if not empty_state(trends_data):
        # Create financial trends chart
        fig = go.Figure()
        
        # Add revenue line
        revenue_data = trends_data[trends_data['transaction_type'] == 'Revenue']
        if not revenue_data.empty:
            fig.add_trace(go.Scatter(
                x=revenue_data['month'],
                y=revenue_data['total_amount'],
                mode='lines+markers',
                name='Revenue',
                line=dict(color='#27ae60', width=3),
                marker=dict(size=8)
            ))
        
        # Add expense line
        expense_data = trends_data[trends_data['transaction_type'] == 'Expense']
        if not expense_data.empty:
            fig.add_trace(go.Scatter(
                x=expense_data['month'],
                y=expense_data['total_amount'],
                mode='lines+markers',
                name='Expenses',
                line=dict(color='#e74c3c', width=3),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title="Monthly Financial Trends",
            xaxis_title="Month",
            yaxis_title="Amount ($)",
            height=400,
            showlegend=True,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No financial trends data available for the selected period.")
    
    # Procurement Performance
    st.markdown('<div class="section-header">Procurement Performance</div>', unsafe_allow_html=True)
    
    procurement_trends = get_procurement_trends(from_date, to_date, dept_id)
    if not empty_state(procurement_trends):
        # Create procurement trends chart
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=procurement_trends['month_name'],
            y=procurement_trends['total_value'],
            mode='lines+markers',
            name='Procurement Value',
            line=dict(color='#3498db', width=3),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Procurement Trends Over Time",
            xaxis_title="Month",
            yaxis_title="Total Value ($)",
            height=400,
            showlegend=True
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No procurement trends data available for the selected period.")
    
    # Vendor Performance Analysis
    st.markdown('<div class="section-header">Top Vendors by Performance</div>', unsafe_allow_html=True)
    
    vendor_performance = get_vendor_performance(from_date, to_date, dept_id)
    if not empty_state(vendor_performance):
        # Create vendor performance chart
        fig = go.Figure()
        
        # Sort by total value and take top 10
        top_vendors = vendor_performance.head(10)
        
        fig.add_trace(go.Bar(
            x=top_vendors['total_value'],
            y=top_vendors['vendor_name'],
            orientation='h',
            marker=dict(color='#9b59b6'),
            text=top_vendors['total_value'],
            texttemplate='$%{text:,.0f}',
            textposition='auto'
        ))
        
        fig.update_layout(
            title="Top 10 Vendors by Total Value",
            xaxis_title="Total Value ($)",
            yaxis_title="Vendor",
            height=500,
            showlegend=False
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No vendor performance data available for the selected period.")
    
    # Department Performance Summary
    st.markdown('<div class="section-header">Department Performance Summary</div>', unsafe_allow_html=True)
    
    # Create a simple department performance table
    if dept_id is None:  # Show all departments
        dept_summary = []
        departments = ["Finance", "Procurement", "IT", "HR", "Operations", "Marketing", "Sales", "Legal"]
        
        for dept_name in departments:
            dept_mapping = {
                "Finance": 1, "Procurement": 2, "IT": 3, "HR": 4, "Operations": 5,
                "Marketing": 6, "Sales": 7, "Legal": 8
            }
            current_dept_id = dept_mapping.get(dept_name)
            
            if current_dept_id:
                dept_finance = get_finance_kpis(from_date, to_date, current_dept_id)
                dept_procurement = get_procurement_kpis(from_date, to_date, current_dept_id)
                
                if not dept_finance.empty and not dept_procurement.empty:
                    fin_row = dept_finance.iloc[0]
                    proc_row = dept_procurement.iloc[0]
                    
                    dept_summary.append({
                        'Department': dept_name,
                        'Revenue': fin_row['total_revenue'],
                        'Expenses': fin_row['total_expenses'],
                        'Net Income': fin_row['net_income'],
                        'Orders': proc_row['total_orders'],
                        'Spend': proc_row['total_spend']
                    })
        
        if dept_summary:
            summary_df = pd.DataFrame(dept_summary)
            st.dataframe(
                summary_df,
                hide_index=True,
                column_config={
                    "Revenue": st.column_config.NumberColumn("Revenue ($)", format="$%.2f"),
                    "Expenses": st.column_config.NumberColumn("Expenses ($)", format="$%.2f"),
                    "Net Income": st.column_config.NumberColumn("Net Income ($)", format="$%.2f"),
                    "Orders": st.column_config.NumberColumn("Orders", format="%d"),
                    "Spend": st.column_config.NumberColumn("Spend ($)", format="$%.2f")
                }
            )
        else:
            st.info("No department performance data available for the selected period.")
    else:
        st.info("Department-specific view selected. Use 'All' departments to see department comparison.")

except Exception as e:
    st.error(f"Error loading analytics data: {str(e)}")
    st.info("Please check your database connection and try again.")

# Render global AI chat
from src.global_ai_chat import render_global_ai_chat
render_global_ai_chat()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p>📊 Business Intelligence Dashboard - Reflexta Data Intelligence</p>
    <p>Executive Analytics & Key Performance Indicators</p>
</div>
""", unsafe_allow_html=True)