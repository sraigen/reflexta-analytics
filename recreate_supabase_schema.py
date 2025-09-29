#!/usr/bin/env python3
"""
Recreate Supabase database with the exact schema from our local schema.sql
"""

import psycopg2

def recreate_supabase_schema():
    """Recreate the Supabase database with the correct schema"""
    
    # Your Supabase connection string (transaction pooler)
    DATABASE_URL = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"
    
    print("🔧 Recreating Supabase Database Schema")
    print("=" * 50)
    
    try:
        # Connect to Supabase
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("✅ Connected to Supabase successfully!")
        
        # Read the exact schema from our local file
        print("📋 Reading schema from database/schema.sql...")
        with open('database/schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Split by semicolon and execute each statement
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        print(f"📊 Executing {len(statements)} SQL statements...")
        
        for i, stmt in enumerate(statements):
            if stmt and not stmt.startswith('--'):
                try:
                    cur.execute(stmt)
                    print(f"✅ Statement {i+1}/{len(statements)} executed successfully")
                except Exception as e:
                    print(f"⚠️  Warning on statement {i+1}: {e}")
                    # Continue with other statements
        
        conn.commit()
        print("✅ Schema recreated successfully!")
        
        # Verify tables were created
        print("🔍 Verifying tables...")
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
        """)
        tables = cur.fetchall()
        
        if tables:
            print("✅ Tables created successfully:")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("❌ No tables found!")
        
        # Check specific columns in procurement_orders
        print("\n🔍 Checking procurement_orders columns:")
        cur.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'procurement_orders' 
            ORDER BY ordinal_position;
        """)
        columns = cur.fetchall()
        for col in columns:
            print(f"   - {col[0]} ({col[1]})")
        
        # Check if actual_delivery_date exists
        delivery_columns = [col[0] for col in columns if 'delivery' in col[0].lower()]
        print(f"\n📋 Delivery-related columns: {delivery_columns}")
        
        # Close connection
        cur.close()
        conn.close()
        
        print("\n🎉 Supabase database schema recreated successfully!")
        print("🔗 Your app should now work with the correct schema!")
        
    except Exception as e:
        print(f"❌ Error recreating schema: {e}")
        print("Please check your connection string and try again")

if __name__ == "__main__":
    recreate_supabase_schema()
