from __future__ import annotations

import datetime as dt

import streamlit as st

from src.db import health_check
from src.finance_queries import (
    get_finance_summary,
    get_finance_monthly_trends,
    get_finance_kpis,
    get_finance_transactions,
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
    
    # Interactive Charts with Drill-Down
    st.markdown('<div class="section-header">Interactive Analytics</div>', unsafe_allow_html=True)
    
    # Get finance transactions for drill-down
    finance_data = get_finance_transactions(from_date, to_date, dept_id, transaction_type)
    
    if not finance_data.empty:
        # Create tabs for different chart types
        tab1, tab2, tab3 = st.tabs([
            "🏢 Department Analysis", 
            "📅 Monthly Trends", 
            "📊 Category Breakdown"
        ])
        
        with tab1:
            st.markdown("### Department Spending with Drill-Down")
            st.markdown("**Click on any department bar to see detailed breakdown**")
            
            # Prepare department data
            dept_data = finance_data.groupby('department')['amount'].sum().reset_index()
            dept_data = dept_data.sort_values('amount', ascending=False)
            
            # Create department chart with drill-down
            import plotly.express as px
            import plotly.graph_objects as go
            
            fig = px.bar(
                dept_data,
                x='department',
                y='amount',
                title="Department Spending Overview",
                color='amount',
                color_continuous_scale='Blues',
                hover_data={'amount': ':$,.0f'}
            )
            
            # Add click functionality
            fig.update_traces(
                hovertemplate="<b>%{x}</b><br>Total: $%{y:,.0f}<br><extra></extra>",
                customdata=dept_data['department'].tolist()
            )
            
            # Configure layout
            fig.update_layout(
                title={
                    'text': "Department Spending Overview",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#1e293b'}
                },
                xaxis_title="Department",
                yaxis_title="Total Spending ($)",
                hovermode='closest',
                clickmode='event+select',
                height=500,
                showlegend=False
            )
            
            # Display the chart
            st.plotly_chart(fig, use_container_width=True, key="dept_chart")
            
            # Handle drill-down
            if st.session_state.get('dept_chart_click'):
                clicked_data = st.session_state['dept_chart_click']
                if clicked_data and 'points' in clicked_data:
                    point = clicked_data['points'][0]
                    selected_dept = point.get('x', '')
                    
                    st.markdown(f"#### 🔍 Drill-Down: {selected_dept}")
                    
                    # Filter data for selected department
                    filtered_data = finance_data[finance_data['department'] == selected_dept]
                    
                    if not filtered_data.empty:
                        # Show detailed transactions
                        st.markdown("#### 📋 Detailed Transactions")
                        st.dataframe(
                            filtered_data[['date', 'description', 'amount', 'category', 'status']],
                            use_container_width=True
                        )
        
        with tab2:
            st.markdown("### Monthly Spending Trends with Drill-Down")
            st.markdown("**Click on any month point to see daily breakdown**")
            
            # Prepare monthly data
            finance_data['month'] = pd.to_datetime(finance_data['date']).dt.to_period('M')
            monthly_data = finance_data.groupby('month')['amount'].sum().reset_index()
            monthly_data['month_str'] = monthly_data['month'].astype(str)
            
            # Create monthly trend chart
            trend_fig = px.line(
                monthly_data,
                x='month_str',
                y='amount',
                title="Monthly Spending Trends",
                markers=True,
                line_shape='spline'
            )
            
            # Add click functionality
            trend_fig.update_traces(
                hovertemplate="<b>%{x}</b><br>Total: $%{y:,.0f}<br><extra></extra>",
                customdata=monthly_data['month'].tolist()
            )
            
            # Configure layout
            trend_fig.update_layout(
                title={
                    'text': "Monthly Spending Trends",
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
            st.plotly_chart(trend_fig, use_container_width=True, key="trend_chart")
            
            # Handle drill-down
            if st.session_state.get('trend_chart_click'):
                clicked_data = st.session_state['trend_chart_click']
                if clicked_data and 'points' in clicked_data:
                    point = clicked_data['points'][0]
                    selected_month = point.get('x', '')
                    
                    st.markdown(f"#### 🔍 Drill-Down: {selected_month}")
                    
                    # Filter data for selected month
                    month_data = finance_data[pd.to_datetime(finance_data['date']).dt.to_period('M').astype(str) == selected_month]
                    
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
                            title=f"Daily Spending for {selected_month}",
                            color='amount',
                            color_continuous_scale='Oranges'
                        )
                        
                        daily_fig.update_layout(
                            height=400,
                            showlegend=False,
                            title={
                                'text': f"Daily Spending for {selected_month}",
                                'x': 0.5,
                                'xanchor': 'center'
                            }
                        )
                        
                        st.plotly_chart(daily_fig, use_container_width=True)
        
        with tab3:
            st.markdown("### Category Spending Breakdown with Drill-Down")
            st.markdown("**Click on any category slice to see detailed breakdown**")
            
            # Prepare category data
            category_data = finance_data.groupby('category')['amount'].sum().reset_index()
            category_data = category_data.sort_values('amount', ascending=False)
            
            # Create category pie chart
            category_fig = px.pie(
                category_data,
                values='amount',
                names='category',
                title="Spending by Category",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            # Add click functionality
            category_fig.update_traces(
                hovertemplate="<b>%{label}</b><br>Amount: $%{value:,.0f}<br>Percentage: %{percent}<br><extra></extra>",
                customdata=category_data['category'].tolist()
            )
            
            # Configure layout
            category_fig.update_layout(
                title={
                    'text': "Spending by Category",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 16, 'color': '#1e293b'}
                },
                hovermode='closest',
                clickmode='event+select',
                height=500
            )
            
            # Display the chart
            st.plotly_chart(category_fig, use_container_width=True, key="category_chart")
            
            # Handle drill-down
            if st.session_state.get('category_chart_click'):
                clicked_data = st.session_state['category_chart_click']
                if clicked_data and 'points' in clicked_data:
                    point = clicked_data['points'][0]
                    selected_category = point.get('label', '')
                    
                    st.markdown(f"#### 🔍 Drill-Down: {selected_category}")
                    
                    # Filter data for selected category
                    category_items = finance_data[finance_data['category'] == selected_category]
                    
                    if not category_items.empty:
                        # Show category summary
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric(
                                "Total Items",
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
                                "Average Item",
                                f"${category_items['amount'].mean():,.0f}",
                                delta=None
                            )
                        
                        # Show detailed items
                        st.markdown("#### 📋 Item Details")
                        st.dataframe(
                            category_items[['date', 'description', 'amount', 'department', 'status']],
                            use_container_width=True
                        )

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

# Render sidebar AI chat
from src.sidebar_ai_chat import render_sidebar_ai_chat
render_sidebar_ai_chat()