#!/usr/bin/env python3
"""
Simplified Supabase database setup - creates tables without complex triggers
"""

import psycopg

def setup_supabase_database():
    """Set up the database schema and sample data in Supabase"""
    
    # Your Supabase connection string
    DATABASE_URL = "postgresql://postgres:Sit%401125@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres"
    
    print("🔌 Connecting to Supabase database...")
    
    try:
        # Connect to Supabase
        conn = psycopg.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("✅ Connected to Supabase successfully!")
        
        # Create tables one by one to avoid transaction issues
        print("📋 Creating database tables...")
        
        # 1. Finance Departments
        print("Creating finance_departments...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS finance_departments (
                dept_id SERIAL PRIMARY KEY,
                dept_name VARCHAR(100) NOT NULL,
                dept_code VARCHAR(20) UNIQUE NOT NULL,
                manager_name VARCHAR(100),
                budget_allocated DECIMAL(15,2) DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 2. Cost Centers
        print("Creating finance_cost_centers...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS finance_cost_centers (
                cost_center_id SERIAL PRIMARY KEY,
                cost_center_name VARCHAR(100) NOT NULL,
                cost_center_code VARCHAR(20) UNIQUE NOT NULL,
                dept_id INTEGER REFERENCES finance_departments(dept_id),
                manager_name VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 3. Chart of Accounts
        print("Creating finance_accounts...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS finance_accounts (
                account_id SERIAL PRIMARY KEY,
                account_name VARCHAR(100) NOT NULL,
                account_code VARCHAR(20) UNIQUE NOT NULL,
                account_type VARCHAR(20) CHECK (account_type IN ('Asset', 'Liability', 'Equity', 'Revenue', 'Expense')),
                parent_account_id INTEGER REFERENCES finance_accounts(account_id),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 4. Budgets
        print("Creating finance_budgets...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS finance_budgets (
                budget_id SERIAL PRIMARY KEY,
                dept_id INTEGER REFERENCES finance_departments(dept_id),
                cost_center_id INTEGER REFERENCES finance_cost_centers(cost_center_id),
                account_id INTEGER REFERENCES finance_accounts(account_id),
                budget_year INTEGER NOT NULL,
                allocated_amount DECIMAL(15,2) NOT NULL,
                spent_amount DECIMAL(15,2) DEFAULT 0,
                remaining_amount DECIMAL(15,2) GENERATED ALWAYS AS (allocated_amount - spent_amount) STORED,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 5. Financial Transactions
        print("Creating finance_transactions...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS finance_transactions (
                transaction_id SERIAL PRIMARY KEY,
                dept_id INTEGER REFERENCES finance_departments(dept_id),
                cost_center_id INTEGER REFERENCES finance_cost_centers(cost_center_id),
                account_id INTEGER REFERENCES finance_accounts(account_id),
                transaction_date DATE NOT NULL,
                transaction_type VARCHAR(20) CHECK (transaction_type IN ('Revenue', 'Expense')),
                amount DECIMAL(15,2) NOT NULL,
                description TEXT,
                reference_number VARCHAR(50),
                status VARCHAR(20) DEFAULT 'Completed' CHECK (status IN ('Pending', 'Completed', 'Cancelled')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 6. Vendors
        print("Creating procurement_vendors...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS procurement_vendors (
                vendor_id SERIAL PRIMARY KEY,
                vendor_name VARCHAR(100) NOT NULL,
                vendor_code VARCHAR(20) UNIQUE NOT NULL,
                contact_person VARCHAR(100),
                email VARCHAR(100),
                phone VARCHAR(20),
                address TEXT,
                rating DECIMAL(2,1) CHECK (rating >= 1.0 AND rating <= 5.0),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 7. Categories
        print("Creating procurement_categories...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS procurement_categories (
                category_id SERIAL PRIMARY KEY,
                category_name VARCHAR(100) NOT NULL,
                category_code VARCHAR(20) UNIQUE NOT NULL,
                parent_category_id INTEGER REFERENCES procurement_categories(category_id),
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # 8. Procurement Orders
        print("Creating procurement_orders...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS procurement_orders (
                order_id SERIAL PRIMARY KEY,
                dept_id INTEGER REFERENCES finance_departments(dept_id),
                vendor_id INTEGER REFERENCES procurement_vendors(vendor_id),
                category_id INTEGER REFERENCES procurement_categories(category_id),
                order_date DATE NOT NULL,
                order_number VARCHAR(50) UNIQUE NOT NULL,
                description TEXT,
                quantity INTEGER NOT NULL,
                unit_price DECIMAL(10,2) NOT NULL,
                total_amount DECIMAL(15,2) NOT NULL,
                grand_total DECIMAL(15,2) GENERATED ALWAYS AS (total_amount * 1.1) STORED,
                status VARCHAR(20) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Approved', 'Ordered', 'Delivered', 'Cancelled')),
                priority VARCHAR(10) DEFAULT 'Medium' CHECK (priority IN ('Low', 'Medium', 'High', 'Urgent')),
                delivery_date DATE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Commit all changes
        conn.commit()
        print("✅ All tables created successfully!")
        
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
