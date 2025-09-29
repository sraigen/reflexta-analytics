#!/usr/bin/env python3
"""
Fix Supabase schema to add missing columns that queries expect
"""

import psycopg2

def fix_supabase_schema():
    """Add missing columns to match query expectations"""
    
    # Your Supabase connection string (transaction pooler)
    DATABASE_URL = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
    
    print("🔧 Fixing Supabase Schema - Adding Missing Columns")
    print("=" * 60)
    
    try:
        # Connect to Supabase
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("✅ Connected to Supabase successfully!")
        
        # Add missing columns to procurement_orders
        print("📋 Adding missing columns to procurement_orders...")
        
        # Add expected_delivery_date column
        try:
            cur.execute("ALTER TABLE procurement_orders ADD COLUMN expected_delivery_date DATE;")
            print("✅ Added expected_delivery_date column")
        except Exception as e:
            print(f"⚠️  expected_delivery_date column might already exist: {e}")
        
        # Add actual_delivery_date column
        try:
            cur.execute("ALTER TABLE procurement_orders ADD COLUMN actual_delivery_date DATE;")
            print("✅ Added actual_delivery_date column")
        except Exception as e:
            print(f"⚠️  actual_delivery_date column might already exist: {e}")
        
        # Update existing delivery_date to actual_delivery_date
        try:
            cur.execute("UPDATE procurement_orders SET actual_delivery_date = delivery_date WHERE delivery_date IS NOT NULL;")
            print("✅ Updated actual_delivery_date from delivery_date")
        except Exception as e:
            print(f"⚠️  Could not update actual_delivery_date: {e}")
        
        # Set expected_delivery_date to order_date + 30 days for existing records
        try:
            cur.execute("UPDATE procurement_orders SET expected_delivery_date = order_date + INTERVAL '30 days' WHERE expected_delivery_date IS NULL;")
            print("✅ Set expected_delivery_date for existing records")
        except Exception as e:
            print(f"⚠️  Could not set expected_delivery_date: {e}")
        
        conn.commit()
        print("✅ Schema fixes applied successfully!")
        
        # Verify the columns exist
        print("🔍 Verifying columns...")
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'procurement_orders' 
            AND column_name IN ('delivery_date', 'expected_delivery_date', 'actual_delivery_date')
            ORDER BY column_name;
        """)
        columns = cur.fetchall()
        print("📋 Delivery-related columns:")
        for col in columns:
            print(f"   - {col[0]} ({col[1]})")
        
        # Close connection
        cur.close()
        conn.close()
        
        print("\n🎉 Supabase schema fixed successfully!")
        print("🔗 Your app should now work with the correct columns!")
        
    except Exception as e:
        print(f"❌ Error fixing schema: {e}")
        print("Please check your connection string and try again")

if __name__ == "__main__":
    fix_supabase_schema()
