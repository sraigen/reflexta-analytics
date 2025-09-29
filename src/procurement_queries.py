from __future__ import annotations

"""Procurement module query functions with caching."""

from datetime import date
from typing import Optional

import pandas as pd
import streamlit as st

from .db import get_conn


@st.cache_data(ttl=60, show_spinner=False)
def get_procurement_summary(from_dt: date, to_dt: date, dept_id: Optional[int] = None) -> pd.DataFrame:
    """Get procurement summary by department."""
    
    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if dept_id:
        where_dept = " AND d.dept_id = :dept_id"
        params["dept_id"] = dept_id
    
    sql = f"""
    SELECT 
        d.dept_name,
        d.dept_code,
        COUNT(po.order_id) as total_orders,
        SUM(po.grand_total) as total_value,
        AVG(po.grand_total) as avg_order_value,
        COUNT(CASE WHEN po.status = 'Received' THEN 1 END) as completed_orders,
        COUNT(CASE WHEN po.status IN ('Draft', 'Submitted', 'Approved', 'Ordered') THEN 1 END) as pending_orders,
        COUNT(CASE WHEN po.status = 'Received' THEN 1 END) * 100.0 / NULLIF(COUNT(po.order_id), 0) as completion_rate
    FROM finance_departments d
    LEFT JOIN procurement_orders po ON d.dept_id = po.dept_id
        AND po.order_date BETWEEN :from_dt AND :to_dt
        {where_dept}
    GROUP BY d.dept_id, d.dept_name, d.dept_code
    ORDER BY total_value DESC
    """
    
    conn = get_conn()
    return conn.query(sql, params=params)


@st.cache_data(ttl=60, show_spinner=False)
def get_procurement_kpis(from_dt: date, to_dt: date, dept_id: Optional[int] = None) -> pd.DataFrame:
    """Get key procurement KPIs with growth calculations."""
    
    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if dept_id:
        where_dept = " AND dept_id = :dept_id"
        params["dept_id"] = dept_id
    
    # Calculate previous period for growth comparison
    from datetime import timedelta
    period_days = (to_dt - from_dt).days
    prev_from_dt = from_dt - timedelta(days=period_days)
    prev_to_dt = from_dt - timedelta(days=1)
    
    sql = f"""
    WITH current_period AS (
        SELECT 
            COUNT(*) as total_orders,
            COALESCE(SUM(grand_total), 0) as total_spend,
            COALESCE(AVG(grand_total), 0) as avg_order_value,
            COUNT(DISTINCT vendor_id) as active_vendors,
            COUNT(DISTINCT category_id) as unique_categories,
            COUNT(CASE WHEN status = 'Received' THEN 1 END) as completed_orders,
            COUNT(CASE WHEN status IN ('Draft', 'Submitted', 'Approved', 'Ordered') THEN 1 END) as pending_orders,
            COUNT(CASE WHEN priority = 'High' OR priority = 'Urgent' THEN 1 END) as high_priority_orders
        FROM procurement_orders
        WHERE order_date BETWEEN :from_dt AND :to_dt
            {where_dept}
    ),
    previous_period AS (
        SELECT 
            COUNT(*) as prev_total_orders,
            COALESCE(SUM(grand_total), 0) as prev_total_spend,
            COALESCE(AVG(grand_total), 0) as prev_avg_order_value,
            COUNT(DISTINCT vendor_id) as prev_active_vendors
        FROM procurement_orders
        WHERE order_date BETWEEN :prev_from_dt AND :prev_to_dt
            {where_dept}
    )
    SELECT 
        c.*,
        COALESCE(c.total_orders - p.prev_total_orders, 0) as order_growth,
        COALESCE(c.total_spend - p.prev_total_spend, 0) as spend_growth,
        COALESCE(c.avg_order_value - p.prev_avg_order_value, 0) as aov_growth,
        COALESCE(c.active_vendors - p.prev_active_vendors, 0) as vendor_growth
    FROM current_period c
    CROSS JOIN previous_period p
    """
    
    params["prev_from_dt"] = prev_from_dt
    params["prev_to_dt"] = prev_to_dt
    
    conn = get_conn()
    return conn.query(sql, params=params)


