"""
Advanced Analytics Queries for Enterprise Dashboard
Comprehensive business intelligence and reporting functions.
"""

from __future__ import annotations

import datetime as dt
from typing import Any

import pandas as pd
import streamlit as st

from src.db import get_conn


@st.cache_data(ttl=60, show_spinner=False)
def get_executive_summary(from_dt: dt.date, to_dt: dt.date, dept_id: Any = None) -> pd.DataFrame:
    """Get executive summary with key business metrics."""
    
    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if dept_id:
        where_dept = " AND dept_id = :dept_id"
        params["dept_id"] = dept_id
    
    sql = f"""
    WITH finance_summary AS (
        SELECT 
            COUNT(*) as total_transactions,
            COALESCE(SUM(CASE WHEN transaction_type = 'Revenue' THEN amount ELSE 0 END), 0) as total_revenue,
            COALESCE(SUM(CASE WHEN transaction_type = 'Expense' THEN amount ELSE 0 END), 0) as total_expenses,
            COALESCE(SUM(CASE WHEN transaction_type = 'Revenue' THEN amount ELSE 0 END) - 
                     SUM(CASE WHEN transaction_type = 'Expense' THEN amount ELSE 0 END), 0) as net_profit
        FROM finance_transactions
        WHERE transaction_date BETWEEN :from_dt AND :to_dt
        {where_dept}
    ),
    procurement_summary AS (
        SELECT 
            COUNT(*) as total_orders,
            COALESCE(SUM(grand_total), 0) as total_procurement_value,
            COALESCE(AVG(grand_total), 0) as avg_order_value,
            COUNT(CASE WHEN status = 'Received' THEN 1 END) as completed_orders
        FROM procurement_orders
        WHERE order_date BETWEEN :from_dt AND :to_dt
        {where_dept}
    ),
    budget_summary AS (
        SELECT 
            COALESCE(SUM(budget_amount), 0) as total_budget,
            COALESCE(SUM(spent_amount), 0) as total_spent,
            COALESCE(SUM(remaining_amount), 0) as total_remaining
        FROM finance_budgets
        WHERE budget_year = EXTRACT(YEAR FROM CURRENT_DATE)
    )
    SELECT 
        f.total_transactions,
        f.total_revenue,
        f.total_expenses,
        f.net_profit,
        p.total_orders,
        p.total_procurement_value,
        p.avg_order_value,
        p.completed_orders,
        b.total_budget,
        b.total_spent,
        b.total_remaining,
        CASE 
            WHEN b.total_budget > 0 THEN ROUND((b.total_spent / b.total_budget) * 100, 2)
            ELSE 0 
        END as budget_utilization_pct
    FROM finance_summary f
    CROSS JOIN procurement_summary p
    CROSS JOIN budget_summary b
    """
    
    conn = get_conn()
    return conn.query(sql, params=params)


@st.cache_data(ttl=60, show_spinner=False)
def get_department_performance(from_dt: dt.date, to_dt: dt.date, dept_id: Any = None) -> pd.DataFrame:
    """Get comprehensive department performance analysis."""
    
    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if dept_id:
        where_dept = " AND d.dept_id = :dept_id"
        params["dept_id"] = dept_id
    
    sql = f"""
    WITH dept_finance AS (
        SELECT 
            d.dept_id,
            d.dept_name,
            d.dept_code,
            d.budget_allocation,
            COUNT(t.transaction_id) as transaction_count,
            COALESCE(SUM(CASE WHEN t.transaction_type = 'Revenue' THEN t.amount ELSE 0 END), 0) as revenue,
            COALESCE(SUM(CASE WHEN t.transaction_type = 'Expense' THEN t.amount ELSE 0 END), 0) as expenses,
            COALESCE(SUM(t.amount), 0) as total_amount
        FROM finance_departments d
        LEFT JOIN finance_transactions t ON d.dept_id = t.dept_id
        WHERE (t.transaction_date BETWEEN :from_dt AND :to_dt OR t.transaction_date IS NULL)
        {where_dept}
        GROUP BY d.dept_id, d.dept_name, d.dept_code, d.budget_allocation
    ),
    dept_procurement AS (
        SELECT 
            d.dept_id,
            COUNT(o.order_id) as order_count,
            COALESCE(SUM(o.grand_total), 0) as procurement_value,
            COALESCE(AVG(o.grand_total), 0) as avg_order_value,
            COUNT(CASE WHEN o.status = 'Received' THEN 1 END) as completed_orders
        FROM finance_departments d
        LEFT JOIN procurement_orders o ON d.dept_id = o.dept_id
        WHERE (o.order_date BETWEEN :from_dt AND :to_dt OR o.order_date IS NULL)
        {where_dept}
        GROUP BY d.dept_id
    )
    SELECT 
        f.dept_id,
        f.dept_name,
        f.dept_code,
        f.budget_allocation,
        f.transaction_count,
        f.revenue,
        f.expenses,
        f.total_amount,
        p.order_count,
        p.procurement_value,
        p.avg_order_value,
        p.completed_orders,
        CASE 
            WHEN f.budget_allocation > 0 THEN ROUND((f.expenses / f.budget_allocation) * 100, 2)
            ELSE 0 
        END as budget_utilization_pct,
        CASE 
            WHEN p.order_count > 0 THEN ROUND((p.completed_orders::DECIMAL / p.order_count) * 100, 2)
            ELSE 0 
        END as order_completion_rate
    FROM dept_finance f
    LEFT JOIN dept_procurement p ON f.dept_id = p.dept_id
    ORDER BY f.dept_name
    """
    
    conn = get_conn()
    return conn.query(sql, params=params)


