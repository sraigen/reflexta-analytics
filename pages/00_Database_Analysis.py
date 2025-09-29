from __future__ import annotations

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime as dt
from typing import Optional, Any

# Import database and query functions
from src.db import get_conn, health_check
from src.ui import empty_state

st.set_page_config(page_title="Database Analysis", layout="wide")

# Professional CSS for Database Analysis
st.markdown("""
<style>
    .db-header {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        color: white;
        padding: 3rem 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3), 0 0 0 1px rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        position: relative;
        overflow: hidden;
    }
    
    .db-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: linear-gradient(45deg, rgba(255,255,255,0.1) 0%, transparent 50%);
        pointer-events: none;
    }
    
    .db-header h1 {
        margin: 0;
        font-size: 3rem;
        font-weight: 800;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.4);
        position: relative;
        z-index: 1;
        background: linear-gradient(45deg, #ffffff, #e2e8f0);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .db-header p {
        margin: 1rem 0 0 0;
        font-size: 1.3rem;
        opacity: 0.9;
        font-weight: 500;
        position: relative;
        z-index: 1;
    }
    
    .section-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.2rem 2rem;
        border-radius: 10px;
        margin: 2rem 0 1.5rem 0;
        font-size: 1.4rem;
        font-weight: 600;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .metric-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #667eea;
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }
    
    .metric-value {
        font-size: 2.5rem;
        font-weight: 800;
        color: #2c3e50;
        margin: 0;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
    }
    
    .metric-label {
        font-size: 1rem;
        color: #7f8c8d;
        margin: 0.5rem 0 0 0;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 600;
    }
    
    .status-connected {
        background: linear-gradient(90deg, #27ae60 0%, #2ecc71 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(39, 174, 96, 0.3);
    }
    
    .status-disconnected {
        background: linear-gradient(90deg, #e74c3c 0%, #c0392b 100%);
        color: white;
        padding: 1rem 2rem;
        border-radius: 10px;
        text-align: center;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
    }
    
    .table-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
        border-left: 4px solid #667eea;
    }
    
    .table-name {
        font-size: 1.2rem;
        font-weight: 700;
        color: #2c3e50;
        margin: 0 0 0.5rem 0;
    }
    
    .table-stats {
        font-size: 0.9rem;
        color: #7f8c8d;
        margin: 0;
    }
    
    .analysis-section {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
    
    .data-preview {
        background: white;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="db-header">
    <h1>🗄️ Database Analysis</h1>
    <p>Comprehensive Database Structure & Data Insights</p>
</div>
""", unsafe_allow_html=True)

# Check database connection
if not health_check():
    st.markdown("""
    <div class="status-disconnected">
        ❌ Database Connection Failed
    </div>
    """, unsafe_allow_html=True)
    st.error("Database connection failed. Please check your connection settings.")
    st.stop()
else:
    st.markdown("""
    <div class="status-connected">
        ✅ Database Connected Successfully
    </div>
    """, unsafe_allow_html=True)