@st.cache_data(ttl=60, show_spinner=False)
def get_vendor_performance(from_dt: date, to_dt: date, dept_id: Optional[int] = None) -> pd.DataFrame:
    """Get vendor performance analysis."""
    
    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if dept_id:
        where_dept = " AND po.dept_id = :dept_id"
        params["dept_id"] = dept_id
    
    sql = f"""
    SELECT 
        v.vendor_name,
        v.vendor_code,
        v.rating,
        COUNT(po.order_id) as total_orders,
        SUM(po.grand_total) as total_value,
        AVG(po.grand_total) as avg_order_value,
        COUNT(CASE WHEN po.status = 'Received' THEN 1 END) as completed_orders,
        COUNT(CASE WHEN po.status = 'Received' THEN 1 END) * 100.0 / NULLIF(COUNT(po.order_id), 0) as completion_rate,
        NULL as avg_delivery_delay_days
    FROM procurement_vendors v
    LEFT JOIN procurement_orders po ON v.vendor_id = po.vendor_id
        AND po.order_date BETWEEN :from_dt AND :to_dt
        {where_dept}
    GROUP BY v.vendor_id, v.vendor_name, v.vendor_code, v.rating
    ORDER BY total_value DESC
    """
    
    conn = get_conn()
    return conn.query(sql, params=params)


@st.cache_data(ttl=60, show_spinner=False)
def get_category_analysis(from_dt: date, to_dt: date, dept_id: Optional[int] = None) -> pd.DataFrame:
    """Get category-wise procurement analysis."""
    
    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if dept_id:
        where_dept = " AND po.dept_id = :dept_id"
        params["dept_id"] = dept_id
    
    sql = f"""
    SELECT 
        c.category_name,
        c.category_code,
        COUNT(po.order_id) as order_count,
        SUM(po.grand_total) as total_value,
        AVG(po.grand_total) as avg_order_value,
        COUNT(DISTINCT po.vendor_id) as unique_vendors,
        COUNT(DISTINCT po.dept_id) as departments_using,
        COUNT(CASE WHEN po.status = 'Received' THEN 1 END) as completed_orders,
        COUNT(CASE WHEN po.status = 'Received' THEN 1 END) * 100.0 / NULLIF(COUNT(po.order_id), 0) as completion_rate
    FROM procurement_categories c
    LEFT JOIN procurement_orders po ON c.category_id = po.category_id
        AND po.order_date BETWEEN :from_dt AND :to_dt
        {where_dept}
    GROUP BY c.category_id, c.category_name, c.category_code
    ORDER BY total_value DESC
    """
    
    conn = get_conn()
    return conn.query(sql, params=params)


@st.cache_data(ttl=60, show_spinner=False)
def get_procurement_trends(from_dt: date, to_dt: date, dept_id: Optional[int] = None, group_by: str = "month") -> pd.DataFrame:
    """Get procurement trends over time."""
    
    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if dept_id:
        where_dept = " AND dept_id = :dept_id"
        params["dept_id"] = dept_id
    
    if group_by == "month":
        date_part = "EXTRACT(MONTH FROM order_date)"
        date_label = "month"
        date_name = "TO_CHAR(order_date, 'Mon') as month_name"
    elif group_by == "quarter":
        date_part = "EXTRACT(QUARTER FROM order_date)"
        date_label = "quarter"
        date_name = "TO_CHAR(order_date, 'Q') as quarter_name"
    else:  # week
        date_part = "EXTRACT(WEEK FROM order_date)"
        date_label = "week"
        date_name = "TO_CHAR(order_date, 'WW') as week_name"
    
    sql = f"""
    SELECT 
        EXTRACT(YEAR FROM order_date) as year,
        {date_part} as {date_label},
        {date_name},
        COUNT(*) as order_count,
        SUM(grand_total) as total_value,
        AVG(grand_total) as avg_order_value,
        COUNT(CASE WHEN status = 'Received' THEN 1 END) as completed_orders,
        COUNT(CASE WHEN status = 'Received' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0) as completion_rate
    FROM procurement_orders
    WHERE order_date BETWEEN :from_dt AND :to_dt
    {where_dept}
    GROUP BY EXTRACT(YEAR FROM order_date), {date_part}, {date_name.split(' as ')[0]}
    ORDER BY year, {date_label}
    """
    
    conn = get_conn()
    return conn.query(sql, params=params)