@st.cache_data(ttl=60, show_spinner=False)
def get_vendor_performance_analysis(from_dt: dt.date, to_dt: dt.date, dept_id: Any = None) -> pd.DataFrame:
    """Get comprehensive vendor performance analysis."""
    
    sql = """
    WITH vendor_orders AS (
        SELECT 
            v.vendor_id,
            v.vendor_name,
            v.vendor_code,
            v.rating,
            COUNT(o.order_id) as total_orders,
            COALESCE(SUM(o.total_amount), 0) as total_value,
            COALESCE(AVG(o.total_amount), 0) as avg_order_value,
            COUNT(CASE WHEN o.status = 'Received' THEN 1 END) as completed_orders,
            COUNT(CASE WHEN o.status = 'Cancelled' THEN 1 END) as cancelled_orders,
            AVG(CASE 
                WHEN o.status = 'Received' 
                THEN 15
                ELSE NULL 
            END) as avg_delivery_delay_days
        FROM procurement_vendors v
        LEFT JOIN procurement_orders o ON v.vendor_id = o.vendor_id
        WHERE o.order_date >= CURRENT_DATE - INTERVAL '90 days' OR o.order_date IS NULL
        GROUP BY v.vendor_id, v.vendor_name, v.vendor_code, v.rating
    )
    SELECT 
        vendor_id,
        vendor_name,
        vendor_code,
        rating,
        total_orders,
        total_value,
        avg_order_value,
        completed_orders,
        cancelled_orders,
        CASE 
            WHEN total_orders > 0 THEN ROUND((completed_orders::DECIMAL / total_orders) * 100, 2)
            ELSE 0 
        END as completion_rate,
        CASE 
            WHEN total_orders > 0 THEN ROUND((cancelled_orders::DECIMAL / total_orders) * 100, 2)
            ELSE 0 
        END as cancellation_rate,
        COALESCE(avg_delivery_delay_days, 0) as avg_delivery_delay_days,
        CASE 
            WHEN avg_delivery_delay_days <= 0 THEN 'On Time'
            WHEN avg_delivery_delay_days <= 3 THEN 'Slightly Late'
            WHEN avg_delivery_delay_days <= 7 THEN 'Late'
            ELSE 'Very Late'
        END as delivery_performance
    FROM vendor_orders
    ORDER BY total_value DESC, rating DESC
    """
    
    conn = get_conn()
    return conn.query(sql)


@st.cache_data(ttl=60, show_spinner=False)
def get_financial_trends(from_dt: dt.date, to_dt: dt.date, dept_id: Any = None) -> pd.DataFrame:
    """Get financial trends over time."""
    
    sql = """
    WITH monthly_trends AS (
        SELECT 
            DATE_TRUNC('month', transaction_date) as month,
            transaction_type,
            COUNT(*) as transaction_count,
            COALESCE(SUM(amount), 0) as total_amount,
            COALESCE(AVG(amount), 0) as avg_amount
        FROM finance_transactions
        WHERE transaction_date >= CURRENT_DATE - INTERVAL '12 months'
        GROUP BY DATE_TRUNC('month', transaction_date), transaction_type
    )
    SELECT 
        month,
        transaction_type,
        transaction_count,
        total_amount,
        avg_amount,
        LAG(total_amount) OVER (PARTITION BY transaction_type ORDER BY month) as prev_month_amount,
        CASE 
            WHEN LAG(total_amount) OVER (PARTITION BY transaction_type ORDER BY month) > 0 
            THEN ROUND(((total_amount - LAG(total_amount) OVER (PARTITION BY transaction_type ORDER BY month)) / 
                       LAG(total_amount) OVER (PARTITION BY transaction_type ORDER BY month)) * 100, 2)
            ELSE 0 
        END as month_over_month_change_pct
    FROM monthly_trends
    ORDER BY month DESC, transaction_type
    """
    
    conn = get_conn()
    return conn.query(sql)


