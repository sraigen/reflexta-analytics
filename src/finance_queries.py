from __future__ import annotations

"""Finance module query functions with caching."""

from datetime import date
from typing import Optional

import pandas as pd
import streamlit as st

from .db import get_conn


@st.cache_data(ttl=60, show_spinner=False)
def get_finance_summary(from_dt: date, to_dt: date, dept_id: Optional[int] = None) -> pd.DataFrame:
    """Get finance summary with budget vs actual spending."""
    
    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if dept_id:
        where_dept = " AND d.dept_id = :dept_id"
        params["dept_id"] = dept_id
    
    sql = f"""
    SELECT 
        d.dept_name,
        d.dept_code,
        d.budget_allocation,
        COALESCE(SUM(t.amount), 0) as total_spent,
        d.budget_allocation - COALESCE(SUM(t.amount), 0) as remaining_budget,
        CASE 
            WHEN d.budget_allocation > 0 THEN 
                ROUND((COALESCE(SUM(t.amount), 0) / d.budget_allocation) * 100, 2)
            ELSE 0 
        END as budget_utilization_pct
    FROM finance_departments d
    LEFT JOIN finance_transactions t ON d.dept_id = t.dept_id 
        AND t.transaction_date BETWEEN :from_dt AND :to_dt
        AND t.status = 'Completed'
        {where_dept}
    GROUP BY d.dept_id, d.dept_name, d.dept_code, d.budget_allocation
    ORDER BY total_spent DESC
    """
    
    conn = get_conn()
    return conn.query(sql, params=params)


@st.cache_data(ttl=60, show_spinner=False)
def get_finance_monthly_trends(from_dt: date, to_dt: date, transaction_type: Optional[str] = None) -> pd.DataFrame:
    """Get monthly finance trends by transaction type."""
    
    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_type = ""
    if transaction_type and transaction_type != "All":
        where_type = " AND transaction_type = :transaction_type"
        params["transaction_type"] = transaction_type
    
    sql = f"""
    SELECT 
        EXTRACT(YEAR FROM transaction_date) as year,
        EXTRACT(MONTH FROM transaction_date) as month_num,
        TO_CHAR(transaction_date, 'Mon') as month,
        transaction_type,
        SUM(amount) as total_amount,
        COUNT(*) as transaction_count,
        AVG(amount) as avg_amount
    FROM finance_transactions
    WHERE transaction_date BETWEEN :from_dt AND :to_dt
        AND status = 'Completed'
        {where_type}
    GROUP BY EXTRACT(YEAR FROM transaction_date), EXTRACT(MONTH FROM transaction_date), TO_CHAR(transaction_date, 'Mon'), transaction_type
    ORDER BY year, month_num, transaction_type
    """
    
    conn = get_conn()
    return conn.query(sql, params=params)


