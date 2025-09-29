#!/usr/bin/env python3
"""
Setup Users and Authentication for Reflexta Analytics Platform
Creates users table and initial authentication data.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from src.db import get_conn
import streamlit as st


def setup_users_database():
    """Setup users database tables and initial data."""
    
    st.title("🔐 Setup Users Database")
    st.markdown("Setting up authentication system for Reflexta Analytics Platform")
    
    try:
        # Read the users schema
        schema_path = Path(__file__).parent / "database" / "users_schema.sql"
        
        if not schema_path.exists():
            st.error(f"❌ Schema file not found: {schema_path}")
            return False
        
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        # Execute schema
        conn = get_conn()
        
        st.info("📝 Creating users tables...")
        
        # Split schema into individual statements
        statements = [stmt.strip() for stmt in schema_sql.split(';') if stmt.strip()]
        
        for statement in statements:
            if statement:
                try:
                    conn.query(statement)
                except Exception as e:
                    st.warning(f"Statement may have already been executed: {str(e)}")
        
        st.info("✅ Users database setup completed successfully!")
        
        # Show created tables
        st.markdown("### 📊 Created Tables:")
        
        tables_query = """
        SELECT table_name, table_type
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name IN ('users', 'user_roles', 'user_sessions')
        ORDER BY table_name
        """
        
        import pandas as pd
        tables_df = conn.query(tables_query)
        
        if not tables_df.empty:
            st.dataframe(tables_df, use_container_width=True)
        else:
            st.warning("No tables found.")
        
        # Show default users
        st.markdown("### 👥 Default Users Created:")
        
        users_query = """
        SELECT u.username, u.email, u.first_name, u.last_name, r.role_name, u.is_active
        FROM users u
        JOIN user_roles r ON u.role_id = r.role_id
        ORDER BY u.user_id
        """
        
        users_df = conn.query(users_query)
        
        if not users_df.empty:
            st.dataframe(users_df, use_container_width=True)
            
            st.markdown("### 🔑 Default Login Credentials:")
            st.info("""
            **Admin User:**
            - Username: `admin`
            - Password: `admin123`
            - Role: Administrator
            
            **Demo User:**
            - Username: `demo`
            - Password: `admin123`
            - Role: Manager
            """)
        else:
            st.warning("No users found.")
        
        # Show roles and permissions
        st.markdown("### 🔐 Roles and Permissions:")
        
        roles_query = """
        SELECT role_name, role_description, permissions
        FROM user_roles
        ORDER BY role_id
        """
        
        roles_df = conn.query(roles_query)
        
        if not roles_df.empty:
            for _, role in roles_df.iterrows():
                with st.expander(f"🔐 {role['role_name'].upper()}", expanded=False):
                    st.markdown(f"**Description:** {role['role_description']}")
                    
                    permissions = role['permissions'] if isinstance(role['permissions'], dict) else {}
                    st.markdown("**Permissions:**")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        for perm, value in permissions.items():
                            if value:
                                st.markdown(f"✅ {perm.replace('_', ' ').title()}")
                    
                    with col2:
                        for perm, value in permissions.items():
                            if not value:
                                st.markdown(f"❌ {perm.replace('_', ' ').title()}")
        
        st.success("🎉 Users database setup completed successfully!")
        st.info("You can now use the login system. Navigate to the main app to test authentication.")
        
        return True
        
    except Exception as e:
        st.error(f"❌ Error setting up users database: {str(e)}")
        return False


def verify_users_setup():
    """Verify that users database is properly set up."""
    
    try:
        conn = get_conn()
        
        # Check if tables exist
        tables_query = """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name IN ('users', 'user_roles', 'user_sessions')
        """
        
        import pandas as pd
        tables_df = conn.query(tables_query)
        
        required_tables = ['users', 'user_roles', 'user_sessions']
        existing_tables = tables_df['table_name'].tolist() if not tables_df.empty else []
        
        missing_tables = [table for table in required_tables if table not in existing_tables]
        
        if missing_tables:
            st.error(f"❌ Missing tables: {', '.join(missing_tables)}")
            return False
        
        # Check if default users exist
        users_query = """
        SELECT COUNT(*) as user_count
        FROM users
        """
        
        users_df = conn.query(users_query)
        users_count = users_df.iloc[0]['user_count'] if not users_df.empty else 0
        
        if users_count == 0:
            st.warning("⚠️ No users found. Please run the setup.")
            return False
        
        st.success("✅ Users database is properly set up!")
        return True
        
    except Exception as e:
        st.error(f"❌ Error verifying users setup: {str(e)}")
        return False


def main():
    """Main function to setup users database."""
    
    st.set_page_config(
        page_title="Setup Users - Reflexta Analytics",
        page_icon="🔐",
        layout="wide"
    )
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <h1>🔐 Reflexta Analytics Platform</h1>
        <h2>Users Database Setup</h2>
        <p>Setting up authentication system for secure access</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Check if already set up
    if verify_users_setup():
        st.info("✅ Users database is already set up!")
        
        if st.button("🔄 Reset Database", type="secondary"):
            st.warning("This will delete all existing users and recreate the database.")
            if st.button("⚠️ Confirm Reset", type="primary"):
                # Drop and recreate tables
                try:
                    conn = get_conn()
                    cursor = conn.cursor()
                    
                    cursor.execute("DROP TABLE IF EXISTS user_sessions CASCADE;")
                    cursor.execute("DROP TABLE IF EXISTS user_roles CASCADE;")
                    cursor.execute("DROP TABLE IF EXISTS users CASCADE;")
                    
                    conn.commit()
                    cursor.close()
                    
                    st.success("✅ Database reset completed!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Error resetting database: {str(e)}")
    else:
        if st.button("🚀 Setup Users Database", type="primary"):
            setup_users_database()
    
    # Show current status
    st.markdown("### 📊 Current Status:")
    
    try:
        conn = get_conn()
        
        # Table status
        tables_query = """
        SELECT table_name, 
               CASE WHEN table_name IN ('users', 'user_roles', 'user_sessions') 
                    THEN '✅ Exists' 
                    ELSE '❌ Missing' 
               END as status
        FROM information_schema.tables
        WHERE table_schema = 'public'
        AND table_name IN ('users', 'user_roles', 'user_sessions')
        ORDER BY table_name
        """
        
        import pandas as pd
        tables_df = conn.query(tables_query)
        
        if not tables_df.empty:
            st.dataframe(tables_df, use_container_width=True)
        else:
            st.warning("No authentication tables found.")
        
        # User count
        try:
            users_query = "SELECT COUNT(*) as user_count FROM users"
            users_df = conn.query(users_query)
            user_count = users_df.iloc[0]['user_count'] if not users_df.empty else 0
            st.metric("Total Users", user_count)
        except:
            st.metric("Total Users", "N/A")
        
    except Exception as e:
        st.error(f"❌ Error checking status: {str(e)}")


if __name__ == "__main__":
    main()
