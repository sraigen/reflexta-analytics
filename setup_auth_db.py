#!/usr/bin/env python3
"""
Database Setup Script for Authentication System
Creates the users table and default admin user.
"""

import streamlit as st
from src.db import get_conn, health_check
from src.auth import UserAuth

def setup_authentication_database():
    """Set up the authentication database with users table and default admin user."""
    
    st.title("🔐 Authentication Database Setup")
    st.markdown("Setting up user authentication system...")
    
    try:
        # Check database connection
        if not health_check():
            st.error("❌ Database connection failed. Please check your database configuration.")
            return False
        
        st.success("✅ Database connection successful!")
        
        # Create users table
        st.markdown("### Creating Users Table")
        conn = get_conn()
        
        # Create users table
        conn.query("""
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role VARCHAR(20) DEFAULT 'user',
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        st.success("✅ Users table created successfully!")
        
        # Check if any users exist
        user_count_result = conn.query("SELECT COUNT(*) as count FROM users")
        user_count = user_count_result.iloc[0]['count'] if not user_count_result.empty else 0
        
        st.info(f"📊 Current users in database: {user_count}")
        
        # Create default admin user if no users exist
        if user_count == 0:
            st.markdown("### Creating Default Admin User")
            
            auth = UserAuth()
            password_hash = auth.hash_password('admin123')
            
            conn.query("""
                INSERT INTO users (username, email, password_hash, role)
                VALUES (:username, :email, :password_hash, :role)
            """, params={
                'username': 'admin', 
                'email': 'admin@reflexta.com', 
                'password_hash': password_hash, 
                'role': 'admin'
            })
            
            st.success("✅ Default admin user created!")
            st.info("🔑 Default credentials: admin / admin123")
        else:
            st.info("ℹ️ Users already exist in database. Skipping default user creation.")
        
        # Verify setup
        st.markdown("### Verification")
        users_result = conn.query("SELECT username, email, role, is_active FROM users")
        
        if not users_result.empty:
            st.dataframe(users_result, use_container_width=True)
            st.success("🎉 Authentication database setup completed successfully!")
            return True
        else:
            st.error("❌ No users found after setup.")
            return False
            
    except Exception as e:
        st.error(f"❌ Error setting up authentication database: {str(e)}")
        return False

if __name__ == "__main__":
    setup_authentication_database()
