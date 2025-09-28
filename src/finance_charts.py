from __future__ import annotations

"""Finance-specific chart functions with advanced visualizations."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def budget_vs_actual_chart(df: pd.DataFrame) -> go.Figure:
    """Create budget vs actual spending chart."""
    
    fig = go.Figure()
    
    # Add budget bars
    fig.add_trace(go.Bar(
        name='Budget',
        x=df['dept_name'],
        y=df['budget_amount'],
        marker_color='lightblue',
        opacity=0.7
    ))
    
    # Add actual spending bars
    fig.add_trace(go.Bar(
        name='Actual Spent',
        x=df['dept_name'],
        y=df['actual_spent'],
        marker_color='darkblue',
        opacity=0.9
    ))
    
    fig.update_layout(
        title="Budget vs Actual Spending by Department",
        xaxis_title="Department",
        yaxis_title="Amount ($)",
        barmode='group',
        height=500,
        showlegend=True
    )
    
    return fig


def budget_utilization_gauge(df: pd.DataFrame) -> go.Figure:
    """Create budget utilization gauge chart."""
    
    if df.empty:
        return go.Figure()
    
    # Calculate overall utilization
    total_budget = df['budget_amount'].sum()
    total_spent = df['actual_spent'].sum()
    utilization = (total_spent / total_budget * 100) if total_budget > 0 else 0
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=utilization,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Overall Budget Utilization (%)"},
        delta={'reference': 80},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))
    
    fig.update_layout(height=400)
    return fig


def monthly_trends_chart(df: pd.DataFrame) -> go.Figure:
    """Create monthly finance trends chart."""
    
    if df.empty:
        return go.Figure()
    
    fig = px.line(
        df,
        x='month',
        y='total_amount',
        color='transaction_type',
        title="Monthly Finance Trends",
        labels={'total_amount': 'Amount ($)', 'month': 'Month'},
        markers=True
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        hovermode='x unified'
    )
    
    return fig


def account_analysis_pie(df: pd.DataFrame) -> go.Figure:
    """Create account analysis pie chart."""
    
    if df.empty:
        return go.Figure()
    
    # Filter out zero amounts
    df_filtered = df[df['total_amount'] > 0]
    
    fig = px.pie(
        df_filtered,
        values='total_amount',
        names='account_name',
        title="Spending by Account",
        hole=0.4
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Amount: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(height=500)
    return fig


def cost_center_analysis_chart(df: pd.DataFrame) -> go.Figure:
    """Create cost center analysis chart."""
    
    if df.empty:
        return go.Figure()
    
    fig = px.bar(
        df,
        x='cost_center_name',
        y='total_amount',
        color='dept_name',
        title="Spending by Cost Center",
        labels={'total_amount': 'Total Amount ($)', 'cost_center_name': 'Cost Center'}
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Cost Center",
        yaxis_title="Total Amount ($)",
        xaxis_tickangle=-45
    )
    
    return fig


def vendor_spending_chart(df: pd.DataFrame) -> go.Figure:
    """Create vendor spending analysis chart."""
    
    if df.empty:
        return go.Figure()
    
    # Top 10 vendors by spending
    top_vendors = df.nlargest(10, 'total_amount')
    
    fig = px.bar(
        top_vendors,
        x='vendor_name',
        y='total_amount',
        title="Top 10 Vendors by Spending",
        labels={'total_amount': 'Total Amount ($)', 'vendor_name': 'Vendor'}
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Vendor",
        yaxis_title="Total Amount ($)",
        xaxis_tickangle=-45
    )
    
    return fig


def financial_health_dashboard(df: pd.DataFrame) -> go.Figure:
    """Create comprehensive financial health dashboard."""
    
    if df.empty:
        return go.Figure()
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Budget Utilization', 'Monthly Trends', 'Account Distribution', 'Department Performance'),
        specs=[[{"type": "indicator"}, {"type": "scatter"}],
               [{"type": "pie"}, {"type": "bar"}]]
    )
    
    # Budget utilization gauge
    total_budget = df['budget_amount'].sum()
    total_spent = df['actual_spent'].sum()
    utilization = (total_spent / total_budget * 100) if total_budget > 0 else 0
    
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=utilization,
        title={'text': "Budget Utilization (%)"},
        gauge={'axis': {'range': [None, 100]}}
    ), row=1, col=1)
    
    # Add other charts as needed...
    
    fig.update_layout(height=800, showlegend=False)
    return fig


def cash_flow_chart(df: pd.DataFrame) -> go.Figure:
    """Create cash flow analysis chart."""
    
    if df.empty:
        return go.Figure()
    
    # Calculate cumulative cash flow
    df_sorted = df.sort_values('month')
    df_sorted['cumulative_flow'] = df_sorted['total_amount'].cumsum()
    
    fig = go.Figure()
    
    # Add monthly cash flow
    fig.add_trace(go.Bar(
        name='Monthly Flow',
        x=df_sorted['month'],
        y=df_sorted['total_amount'],
        marker_color='lightblue'
    ))
    
    # Add cumulative line
    fig.add_trace(go.Scatter(
        name='Cumulative Flow',
        x=df_sorted['month'],
        y=df_sorted['cumulative_flow'],
        mode='lines+markers',
        line=dict(color='red', width=3),
        yaxis='y2'
    ))
    
    fig.update_layout(
        title="Cash Flow Analysis",
        xaxis_title="Month",
        yaxis_title="Monthly Amount ($)",
        yaxis2=dict(title="Cumulative Amount ($)", overlaying="y", side="right"),
        height=500
    )
    
    return fig
