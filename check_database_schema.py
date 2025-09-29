#!/usr/bin/env python3
"""
Check the actual database schema to fix column mismatches
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Database Schema Check",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Database Schema Check")

# Test database connection
try:
    conn = st.connection("sql", type="sql")
    
    st.header("1. Database Connection Test")
    st.success("✅ Database connection successful!")
    
    st.header("2. Check Table Schemas")
    
    # Check procurement_orders table schema
    st.subheader("procurement_orders table schema:")
    try:
        schema_query = """
        SELECT column_name, data_type, is_nullable 
        FROM information_schema.columns 
        WHERE table_name = 'procurement_orders' 
        ORDER BY ordinal_position;
        """
        schema_df = conn.query(schema_query)
        st.dataframe(schema_df)
        
        # Show the actual columns
        columns = schema_df['column_name'].tolist()
        st.write("**Available columns in procurement_orders:**")
        for col in columns:
            st.write(f"- {col}")
            
    except Exception as e:
        st.error(f"❌ Error checking procurement_orders schema: {e}")
    
    # Check finance_transactions table schema
    st.subheader("finance_transactions table schema:")
    try:
        schema_query = """
        SELECT column_name, data_type, is_nullable 
        FROM information_schema.columns 
        WHERE table_name = 'finance_transactions' 
        ORDER BY ordinal_position;
        """
        schema_df = conn.query(schema_query)
        st.dataframe(schema_df)
        
    except Exception as e:
        st.error(f"❌ Error checking finance_transactions schema: {e}")
    
    st.header("3. Sample Data Check")
    
    # Check procurement_orders sample data
    st.subheader("Sample procurement_orders data:")
    try:
        sample_query = "SELECT * FROM procurement_orders LIMIT 3;"
        sample_df = conn.query(sample_query)
        st.dataframe(sample_df)
    except Exception as e:
        st.error(f"❌ Error getting sample data: {e}")
    
    # Check finance_transactions sample data
    st.subheader("Sample finance_transactions data:")
    try:
        sample_query = "SELECT * FROM finance_transactions LIMIT 3;"
        sample_df = conn.query(sample_query)
        st.dataframe(sample_df)
    except Exception as e:
        st.error(f"❌ Error getting sample data: {e}")
    
    st.header("4. All Tables in Database")
    try:
        tables_query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public' 
        ORDER BY table_name;
        """
        tables_df = conn.query(tables_query)
        st.dataframe(tables_df)
    except Exception as e:
        st.error(f"❌ Error getting table list: {e}")
        
except Exception as e:
    st.error(f"❌ Database connection failed: {e}")
