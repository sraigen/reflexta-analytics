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
    """Get key procurement KPIs."""
    
    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if dept_id:
        where_dept = " AND dept_id = :dept_id"
        params["dept_id"] = dept_id
    
    sql = f"""
    SELECT 
        COUNT(*) as total_orders,
        SUM(grand_total) as total_value,
        AVG(grand_total) as avg_order_value,
        COUNT(DISTINCT vendor_id) as unique_vendors,
        COUNT(DISTINCT category_id) as unique_categories,
        COUNT(CASE WHEN status = 'Received' THEN 1 END) as completed_orders,
        COUNT(CASE WHEN status IN ('Draft', 'Submitted', 'Approved', 'Ordered') THEN 1 END) as pending_orders,
        COUNT(CASE WHEN priority = 'High' OR priority = 'Urgent' THEN 1 END) as high_priority_orders,
        AVG(CASE WHEN actual_delivery_date IS NOT NULL AND expected_delivery_date IS NOT NULL 
            THEN (actual_delivery_date - expected_delivery_date) END) as avg_delivery_delay_days
    FROM procurement_orders
    WHERE order_date BETWEEN :from_dt AND :to_dt
        {where_dept}
    """
    
    conn = get_conn()
    return conn.query(sql, params=params)


@st.cache_data(ttl=60, show_spinner=False)
def get_vendor_performance(from_dt: date, to_dt: date) -> pd.DataFrame:
    """Get vendor performance analysis."""
    
    sql = """
    SELECT 
        v.vendor_name,
        v.vendor_code,
        v.rating,
        COUNT(po.order_id) as total_orders,
        SUM(po.grand_total) as total_value,
        AVG(po.grand_total) as avg_order_value,
        COUNT(CASE WHEN po.status = 'Received' THEN 1 END) as completed_orders,
        COUNT(CASE WHEN po.status = 'Received' THEN 1 END) * 100.0 / NULLIF(COUNT(po.order_id), 0) as completion_rate,
        AVG(CASE WHEN po.actual_delivery_date IS NOT NULL AND po.expected_delivery_date IS NOT NULL 
            THEN (po.actual_delivery_date - po.expected_delivery_date) END) as avg_delivery_delay_days
    FROM procurement_vendors v
    LEFT JOIN procurement_orders po ON v.vendor_id = po.vendor_id
        AND po.order_date BETWEEN :from_dt AND :to_dt
    GROUP BY v.vendor_id, v.vendor_name, v.vendor_code, v.rating
    ORDER BY total_value DESC
    """
    
    conn = get_conn()
    return conn.query(sql, params={"from_dt": from_dt, "to_dt": to_dt})


@st.cache_data(ttl=60, show_spinner=False)
def get_category_analysis(from_dt: date, to_dt: date) -> pd.DataFrame:
    """Get category-wise procurement analysis."""
    
    sql = """
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
    GROUP BY c.category_id, c.category_name, c.category_code
    ORDER BY total_value DESC
    """
    
    conn = get_conn()
    return conn.query(sql, params={"from_dt": from_dt, "to_dt": to_dt})


@st.cache_data(ttl=60, show_spinner=False)
def get_procurement_trends(from_dt: date, to_dt: date, group_by: str = "month") -> pd.DataFrame:
    """Get procurement trends over time."""
    
    if group_by == "month":
        date_part = "EXTRACT(MONTH FROM order_date)"
        date_label = "month"
    elif group_by == "quarter":
        date_part = "EXTRACT(QUARTER FROM order_date)"
        date_label = "quarter"
    else:  # week
        date_part = "EXTRACT(WEEK FROM order_date)"
        date_label = "week"
    
    sql = f"""
    SELECT 
        EXTRACT(YEAR FROM order_date) as year,
        {date_part} as {date_label},
        COUNT(*) as order_count,
        SUM(grand_total) as total_value,
        AVG(grand_total) as avg_order_value,
        COUNT(CASE WHEN status = 'Received' THEN 1 END) as completed_orders,
        COUNT(CASE WHEN status = 'Received' THEN 1 END) * 100.0 / NULLIF(COUNT(*), 0) as completion_rate
    FROM procurement_orders
    WHERE order_date BETWEEN :from_dt AND :to_dt
    GROUP BY EXTRACT(YEAR FROM order_date), {date_part}
    ORDER BY year, {date_label}
    """
    
    conn = get_conn()
    return conn.query(sql, params={"from_dt": from_dt, "to_dt": to_dt})


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
        po.expected_delivery_date,
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
def get_delivery_performance(from_dt: date, to_dt: date) -> pd.DataFrame:
    """Get delivery performance analysis."""
    
    sql = """
    SELECT 
        v.vendor_name,
        COUNT(po.order_id) as total_orders,
        COUNT(CASE WHEN po.actual_delivery_date IS NOT NULL THEN 1 END) as delivered_orders,
        COUNT(CASE WHEN po.actual_delivery_date <= po.expected_delivery_date THEN 1 END) as on_time_deliveries,
        COUNT(CASE WHEN po.actual_delivery_date > po.expected_delivery_date THEN 1 END) as late_deliveries,
        AVG(CASE WHEN po.actual_delivery_date IS NOT NULL AND po.expected_delivery_date IS NOT NULL 
            THEN (po.actual_delivery_date - po.expected_delivery_date) END) as avg_delivery_delay_days,
        COUNT(CASE WHEN po.actual_delivery_date <= po.expected_delivery_date THEN 1 END) * 100.0 / 
            NULLIF(COUNT(CASE WHEN po.actual_delivery_date IS NOT NULL THEN 1 END), 0) as on_time_percentage
    FROM procurement_orders po
    JOIN procurement_vendors v ON po.vendor_id = v.vendor_id
    WHERE po.order_date BETWEEN :from_dt AND :to_dt
        AND po.status = 'Received'
    GROUP BY v.vendor_id, v.vendor_name
    ORDER BY on_time_percentage DESC
    """
    
    conn = get_conn()
    return conn.query(sql, params={"from_dt": from_dt, "to_dt": to_dt})


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
        po.expected_delivery_date,
        po.actual_delivery_date
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