@st.cache_data(ttl=60, show_spinner=False)
def get_pending_orders() -> pd.DataFrame:
    """Get pending orders requiring attention."""
    
    sql = """
    SELECT 
        po.order_id,
        po.order_number,
        po.order_date,
        po.grand_total,
        po.status,
        po.priority,
        v.vendor_name,
        c.category_name,
        d.dept_name,
        po.requested_by,
        po.order_date + INTERVAL '30 days' as expected_delivery_date,
        po.notes
    FROM procurement_orders po
    JOIN procurement_vendors v ON po.vendor_id = v.vendor_id
    JOIN procurement_categories c ON po.category_id = c.category_id
    JOIN finance_departments d ON po.dept_id = d.dept_id
    WHERE po.status IN ('Draft', 'Submitted', 'Approved', 'Ordered')
    ORDER BY 
        CASE po.priority 
            WHEN 'Urgent' THEN 1 
            WHEN 'High' THEN 2 
            WHEN 'Medium' THEN 3 
            ELSE 4 
        END,
        po.order_date DESC
    """
    
    conn = get_conn()
    return conn.query(sql)


@st.cache_data(ttl=60, show_spinner=False)
def get_delivery_performance(from_dt: date, to_dt: date, dept_id: Optional[int] = None) -> pd.DataFrame:
    """Get delivery performance analysis."""
    
    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if dept_id:
        where_dept = " AND po.dept_id = :dept_id"
        params["dept_id"] = dept_id
    
    sql = f"""
    SELECT 
        v.vendor_name,
        COUNT(po.order_id) as total_orders,
        COUNT(CASE WHEN po.status = 'Received' THEN 1 END) as delivered_orders,
        COUNT(CASE WHEN po.status = 'Received' THEN 1 END) as on_time_deliveries,
        0 as late_deliveries,
        NULL as avg_delivery_delay_days,
        CASE WHEN COUNT(po.order_id) > 0 THEN 100.0 ELSE 0 END as on_time_percentage
    FROM procurement_orders po
    JOIN procurement_vendors v ON po.vendor_id = v.vendor_id
    WHERE po.order_date BETWEEN :from_dt AND :to_dt
        AND po.status = 'Received'
        {where_dept}
    GROUP BY v.vendor_id, v.vendor_name
    ORDER BY on_time_percentage DESC
    """
    
    conn = get_conn()
    return conn.query(sql, params=params)


@st.cache_data(ttl=60, show_spinner=False)
def get_spend_analysis(from_dt: date, to_dt: date, dept_id: Optional[int] = None) -> pd.DataFrame:
    """Get detailed spend analysis."""
    
    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if dept_id:
        where_dept = " AND po.dept_id = :dept_id"
        params["dept_id"] = dept_id
    
    sql = f"""
    SELECT 
        po.order_id,
        po.order_number,
        po.order_date,
        po.grand_total,
        po.status,
        v.vendor_name,
        c.category_name,
        d.dept_name,
        cc.cost_center_name,
        po.requested_by,
        po.priority,
        po.order_date + INTERVAL '30 days' as expected_delivery_date,
        NULL as delivery_date
    FROM procurement_orders po
    JOIN procurement_vendors v ON po.vendor_id = v.vendor_id
    JOIN procurement_categories c ON po.category_id = c.category_id
    JOIN finance_departments d ON po.dept_id = d.dept_id
    JOIN finance_cost_centers cc ON po.cost_center_id = cc.cost_center_id
    WHERE po.order_date BETWEEN :from_dt AND :to_dt
        {where_dept}
    ORDER BY po.order_date DESC
    """
    
    conn = get_conn()
    return conn.query(sql, params=params)