@st.cache_data(ttl=60, show_spinner=False)
def get_finance_kpis(from_dt: date, to_dt: date, dept_id: Optional[int] = None) -> pd.DataFrame:
    """Get key finance KPIs with growth calculations."""
    
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
            COUNT(*) as total_transactions,
            COALESCE(SUM(CASE WHEN transaction_type = 'Revenue' THEN amount ELSE 0 END), 0) as total_revenue,
            COALESCE(SUM(CASE WHEN transaction_type = 'Expense' THEN amount ELSE 0 END), 0) as total_expenses,
            COALESCE(SUM(CASE WHEN transaction_type = 'Revenue' THEN amount ELSE 0 END), 0) - 
            COALESCE(SUM(CASE WHEN transaction_type = 'Expense' THEN amount ELSE 0 END), 0) as net_income,
            COALESCE(AVG(amount), 0) as avg_transaction_amount,
            COUNT(DISTINCT dept_id) as departments_involved,
            COUNT(DISTINCT account_id) as accounts_used
        FROM finance_transactions
        WHERE transaction_date BETWEEN :from_dt AND :to_dt
            AND status = 'Completed'
            {where_dept}
    ),
    previous_period AS (
        SELECT 
            COUNT(*) as prev_total_transactions,
            COALESCE(SUM(CASE WHEN transaction_type = 'Revenue' THEN amount ELSE 0 END), 0) as prev_total_revenue,
            COALESCE(SUM(CASE WHEN transaction_type = 'Expense' THEN amount ELSE 0 END), 0) as prev_total_expenses,
            COALESCE(SUM(CASE WHEN transaction_type = 'Revenue' THEN amount ELSE 0 END), 0) - 
            COALESCE(SUM(CASE WHEN transaction_type = 'Expense' THEN amount ELSE 0 END), 0) as prev_net_income
        FROM finance_transactions
        WHERE transaction_date BETWEEN :prev_from_dt AND :prev_to_dt
            AND status = 'Completed'
            {where_dept}
    )
    SELECT 
        c.*,
        COALESCE(c.total_revenue - p.prev_total_revenue, 0) as revenue_growth,
        COALESCE(c.total_expenses - p.prev_total_expenses, 0) as expense_growth,
        COALESCE(c.net_income - p.prev_net_income, 0) as net_income_growth,
        COALESCE(c.total_transactions - p.prev_total_transactions, 0) as transaction_growth
    FROM current_period c
    CROSS JOIN previous_period p
    """
    
    params["prev_from_dt"] = prev_from_dt
    params["prev_to_dt"] = prev_to_dt
    
    conn = get_conn()
    return conn.query(sql, params=params)


@st.cache_data(ttl=60, show_spinner=False)
def get_account_analysis(from_dt: date, to_dt: date) -> pd.DataFrame:
    """Get account-wise analysis."""
    
    sql = """
    SELECT 
        a.account_name,
        a.account_type,
        COUNT(t.transaction_id) as transaction_count,
        SUM(t.amount) as total_amount,
        AVG(t.amount) as avg_amount,
        MIN(t.amount) as min_amount,
        MAX(t.amount) as max_amount
    FROM finance_accounts a
    LEFT JOIN finance_transactions t ON a.account_id = t.account_id
        AND t.transaction_date BETWEEN :from_dt AND :to_dt
        AND t.status = 'Completed'
    GROUP BY a.account_id, a.account_name, a.account_type
    ORDER BY total_amount DESC
    """
    
    conn = get_conn()
    return conn.query(sql, params={"from_dt": from_dt, "to_dt": to_dt})


@st.cache_data(ttl=60, show_spinner=False)
def get_cost_center_analysis(from_dt: date, to_dt: date) -> pd.DataFrame:
    """Get cost center analysis."""
    
    sql = """
    SELECT 
        cc.cost_center_name,
        d.dept_name,
        COUNT(t.transaction_id) as transaction_count,
        SUM(t.amount) as total_amount,
        AVG(t.amount) as avg_amount
    FROM finance_cost_centers cc
    JOIN finance_departments d ON cc.dept_id = d.dept_id
    LEFT JOIN finance_transactions t ON cc.cost_center_id = t.cost_center_id
        AND t.transaction_date BETWEEN :from_dt AND :to_dt
        AND t.status = 'Completed'
    GROUP BY cc.cost_center_id, cc.cost_center_name, d.dept_name
    ORDER BY total_amount DESC
    """
    
    conn = get_conn()
    return conn.query(sql, params={"from_dt": from_dt, "to_dt": to_dt})


@st.cache_data(ttl=60, show_spinner=False)
def get_budget_vs_actual(from_dt: date, to_dt: date, dept_id: Optional[int] = None) -> pd.DataFrame:
    """Get budget vs actual spending analysis."""
    
    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if dept_id:
        where_dept = " AND b.dept_id = :dept_id"
        params["dept_id"] = dept_id
    
    sql = f"""
    SELECT 
        d.dept_name,
        b.budget_name,
        b.budget_amount,
        COALESCE(SUM(t.amount), 0) as actual_spent,
        b.budget_amount - COALESCE(SUM(t.amount), 0) as variance,
        CASE 
            WHEN b.budget_amount > 0 THEN 
                ROUND((COALESCE(SUM(t.amount), 0) / b.budget_amount) * 100, 2)
            ELSE 0 
        END as utilization_pct,
        CASE 
            WHEN COALESCE(SUM(t.amount), 0) > b.budget_amount THEN 'Over Budget'
            WHEN COALESCE(SUM(t.amount), 0) > b.budget_amount * 0.9 THEN 'Near Budget'
            ELSE 'Under Budget'
        END as budget_status
    FROM finance_budgets b
    JOIN finance_departments d ON b.dept_id = d.dept_id
    LEFT JOIN finance_transactions t ON b.dept_id = t.dept_id 
        AND b.cost_center_id = t.cost_center_id
        AND b.account_id = t.account_id
        AND t.transaction_date BETWEEN :from_dt AND :to_dt
        AND t.status = 'Completed'
        {where_dept}
    GROUP BY d.dept_id, d.dept_name, b.budget_id, b.budget_name, b.budget_amount
    ORDER BY utilization_pct DESC
    """
    
    conn = get_conn()
    return conn.query(sql, params=params)


@st.cache_data(ttl=60, show_spinner=False)
def get_pending_transactions() -> pd.DataFrame:
    """Get pending transactions requiring approval."""
    
    sql = """
    SELECT 
        t.transaction_id,
        t.transaction_date,
        t.transaction_type,
        t.amount,
        t.description,
        d.dept_name,
        a.account_name,
        t.status,
        t.created_by,
        t.created_at
    FROM finance_transactions t
    JOIN finance_departments d ON t.dept_id = d.dept_id
    JOIN finance_accounts a ON t.account_id = a.account_id
    WHERE t.status IN ('Pending', 'Approved')
    ORDER BY t.created_at DESC
    """
    
    conn = get_conn()
    return conn.query(sql)


@st.cache_data(ttl=60, show_spinner=False)
def get_vendor_analysis(from_dt: date, to_dt: date) -> pd.DataFrame:
    """Get vendor spending analysis."""
    
    sql = """
    SELECT 
        vendor_name,
        COUNT(*) as transaction_count,
        SUM(amount) as total_amount,
        AVG(amount) as avg_amount,
        MIN(amount) as min_amount,
        MAX(amount) as max_amount,
        COUNT(DISTINCT dept_id) as departments_used
    FROM finance_transactions
    WHERE transaction_date BETWEEN :from_dt AND :to_dt
        AND status = 'Completed'
        AND vendor_name IS NOT NULL
    GROUP BY vendor_name
    ORDER BY total_amount DESC
    """
    
    conn = get_conn()
    return conn.query(sql, params={"from_dt": from_dt, "to_dt": to_dt})
