#!/usr/bin/env python3
"""
Direct script to create users table in the database.
"""

import streamlit as st
from src.db import get_conn, health_check
from src.auth import UserAuth

def create_users_table_direct():
    """Directly create the users table."""
    
    st.title("🔧 Create Users Table")
    
    try:
        # Check database connection
        if not health_check():
            st.error("❌ Database connection failed!")
            return False
        
        st.success("✅ Database connection successful!")
        
        # Get connection
        conn = get_conn()
        
        # Create users table
        st.markdown("Creating users table...")
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
        
        # Create default admin user
        st.markdown("Creating default admin user...")
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
        
        # Verify
        users_result = conn.query("SELECT username, email, role FROM users")
        if not users_result.empty:
            st.dataframe(users_result, use_container_width=True)
            st.success("🎉 Setup completed successfully!")
            return True
        else:
            st.error("❌ No users found!")
            return False
            
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    create_users_table_direct()
