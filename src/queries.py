from __future__ import annotations

"""Reusable, parameterized SQL query functions with caching.

Assumed schema: a `sales` table or view with columns:
- dt (DATE or TIMESTAMP), department (TEXT), region (TEXT), amount (NUMERIC), order_id (TEXT/INT)
"""

from datetime import date
from typing import Optional

import pandas as pd
import streamlit as st

from .db import get_conn


@st.cache_data(ttl=60, show_spinner=False)
def fetch_sales(from_dt: date, to_dt: date, department: Optional[str]) -> pd.DataFrame:
    """Return raw sales rows filtered by date range and optional department.

    Parameters are bound safely; no string concatenation is used.
    """

    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if department and department != "All":
        where_dept = " AND department = :department"
        params["department"] = department

    sql = f"""
        SELECT
            dt,
            department,
            region,
            amount,
            order_id
        FROM sales
        WHERE dt >= :from_dt AND dt <= :to_dt
        {where_dept}
        ORDER BY dt ASC
    """

    conn = get_conn()
    return conn.query(sql, params=params)


@st.cache_data(ttl=60, show_spinner=False)
def kpi_aggregates(from_dt: date, to_dt: date, department: Optional[str]) -> pd.DataFrame:
    """Return count, total, and average amount as a single-row DataFrame."""

    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if department and department != "All":
        where_dept = " AND department = :department"
        params["department"] = department

    sql = f"""
        SELECT
            COUNT(*) AS order_count,
            COALESCE(SUM(amount), 0) AS total_amount,
            COALESCE(AVG(amount), 0) AS avg_amount
        FROM sales
        WHERE dt >= :from_dt AND dt <= :to_dt
        {where_dept}
    """

    conn = get_conn()
    return conn.query(sql, params=params)


@st.cache_data(ttl=60, show_spinner=False)
def totals_by_department(from_dt: date, to_dt: date, department: Optional[str]) -> pd.DataFrame:
    """Return aggregated totals grouped by department (filtered by optional department).

    When a specific department is chosen, this effectively returns a single row.
    """

    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if department and department != "All":
        where_dept = " AND department = :department"
        params["department"] = department

    sql = f"""
        SELECT
            department,
            COALESCE(SUM(amount), 0) AS total_amount
        FROM sales
        WHERE dt >= :from_dt AND dt <= :to_dt
        {where_dept}
        GROUP BY department
        ORDER BY total_amount DESC
    """

    conn = get_conn()
    return conn.query(sql, params=params)


@st.cache_data(ttl=60, show_spinner=False)
def share_by_region(from_dt: date, to_dt: date, department: Optional[str]) -> pd.DataFrame:
    """Return totals grouped by region for pie chart shares."""

    params = {"from_dt": from_dt, "to_dt": to_dt}
    where_dept = ""
    if department and department != "All":
        where_dept = " AND department = :department"
        params["department"] = department

    sql = f"""
        SELECT
            region,
            COALESCE(SUM(amount), 0) AS total_amount
        FROM sales
        WHERE dt >= :from_dt AND dt <= :to_dt
        {where_dept}
        GROUP BY region
        ORDER BY total_amount DESC
    """

    conn = get_conn()
    return conn.query(sql, params=params)


