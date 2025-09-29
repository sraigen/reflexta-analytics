#!/usr/bin/env python3
"""
Check the local database schema to understand what columns exist
"""

import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Local Database Schema Check",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Local Database Schema Check")

# Test database connection
try:
    conn = st.connection("sql", type="sql")
    
    st.header("1. Database Connection Test")
    st.success("✅ Database connection successful!")
    
    st.header("2. Check procurement_orders table schema")
    
    # Check procurement_orders table schema
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
            
        # Check for delivery-related columns
        delivery_columns = [col for col in columns if 'delivery' in col.lower()]
        st.write("**Delivery-related columns:**")
        for col in delivery_columns:
            st.write(f"- {col}")
            
    except Exception as e:
        st.error(f"❌ Error checking procurement_orders schema: {e}")
    
    st.header("3. Sample Data Check")
    
    # Check procurement_orders sample data
    try:
        sample_query = "SELECT * FROM procurement_orders LIMIT 3;"
        sample_df = conn.query(sample_query)
        st.dataframe(sample_df)
    except Exception as e:
        st.error(f"❌ Error getting sample data: {e}")
    
    st.header("4. Test Current Query")
    
    # Test the current query that's failing
    try:
        test_query = """
        SELECT COUNT(*) as total_orders, 
               SUM(grand_total) as total_value,
               AVG(grand_total) as avg_order_value
        FROM procurement_orders 
        WHERE order_date BETWEEN '2025-08-30' AND '2025-09-29';
        """
        result_df = conn.query(test_query)
        st.success("✅ Basic query works!")
        st.dataframe(result_df)
    except Exception as e:
        st.error(f"❌ Basic query failed: {e}")
    
    st.header("5. Test Delivery Date Query")
    
    # Test if delivery_date column exists and works
    try:
        delivery_query = """
        SELECT COUNT(*) as total_orders,
               AVG(CASE WHEN delivery_date IS NOT NULL 
                   THEN (delivery_date - order_date) END) as avg_delivery_delay_days 
        FROM procurement_orders 
        WHERE order_date BETWEEN '2025-08-30' AND '2025-09-29';
        """
        result_df = conn.query(delivery_query)
        st.success("✅ Delivery date query works!")
        st.dataframe(result_df)
    except Exception as e:
        st.error(f"❌ Delivery date query failed: {e}")
        st.info("This means delivery_date column doesn't exist in local database")
        
except Exception as e:
    st.error(f"❌ Database connection failed: {e}")
    st.info("This might be a local database configuration issue")
