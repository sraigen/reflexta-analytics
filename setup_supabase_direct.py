#!/usr/bin/env python3
"""
Direct Supabase database setup with your connection string
"""

import psycopg
import os

def setup_supabase_database():
    """Set up the database schema and sample data in Supabase"""
    
    # Your Supabase connection string
    DATABASE_URL = "postgresql://postgres:Sit%401125@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres"
    
    print("🔌 Connecting to Supabase database...")
    print(f"📋 Database URL: {DATABASE_URL[:50]}...")
    
    try:
        # Connect to Supabase
        conn = psycopg.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("✅ Connected to Supabase successfully!")
        
        # Test connection
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"📊 Database version: {version[0][:50]}...")
        
        # Read and execute schema
        print("📋 Creating database schema...")
        with open('database/schema.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        # Split by semicolon and execute each statement
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        for i, stmt in enumerate(statements):
            if stmt and not stmt.startswith('--'):
                try:
                    cur.execute(stmt)
                    print(f"✅ Statement {i+1}/{len(statements)} executed successfully")
                except Exception as e:
                    print(f"⚠️  Warning on statement {i+1}: {e}")
                    # Continue with other statements
        
        conn.commit()
        print("✅ Database schema committed successfully!")
        
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
        
        # Close connection
        cur.close()
        conn.close()
        
        print("🎉 Supabase database setup completed!")
        print("🔗 You can now check your Supabase dashboard")
        
    except Exception as e:
        print(f"❌ Error setting up Supabase database: {e}")
        print("Please check your connection string and try again")

if __name__ == "__main__":
    setup_supabase_database()
