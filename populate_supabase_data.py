#!/usr/bin/env python3
"""
Direct data population for Supabase database
"""

import psycopg
import random
from datetime import datetime, date, timedelta
from decimal import Decimal

def populate_supabase_data():
    """Populate Supabase database with sample data"""
    
    # Your Supabase connection string
    DATABASE_URL = "postgresql://postgres:Sit%401125@db.vbowznmcdzsgzntnzwfi.supabase.co:5432/postgres"
    
    print("🔌 Connecting to Supabase database...")
    
    try:
        # Connect to Supabase
        conn = psycopg.connect(DATABASE_URL)
        cur = conn.cursor()
        
        print("✅ Connected to Supabase successfully!")
        
        # Clear existing data first
        print("🧹 Clearing existing data...")
        tables_to_clear = [
            'procurement_orders',
            'procurement_categories', 
            'procurement_vendors',
            'finance_transactions',
            'finance_budgets',
            'finance_accounts',
            'finance_cost_centers',
            'finance_departments'
        ]
        
        for table in tables_to_clear:
            try:
                cur.execute(f"DELETE FROM {table}")
                print(f"✅ Cleared {table}")
            except Exception as e:
                print(f"⚠️  Warning clearing {table}: {e}")
        
        conn.commit()
        print("✅ All tables cleared!")
        
        # 1. Populate Finance Departments
        print("📊 Populating finance_departments...")
        departments = [
            ('Finance', 'FIN', 'John Smith', 500000),
            ('Procurement', 'PROC', 'Sarah Johnson', 300000),
            ('IT', 'IT', 'Mike Chen', 400000),
            ('HR', 'HR', 'Lisa Brown', 200000),
            ('Operations', 'OPS', 'David Wilson', 600000),
            ('Marketing', 'MKT', 'Emma Davis', 350000),
            ('Sales', 'SALES', 'Tom Anderson', 450000),
            ('Legal', 'LEGAL', 'Anna Taylor', 150000)
        ]
        
        for dept_name, dept_code, manager, budget in departments:
            cur.execute("""
                INSERT INTO finance_departments (dept_name, dept_code, manager_name, budget_allocated)
                VALUES (%s, %s, %s, %s)
            """, (dept_name, dept_code, manager, budget))
        
        print(f"✅ Inserted {len(departments)} departments")
        
        # 2. Populate Cost Centers
        print("📊 Populating finance_cost_centers...")
        cost_centers = [
            ('Corporate Finance', 'CF001', 1, 'John Smith'),
            ('Treasury', 'TR001', 1, 'Jane Doe'),
            ('Vendor Management', 'VM001', 2, 'Sarah Johnson'),
            ('IT Infrastructure', 'IT001', 3, 'Mike Chen'),
            ('Software Development', 'SD001', 3, 'Alex Kim'),
            ('Recruitment', 'REC001', 4, 'Lisa Brown'),
            ('Training', 'TRN001', 4, 'Mark Lee'),
            ('Manufacturing', 'MFG001', 5, 'David Wilson'),
            ('Quality Control', 'QC001', 5, 'Susan Park'),
            ('Digital Marketing', 'DM001', 6, 'Emma Davis')
        ]
        
        for cc_name, cc_code, dept_id, manager in cost_centers:
            cur.execute("""
                INSERT INTO finance_cost_centers (cost_center_name, cost_center_code, dept_id, manager_name)
                VALUES (%s, %s, %s, %s)
            """, (cc_name, cc_code, dept_id, manager))
        
        print(f"✅ Inserted {len(cost_centers)} cost centers")
        
        # 3. Populate Chart of Accounts
        print("📊 Populating finance_accounts...")
        accounts = [
            ('Cash', '1001', 'Asset', None),
            ('Accounts Receivable', '1002', 'Asset', None),
            ('Inventory', '1003', 'Asset', None),
            ('Equipment', '1004', 'Asset', None),
            ('Accounts Payable', '2001', 'Liability', None),
            ('Salaries Payable', '2002', 'Liability', None),
            ('Common Stock', '3001', 'Equity', None),
            ('Sales Revenue', '4001', 'Revenue', None),
            ('Service Revenue', '4002', 'Revenue', None),
            ('Office Supplies', '5001', 'Expense', None)
        ]
        
        for acc_name, acc_code, acc_type, parent_id in accounts:
            cur.execute("""
                INSERT INTO finance_accounts (account_name, account_code, account_type, parent_account_id)
                VALUES (%s, %s, %s, %s)
            """, (acc_name, acc_code, acc_type, parent_id))
        
        print(f"✅ Inserted {len(accounts)} accounts")
        
        # 4. Populate Budgets
        print("📊 Populating finance_budgets...")
        current_year = datetime.now().year
        
        for dept_id in range(1, 9):  # 8 departments
            for cost_center_id in range(1, 11):  # 10 cost centers
                for account_id in range(1, 11):  # 10 accounts
                    allocated = random.randint(10000, 100000)
                    spent = random.randint(0, int(allocated * 0.8))
                    
                    cur.execute("""
                        INSERT INTO finance_budgets (dept_id, cost_center_id, account_id, budget_year, allocated_amount, spent_amount)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (dept_id, cost_center_id, account_id, current_year, allocated, spent))
        
        print("✅ Inserted budget allocations")
        
        # 5. Populate Financial Transactions
        print("📊 Populating finance_transactions...")
        transaction_types = ['Revenue', 'Expense']
        statuses = ['Completed', 'Pending', 'Cancelled']
        
        for i in range(200):  # 200 transactions
            dept_id = random.randint(1, 8)
            cost_center_id = random.randint(1, 10)
            account_id = random.randint(1, 10)
            transaction_date = date.today() - timedelta(days=random.randint(0, 365))
            transaction_type = random.choice(transaction_types)
            amount = random.randint(100, 50000)
            description = f"Transaction {i+1} - {transaction_type}"
            reference = f"REF-{i+1:06d}"
            status = random.choice(statuses)
            
            cur.execute("""
                INSERT INTO finance_transactions 
                (dept_id, cost_center_id, account_id, transaction_date, transaction_type, 
                 amount, description, reference_number, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (dept_id, cost_center_id, account_id, transaction_date, transaction_type,
                  amount, description, reference, status))
        
        print("✅ Inserted 200 financial transactions")
        
        # 6. Populate Vendors
        print("📊 Populating procurement_vendors...")
        vendors = [
            ('TechCorp Solutions', 'V001', 'John Smith', 'john@techcorp.com', '+1-555-0101', '123 Tech St, Silicon Valley, CA', 4.5),
            ('Office Supplies Inc', 'V002', 'Jane Doe', 'jane@officesupplies.com', '+1-555-0102', '456 Office Ave, New York, NY', 4.2),
            ('Global Services Ltd', 'V003', 'Mike Johnson', 'mike@globalservices.com', '+1-555-0103', '789 Global Blvd, London, UK', 4.8),
            ('Software Solutions', 'V004', 'Sarah Wilson', 'sarah@software.com', '+1-555-0104', '321 Software Dr, Austin, TX', 4.3),
            ('Hardware Plus', 'V005', 'David Brown', 'david@hardware.com', '+1-555-0105', '654 Hardware Ln, Seattle, WA', 4.1),
            ('Consulting Group', 'V006', 'Lisa Davis', 'lisa@consulting.com', '+1-555-0106', '987 Consulting Way, Boston, MA', 4.6),
            ('Marketing Pro', 'V007', 'Tom Anderson', 'tom@marketing.com', '+1-555-0107', '147 Marketing St, Los Angeles, CA', 4.4),
            ('Legal Services', 'V008', 'Anna Taylor', 'anna@legal.com', '+1-555-0108', '258 Legal Ave, Chicago, IL', 4.7),
            ('Training Experts', 'V009', 'Mark Lee', 'mark@training.com', '+1-555-0109', '369 Training Rd, Miami, FL', 4.0),
            ('Support Systems', 'V010', 'Susan Park', 'susan@support.com', '+1-555-0110', '741 Support Blvd, Denver, CO', 4.9)
        ]
        
        for vendor_name, vendor_code, contact, email, phone, address, rating in vendors:
            cur.execute("""
                INSERT INTO procurement_vendors 
                (vendor_name, vendor_code, contact_person, email, phone, address, rating)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (vendor_name, vendor_code, contact, email, phone, address, rating))
        
        print(f"✅ Inserted {len(vendors)} vendors")
        
        # 7. Populate Categories
        print("📊 Populating procurement_categories...")
        categories = [
            ('Office Supplies', 'CAT001', None),
            ('IT Equipment', 'CAT002', None),
            ('Software', 'CAT003', None),
            ('Services', 'CAT004', None),
            ('Marketing', 'CAT005', None),
            ('Training', 'CAT006', None),
            ('Legal', 'CAT007', None),
            ('Consulting', 'CAT008', None),
            ('Hardware', 'CAT009', None),
            ('Support', 'CAT010', None)
        ]
        
        for cat_name, cat_code, parent_id in categories:
            cur.execute("""
                INSERT INTO procurement_categories (category_name, category_code, parent_category_id)
                VALUES (%s, %s, %s)
            """, (cat_name, cat_code, parent_id))
        
        print(f"✅ Inserted {len(categories)} categories")
        
        # 8. Populate Procurement Orders
        print("📊 Populating procurement_orders...")
        order_statuses = ['Pending', 'Approved', 'Ordered', 'Delivered', 'Cancelled']
        priorities = ['Low', 'Medium', 'High', 'Urgent']
        
        for i in range(150):  # 150 orders
            dept_id = random.randint(1, 8)
            vendor_id = random.randint(1, 10)
            category_id = random.randint(1, 10)
            order_date = date.today() - timedelta(days=random.randint(0, 180))
            order_number = f"PO-{i+1:06d}"
            description = f"Procurement Order {i+1}"
            quantity = random.randint(1, 100)
            unit_price = random.randint(10, 1000)
            total_amount = quantity * unit_price
            status = random.choice(order_statuses)
            priority = random.choice(priorities)
            delivery_date = order_date + timedelta(days=random.randint(7, 30))
            
            cur.execute("""
                INSERT INTO procurement_orders 
                (dept_id, vendor_id, category_id, order_date, order_number, description, 
                 quantity, unit_price, total_amount, status, priority, delivery_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (dept_id, vendor_id, category_id, order_date, order_number, description,
                  quantity, unit_price, total_amount, status, priority, delivery_date))
        
        print("✅ Inserted 150 procurement orders")
        
        # Commit all changes
        conn.commit()
        print("✅ All data committed successfully!")
        
        # Verify data was inserted
        print("🔍 Verifying data insertion...")
        tables_to_check = [
            'finance_departments', 'finance_cost_centers', 'finance_accounts', 
            'finance_budgets', 'finance_transactions', 'procurement_vendors', 
            'procurement_categories', 'procurement_orders'
        ]
        
        for table in tables_to_check:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            print(f"   - {table}: {count} rows")
        
        # Close connection
        cur.close()
        conn.close()
        
        print("🎉 Supabase data population completed successfully!")
        print("🔗 Check your Supabase dashboard - you should now see data in all tables!")
        
    except Exception as e:
        print(f"❌ Error populating Supabase database: {e}")
        print("Please check your connection string and try again")

if __name__ == "__main__":
    populate_supabase_data()
