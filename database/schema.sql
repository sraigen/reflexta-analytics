-- =====================================================
-- COMPREHENSIVE FINANCE & PROCUREMENT DATABASE SCHEMA
-- Production-ready with proper indexing and constraints
-- =====================================================

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS procurement_orders CASCADE;
DROP TABLE IF EXISTS procurement_vendors CASCADE;
DROP TABLE IF EXISTS procurement_categories CASCADE;
DROP TABLE IF EXISTS finance_transactions CASCADE;
DROP TABLE IF EXISTS finance_accounts CASCADE;
DROP TABLE IF EXISTS finance_budgets CASCADE;
DROP TABLE IF EXISTS finance_departments CASCADE;
DROP TABLE IF EXISTS finance_cost_centers CASCADE;

-- =====================================================
-- FINANCE MODULE TABLES
-- =====================================================

-- Finance Departments
CREATE TABLE finance_departments (
    dept_id SERIAL PRIMARY KEY,
    dept_name VARCHAR(100) NOT NULL UNIQUE,
    dept_code VARCHAR(10) NOT NULL UNIQUE,
    manager_name VARCHAR(100),
    budget_allocation DECIMAL(15,2) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Cost Centers
CREATE TABLE finance_cost_centers (
    cost_center_id SERIAL PRIMARY KEY,
    cost_center_name VARCHAR(100) NOT NULL,
    cost_center_code VARCHAR(20) NOT NULL UNIQUE,
    dept_id INTEGER REFERENCES finance_departments(dept_id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chart of Accounts
CREATE TABLE finance_accounts (
    account_id SERIAL PRIMARY KEY,
    account_code VARCHAR(20) NOT NULL UNIQUE,
    account_name VARCHAR(200) NOT NULL,
    account_type VARCHAR(50) NOT NULL CHECK (account_type IN ('Asset', 'Liability', 'Equity', 'Revenue', 'Expense')),
    parent_account_id INTEGER REFERENCES finance_accounts(account_id),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Budgets
CREATE TABLE finance_budgets (
    budget_id SERIAL PRIMARY KEY,
    budget_name VARCHAR(200) NOT NULL,
    dept_id INTEGER REFERENCES finance_departments(dept_id),
    cost_center_id INTEGER REFERENCES finance_cost_centers(cost_center_id),
    account_id INTEGER REFERENCES finance_accounts(account_id),
    budget_year INTEGER NOT NULL,
    budget_amount DECIMAL(15,2) NOT NULL,
    spent_amount DECIMAL(15,2) DEFAULT 0,
    remaining_amount DECIMAL(15,2) GENERATED ALWAYS AS (budget_amount - spent_amount) STORED,
    status VARCHAR(20) DEFAULT 'Active' CHECK (status IN ('Active', 'Closed', 'Suspended')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Financial Transactions
CREATE TABLE finance_transactions (
    transaction_id SERIAL PRIMARY KEY,
    transaction_date DATE NOT NULL,
    transaction_type VARCHAR(50) NOT NULL CHECK (transaction_type IN ('Revenue', 'Expense', 'Asset', 'Liability', 'Equity')),
    account_id INTEGER REFERENCES finance_accounts(account_id),
    dept_id INTEGER REFERENCES finance_departments(dept_id),
    cost_center_id INTEGER REFERENCES finance_cost_centers(cost_center_id),
    amount DECIMAL(15,2) NOT NULL,
    description TEXT,
    reference_number VARCHAR(100),
    vendor_name VARCHAR(200),
    payment_method VARCHAR(50),
    status VARCHAR(20) DEFAULT 'Pending' CHECK (status IN ('Pending', 'Approved', 'Rejected', 'Completed')),
    created_by VARCHAR(100),
    approved_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- PROCUREMENT MODULE TABLES
-- =====================================================

-- Procurement Categories
CREATE TABLE procurement_categories (
    category_id SERIAL PRIMARY KEY,
    category_name VARCHAR(100) NOT NULL UNIQUE,
    category_code VARCHAR(20) NOT NULL UNIQUE,
    parent_category_id INTEGER REFERENCES procurement_categories(category_id),
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Vendors
CREATE TABLE procurement_vendors (
    vendor_id SERIAL PRIMARY KEY,
    vendor_name VARCHAR(200) NOT NULL,
    vendor_code VARCHAR(20) NOT NULL UNIQUE,
    contact_person VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    tax_id VARCHAR(50),
    payment_terms VARCHAR(100),
    credit_limit DECIMAL(15,2) DEFAULT 0,
    rating DECIMAL(3,2) DEFAULT 0 CHECK (rating >= 0 AND rating <= 5),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Procurement Orders
CREATE TABLE procurement_orders (
    order_id SERIAL PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL UNIQUE,
    order_date DATE NOT NULL,
    vendor_id INTEGER REFERENCES procurement_vendors(vendor_id),
    category_id INTEGER REFERENCES procurement_categories(category_id),
    dept_id INTEGER REFERENCES finance_departments(dept_id),
    cost_center_id INTEGER REFERENCES finance_cost_centers(cost_center_id),
    total_amount DECIMAL(15,2) NOT NULL,
    tax_amount DECIMAL(15,2) DEFAULT 0,
    shipping_amount DECIMAL(15,2) DEFAULT 0,
    grand_total DECIMAL(15,2) GENERATED ALWAYS AS (total_amount + tax_amount + shipping_amount) STORED,
    currency VARCHAR(3) DEFAULT 'USD',
    status VARCHAR(20) DEFAULT 'Draft' CHECK (status IN ('Draft', 'Submitted', 'Approved', 'Rejected', 'Ordered', 'Received', 'Closed', 'Cancelled')),
    priority VARCHAR(10) DEFAULT 'Medium' CHECK (priority IN ('Low', 'Medium', 'High', 'Urgent')),
    requested_by VARCHAR(100),
    approved_by VARCHAR(100),
    notes TEXT,
    expected_delivery_date DATE,
    actual_delivery_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- Finance indexes
CREATE INDEX idx_finance_transactions_date ON finance_transactions(transaction_date);
CREATE INDEX idx_finance_transactions_type ON finance_transactions(transaction_type);
CREATE INDEX idx_finance_transactions_dept ON finance_transactions(dept_id);
CREATE INDEX idx_finance_transactions_account ON finance_transactions(account_id);
CREATE INDEX idx_finance_budgets_year ON finance_budgets(budget_year);
CREATE INDEX idx_finance_budgets_dept ON finance_budgets(dept_id);

-- Procurement indexes
CREATE INDEX idx_procurement_orders_date ON procurement_orders(order_date);
CREATE INDEX idx_procurement_orders_vendor ON procurement_orders(vendor_id);
CREATE INDEX idx_procurement_orders_status ON procurement_orders(status);
CREATE INDEX idx_procurement_orders_dept ON procurement_orders(dept_id);
CREATE INDEX idx_procurement_vendors_active ON procurement_vendors(is_active);

-- =====================================================
-- TRIGGERS FOR AUTOMATIC UPDATES
-- =====================================================

-- Update budget spent amount when transactions are added
CREATE OR REPLACE FUNCTION update_budget_spent()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'Completed' AND OLD.status != 'Completed' THEN
        UPDATE finance_budgets 
        SET spent_amount = spent_amount + NEW.amount,
            updated_at = CURRENT_TIMESTAMP
        WHERE dept_id = NEW.dept_id 
        AND cost_center_id = NEW.cost_center_id
        AND account_id = NEW.account_id
        AND budget_year = EXTRACT(YEAR FROM NEW.transaction_date);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_budget_spent
    AFTER UPDATE ON finance_transactions
    FOR EACH ROW
    EXECUTE FUNCTION update_budget_spent();

-- =====================================================
-- SAMPLE DATA INSERTION
-- =====================================================

-- Insert sample departments
INSERT INTO finance_departments (dept_name, dept_code, manager_name, budget_allocation) VALUES
('Finance', 'FIN', 'John Smith', 500000.00),
('Procurement', 'PROC', 'Sarah Johnson', 300000.00),
('IT', 'IT', 'Mike Chen', 200000.00),
('HR', 'HR', 'Lisa Brown', 150000.00),
('Operations', 'OPS', 'David Wilson', 400000.00);

-- Insert sample cost centers
INSERT INTO finance_cost_centers (cost_center_name, cost_center_code, dept_id) VALUES
('Finance Operations', 'FIN-OPS', 1),
('Financial Planning', 'FIN-PLAN', 1),
('Procurement Operations', 'PROC-OPS', 2),
('Vendor Management', 'PROC-VEND', 2),
('IT Infrastructure', 'IT-INFRA', 3),
('IT Support', 'IT-SUPPORT', 3),
('HR Operations', 'HR-OPS', 4),
('Recruitment', 'HR-RECRUIT', 4),
('Operations Management', 'OPS-MGMT', 5),
('Logistics', 'OPS-LOG', 5);

-- Insert sample chart of accounts
INSERT INTO finance_accounts (account_code, account_name, account_type) VALUES
('1000', 'Cash and Cash Equivalents', 'Asset'),
('1100', 'Accounts Receivable', 'Asset'),
('1200', 'Inventory', 'Asset'),
('2000', 'Accounts Payable', 'Liability'),
('2100', 'Accrued Expenses', 'Liability'),
('3000', 'Equity', 'Equity'),
('4000', 'Revenue', 'Revenue'),
('5000', 'Cost of Goods Sold', 'Expense'),
('5100', 'Operating Expenses', 'Expense'),
('5200', 'Administrative Expenses', 'Expense');

-- Insert sample budgets
INSERT INTO finance_budgets (budget_name, dept_id, cost_center_id, account_id, budget_year, budget_amount) VALUES
('Finance Operations Budget 2024', 1, 1, 9, 2024, 100000.00),
('IT Infrastructure Budget 2024', 3, 5, 9, 2024, 150000.00),
('Procurement Operations Budget 2024', 2, 3, 9, 2024, 200000.00),
('HR Operations Budget 2024', 4, 7, 9, 2024, 80000.00),
('Operations Management Budget 2024', 5, 9, 9, 2024, 250000.00);

-- Insert sample procurement categories
INSERT INTO procurement_categories (category_name, category_code, description) VALUES
('IT Equipment', 'IT-EQ', 'Computers, servers, networking equipment'),
('Office Supplies', 'OFF-SUP', 'Stationery, office furniture, supplies'),
('Software Licenses', 'SW-LIC', 'Software licenses and subscriptions'),
('Professional Services', 'PRO-SVC', 'Consulting, legal, accounting services'),
('Marketing Materials', 'MKT-MAT', 'Marketing collateral, advertising materials'),
('Facilities', 'FAC', 'Building maintenance, utilities, rent');

-- Insert sample vendors
INSERT INTO procurement_vendors (vendor_name, vendor_code, contact_person, email, phone, payment_terms, credit_limit, rating) VALUES
('Tech Solutions Inc', 'TECH-001', 'Alice Cooper', 'alice@techsolutions.com', '+1-555-0101', 'Net 30', 50000.00, 4.5),
('Office Depot', 'OFF-001', 'Bob Smith', 'bob@officedepot.com', '+1-555-0102', 'Net 15', 25000.00, 4.2),
('Microsoft Corp', 'MS-001', 'Carol Davis', 'carol@microsoft.com', '+1-555-0103', 'Net 30', 100000.00, 4.8),
('Legal Associates', 'LEG-001', 'David Lee', 'david@legalassoc.com', '+1-555-0104', 'Net 30', 15000.00, 4.0),
('Marketing Pro', 'MKT-001', 'Eva Green', 'eva@marketingpro.com', '+1-555-0105', 'Net 15', 30000.00, 4.3);

-- Insert sample transactions
INSERT INTO finance_transactions (transaction_date, transaction_type, account_id, dept_id, cost_center_id, amount, description, reference_number, vendor_name, status, created_by) VALUES
('2024-01-15', 'Expense', 9, 1, 1, 2500.00, 'Office supplies purchase', 'INV-001', 'Office Depot', 'Completed', 'John Smith'),
('2024-01-20', 'Expense', 9, 3, 5, 15000.00, 'IT equipment purchase', 'INV-002', 'Tech Solutions Inc', 'Completed', 'Mike Chen'),
('2024-02-01', 'Expense', 9, 2, 3, 5000.00, 'Software license renewal', 'INV-003', 'Microsoft Corp', 'Completed', 'Sarah Johnson'),
('2024-02-10', 'Expense', 9, 4, 7, 3000.00, 'HR training materials', 'INV-004', 'Training Co', 'Completed', 'Lisa Brown'),
('2024-02-15', 'Expense', 9, 5, 9, 8000.00, 'Operations equipment', 'INV-005', 'Equipment Co', 'Completed', 'David Wilson');

-- Insert sample procurement orders
INSERT INTO procurement_orders (order_number, order_date, vendor_id, category_id, dept_id, cost_center_id, total_amount, tax_amount, shipping_amount, status, priority, requested_by, notes, expected_delivery_date) VALUES
('PO-2024-001', '2024-01-10', 1, 1, 3, 5, 15000.00, 1200.00, 200.00, 'Received', 'High', 'Mike Chen', 'Urgent IT equipment for new office', '2024-01-25'),
('PO-2024-002', '2024-01-15', 2, 2, 1, 1, 2500.00, 200.00, 50.00, 'Received', 'Medium', 'John Smith', 'Quarterly office supplies', '2024-01-30'),
('PO-2024-003', '2024-02-01', 3, 3, 2, 3, 5000.00, 400.00, 0.00, 'Ordered', 'Medium', 'Sarah Johnson', 'Annual software license renewal', '2024-02-15'),
('PO-2024-004', '2024-02-05', 4, 4, 4, 7, 3000.00, 240.00, 0.00, 'Approved', 'Low', 'Lisa Brown', 'Legal consultation services', '2024-02-20'),
('PO-2024-005', '2024-02-10', 5, 5, 5, 9, 8000.00, 640.00, 100.00, 'Draft', 'Medium', 'David Wilson', 'Marketing campaign materials', '2024-02-25');

-- =====================================================
-- ANALYTICAL VIEWS FOR DASHBOARDS
-- =====================================================

-- Finance Dashboard Views
CREATE VIEW v_finance_summary AS
SELECT 
    d.dept_name,
    d.dept_code,
    d.budget_allocation,
    COALESCE(SUM(t.amount), 0) as total_spent,
    d.budget_allocation - COALESCE(SUM(t.amount), 0) as remaining_budget,
    ROUND((COALESCE(SUM(t.amount), 0) / d.budget_allocation) * 100, 2) as budget_utilization_pct
FROM finance_departments d
LEFT JOIN finance_transactions t ON d.dept_id = t.dept_id 
    AND t.status = 'Completed'
    AND EXTRACT(YEAR FROM t.transaction_date) = EXTRACT(YEAR FROM CURRENT_DATE)
GROUP BY d.dept_id, d.dept_name, d.dept_code, d.budget_allocation;

-- Monthly Finance Trends
CREATE VIEW v_finance_monthly_trends AS
SELECT 
    EXTRACT(YEAR FROM transaction_date) as year,
    EXTRACT(MONTH FROM transaction_date) as month,
    transaction_type,
    SUM(amount) as total_amount,
    COUNT(*) as transaction_count
FROM finance_transactions
WHERE status = 'Completed'
GROUP BY EXTRACT(YEAR FROM transaction_date), EXTRACT(MONTH FROM transaction_date), transaction_type
ORDER BY year, month, transaction_type;

-- Procurement Dashboard Views
CREATE VIEW v_procurement_summary AS
SELECT 
    d.dept_name,
    COUNT(po.order_id) as total_orders,
    SUM(po.grand_total) as total_value,
    AVG(po.grand_total) as avg_order_value,
    COUNT(CASE WHEN po.status = 'Received' THEN 1 END) as completed_orders,
    COUNT(CASE WHEN po.status = 'Pending' OR po.status = 'Approved' THEN 1 END) as pending_orders
FROM finance_departments d
LEFT JOIN procurement_orders po ON d.dept_id = po.dept_id
    AND EXTRACT(YEAR FROM po.order_date) = EXTRACT(YEAR FROM CURRENT_DATE)
GROUP BY d.dept_id, d.dept_name;

-- Vendor Performance
CREATE VIEW v_vendor_performance AS
SELECT 
    v.vendor_name,
    v.vendor_code,
    v.rating,
    COUNT(po.order_id) as total_orders,
    SUM(po.grand_total) as total_value,
    AVG(po.grand_total) as avg_order_value,
    COUNT(CASE WHEN po.status = 'Received' THEN 1 END) as completed_orders,
    ROUND((COUNT(CASE WHEN po.status = 'Received' THEN 1 END)::DECIMAL / COUNT(po.order_id)) * 100, 2) as completion_rate
FROM procurement_vendors v
LEFT JOIN procurement_orders po ON v.vendor_id = po.vendor_id
    AND EXTRACT(YEAR FROM po.order_date) = EXTRACT(YEAR FROM CURRENT_DATE)
GROUP BY v.vendor_id, v.vendor_name, v.vendor_code, v.rating;

-- Category Analysis
CREATE VIEW v_category_analysis AS
SELECT 
    c.category_name,
    c.category_code,
    COUNT(po.order_id) as order_count,
    SUM(po.grand_total) as total_value,
    AVG(po.grand_total) as avg_order_value,
    COUNT(DISTINCT po.vendor_id) as unique_vendors
FROM procurement_categories c
LEFT JOIN procurement_orders po ON c.category_id = po.category_id
    AND EXTRACT(YEAR FROM po.order_date) = EXTRACT(YEAR FROM CURRENT_DATE)
GROUP BY c.category_id, c.category_name, c.category_code;

-- =====================================================
-- GRANT PERMISSIONS
-- =====================================================

-- Grant permissions to application user (adjust username as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_app_user;
-- GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO your_app_user;
