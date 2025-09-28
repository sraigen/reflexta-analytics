from __future__ import annotations

"""UI helpers for Streamlit layout and KPIs."""

from typing import Optional

import pandas as pd
import streamlit as st


def kpi_row(order_count: int, total_amount: float, avg_amount: float) -> None:
    """Render a three-column KPI row with professional metric cards."""

    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div style="background: white; border: 1px solid #dee2e6; border-left: 4px solid #007bff; 
                    padding: 1.5rem; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); text-align: center;">
            <div style="font-size: 2rem; font-weight: 600; color: #2c3e50; margin: 0.5rem 0;">{:,}</div>
            <div style="font-size: 0.9rem; color: #6c757d; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Total Transactions</div>
        </div>
        """.format(order_count), unsafe_allow_html=True)
    
    with c2:
        st.markdown("""
        <div style="background: white; border: 1px solid #dee2e6; border-left: 4px solid #28a745; 
                    padding: 1.5rem; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); text-align: center;">
            <div style="font-size: 2rem; font-weight: 600; color: #2c3e50; margin: 0.5rem 0;">${:,.0f}</div>
            <div style="font-size: 0.9rem; color: #6c757d; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Total Revenue</div>
        </div>
        """.format(total_amount), unsafe_allow_html=True)
    
    with c3:
        st.markdown("""
        <div style="background: white; border: 1px solid #dee2e6; border-left: 4px solid #ffc107; 
                    padding: 1.5rem; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); text-align: center;">
            <div style="font-size: 2rem; font-weight: 600; color: #2c3e50; margin: 0.5rem 0;">${:,.0f}</div>
            <div style="font-size: 0.9rem; color: #6c757d; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px;">Average Amount</div>
        </div>
        """.format(avg_amount), unsafe_allow_html=True)


def section_header(title: str, subtitle: Optional[str] = None) -> None:
    """Render a consistent section header with optional subtitle."""

    st.subheader(title)
    if subtitle:
        st.caption(subtitle)
    st.divider()


def empty_state(df: pd.DataFrame, message: str = "No data for selected filters.") -> bool:
    """If DataFrame is empty, show info and return True; otherwise False."""

    if df is None or df.empty:
        st.info(message)
        return True
    return False


