#!/usr/bin/env python3
"""
Test the corrected connection string
"""

import psycopg2

def test_corrected_connection():
    """Test the corrected connection string"""
    
    print("🧪 Testing Corrected Connection String")
    print("=" * 50)
    
    # Your original (wrong) connection string
    wrong_url = "postgresql://postgres:Sit%401125@db@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres"
    
    # Corrected connection string
    correct_url = "postgresql://postgres:Sit%401125@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres"
    
    print(f"❌ Wrong URL: {wrong_url}")
    print(f"✅ Correct URL: {correct_url}")
    
    print("\n🧪 Testing corrected connection...")
    try:
        conn = psycopg2.connect(correct_url)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        print("✅ Corrected connection works!")
        
        # Test actual data
        cur.execute("SELECT COUNT(*) FROM finance_departments")
        count = cur.fetchone()[0]
        print(f"✅ Found {count} departments in database")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Corrected connection failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎯 The issue was the typo: @db@db should be @db")
    print("   Update your Streamlit Cloud secrets with the correct URL!")

if __name__ == "__main__":
    test_corrected_connection()