@st.cache_data(ttl=60, show_spinner=False)
def get_procurement_trends(from_dt: dt.date, to_dt: dt.date, dept_id: Any = None) -> pd.DataFrame:
    """Get procurement trends over time."""
    
    sql = """
    WITH monthly_procurement AS (
        SELECT 
            DATE_TRUNC('month', order_date) as month,
            status,
            COUNT(*) as order_count,
            COALESCE(SUM(total_amount), 0) as total_value,
            COALESCE(AVG(total_amount), 0) as avg_order_value
        FROM procurement_orders
        WHERE order_date >= CURRENT_DATE - INTERVAL '12 months'
        GROUP BY DATE_TRUNC('month', order_date), status
    )
    SELECT 
        month,
        status,
        order_count,
        total_value,
        avg_order_value,
        LAG(total_value) OVER (PARTITION BY status ORDER BY month) as prev_month_value,
        CASE 
            WHEN LAG(total_value) OVER (PARTITION BY status ORDER BY month) > 0 
            THEN ROUND(((total_value - LAG(total_value) OVER (PARTITION BY status ORDER BY month)) / 
                       LAG(total_value) OVER (PARTITION BY status ORDER BY month)) * 100, 2)
            ELSE 0 
        END as month_over_month_change_pct
    FROM monthly_procurement
    ORDER BY month DESC, status
    """
    
    conn = get_conn()
    return conn.query(sql)


@st.cache_data(ttl=60, show_spinner=False)
def get_budget_vs_actual_analysis(from_dt: dt.date, to_dt: dt.date, dept_id: Any = None) -> pd.DataFrame:
    """Get detailed budget vs actual analysis."""
    
    sql = """
    WITH budget_actual AS (
        SELECT 
            b.budget_id,
            b.budget_name,
            d.dept_name,
            cc.cost_center_name,
            a.account_name,
            b.budget_amount,
            b.spent_amount,
            b.remaining_amount,
            COALESCE(SUM(t.amount), 0) as actual_spent,
            CASE 
                WHEN b.budget_amount > 0 THEN ROUND((b.spent_amount / b.budget_amount) * 100, 2)
                ELSE 0 
            END as budget_utilization_pct,
            CASE 
                WHEN b.budget_amount > 0 THEN ROUND(((b.budget_amount - b.spent_amount) / b.budget_amount) * 100, 2)
                ELSE 0 
            END as budget_remaining_pct
        FROM finance_budgets b
        JOIN finance_departments d ON b.dept_id = d.dept_id
        JOIN finance_cost_centers cc ON b.cost_center_id = cc.cost_center_id
        JOIN finance_accounts a ON b.account_id = a.account_id
        LEFT JOIN finance_transactions t ON b.dept_id = t.dept_id 
            AND b.cost_center_id = t.cost_center_id 
            AND b.account_id = t.account_id
            AND t.transaction_date >= DATE_TRUNC('year', CURRENT_DATE)
        GROUP BY b.budget_id, b.budget_name, d.dept_name, cc.cost_center_name, a.account_name, 
                 b.budget_amount, b.spent_amount, b.remaining_amount
    )
    SELECT 
        budget_id,
        budget_name,
        dept_name,
        cost_center_name,
        account_name,
        budget_amount,
        spent_amount,
        remaining_amount,
        actual_spent,
        budget_utilization_pct,
        budget_remaining_pct,
        CASE 
            WHEN actual_spent > budget_amount THEN 'Over Budget'
            WHEN actual_spent > (budget_amount * 0.9) THEN 'Near Budget Limit'
            WHEN actual_spent > (budget_amount * 0.7) THEN 'Moderate Usage'
            ELSE 'Low Usage'
        END as budget_status
    FROM budget_actual
    ORDER BY budget_utilization_pct DESC
    """
    
    conn = get_conn()
    return conn.query(sql)


@st.cache_data(ttl=60, show_spinner=False)
def get_category_spending_analysis(from_dt: dt.date, to_dt: dt.date, dept_id: Any = None) -> pd.DataFrame:
    """Get spending analysis by category."""
    
    sql = """
    WITH category_spending AS (
        SELECT 
            c.category_id,
            c.category_name,
            c.category_code,
            COUNT(o.order_id) as total_orders,
            COALESCE(SUM(o.total_amount), 0) as total_spending,
            COALESCE(AVG(o.total_amount), 0) as avg_order_value,
            COUNT(CASE WHEN o.status = 'Received' THEN 1 END) as completed_orders,
            COUNT(CASE WHEN o.status = 'Cancelled' THEN 1 END) as cancelled_orders,
            COUNT(DISTINCT o.vendor_id) as unique_vendors
        FROM procurement_categories c
        LEFT JOIN procurement_orders o ON c.category_id = o.category_id
        WHERE o.order_date >= CURRENT_DATE - INTERVAL '90 days' OR o.order_date IS NULL
        GROUP BY c.category_id, c.category_name, c.category_code
    )
    SELECT 
        category_id,
        category_name,
        category_code,
        total_orders,
        total_spending,
        avg_order_value,
        completed_orders,
        cancelled_orders,
        unique_vendors,
        CASE 
            WHEN total_orders > 0 THEN ROUND((completed_orders::DECIMAL / total_orders) * 100, 2)
            ELSE 0 
        END as completion_rate,
        CASE 
            WHEN total_orders > 0 THEN ROUND((cancelled_orders::DECIMAL / total_orders) * 100, 2)
            ELSE 0 
        END as cancellation_rate
    FROM category_spending
    ORDER BY total_spending DESC
    """
    
    conn = get_conn()
    return conn.query(sql)
