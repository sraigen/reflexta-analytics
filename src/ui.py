from __future__ import annotations

"""UI helpers for Streamlit layout and KPIs."""

from typing import Optional

import pandas as pd
import streamlit as st


def kpi_row(order_count: int, total_amount: float, avg_amount: float) -> None:
    """Render a three-column KPI row with luxury professional metric cards."""

    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); 
                    border: 1px solid rgba(148, 163, 184, 0.2); border-left: 4px solid #6366f1; 
                    padding: 2rem; border-radius: 16px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(255, 255, 255, 0.8); 
                    text-align: center; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); backdrop-filter: blur(10px);">
            <div style="font-size: 2.5rem; font-weight: 800; color: #1e293b; margin: 0.5rem 0; text-shadow: 0 1px 2px rgba(0,0,0,0.1);">{:,}</div>
            <div style="font-size: 0.9rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Total Transactions</div>
        </div>
        """.format(order_count), unsafe_allow_html=True)
    
    with c2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); 
                    border: 1px solid rgba(148, 163, 184, 0.2); border-left: 4px solid #10b981; 
                    padding: 2rem; border-radius: 16px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(255, 255, 255, 0.8); 
                    text-align: center; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); backdrop-filter: blur(10px);">
            <div style="font-size: 2.5rem; font-weight: 800; color: #1e293b; margin: 0.5rem 0; text-shadow: 0 1px 2px rgba(0,0,0,0.1);">${:,.0f}</div>
            <div style="font-size: 0.9rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Total Revenue</div>
        </div>
        """.format(total_amount), unsafe_allow_html=True)
    
    with c3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%); 
                    border: 1px solid rgba(148, 163, 184, 0.2); border-left: 4px solid #f59e0b; 
                    padding: 2rem; border-radius: 16px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1), 0 0 0 1px rgba(255, 255, 255, 0.8); 
                    text-align: center; transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); backdrop-filter: blur(10px);">
            <div style="font-size: 2.5rem; font-weight: 800; color: #1e293b; margin: 0.5rem 0; text-shadow: 0 1px 2px rgba(0,0,0,0.1);">${:,.0f}</div>
            <div style="font-size: 0.9rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">Average Amount</div>
        </div>
        """.format(avg_amount), unsafe_allow_html=True)


def section_header(title: str, subtitle: Optional[str] = None) -> None:
    """Render a consistent section header with luxury styling."""

    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; padding: 1.5rem 2rem; border-radius: 12px; 
                margin: 2rem 0 1.5rem 0; font-size: 1.4rem; font-weight: 700; 
                text-align: center; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15); 
                border: 1px solid rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px);">
        {title}
    </div>
    """, unsafe_allow_html=True)
    
    if subtitle:
        st.markdown(f"""
        <div style="text-align: center; color: #64748b; font-size: 1rem; margin-bottom: 1rem;">
            {subtitle}
        </div>
        """, unsafe_allow_html=True)


def empty_state(df: pd.DataFrame, message: str = "No data for selected filters.") -> bool:
    """If DataFrame is empty, show info and return True; otherwise False."""

    if df is None or df.empty:
        st.info(message)
        return True
    return False