try:
    conn = get_conn()
    
    # Database Overview
    st.markdown('<div class="section-header">📊 Database Overview</div>', unsafe_allow_html=True)
    
    # Get database statistics
    overview_query = """
    SELECT 
        schemaname,
        tablename,
        tableowner,
        hasindexes,
        hasrules,
        hastriggers
    FROM pg_tables 
    WHERE schemaname = 'public'
    ORDER BY tablename
    """
    
    tables_df = conn.query(overview_query)
    
    if not tables_df.empty:
        # Create overview metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{len(tables_df)}</div>
                <div class="metric-label">Total Tables</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            # Count tables with indexes
            indexed_tables = len(tables_df[tables_df['hasindexes'] == True])
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{indexed_tables}</div>
                <div class="metric-label">Indexed Tables</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            # Count tables with triggers
            triggered_tables = len(tables_df[tables_df['hastriggers'] == True])
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{triggered_tables}</div>
                <div class="metric-label">Tables with Triggers</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            # Count tables with rules
            ruled_tables = len(tables_df[tables_df['hasrules'] == True])
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-value">{ruled_tables}</div>
                <div class="metric-label">Tables with Rules</div>
            </div>
            """, unsafe_allow_html=True)
    
    # Tables List
    st.markdown('<div class="section-header">📋 Database Tables</div>', unsafe_allow_html=True)
    
    if not tables_df.empty:
        # Display tables in a more organized way
        for _, table in tables_df.iterrows():
            table_name = table['tablename']
            
            # Get row count for each table
            try:
                count_query = f"SELECT COUNT(*) as row_count FROM {table_name}"
                count_result = conn.query(count_query)
                row_count = count_result.iloc[0]['row_count'] if not count_result.empty else 0
            except:
                row_count = 0
            
            # Get column count
            try:
                column_query = f"""
                SELECT COUNT(*) as column_count 
                FROM information_schema.columns 
                WHERE table_name = '{table_name}' AND table_schema = 'public'
                """
                column_result = conn.query(column_query)
                column_count = column_result.iloc[0]['column_count'] if not column_result.empty else 0
            except:
                column_count = 0
            
            st.markdown(f"""
            <div class="table-card">
                <div class="table-name">{table_name}</div>
                <div class="table-stats">
                    📊 {row_count:,} rows • 📝 {column_count} columns • 
                    {'🔍 Indexed' if table['hasindexes'] else '❌ No Index'} • 
                    {'⚡ Triggered' if table['hastriggers'] else '❌ No Trigger'}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Table Analysis Section
    st.markdown('<div class="section-header">🔍 Detailed Table Analysis</div>', unsafe_allow_html=True)
    
    # Table selection
    if not tables_df.empty:
        table_names = tables_df['tablename'].tolist()
        selected_table = st.selectbox(
            "Select a table to analyze:",
            options=table_names,
            help="Choose a table to view detailed analysis"
        )
        
        if selected_table:
            st.markdown(f"""
            <div class="analysis-section">
                <h3>📊 Analyzing: {selected_table}</h3>
            </div>
            """, unsafe_allow_html=True)
            
            # Get table structure
            structure_query = f"""
            SELECT 
                column_name,
                data_type,
                is_nullable,
                column_default,
                character_maximum_length
            FROM information_schema.columns 
            WHERE table_name = '{selected_table}' AND table_schema = 'public'
            ORDER BY ordinal_position
            """
            
            structure_df = conn.query(structure_query)
            
            if not structure_df.empty:
                st.markdown("#### 📝 Table Structure")
                st.dataframe(
                    structure_df,
                    hide_index=True,
                    column_config={
                        "column_name": "Column Name",
                        "data_type": "Data Type",
                        "is_nullable": "Nullable",
                        "column_default": "Default Value",
                        "character_maximum_length": "Max Length"
                    }
                )
            
            # Get sample data
            try:
                sample_query = f"SELECT * FROM {selected_table} LIMIT 10"
                sample_df = conn.query(sample_query)
                
                if not sample_df.empty:
                    st.markdown("#### 📋 Sample Data (First 10 rows)")
                    st.dataframe(sample_df, hide_index=True)
                else:
                    st.info("No data available in this table.")
            except Exception as e:
                st.warning(f"Could not retrieve sample data: {str(e)}")
            
            # Get table statistics
            try:
                # Get total row count
                count_query = f"SELECT COUNT(*) as total_rows FROM {selected_table}"
                count_df = conn.query(count_query)
                
                # Get unique row count (approximate using a different approach)
                # For now, we'll just use the total count as unique count
                # In a real scenario, you might want to check for primary keys or unique constraints
                stats_df = count_df.copy()
                stats_df['unique_rows'] = stats_df['total_rows']  # Simplified approach
                
                if not stats_df.empty:
                    stats_row = stats_df.iloc[0]
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric("Total Rows", f"{stats_row['total_rows']:,}")
                    
                    with col2:
                        st.metric("Unique Rows", f"{stats_row['unique_rows']:,}")
                    
                    with col3:
                        if stats_row['total_rows'] > 0:
                            uniqueness = (stats_row['unique_rows'] / stats_row['total_rows']) * 100
                            st.metric("Data Uniqueness", f"{uniqueness:.1f}%")
                        else:
                            st.metric("Data Uniqueness", "N/A")
            except Exception as e:
                st.warning(f"Could not retrieve table statistics: {str(e)}")
    
    # Database Health Check
    st.markdown('<div class="section-header">🏥 Database Health Check</div>', unsafe_allow_html=True)
    
    try:
        # Check for foreign key constraints
        fk_query = """
        SELECT 
            tc.table_name,
            kcu.column_name,
            ccu.table_name AS foreign_table_name,
            ccu.column_name AS foreign_column_name
        FROM information_schema.table_constraints AS tc 
        JOIN information_schema.key_column_usage AS kcu
            ON tc.constraint_name = kcu.constraint_name
            AND tc.table_schema = kcu.table_schema
        JOIN information_schema.constraint_column_usage AS ccu
            ON ccu.constraint_name = tc.constraint_name
            AND ccu.table_schema = tc.table_schema
        WHERE tc.constraint_type = 'FOREIGN KEY'
        """
        
        fk_df = conn.query(fk_query)
        
        if not fk_df.empty:
            st.success(f"✅ Found {len(fk_df)} foreign key relationships")
            st.dataframe(fk_df, hide_index=True)
        else:
            st.warning("⚠️ No foreign key relationships found")
        
        # Check for indexes
        index_query = """
        SELECT 
            schemaname,
            tablename,
            indexname,
            indexdef
        FROM pg_indexes 
        WHERE schemaname = 'public'
        ORDER BY tablename, indexname
        """
        
        index_df = conn.query(index_query)
        
        if not index_df.empty:
            st.success(f"✅ Found {len(index_df)} indexes")
        else:
            st.warning("⚠️ No indexes found")
            
    except Exception as e:
        st.error(f"Error during health check: {str(e)}")

except Exception as e:
    st.error(f"Error loading database analysis: {str(e)}")
    st.info("Please check your database connection and try again.")

# Render floating AI chat
from src.floating_ai_chat import render_floating_ai_chat
render_floating_ai_chat()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <p>🗄️ Database Analysis - Reflexta Data Intelligence</p>
    <p>Comprehensive Database Structure & Data Insights</p>
</div>
""", unsafe_allow_html=True)