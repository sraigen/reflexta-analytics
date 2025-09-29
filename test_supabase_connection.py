#!/usr/bin/env python3
"""
Test Supabase connection string to verify it works
"""

import psycopg
import streamlit as st

def test_supabase_connection():
    """Test the Supabase connection string"""
    
    # Your Supabase connection string
    DATABASE_URL = "postgresql://postgres:Sit%401125@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres"
    
    print("🔌 Testing Supabase connection...")
    print(f"📋 Database URL: {DATABASE_URL[:50]}...")
    
    try:
        # Test direct connection
        conn = psycopg.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("✅ Direct connection successful!")
        
        # Test basic query
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"📊 Database version: {version[0][:50]}...")
        
        # Test table access
        cur.execute("SELECT COUNT(*) FROM finance_departments;")
        dept_count = cur.fetchone()[0]
        print(f"📊 Finance departments: {dept_count} rows")
        
        cur.execute("SELECT COUNT(*) FROM finance_transactions;")
        trans_count = cur.fetchone()[0]
        print(f"📊 Finance transactions: {trans_count} rows")
        
        cur.execute("SELECT COUNT(*) FROM procurement_orders;")
        order_count = cur.fetchone()[0]
        print(f"📊 Procurement orders: {order_count} rows")
        
        cur.close()
        conn.close()
        
        print("✅ All database queries successful!")
        print("🔗 Your connection string is working correctly!")
        
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

def test_streamlit_connection():
    """Test Streamlit connection using st.connection"""
    
    print("\n🔌 Testing Streamlit connection...")
    
    try:
        # Test Streamlit connection
        conn = st.connection("sql", type="sql")
        
        if conn is None:
            print("❌ Streamlit connection is None")
            return False
            
        print("✅ Streamlit connection created!")
        
        # Test query
        df = conn.query("SELECT COUNT(*) as count FROM finance_departments")
        print(f"📊 Query result: {df}")
        
        return True
        
    except Exception as e:
        print(f"❌ Streamlit connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Supabase Connection")
    print("=" * 50)
    
    # Test direct connection
    direct_success = test_supabase_connection()
    
    if direct_success:
        print("\n" + "=" * 50)
        print("🧪 Testing Streamlit Connection")
        print("=" * 50)
        
        # Test Streamlit connection
        streamlit_success = test_streamlit_connection()
        
        if streamlit_success:
            print("\n🎉 All tests passed! Your connection should work in Streamlit Cloud.")
        else:
            print("\n⚠️  Direct connection works but Streamlit connection failed.")
            print("This might be a secrets configuration issue.")
    else:
        print("\n❌ Direct connection failed. Check your connection string.")
