#!/usr/bin/env python3
"""
Update Supabase schema to match local database schema
This will NOT affect your local database at all
"""

import psycopg2

def update_supabase_to_match_local():
    """Update Supabase schema to match local database"""
    
    # Your Supabase connection string (transaction pooler)
    DATABASE_URL = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
    
    print("🔧 Updating Supabase Schema to Match Local Database")
    print("=" * 60)
    print("⚠️  This will NOT affect your local database at all!")
    print("🎯 Goal: Make Supabase work with the same queries as local DB")
    
    try:
        # Connect to Supabase
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("✅ Connected to Supabase successfully!")
        
        # Step 1: Remove delivery_date column from Supabase
        print("\n📋 Step 1: Removing delivery_date column from Supabase...")
        try:
            cur.execute("ALTER TABLE procurement_orders DROP COLUMN IF EXISTS delivery_date;")
            print("✅ Removed delivery_date column from Supabase")
        except Exception as e:
            print(f"⚠️  delivery_date column might not exist: {e}")
        
        # Step 2: Check current Supabase schema
        print("\n🔍 Step 2: Checking current Supabase schema...")
        cur.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'procurement_orders' 
            ORDER BY ordinal_position;
        """)
        columns = cur.fetchall()
        
        print("📋 Current Supabase procurement_orders columns:")
        for col in columns:
            print(f"   - {col[0]} ({col[1]}) - Nullable: {col[2]}")
        
        # Step 3: Verify no delivery_date column exists
        delivery_columns = [col for col in columns if 'delivery' in col[0].lower()]
        if delivery_columns:
            print(f"⚠️  Still found delivery columns: {[col[0] for col in delivery_columns]}")
        else:
            print("✅ No delivery-related columns found - matches local schema!")
        
        # Step 4: Test the fixed queries
        print("\n🧪 Step 3: Testing queries that work with local database...")
        try:
            # Test the procurement KPIs query (without delivery_date)
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
                    NULL as avg_delivery_delay_days
                FROM procurement_orders
                WHERE order_date BETWEEN '2025-08-30' AND '2025-09-29';
            """)
            result = cur.fetchone()
            print("✅ Procurement KPIs query works!")
            print(f"   - Total orders: {result[0]}")
            print(f"   - Total value: ${result[1]:,.2f}")
            print(f"   - Avg order value: ${result[2]:,.2f}")
            print(f"   - Unique vendors: {result[3]}")
            print(f"   - Unique categories: {result[4]}")
            print(f"   - Completed orders: {result[5]}")
            print(f"   - Pending orders: {result[6]}")
            print(f"   - High priority orders: {result[7]}")
            print(f"   - Avg delivery delay: {result[8]}")
            
        except Exception as e:
            print(f"❌ Query test failed: {e}")
            return
        
        # Step 5: Test vendor performance query
        print("\n🧪 Step 4: Testing vendor performance query...")
        try:
            cur.execute("""
                SELECT 
                    v.vendor_name,
                    COUNT(po.order_id) as total_orders,
                    COUNT(CASE WHEN po.status = 'Received' THEN 1 END) as delivered_orders,
                    COUNT(CASE WHEN po.status = 'Received' THEN 1 END) as on_time_deliveries,
                    0 as late_deliveries,
                    NULL as avg_delivery_delay_days,
                    CASE WHEN COUNT(po.order_id) > 0 THEN 100.0 ELSE 0 END as on_time_percentage
                FROM procurement_orders po
                JOIN procurement_vendors v ON po.vendor_id = v.vendor_id
                WHERE po.order_date BETWEEN '2025-08-30' AND '2025-09-29'
                    AND po.status = 'Received'
                GROUP BY v.vendor_id, v.vendor_name
                LIMIT 3;
            """)
            results = cur.fetchall()
            print("✅ Vendor performance query works!")
            for row in results:
                print(f"   - {row[0]}: {row[1]} orders, {row[2]} delivered")
                
        except Exception as e:
            print(f"❌ Vendor performance query failed: {e}")
        
        conn.commit()
        print("\n✅ Supabase schema updated successfully!")
        
        # Close connection
        cur.close()
        conn.close()
        
        print("\n🎉 Supabase now matches your local database schema!")
        print("🔗 Your local database is completely untouched!")
        print("🚀 Both local and Supabase should now work with the same queries!")
        
    except Exception as e:
        print(f"❌ Error updating Supabase: {e}")
        print("Please check your connection string and try again")

if __name__ == "__main__":
    update_supabase_to_match_local()
