"""
Advanced Analytics Charts for Enterprise Dashboard
Professional visualizations with enhanced styling and interactivity.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


# Professional color palette
PROFESSIONAL_COLORS = [
    "#2E86AB",  # Professional Blue
    "#A23B72",  # Deep Purple
    "#F18F01",  # Golden Orange
    "#C73E1D",  # Deep Red
    "#2D5016",  # Forest Green
    "#6B5B95",  # Purple
    "#F7DC6F",  # Light Yellow
    "#BB8FCE",  # Light Purple
    "#85C1E9",  # Light Blue
    "#F8C471",  # Light Orange
]


def executive_summary_chart(df: pd.DataFrame) -> go.Figure:
    """Create executive summary dashboard chart."""
    
    if df.empty:
        return go.Figure()
    
    row = df.iloc[0]
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Revenue vs Expenses", "Budget Utilization", "Procurement Performance", "Financial Health"),
        specs=[[{"type": "bar"}, {"type": "indicator"}],
               [{"type": "bar"}, {"type": "indicator"}]]
    )
    
    # Revenue vs Expenses
    fig.add_trace(
        go.Bar(
            x=["Revenue", "Expenses"],
            y=[row["total_revenue"], row["total_expenses"]],
            marker_color=[PROFESSIONAL_COLORS[0], PROFESSIONAL_COLORS[3]],
            name="Financial Performance",
            showlegend=False
        ),
        row=1, col=1
    )
    
    # Budget Utilization Gauge
    budget_util = row["budget_utilization_pct"]
    fig.add_trace(
        go.Indicator(
            mode="gauge+number+delta",
            value=budget_util,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Budget Utilization (%)"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': PROFESSIONAL_COLORS[0]},
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
        ),
        row=1, col=2
    )
    
    # Procurement Performance
    fig.add_trace(
        go.Bar(
            x=["Total Orders", "Completed Orders"],
            y=[row["total_orders"], row["completed_orders"]],
            marker_color=[PROFESSIONAL_COLORS[1], PROFESSIONAL_COLORS[4]],
            name="Procurement Performance",
            showlegend=False
        ),
        row=2, col=1
    )
    
    # Financial Health Score
    health_score = min(100, max(0, (row["net_profit"] / max(row["total_revenue"], 1)) * 100))
    fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=health_score,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Financial Health Score"},
            gauge={
                'axis': {'range': [None, 100]},
                'bar': {'color': PROFESSIONAL_COLORS[4]},
                'steps': [
                    {'range': [0, 30], 'color': "red"},
                    {'range': [30, 60], 'color': "yellow"},
                    {'range': [60, 100], 'color': "green"}
                ]
            }
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=600,
        showlegend=False,
        title_text="Executive Summary Dashboard",
        title_x=0.5,
        font=dict(size=12)
    )
    
    return fig


def department_performance_chart(df: pd.DataFrame) -> go.Figure:
    """Create department performance comparison chart."""
    
    if df.empty:
        return go.Figure()
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Budget Utilization by Department", "Revenue by Department", 
                       "Procurement Value by Department", "Order Completion Rate"),
        specs=[[{"type": "bar"}, {"type": "bar"}],
               [{"type": "bar"}, {"type": "bar"}]]
    )
    
    # Budget Utilization
    fig.add_trace(
        go.Bar(
            x=df["dept_name"],
            y=df["budget_utilization_pct"],
            marker_color=PROFESSIONAL_COLORS[0],
            name="Budget Utilization %",
            showlegend=False
        ),
        row=1, col=1
    )
    
    # Revenue
    fig.add_trace(
        go.Bar(
            x=df["dept_name"],
            y=df["revenue"],
            marker_color=PROFESSIONAL_COLORS[1],
            name="Revenue",
            showlegend=False
        ),
        row=1, col=2
    )
    
    # Procurement Value
    fig.add_trace(
        go.Bar(
            x=df["dept_name"],
            y=df["procurement_value"],
            marker_color=PROFESSIONAL_COLORS[2],
            name="Procurement Value",
            showlegend=False
        ),
        row=2, col=1
    )
    
    # Order Completion Rate
    fig.add_trace(
        go.Bar(
            x=df["dept_name"],
            y=df["order_completion_rate"],
            marker_color=PROFESSIONAL_COLORS[4],
            name="Completion Rate %",
            showlegend=False
        ),
        row=2, col=2
    )
    
    fig.update_layout(
        height=700,
        showlegend=False,
        title_text="Department Performance Analysis",
        title_x=0.5,
        font=dict(size=12)
    )
    
    # Update axes
    fig.update_xaxes(tickangle=45)
    fig.update_yaxes(title_text="Budget Utilization %", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($)", row=1, col=2)
    fig.update_yaxes(title_text="Procurement Value ($)", row=2, col=1)
    fig.update_yaxes(title_text="Completion Rate %", row=2, col=2)
    
    return fig


def vendor_performance_radar_chart(df: pd.DataFrame) -> go.Figure:
    """Create vendor performance radar chart."""
    
    if df.empty:
        return go.Figure()
    
    # Select top 5 vendors by total value
    top_vendors = df.nlargest(5, "total_value")
    
    fig = go.Figure()
    
    for i, (_, vendor) in enumerate(top_vendors.iterrows()):
        fig.add_trace(go.Scatterpolar(
            r=[
                vendor["rating"],
                vendor["completion_rate"],
                100 - vendor["cancellation_rate"],  # Invert cancellation rate
                min(100, vendor["total_orders"] / 10),  # Normalize order count
                min(100, vendor["avg_order_value"] / 1000)  # Normalize order value
            ],
            theta=['Rating', 'Completion Rate', 'Reliability', 'Order Volume', 'Order Value'],
            fill='toself',
            name=vendor["vendor_name"],
            line_color=PROFESSIONAL_COLORS[i % len(PROFESSIONAL_COLORS)]
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        title="Top 5 Vendors Performance Comparison",
        font=dict(size=12)
    )
    
    return fig


def financial_trends_chart(df: pd.DataFrame) -> go.Figure:
    """Create financial trends over time chart."""
    
    if df.empty:
        return go.Figure()
    
    fig = go.Figure()
    
    # Group by transaction type
    for i, transaction_type in enumerate(df["transaction_type"].unique()):
        type_data = df[df["transaction_type"] == transaction_type]
        
        fig.add_trace(go.Scatter(
            x=type_data["month"],
            y=type_data["total_amount"],
            mode='lines+markers',
            name=transaction_type,
            line=dict(color=PROFESSIONAL_COLORS[i % len(PROFESSIONAL_COLORS)], width=3),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title="Financial Trends Over Time",
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        hovermode='x unified',
        font=dict(size=12),
        height=500
    )
    
    return fig


def budget_vs_actual_chart(df: pd.DataFrame) -> go.Figure:
    """Create budget vs actual analysis chart."""
    
    if df.empty:
        return go.Figure()
    
    # Create horizontal bar chart
    fig = go.Figure()
    
    # Budget amounts
    fig.add_trace(go.Bar(
        y=df["budget_name"],
        x=df["budget_amount"],
        orientation='h',
        name='Budgeted Amount',
        marker_color=PROFESSIONAL_COLORS[0],
        text=df["budget_amount"],
        textposition='auto'
    ))
    
    # Spent amounts
    fig.add_trace(go.Bar(
        y=df["budget_name"],
        x=df["spent_amount"],
        orientation='h',
        name='Spent Amount',
        marker_color=PROFESSIONAL_COLORS[3],
        text=df["spent_amount"],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Budget vs Actual Spending Analysis",
        xaxis_title="Amount ($)",
        yaxis_title="Budget",
        barmode='group',
        height=max(400, len(df) * 40),
        font=dict(size=12)
    )
    
    return fig


def category_spending_pie_chart(df: pd.DataFrame) -> go.Figure:
    """Create category spending pie chart."""
    
    if df.empty:
        return go.Figure()
    
    fig = go.Figure(data=[go.Pie(
        labels=df["category_name"],
        values=df["total_spending"],
        hole=0.4,
        marker_colors=PROFESSIONAL_COLORS[:len(df)],
        textinfo='label+percent',
        textposition='auto'
    )])
    
    fig.update_layout(
        title="Spending Distribution by Category",
        font=dict(size=12),
        height=500
    )
    
    return fig


def procurement_trends_chart(df: pd.DataFrame) -> go.Figure:
    """Create procurement trends over time chart."""
    
    if df.empty:
        return go.Figure()
    
    fig = go.Figure()
    
    # Group by status
    for i, status in enumerate(df["status"].unique()):
        status_data = df[df["status"] == status]
        
        fig.add_trace(go.Scatter(
            x=status_data["month"],
            y=status_data["total_value"],
            mode='lines+markers',
            name=status,
            line=dict(color=PROFESSIONAL_COLORS[i % len(PROFESSIONAL_COLORS)], width=3),
            marker=dict(size=8)
        ))
    
    fig.update_layout(
        title="Procurement Trends Over Time",
        xaxis_title="Month",
        yaxis_title="Value ($)",
        hovermode='x unified',
        font=dict(size=12),
        height=500
    )
    
    return fig


def performance_heatmap(df: pd.DataFrame) -> go.Figure:
    """Create performance heatmap."""
    
    if df.empty:
        return go.Figure()
    
    # Create pivot table for heatmap
    pivot_data = df.pivot_table(
        values=['completion_rate', 'budget_utilization_pct'],
        index='dept_name',
        aggfunc='mean'
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=pivot_data.values,
        x=['Completion Rate', 'Budget Utilization'],
        y=pivot_data.index,
        colorscale='RdYlGn',
        showscale=True
    ))
    
    fig.update_layout(
        title="Department Performance Heatmap",
        xaxis_title="Metrics",
        yaxis_title="Department",
        font=dict(size=12),
        height=400
    )
    
    return fig
