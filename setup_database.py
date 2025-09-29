#!/usr/bin/env python3
"""
Simple Database Setup Script
Creates the users table and default admin user.
"""

import streamlit as st
from src.db import get_conn, health_check
from src.auth import UserAuth

def setup_database():
    """Set up the database with users table."""
    
    st.title("🔧 Database Setup")
    st.markdown("Setting up authentication database...")
    
    try:
        # Check database connection
        if not health_check():
            st.error("❌ Database connection failed!")
            return False
        
        st.success("✅ Database connection successful!")
        
        # Get connection
        conn = get_conn()
        
        # Create users table
        st.markdown("### Creating Users Table")
        try:
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
        except Exception as e:
            st.error(f"❌ Error creating users table: {str(e)}")
            return False
        
        # Check if users exist
        try:
            users_result = conn.query("SELECT COUNT(*) as count FROM users")
            user_count = users_result.iloc[0]['count'] if not users_result.empty else 0
            st.info(f"📊 Current users: {user_count}")
        except Exception as e:
            st.warning(f"⚠️ Could not count users: {str(e)}")
            user_count = 0
        
        # Create default admin user if no users exist
        if user_count == 0:
            st.markdown("### Creating Default Admin User")
            try:
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
            except Exception as e:
                st.error(f"❌ Error creating admin user: {str(e)}")
                return False
        
        # Verify setup
        st.markdown("### Verification")
        try:
            users_result = conn.query("SELECT username, email, role, is_active FROM users")
            if not users_result.empty:
                st.dataframe(users_result, use_container_width=True)
                st.success("🎉 Database setup completed successfully!")
                return True
            else:
                st.error("❌ No users found after setup.")
                return False
        except Exception as e:
            st.error(f"❌ Error verifying setup: {str(e)}")
            return False
            
    except Exception as e:
        st.error(f"❌ Setup failed: {str(e)}")
        return False

if __name__ == "__main__":
    setup_database()
