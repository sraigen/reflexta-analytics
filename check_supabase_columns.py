#!/usr/bin/env python3
"""
Check what columns actually exist in Supabase procurement_orders table
"""

import psycopg2

def check_supabase_columns():
    """Check the actual columns in Supabase procurement_orders table"""
    
    # Your Supabase connection string (transaction pooler)
    DATABASE_URL = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
    
    print("🔍 Checking Supabase procurement_orders columns")
    print("=" * 50)
    
    try:
        # Connect to Supabase
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("✅ Connected to Supabase successfully!")
        
        # Get all columns in procurement_orders
        print("📋 All columns in procurement_orders table:")
        cur.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'procurement_orders' 
            ORDER BY ordinal_position;
        """)
        columns = cur.fetchall()
        
        for col in columns:
            print(f"   - {col[0]} ({col[1]}) - Nullable: {col[2]}")
        
        # Check specifically for delivery-related columns
        print("\n🔍 Delivery-related columns:")
        delivery_columns = [col for col in columns if 'delivery' in col[0].lower()]
        for col in delivery_columns:
            print(f"   ✅ {col[0]} ({col[1]})")
        
        if not delivery_columns:
            print("   ❌ No delivery-related columns found!")
        
        # Test a simple query
        print("\n🧪 Testing simple query...")
        try:
            cur.execute("SELECT COUNT(*) FROM procurement_orders;")
            count = cur.fetchone()[0]
            print(f"✅ Total orders in Supabase: {count}")
        except Exception as e:
            print(f"❌ Error counting orders: {e}")
        
        # Test the problematic query
        print("\n🧪 Testing the problematic query...")
        try:
            cur.execute("""
                SELECT COUNT(*) as total_orders, 
                       AVG(CASE WHEN delivery_date IS NOT NULL 
                           THEN EXTRACT(DAYS FROM (delivery_date - order_date)) END) as avg_delivery_delay_days 
                FROM procurement_orders 
                WHERE order_date BETWEEN '2025-08-30' AND '2025-09-29';
            """)
            result = cur.fetchone()
            print(f"✅ Query successful! Orders: {result[0]}, Avg delay: {result[1]}")
        except Exception as e:
            print(f"❌ Query failed: {e}")
        
        # Close connection
        cur.close()
        conn.close()
        
        print("\n🎉 Column check completed!")
        
    except Exception as e:
        print(f"❌ Error checking columns: {e}")

if __name__ == "__main__":
    check_supabase_columns()
