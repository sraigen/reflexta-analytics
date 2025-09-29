#!/usr/bin/env python3
"""
Test different connection string variants for Supabase
"""

import psycopg2
import psycopg2.extras

def test_connection_variants():
    """Test different connection string formats"""
    
    print("🧪 Testing Different Supabase Connection Variants")
    print("=" * 60)
    
    # Test 1: Your current connection string
    current_url = "postgresql://postgres:Sit%401125@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres"
    
    print(f"\n1. Testing current URL: {current_url[:50]}...")
    try:
        conn = psycopg2.connect(current_url)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        print("✅ Current URL works!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Current URL failed: {e}")
    
    # Test 2: Alternative format with different parameters
    alt_url = "postgresql://postgres:Sit%401125@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres?sslmode=require"
    
    print(f"\n2. Testing with SSL mode: {alt_url[:50]}...")
    try:
        conn = psycopg2.connect(alt_url)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        print("✅ SSL mode URL works!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ SSL mode URL failed: {e}")
    
    # Test 3: Connection with explicit parameters
    print(f"\n3. Testing with explicit parameters...")
    try:
        conn = psycopg2.connect(
            host="db.vbowznmcdzsgzntnzwfi.supabase.co",
            port=5432,
            database="postgres",
            user="postgres",
            password="Sit@1125",
            sslmode="require"
        )
        cur = conn.cursor()
        cur.execute("SELECT 1")
        result = cur.fetchone()
        print("✅ Explicit parameters work!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Explicit parameters failed: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 If all tests fail, the issue might be:")
    print("   - Supabase database is not publicly accessible")
    print("   - Firewall blocking Streamlit Cloud")
    print("   - Database is paused or not running")
    print("   - Wrong connection string from Supabase dashboard")

if __name__ == "__main__":
    test_connection_variants()
