-- =====================================================
-- USERS AND AUTHENTICATION SCHEMA
-- Secure user management for Reflexta Analytics Platform
-- =====================================================

-- Drop existing tables if they exist (for clean setup)
DROP TABLE IF EXISTS user_sessions CASCADE;
DROP TABLE IF EXISTS user_roles CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- =====================================================
-- USER MANAGEMENT TABLES
-- =====================================================

-- User Roles
CREATE TABLE user_roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL UNIQUE,
    role_description TEXT,
    permissions JSONB DEFAULT '{}',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Users Table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    role_id INTEGER REFERENCES user_roles(role_id),
    department_id INTEGER REFERENCES finance_departments(dept_id),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP,
    login_attempts INTEGER DEFAULT 0,
    locked_until TIMESTAMP,
    password_reset_token VARCHAR(255),
    password_reset_expires TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- User Sessions
CREATE TABLE user_sessions (
    session_id VARCHAR(255) PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id) ON DELETE CASCADE,
    ip_address INET,
    user_agent TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- User indexes
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role_id);
CREATE INDEX idx_users_department ON users(department_id);
CREATE INDEX idx_users_active ON users(is_active);
CREATE INDEX idx_users_last_login ON users(last_login);

-- Session indexes
CREATE INDEX idx_user_sessions_user_id ON user_sessions(user_id);
CREATE INDEX idx_user_sessions_active ON user_sessions(is_active);
CREATE INDEX idx_user_sessions_expires ON user_sessions(expires_at);

-- =====================================================
-- INSERT DEFAULT DATA
-- =====================================================

-- Insert default roles
INSERT INTO user_roles (role_name, role_description, permissions) VALUES
('admin', 'System Administrator', '{"dashboard": true, "finance": true, "procurement": true, "analytics": true, "database": true, "users": true}'),
('manager', 'Department Manager', '{"dashboard": true, "finance": true, "procurement": true, "analytics": true, "database": false, "users": false}'),
('analyst', 'Data Analyst', '{"dashboard": true, "finance": true, "procurement": true, "analytics": true, "database": false, "users": false}'),
('viewer', 'Read-Only User', '{"dashboard": true, "finance": false, "procurement": false, "analytics": true, "database": false, "users": false}');

-- Insert default admin user (password: admin123)
-- Password hash for 'admin123' using bcrypt
INSERT INTO users (username, email, password_hash, first_name, last_name, role_id, department_id, is_active, is_verified) VALUES
('admin', 'admin@reflexta.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Qz8K2K', 'System', 'Administrator', 1, 1, TRUE, TRUE),
('demo', 'demo@reflexta.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8Qz8K2K', 'Demo', 'User', 2, 1, TRUE, TRUE);

-- =====================================================
-- FUNCTIONS AND TRIGGERS
-- =====================================================

-- Function to update last_login
CREATE OR REPLACE FUNCTION update_last_login()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE user_id = NEW.user_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to update last_login on session creation
CREATE TRIGGER trigger_update_last_login
    AFTER INSERT ON user_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_last_login();

-- Function to clean expired sessions
CREATE OR REPLACE FUNCTION clean_expired_sessions()
RETURNS void AS $$
BEGIN
    DELETE FROM user_sessions WHERE expires_at < CURRENT_TIMESTAMP;
END;
$$ LANGUAGE plpgsql;

-- =====================================================
-- SECURITY VIEWS
-- =====================================================

-- View for user permissions
CREATE VIEW user_permissions AS
SELECT 
    u.user_id,
    u.username,
    u.email,
    u.first_name,
    u.last_name,
    r.role_name,
    r.permissions,
    d.dept_name as department_name,
    u.is_active,
    u.last_login
FROM users u
JOIN user_roles r ON u.role_id = r.role_id
LEFT JOIN finance_departments d ON u.department_id = d.dept_id
WHERE u.is_active = TRUE;

-- View for active sessions
CREATE VIEW active_sessions AS
SELECT 
    s.session_id,
    s.user_id,
    u.username,
    u.first_name,
    u.last_name,
    s.ip_address,
    s.created_at,
    s.last_activity,
    s.expires_at
FROM user_sessions s
JOIN users u ON s.user_id = u.user_id
WHERE s.is_active = TRUE AND s.expires_at > CURRENT_TIMESTAMP;
