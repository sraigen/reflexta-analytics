#!/usr/bin/env python3
"""
Setup script for cloud database deployment
Run this script to set up your database schema and sample data in the cloud
"""

import os
import psycopg
from dotenv import load_dotenv

def setup_cloud_database():
    """Set up the database schema and sample data in the cloud"""
    
    # Load environment variables
    load_dotenv()
    
    # Get database URL from environment
    database_url = os.getenv('DATABASE_URL')
    if not database_url:
        print("❌ DATABASE_URL not found in environment variables")
        print("Please set DATABASE_URL in your Streamlit Cloud secrets")
        return False
    
    try:
        # Connect to database
        print("🔌 Connecting to cloud database...")
        conn = psycopg.connect(database_url)
        cur = conn.cursor()
        
        # Read and execute schema
        print("📋 Creating database schema...")
        with open('database/schema.sql', 'r') as f:
            schema_sql = f.read()
        
        # Split by semicolon and execute each statement
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        for stmt in statements:
            if stmt:
                cur.execute(stmt)
        
        conn.commit()
        print("✅ Database schema created successfully!")
        
        # Populate sample data
        print("📊 Populating sample data...")
        exec(open('populate_sample_data.py').read())
        print("✅ Sample data populated successfully!")
        
        # Close connection
        cur.close()
        conn.close()
        
        print("🎉 Cloud database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error setting up cloud database: {e}")
        return False

if __name__ == "__main__":
    setup_cloud_database()
