#!/usr/bin/env python3
"""
Test transaction pooler connection for IPv4 compatibility
"""

import psycopg2

def test_pooler_connection():
    """Test the transaction pooler connection"""
    
    print("🧪 Testing Transaction Pooler Connection")
    print("=" * 50)
    
    # Transaction pooler connection string (IPv4 compatible)
    pooler_url = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-0-us-west-1.pooler.supabase.com:6543/postgres"
    
    print(f"🔗 Testing pooler URL: {pooler_url[:60]}...")
    
    try:
        conn = psycopg2.connect(pooler_url)
        cur = conn.cursor()
        
        # Test basic connection
        cur.execute("SELECT 1")
        result = cur.fetchone()
        print("✅ Transaction pooler connection successful!")
        
        # Test actual data
        cur.execute("SELECT COUNT(*) FROM finance_departments")
        count = cur.fetchone()[0]
        print(f"✅ Found {count} departments in database")
        
        # Test more data
        cur.execute("SELECT COUNT(*) FROM finance_transactions")
        trans_count = cur.fetchone()[0]
        print(f"✅ Found {trans_count} transactions in database")
        
        cur.close()
        conn.close()
        
        print("\n🎉 Transaction pooler connection works perfectly!")
        print("🔧 Update your Streamlit Cloud secrets with this URL:")
        print(f"   {pooler_url}")
        
    except Exception as e:
        print(f"❌ Transaction pooler connection failed: {e}")
        print("\n🔍 This might be because:")
        print("   - The pooler URL format is different")
        print("   - You need to get the exact URL from Supabase dashboard")
        print("   - The password might be different")

if __name__ == "__main__":
    test_pooler_connection()
