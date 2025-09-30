#!/usr/bin/env python3
"""
Comprehensive sample data population script for Enterprise Analytics Dashboard.
This script populates all tables with realistic business data.
"""

import datetime as dt
import random
from decimal import Decimal

import psycopg
from psycopg import sql


def get_connection():
    """Get database connection."""
    import os
    
    # Use environment variables for security, fallback to working credentials
    host = os.getenv("DB_HOST", "localhost")
    port = int(os.getenv("DB_PORT", "5432"))
    user = os.getenv("DB_USER", "postgres")
    password = os.getenv("DB_PASSWORD", "Sit@1125")
    dbname = os.getenv("DB_NAME", "Test")
    
    return psycopg.connect(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=dbname
    )


def populate_departments(conn):
    """Populate finance_departments table."""
    departments = [
        (1, "Finance", "FIN", "John Smith", 1000000.00),
        (2, "Procurement", "PROC", "Sarah Johnson", 800000.00),
        (3, "IT", "IT", "Mike Chen", 1200000.00),
        (4, "HR", "HR", "Lisa Brown", 600000.00),
        (5, "Operations", "OPS", "David Wilson", 900000.00),
        (6, "Marketing", "MKT", "Emma Davis", 700000.00),
        (7, "Sales", "SALES", "Tom Anderson", 1100000.00),
        (8, "Legal", "LEGAL", "Rachel Green", 400000.00)
    ]
    
    with conn.cursor() as cur:
        for dept_id, name, code, manager, budget in departments:
            cur.execute("""
                INSERT INTO finance_departments (dept_id, dept_name, dept_code, manager_name, budget_allocation, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (dept_id) DO UPDATE SET
                    dept_name = EXCLUDED.dept_name,
                    dept_code = EXCLUDED.dept_code,
                    manager_name = EXCLUDED.manager_name,
                    budget_allocation = EXCLUDED.budget_allocation
            """, (dept_id, name, code, manager, budget, dt.datetime.now()))


def populate_cost_centers(conn):
    """Populate finance_cost_centers table."""
    cost_centers = [
        (1, "Financial Planning", "FIN-PLAN", 1, True),
        (2, "Finance Operations", "FIN-OPS", 1, True),
        (3, "Procurement Operations", "PROC-OPS", 2, True),
        (4, "Vendor Management", "VENDOR-MGT", 2, True),
        (5, "IT Infrastructure", "IT-INFRA", 3, True),
        (6, "IT Support", "IT-SUPPORT", 3, True),
        (7, "HR Operations", "HR-OPS", 4, True),
        (8, "Recruitment", "RECRUIT", 4, True),
        (9, "Operations Management", "OPS-MGT", 5, True),
        (10, "Logistics", "LOGISTICS", 5, True)
    ]
    
    with conn.cursor() as cur:
        for cc_id, name, code, dept_id, is_active in cost_centers:
            cur.execute("""
                INSERT INTO finance_cost_centers (cost_center_id, cost_center_name, cost_center_code, dept_id, is_active, created_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (cost_center_id) DO UPDATE SET
                    cost_center_name = EXCLUDED.cost_center_name,
                    cost_center_code = EXCLUDED.cost_center_code,
                    dept_id = EXCLUDED.dept_id,
                    is_active = EXCLUDED.is_active
            """, (cc_id, name, code, dept_id, is_active, dt.datetime.now()))


def populate_accounts(conn):
    """Populate finance_accounts table."""
    accounts = [
        (1, "REV", "Revenue", "Revenue", None, True),
        (2, "OPEX", "Operating Expenses", "Expense", None, True),
        (3, "CAPEX", "Capital Expenditure", "Asset", None, True),
        (4, "AR", "Accounts Receivable", "Asset", None, True),
        (5, "AP", "Accounts Payable", "Liability", None, True),
        (6, "CASH", "Cash and Cash Equivalents", "Asset", None, True),
        (7, "INV", "Inventory", "Asset", None, True),
        (8, "EQUIP", "Equipment", "Asset", None, True),
        (9, "SOFT", "Software Licenses", "Asset", None, True),
        (10, "CONSULT", "Consulting Services", "Expense", None, True)
    ]
    
    with conn.cursor() as cur:
        for acc_id, code, name, acc_type, parent_id, is_active in accounts:
            cur.execute("""
                INSERT INTO finance_accounts (account_id, account_code, account_name, account_type, parent_account_id, is_active, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (account_id) DO UPDATE SET
                    account_code = EXCLUDED.account_code,
                    account_name = EXCLUDED.account_name,
                    account_type = EXCLUDED.account_type,
                    parent_account_id = EXCLUDED.parent_account_id,
                    is_active = EXCLUDED.is_active
            """, (acc_id, code, name, acc_type, parent_id, is_active, dt.datetime.now()))


