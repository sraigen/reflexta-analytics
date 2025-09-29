from __future__ import annotations

"""Procurement-specific chart functions with advanced visualizations."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def vendor_performance_chart(df: pd.DataFrame) -> go.Figure:
    """Create vendor performance analysis chart."""
    
    if df.empty:
        return go.Figure()
    
    # Handle None values and ensure proper data types
    df_clean = df.copy()
    df_clean['total_orders'] = df_clean['total_orders'].fillna(0)
    df_clean['completion_rate'] = df_clean['completion_rate'].fillna(0)
    df_clean['total_value'] = df_clean['total_value'].fillna(0)
    df_clean['rating'] = df_clean['rating'].fillna(0)
    
    # Ensure size values are positive numbers
    df_clean['size_value'] = df_clean['total_value'].apply(lambda x: max(0, float(x)) if pd.notna(x) else 0)
    
    fig = px.scatter(
        df_clean,
        x='total_orders',
        y='completion_rate',
        size='size_value',
        color='rating',
        hover_name='vendor_name',
        title="Vendor Performance Analysis",
        labels={
            'total_orders': 'Total Orders',
            'completion_rate': 'Completion Rate (%)',
            'size_value': 'Total Value ($)',
            'rating': 'Vendor Rating'
        }
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Total Orders",
        yaxis_title="Completion Rate (%)"
    )
    
    return fig


def procurement_trends_chart(df: pd.DataFrame, group_by: str = "month") -> go.Figure:
    """Create procurement trends over time."""
    
    if df.empty:
        return go.Figure()
    
    # Determine the correct x-axis column based on available columns
    x_column = None
    if "month_name" in df.columns:
        x_column = "month_name"
    elif "quarter_name" in df.columns:
        x_column = "quarter_name"
    elif "week_name" in df.columns:
        x_column = "week_name"
    elif "month" in df.columns:
        x_column = "month"
    elif "quarter" in df.columns:
        x_column = "quarter"
    elif "week" in df.columns:
        x_column = "week"
    else:
        # Fallback to first available column that looks like a date/time column
        for col in df.columns:
            if col in ['year', 'month', 'quarter', 'week', 'month_name', 'quarter_name', 'week_name']:
                x_column = col
                break
    
    if x_column is None:
        return go.Figure()
    
    fig = px.line(
        df,
        x=x_column,
        y='total_value',
        title=f"Procurement Trends by {group_by.title()}",
        labels={'total_value': 'Total Value ($)', x_column: group_by.title()},
        markers=True
    )
    
    fig.update_layout(
        height=500,
        xaxis_title=group_by.title(),
        yaxis_title="Total Value ($)"
    )
    
    return fig


def category_spending_pie(df: pd.DataFrame) -> go.Figure:
    """Create category spending pie chart."""
    
    if df.empty:
        return go.Figure()
    
    # Filter out zero amounts
    df_filtered = df[df['total_value'] > 0]
    
    fig = px.pie(
        df_filtered,
        values='total_value',
        names='category_name',
        title="Spending by Category",
        hole=0.4
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Value: $%{value:,.0f}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(height=500)
    return fig


def department_procurement_chart(df: pd.DataFrame) -> go.Figure:
    """Create department procurement analysis chart."""
    
    if df.empty:
        return go.Figure()
    
    fig = px.bar(
        df,
        x='dept_name',
        y='total_value',
        color='completion_rate',
        title="Department Procurement Performance",
        labels={
            'dept_name': 'Department',
            'total_value': 'Total Value ($)',
            'completion_rate': 'Completion Rate (%)'
        },
        color_continuous_scale='RdYlGn'
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Department",
        yaxis_title="Total Value ($)"
    )
    
    return fig


def delivery_performance_chart(df: pd.DataFrame) -> go.Figure:
    """Create delivery performance analysis chart."""
    
    if df.empty:
        return go.Figure()
    
    fig = go.Figure()
    
    # Add on-time deliveries
    fig.add_trace(go.Bar(
        name='On Time',
        x=df['vendor_name'],
        y=df['on_time_deliveries'],
        marker_color='green',
        opacity=0.7
    ))
    
    # Add late deliveries (if column exists)
    if 'late_deliveries' in df.columns:
        fig.add_trace(go.Bar(
            name='Late',
            x=df['vendor_name'],
            y=df['late_deliveries'],
            marker_color='red',
            opacity=0.7
        ))
    
    fig.update_layout(
        title="Delivery Performance by Vendor",
        xaxis_title="Vendor",
        yaxis_title="Number of Deliveries",
        barmode='stack',
        height=500,
        xaxis_tickangle=-45
    )
    
    return fig


def procurement_kpi_gauge(df: pd.DataFrame, metric: str = "completion_rate") -> go.Figure:
    """Create procurement KPI gauge chart."""
    
    if df.empty:
        return go.Figure()
    
    # Calculate overall metric
    if metric == "completion_rate":
        value = df['completion_rate'].mean()
        title = "Overall Completion Rate (%)"
    elif metric == "avg_order_value":
        value = df['avg_order_value'].mean()
        title = "Average Order Value ($)"
    else:
        value = 0
        title = "Metric"
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': title},
        gauge={
            'axis': {'range': [None, 100] if metric == "completion_rate" else [None, value * 2]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 50], 'color': "lightgray"},
                {'range': [50, 80], 'color': "yellow"},
                {'range': [80, 100], 'color': "green"}
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


def procurement_heatmap(df: pd.DataFrame) -> go.Figure:
    """Create procurement heatmap by department and category."""
    
    if df.empty:
        return go.Figure()
    
    # Pivot data for heatmap
    pivot_df = df.pivot_table(
        values='total_value',
        index='dept_name',
        columns='category_name',
        fill_value=0
    )
    
    fig = px.imshow(
        pivot_df,
        title="Procurement Heatmap: Department vs Category",
        labels={'x': 'Category', 'y': 'Department', 'color': 'Total Value ($)'},
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Category",
        yaxis_title="Department"
    )
    
    return fig


def order_status_distribution(df: pd.DataFrame) -> go.Figure:
    """Create order status distribution chart."""
    
    if df.empty:
        return go.Figure()
    
    # Count orders by status
    status_counts = df['status'].value_counts()
    
    fig = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        title="Order Status Distribution",
        hole=0.4
    )
    
    fig.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>'
    )
    
    fig.update_layout(height=500)
    return fig


def priority_analysis_chart(df: pd.DataFrame) -> go.Figure:
    """Create priority analysis chart."""
    
    if df.empty:
        return go.Figure()
    
    # Count orders by priority
    priority_counts = df['priority'].value_counts()
    
    fig = px.bar(
        x=priority_counts.index,
        y=priority_counts.values,
        title="Orders by Priority",
        labels={'x': 'Priority', 'y': 'Number of Orders'},
        color=priority_counts.values,
        color_continuous_scale='Reds'
    )
    
    fig.update_layout(
        height=500,
        xaxis_title="Priority Level",
        yaxis_title="Number of Orders"
    )
    
    return fig


def procurement_dashboard(df_summary: pd.DataFrame, df_trends: pd.DataFrame, df_vendors: pd.DataFrame) -> go.Figure:
    """Create comprehensive procurement dashboard."""
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Department Performance', 'Vendor Analysis', 'Monthly Trends', 'Category Distribution'),
        specs=[[{"type": "bar"}, {"type": "scatter"}],
               [{"type": "scatter"}, {"type": "pie"}]]
    )
    
    # Department performance
    if not df_summary.empty:
        fig.add_trace(go.Bar(
            x=df_summary['dept_name'],
            y=df_summary['total_value'],
            name='Total Value',
            marker_color='lightblue'
        ), row=1, col=1)
    
    # Vendor analysis
    if not df_vendors.empty:
        fig.add_trace(go.Scatter(
            x=df_vendors['total_orders'],
            y=df_vendors['completion_rate'],
            mode='markers',
            marker=dict(size=df_vendors['total_value']/1000, color=df_vendors['rating']),
            name='Vendors',
            text=df_vendors['vendor_name']
        ), row=1, col=2)
    
    # Monthly trends
    if not df_trends.empty:
        fig.add_trace(go.Scatter(
            x=df_trends['month'],
            y=df_trends['total_value'],
            mode='lines+markers',
            name='Monthly Value'
        ), row=2, col=1)
    
    fig.update_layout(height=800, showlegend=False)
    return fig
