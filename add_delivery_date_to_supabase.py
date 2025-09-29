#!/usr/bin/env python3
"""
Add delivery_date column to Supabase database only (not touching local system)
"""

import psycopg2

def add_delivery_date_to_supabase():
    """Add the missing delivery_date column to Supabase only"""
    
    # Your Supabase connection string (transaction pooler)
    DATABASE_URL = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
    
    print("🔧 Adding delivery_date column to Supabase ONLY")
    print("=" * 50)
    print("⚠️  This will NOT affect your local database at all!")
    
    try:
        # Connect to Supabase
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("✅ Connected to Supabase successfully!")
        
        # Check if delivery_date column already exists
        print("🔍 Checking if delivery_date column exists...")
        cur.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'procurement_orders' 
            AND column_name = 'delivery_date';
        """)
        result = cur.fetchone()
        
        if result:
            print("✅ delivery_date column already exists in Supabase!")
        else:
            print("📋 Adding delivery_date column to procurement_orders...")
            try:
                cur.execute("ALTER TABLE procurement_orders ADD COLUMN delivery_date DATE;")
                print("✅ Added delivery_date column successfully!")
                
                # Set some sample delivery dates for existing orders
                cur.execute("""
                    UPDATE procurement_orders 
                    SET delivery_date = order_date + INTERVAL '15 days' 
                    WHERE delivery_date IS NULL 
                    AND status = 'Received';
                """)
                print("✅ Set sample delivery dates for existing orders")
                
            except Exception as e:
                print(f"❌ Error adding delivery_date column: {e}")
                return
        
        conn.commit()
        print("✅ Changes committed to Supabase successfully!")
        
        # Verify the column exists
        print("🔍 Verifying delivery_date column...")
        cur.execute("""
            SELECT column_name, data_type, is_nullable 
            FROM information_schema.columns 
            WHERE table_name = 'procurement_orders' 
            AND column_name = 'delivery_date';
        """)
        column_info = cur.fetchone()
        
        if column_info:
            print(f"✅ Column verified: {column_info[0]} ({column_info[1]}) - Nullable: {column_info[2]}")
        else:
            print("❌ Column not found!")
        
        # Show sample data
        print("📊 Sample data with delivery_date:")
        cur.execute("SELECT order_id, order_date, delivery_date, status FROM procurement_orders LIMIT 5;")
        sample_data = cur.fetchall()
        for row in sample_data:
            print(f"   Order {row[0]}: {row[1]} -> {row[2]} ({row[3]})")
        
        # Close connection
        cur.close()
        conn.close()
        
        print("\n🎉 Supabase database updated successfully!")
        print("🔗 Your local database is completely untouched!")
        print("🚀 Your Streamlit app should now work!")
        
    except Exception as e:
        print(f"❌ Error updating Supabase: {e}")
        print("Please check your connection string and try again")

if __name__ == "__main__":
    add_delivery_date_to_supabase()