def populate_budgets(conn):
    """Populate finance_budgets table."""
    budget_data = [
        (1, "Finance Planning Budget", 1, 1, 1, 2024, 1000000.00, 0.00, 1000000.00, "Active"),
        (2, "Finance Operations Budget", 1, 2, 2, 2024, 500000.00, 0.00, 500000.00, "Active"),
        (3, "Procurement Operations Budget", 2, 3, 3, 2024, 800000.00, 0.00, 800000.00, "Active"),
        (4, "Vendor Management Budget", 2, 4, 4, 2024, 300000.00, 0.00, 300000.00, "Active"),
        (5, "IT Infrastructure Budget", 3, 5, 5, 2024, 1200000.00, 0.00, 1200000.00, "Active"),
        (6, "IT Support Budget", 3, 6, 6, 2024, 400000.00, 0.00, 400000.00, "Active"),
        (7, "HR Operations Budget", 4, 7, 7, 2024, 600000.00, 0.00, 600000.00, "Active"),
        (8, "Recruitment Budget", 4, 8, 8, 2024, 200000.00, 0.00, 200000.00, "Active"),
        (9, "Operations Management Budget", 5, 9, 9, 2024, 900000.00, 0.00, 900000.00, "Active"),
        (10, "Logistics Budget", 5, 10, 10, 2024, 700000.00, 0.00, 700000.00, "Active")
    ]
    
    with conn.cursor() as cur:
        for budget_id, name, dept_id, cc_id, acc_id, year, amount, spent, remaining, status in budget_data:
            cur.execute("""
                INSERT INTO finance_budgets (budget_id, budget_name, dept_id, cost_center_id, account_id, budget_year, budget_amount, spent_amount, status, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (budget_id) DO UPDATE SET
                    budget_amount = EXCLUDED.budget_amount,
                    spent_amount = EXCLUDED.spent_amount
            """, (budget_id, name, dept_id, cc_id, acc_id, year, amount, spent, status, dt.datetime.now()))


def populate_transactions(conn):
    """Populate finance_transactions table with realistic data."""
    transaction_types = ["Revenue", "Expense", "Asset", "Liability", "Equity"]
    statuses = ["Pending", "Approved", "Rejected", "Completed"]
    descriptions = [
        "Software license renewal", "Office supplies purchase", "Equipment maintenance",
        "Consulting services", "Training and development", "Travel expenses",
        "Marketing campaign", "Rent payment", "Utilities", "Insurance premium",
        "Professional development", "Conference attendance", "Equipment purchase",
        "Software development", "Marketing materials", "Office furniture",
        "Telecommunications", "Security services", "Cleaning services", "Legal fees"
    ]
    vendors = ["TechCorp", "OfficeSupplies", "ConsultingPro", "SoftwareInc", "EquipmentCo"]
    payment_methods = ["Credit Card", "Bank Transfer", "Check", "Cash", "Wire Transfer"]
    
    with conn.cursor() as cur:
        # Generate 200 transactions over the last 6 months
        for i in range(200):
            transaction_id = i + 1
            dept_id = random.randint(1, 8)
            cc_id = random.randint(1, 10)
            account_id = random.randint(1, 10)
            transaction_type = random.choice(transaction_types)
            amount = round(random.uniform(100, 50000), 2)
            description = random.choice(descriptions)
            status = random.choice(statuses)
            created_by = f"user_{random.randint(1, 20)}"
            vendor = random.choice(vendors)
            payment_method = random.choice(payment_methods)
            reference = f"REF-{random.randint(1000, 9999)}"
            
            # Random date in the last 6 months
            start_date = dt.datetime.now() - dt.timedelta(days=180)
            random_days = random.randint(0, 180)
            transaction_date = start_date + dt.timedelta(days=random_days)
            created_at = transaction_date + dt.timedelta(hours=random.randint(0, 24))
            
            cur.execute("""
                INSERT INTO finance_transactions (
                    transaction_id, transaction_date, transaction_type, account_id, dept_id, cost_center_id,
                    amount, description, reference_number, vendor_name, payment_method, status, created_by, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (transaction_id) DO NOTHING
            """, (
                transaction_id, transaction_date, transaction_type, account_id, dept_id, cc_id,
                amount, description, reference, vendor, payment_method, status, created_by, created_at
            ))


