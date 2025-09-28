#!/usr/bin/env python3
"""
Setup script for Supabase database with your connection string
"""

import psycopg

def setup_supabase_database():
    """Set up the database schema and sample data in Supabase"""
    
    # Your Supabase connection string
    DATABASE_URL = "postgresql://postgres:Sit%401125@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres"
    
    print("🔌 Connecting to Supabase database...")
    print("📋 Setting up database schema and sample data...")
    
    try:
        # Connect to Supabase
        conn = psycopg.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Read and execute schema
        print("📋 Creating database schema...")
        with open('database/schema.sql', 'r') as f:
            schema_sql = f.read()
        
        # Split by semicolon and execute each statement
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        for stmt in statements:
            if stmt:
                try:
                    cur.execute(stmt)
                    print(f"✅ Executed: {stmt[:50]}...")
                except Exception as e:
                    print(f"⚠️  Warning: {e}")
        
        conn.commit()
        print("✅ Database schema created successfully!")
        
        # Populate sample data
        print("📊 Populating sample data...")
        
        # Run the populate script
        import subprocess
        result = subprocess.run(['python', 'populate_sample_data.py'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Sample data populated successfully!")
        else:
            print(f"⚠️  Warning: {result.stderr}")
            print("You may need to run populate_sample_data.py manually")
        
        # Close connection
        cur.close()
        conn.close()
        
        print("🎉 Supabase database setup completed successfully!")
        print("🔗 Your database is ready for Streamlit Cloud deployment!")
        
    except Exception as e:
        print(f"❌ Error setting up Supabase database: {e}")
        print("Please check your connection string and try again")

if __name__ == "__main__":
    setup_supabase_database()
