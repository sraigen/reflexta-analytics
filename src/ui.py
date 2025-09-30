#!/usr/bin/env python3
"""
UI Components for Reflexta Analytics Platform
Professional UI helpers for Streamlit layout and KPIs.
"""

from __future__ import annotations

from typing import Optional

import pandas as pd
import streamlit as st


def kpi_row(order_count: int, total_amount: float, avg_amount: float) -> None:
    """Render a three-column KPI row with modern animated progress indicators."""

    c1, c2, c3 = st.columns(3)
    
    # Calculate progress percentages (normalized to 0-100)
    max_transactions = max(order_count, 100)  # Ensure we have a reasonable max
    max_revenue = max(total_amount, 100000)   # Ensure we have a reasonable max
    max_avg = max(avg_amount, 10000)         # Ensure we have a reasonable max
    
    trans_progress = min((order_count / max_transactions) * 100, 100)
    rev_progress = min((total_amount / max_revenue) * 100, 100)
    avg_progress = min((avg_amount / max_avg) * 100, 100)
    
    with c1:
        st.markdown(f"""
        <div class="modern-kpi-card" style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 20px;
            padding: 1.5rem;
            color: white;
            text-align: center;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
            transition: all 0.3s ease;
        ">
            <div style="position: absolute; top: -50%; right: -50%; width: 200%; height: 200%; 
                        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                        animation: float 6s ease-in-out infinite;"></div>
            <div style="font-size: 2.2rem; font-weight: 800; margin: 0.5rem 0; position: relative; z-index: 2;">{order_count:,}</div>
            <div style="font-size: 0.85rem; opacity: 0.9; margin-bottom: 1rem; position: relative; z-index: 2;">Total Transactions</div>
            <div style="background: rgba(255,255,255,0.2); border-radius: 10px; height: 6px; overflow: hidden; position: relative; z-index: 2;">
                <div style="background: linear-gradient(90deg, #ffffff, #e2e8f0); height: 100%; width: {trans_progress}%; 
                            border-radius: 10px; transition: width 2s ease-out; animation: slideIn 1.5s ease-out;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with c2:
        st.markdown(f"""
        <div class="modern-kpi-card" style="
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            border-radius: 20px;
            padding: 1.5rem;
            color: white;
            text-align: center;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(16, 185, 129, 0.3);
            transition: all 0.3s ease;
        ">
            <div style="position: absolute; top: -50%; right: -50%; width: 200%; height: 200%; 
                        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                        animation: float 6s ease-in-out infinite reverse;"></div>
            <div style="font-size: 2.2rem; font-weight: 800; margin: 0.5rem 0; position: relative; z-index: 2;">${total_amount:,.0f}</div>
            <div style="font-size: 0.85rem; opacity: 0.9; margin-bottom: 1rem; position: relative; z-index: 2;">Total Revenue</div>
            <div style="background: rgba(255,255,255,0.2); border-radius: 10px; height: 6px; overflow: hidden; position: relative; z-index: 2;">
                <div style="background: linear-gradient(90deg, #ffffff, #d1fae5); height: 100%; width: {rev_progress}%; 
                            border-radius: 10px; transition: width 2s ease-out; animation: slideIn 1.5s ease-out;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with c3:
        st.markdown(f"""
        <div class="modern-kpi-card" style="
            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
            border-radius: 20px;
            padding: 1.5rem;
            color: white;
            text-align: center;
            position: relative;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(245, 158, 11, 0.3);
            transition: all 0.3s ease;
        ">
            <div style="position: absolute; top: -50%; right: -50%; width: 200%; height: 200%; 
                        background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
                        animation: float 6s ease-in-out infinite;"></div>
            <div style="font-size: 2.2rem; font-weight: 800; margin: 0.5rem 0; position: relative; z-index: 2;">${avg_amount:,.0f}</div>
            <div style="font-size: 0.85rem; opacity: 0.9; margin-bottom: 1rem; position: relative; z-index: 2;">Average Amount</div>
            <div style="background: rgba(255,255,255,0.2); border-radius: 10px; height: 6px; overflow: hidden; position: relative; z-index: 2;">
                <div style="background: linear-gradient(90deg, #ffffff, #fef3c7); height: 100%; width: {avg_progress}%; 
                            border-radius: 10px; transition: width 2s ease-out; animation: slideIn 1.5s ease-out;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)


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


