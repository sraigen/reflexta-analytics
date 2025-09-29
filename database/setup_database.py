#!/usr/bin/env python3
"""
Database setup script for Reflexta Analytics Platform.
Creates all necessary tables, views, and sample data for Finance and Procurement modules.
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

import pandas as pd
from sqlalchemy import create_engine, text

def get_database_url():
    """Get database URL from environment or secrets."""
    # Try to get from environment first
    db_url = os.getenv('DATABASE_URL')
    
    if not db_url:
        # Try to read from Streamlit secrets
        try:
            import streamlit as st
            if hasattr(st, 'secrets'):
                db_url = st.secrets.get('connections', {}).get('sql', {}).get('url')
        except:
            pass
    
    if not db_url:
        # Default fallback
        db_url = "postgresql+psycopg://postgres:Sit%401125@localhost:5432/Test"
    
    return db_url

def setup_database():
    """Set up the database with all tables and sample data."""
    
    db_url = get_database_url()
    engine = create_engine(db_url)
    
    # Read the schema file
    schema_file = Path(__file__).parent / "schema.sql"
    
    if not schema_file.exists():
        print(f"❌ Schema file not found: {schema_file}")
        return False
    
    try:
        with open(schema_file, 'r', encoding='utf-8') as f:
            schema_sql = f.read()
        
        print("🔄 Setting up database schema...")
        
        # Execute the schema
        with engine.connect() as conn:
            # Split by semicolon and execute each statement
            statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
            
            for i, statement in enumerate(statements):
                if statement:
                    try:
                        conn.execute(text(statement))
                        conn.commit()
                        print(f"✅ Executed statement {i+1}/{len(statements)}")
                    except Exception as e:
                        print(f"⚠️ Warning executing statement {i+1}: {e}")
                        # Continue with other statements
        
        print("✅ Database setup completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False

def verify_setup():
    """Verify that the database setup was successful."""
    
    db_url = get_database_url()
    engine = create_engine(db_url)
    
    try:
        with engine.connect() as conn:
            # Check if tables exist
            tables_query = """
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_type = 'BASE TABLE'
            ORDER BY table_name;
            """
            
            tables_df = pd.read_sql(tables_query, conn)
            
            print("\n📋 Database Tables Created:")
            for table in tables_df['table_name']:
                print(f"  ✅ {table}")
            
            # Check if views exist
            views_query = """
            SELECT table_name 
            FROM information_schema.views 
            WHERE table_schema = 'public'
            ORDER BY table_name;
            """
            
            views_df = pd.read_sql(views_query, conn)
            
            print("\n👁️ Database Views Created:")
            for view in views_df['table_name']:
                print(f"  ✅ {view}")
            
            # Check sample data
            sample_queries = [
                ("Departments", "SELECT COUNT(*) as count FROM finance_departments"),
                ("Vendors", "SELECT COUNT(*) as count FROM procurement_vendors"),
                ("Transactions", "SELECT COUNT(*) as count FROM finance_transactions"),
                ("Orders", "SELECT COUNT(*) as count FROM procurement_orders")
            ]
            
            print("\n📊 Sample Data:")
            for name, query in sample_queries:
                try:
                    result = pd.read_sql(query, conn)
                    count = result.iloc[0]['count']
                    print(f"  ✅ {name}: {count} records")
                except Exception as e:
                    print(f"  ❌ {name}: Error - {e}")
            
            return True
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 Finance & Procurement Database Setup")
    print("=" * 50)
    
    # Setup database
    if setup_database():
        print("\n🔍 Verifying setup...")
        if verify_setup():
            print("\n🎉 Database setup completed successfully!")
            print("\nNext steps:")
            print("1. Run 'streamlit run app.py' to start the application")
            print("2. Navigate to the Finance and Procurement dashboards")
            print("3. Explore the analytics and visualizations")
        else:
            print("\n⚠️ Setup completed but verification failed. Please check the database manually.")
    else:
        print("\n❌ Database setup failed. Please check your database connection and try again.")

if __name__ == "__main__":
    main()
