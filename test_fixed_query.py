#!/usr/bin/env python3
"""
Test the fixed query to make sure it works
"""

import psycopg2

def test_fixed_query():
    """Test the fixed query without EXTRACT function"""
    
    # Your Supabase connection string (transaction pooler)
    DATABASE_URL = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
    
    print("🧪 Testing Fixed Query")
    print("=" * 30)
    
    try:
        # Connect to Supabase
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("✅ Connected to Supabase successfully!")
        
        # Test the fixed query
        print("🧪 Testing the fixed query...")
        try:
            cur.execute("""
                SELECT COUNT(*) as total_orders, 
                       AVG(CASE WHEN delivery_date IS NOT NULL 
                           THEN (delivery_date - order_date) END) as avg_delivery_delay_days 
                FROM procurement_orders 
                WHERE order_date BETWEEN '2025-08-30' AND '2025-09-29';
            """)
            result = cur.fetchone()
            print(f"✅ Query successful!")
            print(f"   - Total orders: {result[0]}")
            print(f"   - Avg delivery delay: {result[1]} days")
        except Exception as e:
            print(f"❌ Query failed: {e}")
            return
        
        # Test the full procurement KPIs query
        print("\n🧪 Testing full procurement KPIs query...")
        try:
            cur.execute("""
                SELECT 
                    COUNT(*) as total_orders,
                    SUM(grand_total) as total_value,
                    AVG(grand_total) as avg_order_value,
                    COUNT(DISTINCT vendor_id) as unique_vendors,
                    COUNT(DISTINCT category_id) as unique_categories,
                    COUNT(CASE WHEN status = 'Received' THEN 1 END) as completed_orders,
                    COUNT(CASE WHEN status IN ('Draft', 'Submitted', 'Approved', 'Ordered') THEN 1 END) as pending_orders,
                    COUNT(CASE WHEN priority = 'High' OR priority = 'Urgent' THEN 1 END) as high_priority_orders,
                    AVG(CASE WHEN delivery_date IS NOT NULL 
                        THEN (delivery_date - order_date) END) as avg_delivery_delay_days
                FROM procurement_orders
                WHERE order_date BETWEEN '2025-08-30' AND '2025-09-29';
            """)
            result = cur.fetchone()
            print(f"✅ Full query successful!")
            print(f"   - Total orders: {result[0]}")
            print(f"   - Total value: ${result[1]:,.2f}")
            print(f"   - Avg order value: ${result[2]:,.2f}")
            print(f"   - Unique vendors: {result[3]}")
            print(f"   - Unique categories: {result[4]}")
            print(f"   - Completed orders: {result[5]}")
            print(f"   - Pending orders: {result[6]}")
            print(f"   - High priority orders: {result[7]}")
            print(f"   - Avg delivery delay: {result[8]} days")
        except Exception as e:
            print(f"❌ Full query failed: {e}")
        
        # Close connection
        cur.close()
        conn.close()
        
        print("\n🎉 All queries working successfully!")
        print("🚀 Your Streamlit app should now work!")
        
    except Exception as e:
        print(f"❌ Error testing queries: {e}")

if __name__ == "__main__":
    test_fixed_query()
