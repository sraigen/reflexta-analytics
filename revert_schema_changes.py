#!/usr/bin/env python3
"""
Revert the schema changes that caused issues
"""

import psycopg2

def revert_schema_changes():
    """Remove the columns that were added and caused issues"""
    
    # Your Supabase connection string (transaction pooler)
    DATABASE_URL = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
    
    print("🔄 Reverting Schema Changes")
    print("=" * 40)
    
    try:
        # Connect to Supabase
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("✅ Connected to Supabase successfully!")
        
        # Remove the problematic columns
        print("📋 Removing problematic columns...")
        
        # Remove actual_delivery_date column
        try:
            cur.execute("ALTER TABLE procurement_orders DROP COLUMN IF EXISTS actual_delivery_date;")
            print("✅ Removed actual_delivery_date column")
        except Exception as e:
            print(f"⚠️  Could not remove actual_delivery_date: {e}")
        
        # Remove expected_delivery_date column
        try:
            cur.execute("ALTER TABLE procurement_orders DROP COLUMN IF EXISTS expected_delivery_date;")
            print("✅ Removed expected_delivery_date column")
        except Exception as e:
            print(f"⚠️  Could not remove expected_delivery_date: {e}")
        
        conn.commit()
        print("✅ Schema changes reverted successfully!")
        
        # Verify the columns are gone
        print("🔍 Verifying columns...")
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'procurement_orders' 
            AND column_name IN ('delivery_date', 'expected_delivery_date', 'actual_delivery_date')
            ORDER BY column_name;
        """)
        columns = cur.fetchall()
        print("📋 Remaining delivery-related columns:")
        for col in columns:
            print(f"   - {col[0]} ({col[1]})")
        
        # Close connection
        cur.close()
        conn.close()
        
        print("\n🎉 Schema changes reverted successfully!")
        print("🔗 Now we'll fix the queries to work with the original schema!")
        
    except Exception as e:
        print(f"❌ Error reverting schema: {e}")
        print("Please check your connection string and try again")

if __name__ == "__main__":
    revert_schema_changes()