def populate_vendors(conn):
    """Populate procurement_vendors table."""
    vendors = [
        (1, "TechCorp Solutions", "TECH", "John Smith", "john@techcorp.com", "+1-555-0101", "123 Tech St, Silicon Valley", "TAX123456", "Net 30", 100000.00, 4.5),
        (2, "Office Supplies Inc", "OFFICE", "Jane Doe", "jane@officesupplies.com", "+1-555-0102", "456 Office Ave, Business District", "TAX123457", "Net 15", 50000.00, 4.2),
        (3, "Consulting Partners", "CONSULT", "Bob Wilson", "bob@consulting.com", "+1-555-0103", "789 Consulting Blvd, Downtown", "TAX123458", "Net 30", 200000.00, 4.8),
        (4, "Software Systems Ltd", "SOFTWARE", "Alice Brown", "alice@software.com", "+1-555-0104", "321 Software Lane, Tech Park", "TAX123459", "Net 30", 150000.00, 4.3),
        (5, "Logistics Pro", "LOGISTICS", "Charlie Davis", "charlie@logistics.com", "+1-555-0105", "654 Logistics Way, Industrial Zone", "TAX123460", "Net 15", 75000.00, 4.1),
        (6, "Marketing Agency", "MARKETING", "Diana Lee", "diana@marketing.com", "+1-555-0106", "987 Marketing St, Creative District", "TAX123461", "Net 30", 120000.00, 4.6),
        (7, "Legal Associates", "LEGAL", "Eve Johnson", "eve@legal.com", "+1-555-0107", "147 Legal Plaza, Law District", "TAX123462", "Net 30", 300000.00, 4.7),
        (8, "HR Services Co", "HR", "Frank Miller", "frank@hrservices.com", "+1-555-0108", "258 HR Center, Business Park", "TAX123463", "Net 15", 80000.00, 4.4),
        (9, "Equipment Rentals", "EQUIPMENT", "Grace Taylor", "grace@equipment.com", "+1-555-0109", "369 Equipment Blvd, Industrial Area", "TAX123464", "Net 30", 60000.00, 4.0),
        (10, "Security Solutions", "SECURITY", "Henry Clark", "henry@security.com", "+1-555-0110", "741 Security Ave, Tech Center", "TAX123465", "Net 30", 90000.00, 4.2)
    ]
    
    with conn.cursor() as cur:
        for vendor_id, name, code, contact, email, phone, address, tax_id, terms, credit, rating in vendors:
            cur.execute("""
                INSERT INTO procurement_vendors (vendor_id, vendor_name, vendor_code, contact_person, email, phone, address, tax_id, payment_terms, credit_limit, rating, is_active, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (vendor_id) DO UPDATE SET
                    vendor_name = EXCLUDED.vendor_name,
                    vendor_code = EXCLUDED.vendor_code,
                    contact_person = EXCLUDED.contact_person,
                    email = EXCLUDED.email,
                    phone = EXCLUDED.phone,
                    address = EXCLUDED.address,
                    tax_id = EXCLUDED.tax_id,
                    payment_terms = EXCLUDED.payment_terms,
                    credit_limit = EXCLUDED.credit_limit,
                    rating = EXCLUDED.rating
            """, (vendor_id, name, code, contact, email, phone, address, tax_id, terms, credit, rating, True, dt.datetime.now()))


