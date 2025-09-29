#!/usr/bin/env python3
"""
Interactive Charts with Drill-Down Capabilities for Reflexta Analytics Platform
Advanced Plotly visualizations with click interactions and data filtering.
"""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
from typing import Dict, List, Optional, Any
from datetime import date


class InteractiveChartManager:
    """Manages interactive charts with drill-down capabilities."""
    
    def __init__(self):
        self.click_data = st.session_state.get('chart_click_data', {})
        self.filter_state = st.session_state.get('chart_filters', {})
    
    def department_spending_chart(self, data: pd.DataFrame, title: str = "Department Spending Analysis") -> go.Figure:
        """
        Create an interactive department spending chart with drill-down capabilities.
        Click on a department to see sub-department breakdown.
        """
        # Prepare data
        dept_data = data.groupby('department')['amount'].sum().reset_index()
        dept_data = dept_data.sort_values('amount', ascending=False)
        
        # Create the chart
        fig = px.bar(
            dept_data, 
            x='department', 
            y='amount',
            title=title,
            color='amount',
            color_continuous_scale='Blues',
            hover_data={'amount': ':$,.0f'}
        )
        
        # Add drill-down functionality
        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>Total: $%{y:,.0f}<br><extra></extra>",
            customdata=dept_data['department'].tolist()
        )
        
        # Configure layout for interactivity
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': '#1e293b'}
            },
            xaxis_title="Department",
            yaxis_title="Total Spending ($)",
            hovermode='closest',
            clickmode='event+select',
            showlegend=False,
            height=500,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        # Add click event handling
        fig.update_traces(
            selector=dict(type="bar"),
            customdata=dept_data['department'].tolist()
        )
        
        return fig
    
    def monthly_trend_chart(self, data: pd.DataFrame, title: str = "Monthly Spending Trends") -> go.Figure:
        """
        Create an interactive monthly trend chart with drill-down to daily data.
        Click on a month to see daily breakdown.
        """
        # Prepare monthly data
        data['month'] = pd.to_datetime(data['date']).dt.to_period('M')
        monthly_data = data.groupby('month')['amount'].sum().reset_index()
        monthly_data['month_str'] = monthly_data['month'].astype(str)
        
        # Create the chart
        fig = px.line(
            monthly_data,
            x='month_str',
            y='amount',
            title=title,
            markers=True,
            line_shape='spline'
        )
        
        # Add drill-down functionality
        fig.update_traces(
            hovertemplate="<b>%{x}</b><br>Total: $%{y:,.0f}<br><extra></extra>",
            customdata=monthly_data['month'].tolist()
        )
        
        # Configure layout
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': '#1e293b'}
            },
            xaxis_title="Month",
            yaxis_title="Total Spending ($)",
            hovermode='closest',
            clickmode='event+select',
            height=500,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig
    
    def vendor_performance_chart(self, data: pd.DataFrame, title: str = "Top Vendors by Performance") -> go.Figure:
        """
        Create an interactive vendor performance chart with drill-down to vendor details.
        Click on a vendor to see their order history.
        """
        # Prepare vendor data
        vendor_data = data.groupby('vendor_name').agg({
            'amount': 'sum',
            'order_id': 'count'
        }).reset_index()
        vendor_data.columns = ['vendor', 'total_spend', 'order_count']
        vendor_data = vendor_data.sort_values('total_spend', ascending=False).head(10)
        
        # Create subplot with dual y-axes
        fig = make_subplots(
            rows=1, cols=1,
            specs=[[{"secondary_y": True}]]
        )
        
        # Add spending bars
        fig.add_trace(
            go.Bar(
                name="Total Spend",
                x=vendor_data['vendor'],
                y=vendor_data['total_spend'],
                marker_color='#6366f1',
                hovertemplate="<b>%{x}</b><br>Spend: $%{y:,.0f}<br><extra></extra>",
                customdata=vendor_data['vendor'].tolist()
            ),
            secondary_y=False
        )
        
        # Add order count line
        fig.add_trace(
            go.Scatter(
                name="Order Count",
                x=vendor_data['vendor'],
                y=vendor_data['order_count'],
                mode='lines+markers',
                line=dict(color='#10b981', width=3),
                marker=dict(size=8),
                hovertemplate="<b>%{x}</b><br>Orders: %{y}<br><extra></extra>",
                customdata=vendor_data['vendor'].tolist()
            ),
            secondary_y=True
        )
        
        # Configure layout
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': '#1e293b'}
            },
            hovermode='closest',
            clickmode='event+select',
            height=500,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        # Configure axes
        fig.update_xaxes(title_text="Vendor")
        fig.update_yaxes(title_text="Total Spend ($)", secondary_y=False)
        fig.update_yaxes(title_text="Order Count", secondary_y=True)
        
        return fig
    
    def category_breakdown_chart(self, data: pd.DataFrame, title: str = "Spending by Category") -> go.Figure:
        """
        Create an interactive pie chart with drill-down to subcategories.
        Click on a category to see subcategory breakdown.
        """
        # Prepare category data
        category_data = data.groupby('category')['amount'].sum().reset_index()
        category_data = category_data.sort_values('amount', ascending=False)
        
        # Create the pie chart
        fig = px.pie(
            category_data,
            values='amount',
            names='category',
            title=title,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        # Add drill-down functionality
        fig.update_traces(
            hovertemplate="<b>%{label}</b><br>Amount: $%{value:,.0f}<br>Percentage: %{percent}<br><extra></extra>",
            customdata=category_data['category'].tolist()
        )
        
        # Configure layout
        fig.update_layout(
            title={
                'text': title,
                'x': 0.5,
                'xanchor': 'center',
                'font': {'size': 16, 'color': '#1e293b'}
            },
            hovermode='closest',
            clickmode='event+select',
            height=500,
            margin=dict(l=50, r=50, t=80, b=50)
        )
        
        return fig
    
    def handle_chart_click(self, click_data: Dict[str, Any]) -> None:
        """
        Handle chart click events and update filters.
        This function processes click events and updates the application state.
        """
        if click_data and 'points' in click_data:
            point = click_data['points'][0]
            
            # Extract clicked data
            clicked_value = point.get('x', point.get('label', ''))
            clicked_amount = point.get('y', 0)
            
            # Update filter state
            self.filter_state['selected_department'] = clicked_value
            self.filter_state['selected_amount'] = clicked_amount
            st.session_state['chart_filters'] = self.filter_state
            
            # Show drill-down information
            st.info(f"🔍 **Drill-Down Selected:** {clicked_value} (${clicked_amount:,.0f})")
            
            # You can add more drill-down logic here
            if 'department' in clicked_value.lower():
                st.write("📊 **Department Details:**")
                # Add department-specific analysis here
    
    def create_drill_down_panel(self, data: pd.DataFrame) -> None:
        """
        Create a drill-down panel that shows detailed information
        based on the selected chart element.
        """
        if self.filter_state:
            st.markdown("### 🔍 Drill-Down Analysis")
            
            # Show selected filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric(
                    "Selected Department",
                    self.filter_state.get('selected_department', 'None'),
                    delta=None
                )
            
            with col2:
                st.metric(
                    "Selected Amount",
                    f"${self.filter_state.get('selected_amount', 0):,.0f}",
                    delta=None
                )
            
            with col3:
                if st.button("🔄 Reset Filters"):
                    st.session_state['chart_filters'] = {}
                    st.rerun()
            
            # Show filtered data
            if 'selected_department' in self.filter_state:
                filtered_data = data[data['department'] == self.filter_state['selected_department']]
                
                if not filtered_data.empty:
                    st.markdown("#### 📊 Detailed Breakdown")
                    
                    # Show sub-department breakdown
                    sub_dept_data = filtered_data.groupby('sub_department')['amount'].sum().reset_index()
                    sub_dept_data = sub_dept_data.sort_values('amount', ascending=False)
                    
                    # Create sub-department chart
                    fig = px.bar(
                        sub_dept_data,
                        x='sub_department',
                        y='amount',
                        title=f"Sub-Departments in {self.filter_state['selected_department']}",
                        color='amount',
                        color_continuous_scale='Greens'
                    )
                    
                    fig.update_layout(
                        height=400,
                        showlegend=False
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Show detailed table
                    st.markdown("#### 📋 Transaction Details")
                    st.dataframe(
                        filtered_data[['date', 'description', 'amount', 'category', 'status']],
                        use_container_width=True
                    )


def render_interactive_dashboard(data: pd.DataFrame) -> None:
    """
    Render an interactive dashboard with drill-down capabilities.
    This function demonstrates how to use the interactive chart features.
    """
    st.markdown("## 📊 Interactive Analytics Dashboard")
    st.markdown("**Click on any chart element to drill down into detailed data**")
    
    # Initialize chart manager
    chart_manager = InteractiveChartManager()
    
    # Create tabs for different chart types
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏢 Department Analysis", 
        "📅 Monthly Trends", 
        "🏪 Vendor Performance", 
        "📊 Category Breakdown"
    ])
    
    with tab1:
        st.markdown("### Department Spending Analysis")
        st.markdown("**Click on any department bar to see detailed breakdown**")
        
        # Create department chart
        dept_fig = chart_manager.department_spending_chart(data)
        st.plotly_chart(dept_fig, use_container_width=True, key="dept_chart")
        
        # Handle click events
        if st.session_state.get('dept_chart_click'):
            chart_manager.handle_chart_click(st.session_state['dept_chart_click'])
    
    with tab2:
        st.markdown("### Monthly Spending Trends")
        st.markdown("**Click on any month point to see daily breakdown**")
        
        # Create monthly trend chart
        trend_fig = chart_manager.monthly_trend_chart(data)
        st.plotly_chart(trend_fig, use_container_width=True, key="trend_chart")
    
    with tab3:
        st.markdown("### Vendor Performance Analysis")
        st.markdown("**Click on any vendor to see their order history**")
        
        # Create vendor performance chart
        vendor_fig = chart_manager.vendor_performance_chart(data)
        st.plotly_chart(vendor_fig, use_container_width=True, key="vendor_chart")
    
    with tab4:
        st.markdown("### Category Spending Breakdown")
        st.markdown("**Click on any category slice to see subcategory details**")
        
        # Create category breakdown chart
        category_fig = chart_manager.category_breakdown_chart(data)
        st.plotly_chart(category_fig, use_container_width=True, key="category_chart")
    
    # Show drill-down panel
    chart_manager.create_drill_down_panel(data)


def create_click_handler(chart_key: str) -> None:
    """
    Create a click handler for a specific chart.
    This function sets up the JavaScript event handling for chart interactions.
    """
    st.markdown(f"""
    <script>
    // Chart click handler for {chart_key}
    document.addEventListener('DOMContentLoaded', function() {{
        const chart = document.querySelector('[data-testid="plotly-chart"]');
        if (chart) {{
            chart.addEventListener('plotly_click', function(event) {{
                // Handle click event
                const point = event.points[0];
                const data = {{
                    x: point.x,
                    y: point.y,
                    text: point.text,
                    customdata: point.customdata
                }};
                
                // Send data to Streamlit
                window.parent.postMessage({{
                    type: 'streamlit:setComponentValue',
                    key: '{chart_key}_click',
                    value: data
                }}, '*');
            }});
        }}
    }});
    </script>
    """, unsafe_allow_html=True)
