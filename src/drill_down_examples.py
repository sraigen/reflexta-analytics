#!/usr/bin/env python3
"""
Drill-Down Implementation Examples for Reflexta Analytics Platform
Practical examples of how to implement interactive drill-down features.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from typing import Dict, List, Optional, Any
from datetime import date, datetime


def create_department_drill_down(data: pd.DataFrame) -> None:
    """
    Example: Department Spending with Drill-Down
    Click on a department to see sub-department breakdown.
    """
    st.markdown("### 🏢 Department Spending with Drill-Down")
    st.markdown("**Click on any department bar to see detailed breakdown**")
    
    # Prepare department data
    dept_data = data.groupby('department')['amount'].sum().reset_index()
    dept_data = dept_data.sort_values('amount', ascending=False)
    
    # Create the main chart
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
            filtered_data = data[data['department'] == selected_dept]
            
            if not filtered_data.empty:
                # Show sub-department breakdown
                sub_dept_data = filtered_data.groupby('sub_department')['amount'].sum().reset_index()
                sub_dept_data = sub_dept_data.sort_values('amount', ascending=False)
                
                # Create sub-department chart
                sub_fig = px.bar(
                    sub_dept_data,
                    x='sub_department',
                    y='amount',
                    title=f"Sub-Departments in {selected_dept}",
                    color='amount',
                    color_continuous_scale='Greens'
                )
                
                sub_fig.update_layout(
                    height=400,
                    showlegend=False,
                    title={
                        'text': f"Sub-Departments in {selected_dept}",
                        'x': 0.5,
                        'xanchor': 'center'
                    }
                )
                
                st.plotly_chart(sub_fig, use_container_width=True)
                
                # Show detailed transactions
                st.markdown("#### 📋 Detailed Transactions")
                st.dataframe(
                    filtered_data[['date', 'description', 'amount', 'category', 'status']],
                    use_container_width=True
                )


def create_monthly_drill_down(data: pd.DataFrame) -> None:
    """
    Example: Monthly Trends with Drill-Down
    Click on a month to see daily breakdown.
    """
    st.markdown("### 📅 Monthly Trends with Drill-Down")
    st.markdown("**Click on any month point to see daily breakdown**")
    
    # Prepare monthly data
    data['month'] = pd.to_datetime(data['date']).dt.to_period('M')
    monthly_data = data.groupby('month')['amount'].sum().reset_index()
    monthly_data['month_str'] = monthly_data['month'].astype(str)
    
    # Create the main chart
    fig = px.line(
        monthly_data,
        x='month_str',
        y='amount',
        title="Monthly Spending Trends",
        markers=True,
        line_shape='spline'
    )
    
    # Add click functionality
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Total: $%{y:,.0f}<br><extra></extra>",
        customdata=monthly_data['month'].tolist()
    )
    
    # Configure layout
    fig.update_layout(
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
    st.plotly_chart(fig, use_container_width=True, key="monthly_chart")
    
    # Handle drill-down
    if st.session_state.get('monthly_chart_click'):
        clicked_data = st.session_state['monthly_chart_click']
        if clicked_data and 'points' in clicked_data:
            point = clicked_data['points'][0]
            selected_month = point.get('x', '')
            
            st.markdown(f"#### 🔍 Drill-Down: {selected_month}")
            
            # Filter data for selected month
            month_data = data[pd.to_datetime(data['date']).dt.to_period('M').astype(str) == selected_month]
            
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
                
                # Show daily summary
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Total Days",
                        len(daily_data),
                        delta=None
                    )
                
                with col2:
                    st.metric(
                        "Average Daily",
                        f"${daily_data['amount'].mean():,.0f}",
                        delta=None
                    )
                
                with col3:
                    st.metric(
                        "Peak Day",
                        f"${daily_data['amount'].max():,.0f}",
                        delta=None
                    )


def create_vendor_drill_down(data: pd.DataFrame) -> None:
    """
    Example: Vendor Performance with Drill-Down
    Click on a vendor to see their order history.
    """
    st.markdown("### 🏪 Vendor Performance with Drill-Down")
    st.markdown("**Click on any vendor bar to see their order history**")
    
    # Prepare vendor data
    vendor_data = data.groupby('vendor_name').agg({
        'amount': 'sum',
        'order_id': 'count'
    }).reset_index()
    vendor_data.columns = ['vendor', 'total_spend', 'order_count']
    vendor_data = vendor_data.sort_values('total_spend', ascending=False).head(10)
    
    # Create the main chart
    fig = px.bar(
        vendor_data,
        x='vendor',
        y='total_spend',
        title="Top Vendors by Total Spend",
        color='total_spend',
        color_continuous_scale='Purples',
        hover_data={'total_spend': ':$,.0f', 'order_count': True}
    )
    
    # Add click functionality
    fig.update_traces(
        hovertemplate="<b>%{x}</b><br>Spend: $%{y:,.0f}<br>Orders: %{customdata[1]}<br><extra></extra>",
        customdata=vendor_data[['total_spend', 'order_count']].values.tolist()
    )
    
    # Configure layout
    fig.update_layout(
        title={
            'text': "Top Vendors by Total Spend",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 16, 'color': '#1e293b'}
        },
        xaxis_title="Vendor",
        yaxis_title="Total Spend ($)",
        hovermode='closest',
        clickmode='event+select',
        height=500,
        showlegend=False
    )
    
    # Display the chart
    st.plotly_chart(fig, use_container_width=True, key="vendor_chart")
    
    # Handle drill-down
    if st.session_state.get('vendor_chart_click'):
        clicked_data = st.session_state['vendor_chart_click']
        if clicked_data and 'points' in clicked_data:
            point = clicked_data['points'][0]
            selected_vendor = point.get('x', '')
            
            st.markdown(f"#### 🔍 Drill-Down: {selected_vendor}")
            
            # Filter data for selected vendor
            vendor_orders = data[data['vendor_name'] == selected_vendor]
            
            if not vendor_orders.empty:
                # Show vendor performance metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Total Orders",
                        len(vendor_orders),
                        delta=None
                    )
                
                with col2:
                    st.metric(
                        "Total Spend",
                        f"${vendor_orders['amount'].sum():,.0f}",
                        delta=None
                    )
                
                with col3:
                    st.metric(
                        "Average Order",
                        f"${vendor_orders['amount'].mean():,.0f}",
                        delta=None
                    )
                
                with col4:
                    st.metric(
                        "Largest Order",
                        f"${vendor_orders['amount'].max():,.0f}",
                        delta=None
                    )
                
                # Show order timeline
                timeline_data = vendor_orders.groupby(pd.to_datetime(vendor_orders['date']).dt.date)['amount'].sum().reset_index()
                timeline_data.columns = ['date', 'amount']
                timeline_data = timeline_data.sort_values('date')
                
                timeline_fig = px.line(
                    timeline_data,
                    x='date',
                    y='amount',
                    title=f"Order Timeline for {selected_vendor}",
                    markers=True
                )
                
                timeline_fig.update_layout(
                    height=400,
                    title={
                        'text': f"Order Timeline for {selected_vendor}",
                        'x': 0.5,
                        'xanchor': 'center'
                    }
                )
                
                st.plotly_chart(timeline_fig, use_container_width=True)
                
                # Show detailed orders
                st.markdown("#### 📋 Order Details")
                st.dataframe(
                    vendor_orders[['date', 'order_id', 'amount', 'category', 'status']],
                    use_container_width=True
                )


def create_category_drill_down(data: pd.DataFrame) -> None:
    """
    Example: Category Breakdown with Drill-Down
    Click on a category to see subcategory details.
    """
    st.markdown("### 📊 Category Breakdown with Drill-Down")
    st.markdown("**Click on any category slice to see subcategory details**")
    
    # Prepare category data
    category_data = data.groupby('category')['amount'].sum().reset_index()
    category_data = category_data.sort_values('amount', ascending=False)
    
    # Create the main chart
    fig = px.pie(
        category_data,
        values='amount',
        names='category',
        title="Spending by Category",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # Add click functionality
    fig.update_traces(
        hovertemplate="<b>%{label}</b><br>Amount: $%{value:,.0f}<br>Percentage: %{percent}<br><extra></extra>",
        customdata=category_data['category'].tolist()
    )
    
    # Configure layout
    fig.update_layout(
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
    st.plotly_chart(fig, use_container_width=True, key="category_chart")
    
    # Handle drill-down
    if st.session_state.get('category_chart_click'):
        clicked_data = st.session_state['category_chart_click']
        if clicked_data and 'points' in clicked_data:
            point = clicked_data['points'][0]
            selected_category = point.get('label', '')
            
            st.markdown(f"#### 🔍 Drill-Down: {selected_category}")
            
            # Filter data for selected category
            category_items = data[data['category'] == selected_category]
            
            if not category_items.empty:
                # Show subcategory breakdown
                subcategory_data = category_items.groupby('subcategory')['amount'].sum().reset_index()
                subcategory_data = subcategory_data.sort_values('amount', ascending=False)
                
                # Create subcategory chart
                sub_fig = px.bar(
                    subcategory_data,
                    x='subcategory',
                    y='amount',
                    title=f"Subcategories in {selected_category}",
                    color='amount',
                    color_continuous_scale='Reds'
                )
                
                sub_fig.update_layout(
                    height=400,
                    showlegend=False,
                    title={
                        'text': f"Subcategories in {selected_category}",
                        'x': 0.5,
                        'xanchor': 'center'
                    }
                )
                
                st.plotly_chart(sub_fig, use_container_width=True)
                
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
                    category_items[['date', 'description', 'amount', 'vendor_name', 'status']],
                    use_container_width=True
                )


def create_cross_chart_filtering(data: pd.DataFrame) -> None:
    """
    Example: Cross-Chart Filtering
    Click on one chart to filter all other charts.
    """
    st.markdown("### 🔄 Cross-Chart Filtering")
    st.markdown("**Click on any chart element to filter all other charts**")
    
    # Initialize session state for filters
    if 'cross_filter' not in st.session_state:
        st.session_state['cross_filter'] = {}
    
    # Create filter controls
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏢 Filter by Department"):
            st.session_state['cross_filter']['type'] = 'department'
    
    with col2:
        if st.button("📅 Filter by Month"):
            st.session_state['cross_filter']['type'] = 'month'
    
    with col3:
        if st.button("🔄 Clear Filters"):
            st.session_state['cross_filter'] = {}
            st.rerun()
    
    # Apply filters to data
    filtered_data = data.copy()
    
    if st.session_state['cross_filter'].get('type') == 'department':
        selected_dept = st.selectbox(
            "Select Department",
            data['department'].unique(),
            key="dept_filter"
        )
        filtered_data = filtered_data[filtered_data['department'] == selected_dept]
    
    elif st.session_state['cross_filter'].get('type') == 'month':
        data['month'] = pd.to_datetime(data['date']).dt.to_period('M')
        selected_month = st.selectbox(
            "Select Month",
            data['month'].unique(),
            key="month_filter"
        )
        filtered_data = filtered_data[data['month'] == selected_month]
    
    # Show filtered charts
    if not filtered_data.empty:
        st.markdown("#### 📊 Filtered Charts")
        
        # Department chart
        dept_data = filtered_data.groupby('department')['amount'].sum().reset_index()
        dept_fig = px.bar(dept_data, x='department', y='amount', title="Department Spending (Filtered)")
        st.plotly_chart(dept_fig, use_container_width=True)
        
        # Category chart
        category_data = filtered_data.groupby('category')['amount'].sum().reset_index()
        category_fig = px.pie(category_data, values='amount', names='category', title="Category Breakdown (Filtered)")
        st.plotly_chart(category_fig, use_container_width=True)
        
        # Monthly trend
        monthly_data = filtered_data.groupby(pd.to_datetime(filtered_data['date']).dt.to_period('M'))['amount'].sum().reset_index()
        monthly_data.columns = ['month', 'amount']
        monthly_fig = px.line(monthly_data, x='month', y='amount', title="Monthly Trend (Filtered)")
        st.plotly_chart(monthly_fig, use_container_width=True)
    else:
        st.warning("No data available for the selected filters.")


def render_drill_down_examples(data: pd.DataFrame) -> None:
    """
    Render all drill-down examples in a tabbed interface.
    """
    st.markdown("## 🔍 Interactive Drill-Down Examples")
    st.markdown("**Click on any chart element to see detailed breakdowns**")
    
    # Create tabs for different examples
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏢 Department Drill-Down",
        "📅 Monthly Drill-Down", 
        "🏪 Vendor Drill-Down",
        "📊 Category Drill-Down",
        "🔄 Cross-Chart Filtering"
    ])
    
    with tab1:
        create_department_drill_down(data)
    
    with tab2:
        create_monthly_drill_down(data)
    
    with tab3:
        create_vendor_drill_down(data)
    
    with tab4:
        create_category_drill_down(data)
    
    with tab5:
        create_cross_chart_filtering(data)