def populate_categories(conn):
    """Populate procurement_categories table."""
    categories = [
        (1, "Software", "SOFT", None, "Software licenses and subscriptions", True),
        (2, "Hardware", "HARD", None, "Computer hardware and equipment", True),
        (3, "Services", "SERV", None, "Professional and consulting services", True),
        (4, "Office Supplies", "OFFICE", None, "Office supplies and stationery", True),
        (5, "Raw Materials", "MATERIALS", None, "Raw materials and components", True),
        (6, "Equipment", "EQUIP", None, "Machinery and equipment", True),
        (7, "Marketing", "MKT", None, "Marketing and advertising", True),
        (8, "Travel", "TRAVEL", None, "Travel and accommodation", True),
        (9, "Training", "TRAIN", None, "Training and development", True),
        (10, "Maintenance", "MAINT", None, "Maintenance and repairs", True)
    ]
    
    with conn.cursor() as cur:
        for cat_id, name, code, parent_id, description, is_active in categories:
            cur.execute("""
                INSERT INTO procurement_categories (category_id, category_name, category_code, parent_category_id, description, is_active, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (category_id) DO UPDATE SET
                    category_name = EXCLUDED.category_name,
                    category_code = EXCLUDED.category_code,
                    parent_category_id = EXCLUDED.parent_category_id,
                    description = EXCLUDED.description,
                    is_active = EXCLUDED.is_active
            """, (cat_id, name, code, parent_id, description, is_active, dt.datetime.now()))


def populate_orders(conn):
    """Populate procurement_orders table with realistic data."""
    order_statuses = ["Draft", "Submitted", "Approved", "Rejected", "Ordered", "Received", "Closed", "Cancelled"]
    priorities = ["Low", "Medium", "High", "Urgent"]
    currencies = ["USD", "EUR", "GBP"]
    
    with conn.cursor() as cur:
        # Generate 150 orders over the last 6 months
        for i in range(150):
            order_id = i + 1
            order_number = f"PO-{2024}-{str(i+1).zfill(4)}"
            dept_id = random.randint(1, 8)
            vendor_id = random.randint(1, 10)
            category_id = random.randint(1, 10)
            cc_id = random.randint(1, 10)
            total_amount = round(random.uniform(500, 100000), 2)
            tax_amount = round(total_amount * 0.08, 2)  # 8% tax
            shipping_amount = round(random.uniform(50, 500), 2)
            grand_total = total_amount + tax_amount + shipping_amount
            status = random.choice(order_statuses)
            priority = random.choice(priorities)
            created_by = f"user_{random.randint(1, 20)}"
            currency = random.choice(currencies)
            
            # Random dates
            start_date = dt.datetime.now() - dt.timedelta(days=180)
            random_days = random.randint(0, 180)
            order_date = start_date + dt.timedelta(days=random_days)
            expected_delivery = order_date + dt.timedelta(days=random.randint(7, 30))
            actual_delivery = expected_delivery + dt.timedelta(days=random.randint(-5, 10)) if status == "Completed" else None
            created_at = order_date + dt.timedelta(hours=random.randint(0, 24))
            
            cur.execute("""
                INSERT INTO procurement_orders (
                    order_id, order_number, order_date, vendor_id, category_id, dept_id, cost_center_id,
                    total_amount, tax_amount, shipping_amount, currency, status, priority,
                    requested_by, expected_delivery_date, actual_delivery_date, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (order_id) DO NOTHING
            """, (
                order_id, order_number, order_date, vendor_id, category_id, dept_id, cc_id,
                total_amount, tax_amount, shipping_amount, currency, status, priority,
                created_by, expected_delivery, actual_delivery, created_at
            ))


def main():
    """Main function to populate all sample data."""
    print("Starting comprehensive sample data population...")
    
    try:
        conn = get_connection()
        print("Connected to database successfully")
        
        # Populate all tables
        print("Populating departments...")
        populate_departments(conn)
        
        print("Populating cost centers...")
        populate_cost_centers(conn)
        
        print("Populating accounts...")
        populate_accounts(conn)
        
        print("Populating budgets...")
        populate_budgets(conn)
        
        print("Populating transactions...")
        populate_transactions(conn)
        
        print("Populating vendors...")
        populate_vendors(conn)
        
        print("Populating categories...")
        populate_categories(conn)
        
        print("Populating orders...")
        populate_orders(conn)
        
        conn.commit()
        print("All sample data populated successfully!")
        
    except Exception as e:
        print(f"Error populating data: {e}")
        if 'conn' in locals():
            conn.rollback()
    finally:
        if 'conn' in locals():
            conn.close()


if __name__ == "__main__":
    main()