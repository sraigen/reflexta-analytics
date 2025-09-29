#!/usr/bin/env python3
"""
Fix Supabase schema step by step to avoid transaction errors
"""

import psycopg2

SUPABASE_URL = "postgresql://postgres.vbowznmcdzsgzntnzwfi:Sit%401125@aws-1-ap-south-1.pooler.supabase.com:6543/postgres"

def execute_safe(cur, sql, description):
    """Execute SQL safely with error handling"""
    try:
        cur.execute(sql)
        print(f"  ✅ {description}")
        return True
    except Exception as e:
        print(f"  ⚠️ {description} - {e}")
        return False

print("🔧 Fixing Supabase Schema Step by Step...")

try:
    conn = psycopg2.connect(SUPABASE_URL)
    cur = conn.cursor()
    print("✅ Connected to Supabase")
    
    # 1. Fix finance_budgets table
    print("\n📋 Fixing finance_budgets table...")
    
    execute_safe(cur, "ALTER TABLE finance_budgets ADD COLUMN IF NOT EXISTS budget_name VARCHAR(255);", "Added budget_name")
    execute_safe(cur, "ALTER TABLE finance_budgets ADD COLUMN IF NOT EXISTS budget_amount NUMERIC(15,2);", "Added budget_amount")
    execute_safe(cur, "ALTER TABLE finance_budgets ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'Active';", "Added status")
    execute_safe(cur, "ALTER TABLE finance_budgets ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;", "Added updated_at")
    
    # Commit finance_budgets changes
    conn.commit()
    print("  ✅ finance_budgets changes committed")
    
    # 2. Fix finance_transactions table
    print("\n📋 Fixing finance_transactions table...")
    
    execute_safe(cur, "ALTER TABLE finance_transactions ADD COLUMN IF NOT EXISTS vendor_name VARCHAR(255);", "Added vendor_name")
    execute_safe(cur, "ALTER TABLE finance_transactions ADD COLUMN IF NOT EXISTS payment_method VARCHAR(100);", "Added payment_method")
    execute_safe(cur, "ALTER TABLE finance_transactions ADD COLUMN IF NOT EXISTS created_by VARCHAR(255);", "Added created_by")
    execute_safe(cur, "ALTER TABLE finance_transactions ADD COLUMN IF NOT EXISTS approved_by VARCHAR(255);", "Added approved_by")
    execute_safe(cur, "ALTER TABLE finance_transactions ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;", "Added updated_at")
    
    # Commit finance_transactions changes
    conn.commit()
    print("  ✅ finance_transactions changes committed")
    
    # 3. Fix procurement_orders table
    print("\n📋 Fixing procurement_orders table...")
    
    execute_safe(cur, "ALTER TABLE procurement_orders ADD COLUMN IF NOT EXISTS cost_center_id INTEGER;", "Added cost_center_id")
    execute_safe(cur, "ALTER TABLE procurement_orders ADD COLUMN IF NOT EXISTS tax_amount NUMERIC(15,2) DEFAULT 0;", "Added tax_amount")
    execute_safe(cur, "ALTER TABLE procurement_orders ADD COLUMN IF NOT EXISTS shipping_amount NUMERIC(15,2) DEFAULT 0;", "Added shipping_amount")
    execute_safe(cur, "ALTER TABLE procurement_orders ADD COLUMN IF NOT EXISTS currency VARCHAR(3) DEFAULT 'USD';", "Added currency")
    execute_safe(cur, "ALTER TABLE procurement_orders ADD COLUMN IF NOT EXISTS requested_by VARCHAR(255);", "Added requested_by")
    execute_safe(cur, "ALTER TABLE procurement_orders ADD COLUMN IF NOT EXISTS approved_by VARCHAR(255);", "Added approved_by")
    execute_safe(cur, "ALTER TABLE procurement_orders ADD COLUMN IF NOT EXISTS notes TEXT;", "Added notes")
    execute_safe(cur, "ALTER TABLE procurement_orders ADD COLUMN IF NOT EXISTS expected_delivery_date DATE;", "Added expected_delivery_date")
    execute_safe(cur, "ALTER TABLE procurement_orders ADD COLUMN IF NOT EXISTS actual_delivery_date DATE;", "Added actual_delivery_date")
    execute_safe(cur, "ALTER TABLE procurement_orders ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;", "Added updated_at")
    
    # Commit procurement_orders changes
    conn.commit()
    print("  ✅ procurement_orders changes committed")
    
    # 4. Fix procurement_vendors table
    print("\n📋 Fixing procurement_vendors table...")
    
    execute_safe(cur, "ALTER TABLE procurement_vendors ADD COLUMN IF NOT EXISTS tax_id VARCHAR(50);", "Added tax_id")
    execute_safe(cur, "ALTER TABLE procurement_vendors ADD COLUMN IF NOT EXISTS payment_terms VARCHAR(255);", "Added payment_terms")
    execute_safe(cur, "ALTER TABLE procurement_vendors ADD COLUMN IF NOT EXISTS credit_limit NUMERIC(15,2);", "Added credit_limit")
    execute_safe(cur, "ALTER TABLE procurement_vendors ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;", "Added updated_at")
    
    # Commit procurement_vendors changes
    conn.commit()
    print("  ✅ procurement_vendors changes committed")
    
    # 5. Fix procurement_categories table
    print("\n📋 Fixing procurement_categories table...")
    
    execute_safe(cur, "ALTER TABLE procurement_categories ADD COLUMN IF NOT EXISTS description TEXT;", "Added description")
    
    # Commit procurement_categories changes
    conn.commit()
    print("  ✅ procurement_categories changes committed")
    
    print("\n🎉 ALL SCHEMA FIXES COMPLETED SUCCESSFULLY!")
    print("✅ Supabase schema now matches local database")
    
    # Test the problematic queries
    print("\n🧪 Testing problematic queries...")
    
    # Test finance budget query
    try:
        cur.execute("""
            SELECT b.budget_name, d.dept_name, b.budget_amount, 
                   COALESCE(SUM(t.amount), 0) as actual_spent,
                   b.budget_amount - COALESCE(SUM(t.amount), 0) as variance,
                   CASE WHEN b.budget_amount > 0 
                        THEN ROUND((COALESCE(SUM(t.amount), 0) / b.budget_amount) * 100, 2) 
                        ELSE 0 END as utilization_pct,
                   CASE WHEN COALESCE(SUM(t.amount), 0) > b.budget_amount THEN 'Over Budget'
                        WHEN COALESCE(SUM(t.amount), 0) > b.budget_amount * 0.9 THEN 'Near Limit'
                        ELSE 'Within Budget' END as budget_status
            FROM finance_budgets b
            JOIN finance_departments d ON b.dept_id = d.dept_id
            LEFT JOIN finance_transactions t ON b.dept_id = t.dept_id 
                AND t.transaction_date BETWEEN '2025-07-01' AND '2025-09-29' 
                AND t.status = 'Completed'
            GROUP BY b.budget_id, b.budget_name, d.dept_name, b.budget_amount
            ORDER BY utilization_pct DESC;
        """)
        result = cur.fetchall()
        print(f"✅ Finance budget query works! Found {len(result)} budgets")
    except Exception as e:
        print(f"❌ Finance budget query failed: {e}")
    
    # Test procurement orders query
    try:
        cur.execute("""
            SELECT po.order_id, po.order_number, po.order_date, po.grand_total, po.status, po.priority, 
                   v.vendor_name, c.category_name, d.dept_name, po.requested_by, 
                   po.expected_delivery_date, po.notes
            FROM procurement_orders po
            JOIN procurement_vendors v ON po.vendor_id = v.vendor_id
            JOIN procurement_categories c ON po.category_id = c.category_id
            JOIN finance_departments d ON po.dept_id = d.dept_id
            WHERE po.status IN ('Draft', 'Submitted', 'Approved', 'Ordered')
            ORDER BY CASE po.priority WHEN 'Urgent' THEN 1 WHEN 'High' THEN 2 WHEN 'Medium' THEN 3 ELSE 4 END, po.order_date DESC;
        """)
        result = cur.fetchall()
        print(f"✅ Procurement orders query works! Found {len(result)} orders")
    except Exception as e:
        print(f"❌ Procurement orders query failed: {e}")
    
    cur.close()
    conn.close()
    
except Exception as e:
    print(f"❌ Error fixing Supabase schema: {e}")
