#!/usr/bin/env python3
"""
User Management Page for Reflexta Analytics Platform
Administrative interface for user management and role assignment.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from src.auth import get_auth_manager, require_permission, get_current_user
from src.db import get_conn


@require_permission('users')
def render_user_management():
    """Render the user management interface."""
    
    st.set_page_config(
        page_title="User Management - Reflexta Analytics",
        page_icon="👥",
        layout="wide"
    )
    
    # Professional styling
    st.markdown("""
    <style>
    .user-management-header {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
        color: white;
        padding: 2rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .user-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border: 1px solid rgba(148, 163, 184, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .user-role-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .role-admin {
        background: linear-gradient(135deg, #dc2626 0%, #ef4444 100%);
        color: white;
    }
    
    .role-manager {
        background: linear-gradient(135deg, #2563eb 0%, #3b82f6 100%);
        color: white;
    }
    
    .role-analyst {
        background: linear-gradient(135deg, #059669 0%, #10b981 100%);
        color: white;
    }
    
    .role-viewer {
        background: linear-gradient(135deg, #6b7280 0%, #9ca3af 100%);
        color: white;
    }
    
    .status-active {
        color: #059669;
        font-weight: 600;
    }
    
    .status-inactive {
        color: #dc2626;
        font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="user-management-header">
        <h1>👥 User Management</h1>
        <p>Manage users, roles, and permissions for Reflexta Analytics Platform</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get current user
    current_user = get_current_user()
    st.info(f"👤 Logged in as: {current_user['first_name']} {current_user['last_name']} ({current_user['role_name']})")
    
    # Tabs for different management functions
    tab1, tab2, tab3, tab4 = st.tabs([
        "👥 Users", 
        "🔐 Roles & Permissions", 
        "📊 User Activity", 
        "➕ Add User"
    ])
    
    with tab1:
        render_users_tab()
    
    with tab2:
        render_roles_tab()
    
    with tab3:
        render_activity_tab()
    
    with tab4:
        render_add_user_tab()


def render_users_tab():
    """Render the users management tab."""
    
    st.markdown("### 👥 User Management")
    
    try:
        conn = get_conn()
        
        # Get users data
        query = """
        SELECT u.user_id, u.username, u.email, u.first_name, u.last_name,
               u.is_active, u.is_verified, u.last_login, u.created_at,
               r.role_name, r.permissions,
               d.dept_name as department_name
        FROM users u
        JOIN user_roles r ON u.role_id = r.role_id
        LEFT JOIN finance_departments d ON u.department_id = d.dept_id
        ORDER BY u.created_at DESC
        """
        
        users_df = conn.query(query)
        
        if users_df.empty:
            st.warning("No users found.")
            return
        
        # Display users in cards
        for _, user in users_df.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.markdown(f"""
                    <div class="user-card">
                        <h4>{user['first_name']} {user['last_name']}</h4>
                        <p><strong>Username:</strong> {user['username']}</p>
                        <p><strong>Email:</strong> {user['email']}</p>
                        <p><strong>Department:</strong> {user.get('department_name', 'N/A')}</p>
                        <p><strong>Last Login:</strong> {user['last_login'] if user['last_login'] else 'Never'}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    # Role badge
                    role_class = f"role-{user['role_name'].lower()}"
                    st.markdown(f"""
                    <span class="user-role-badge {role_class}">
                        {user['role_name'].upper()}
                    </span>
                    """, unsafe_allow_html=True)
                    
                    # Status
                    status_class = "status-active" if user['is_active'] else "status-inactive"
                    status_text = "ACTIVE" if user['is_active'] else "INACTIVE"
                    st.markdown(f"""
                    <p class="{status_class}">Status: {status_text}</p>
                    """, unsafe_allow_html=True)
                
                with col3:
                    if st.button("✏️ Edit", key=f"edit_{user['user_id']}"):
                        st.session_state['edit_user_id'] = user['user_id']
                        st.rerun()
                    
                    if st.button("🔒 Toggle", key=f"toggle_{user['user_id']}"):
                        toggle_user_status(user['user_id'], not user['is_active'])
                        st.rerun()
        
        # User statistics
        st.markdown("### 📊 User Statistics")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_users = len(users_df)
            st.metric("Total Users", total_users)
        
        with col2:
            active_users = len(users_df[users_df['is_active'] == True])
            st.metric("Active Users", active_users)
        
        with col3:
            verified_users = len(users_df[users_df['is_verified'] == True])
            st.metric("Verified Users", verified_users)
        
        with col4:
            recent_logins = len(users_df[users_df['last_login'].notna()])
            st.metric("Recent Logins", recent_logins)
        
    except Exception as e:
        st.error(f"Error loading users: {str(e)}")


def render_roles_tab():
    """Render the roles and permissions tab."""
    
    st.markdown("### 🔐 Roles & Permissions")
    
    try:
        conn = get_conn()
        
        # Get roles data
        query = """
        SELECT role_id, role_name, role_description, permissions, is_active, created_at
        FROM user_roles
        ORDER BY role_name
        """
        
        roles_df = conn.query(query)
        
        if roles_df.empty:
            st.warning("No roles found.")
            return
        
        # Display roles
        for _, role in roles_df.iterrows():
            with st.expander(f"🔐 {role['role_name'].upper()}", expanded=True):
                st.markdown(f"**Description:** {role['role_description']}")
                st.markdown(f"**Status:** {'Active' if role['is_active'] else 'Inactive'}")
                
                # Permissions
                st.markdown("**Permissions:**")
                permissions = role['permissions'] if isinstance(role['permissions'], dict) else {}
                
                col1, col2 = st.columns(2)
                
                with col1:
                    for perm, value in permissions.items():
                        if value:
                            st.markdown(f"✅ {perm.replace('_', ' ').title()}")
                
                with col2:
                    for perm, value in permissions.items():
                        if not value:
                            st.markdown(f"❌ {perm.replace('_', ' ').title()}")
        
        # Role statistics
        st.markdown("### 📊 Role Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_roles = len(roles_df)
            st.metric("Total Roles", total_roles)
        
        with col2:
            active_roles = len(roles_df[roles_df['is_active'] == True])
            st.metric("Active Roles", active_roles)
        
        with col3:
            # Get user count per role
            user_count_query = """
            SELECT r.role_name, COUNT(u.user_id) as user_count
            FROM user_roles r
            LEFT JOIN users u ON r.role_id = u.role_id
            GROUP BY r.role_id, r.role_name
            ORDER BY user_count DESC
            """
            
            user_counts = conn.query(user_count_query)
            most_used_role = user_counts.iloc[0]['role_name'] if not user_counts.empty else 'N/A'
            st.metric("Most Used Role", most_used_role)
        
    except Exception as e:
        st.error(f"Error loading roles: {str(e)}")


def render_activity_tab():
    """Render the user activity tab."""
    
    st.markdown("### 📊 User Activity")
    
    try:
        conn = get_conn()
        
        # Get active sessions
        query = """
        SELECT s.session_id, s.user_id, s.ip_address, s.created_at, s.last_activity, s.expires_at,
               u.username, u.first_name, u.last_name, r.role_name
        FROM user_sessions s
        JOIN users u ON s.user_id = u.user_id
        JOIN user_roles r ON u.role_id = r.role_id
        WHERE s.is_active = TRUE AND s.expires_at > CURRENT_TIMESTAMP
        ORDER BY s.last_activity DESC
        """
        
        sessions_df = conn.query(query)
        
        if sessions_df.empty:
            st.info("No active sessions found.")
            return
        
        # Display active sessions
        st.markdown("#### 🔐 Active Sessions")
        
        for _, session in sessions_df.iterrows():
            with st.container():
                col1, col2, col3 = st.columns([3, 2, 1])
                
                with col1:
                    st.markdown(f"""
                    **{session['first_name']} {session['last_name']}** ({session['username']})
                    - Role: {session['role_name']}
                    - IP: {session['ip_address']}
                    - Last Activity: {session['last_activity']}
                    """)
                
                with col2:
                    st.markdown(f"""
                    - Session Started: {session['created_at']}
                    - Expires: {session['expires_at']}
                    """)
                
                with col3:
                    if st.button("🔒 End Session", key=f"end_{session['session_id']}"):
                        end_user_session(session['session_id'])
                        st.rerun()
        
        # Activity statistics
        st.markdown("#### 📊 Activity Statistics")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            active_sessions = len(sessions_df)
            st.metric("Active Sessions", active_sessions)
        
        with col2:
            # Get unique users with active sessions
            unique_users = sessions_df['user_id'].nunique()
            st.metric("Active Users", unique_users)
        
        with col3:
            # Get sessions by role
            role_counts = sessions_df['role_name'].value_counts()
            most_active_role = role_counts.index[0] if not role_counts.empty else 'N/A'
            st.metric("Most Active Role", most_active_role)
        
    except Exception as e:
        st.error(f"Error loading activity: {str(e)}")


def render_add_user_tab():
    """Render the add user tab."""
    
    st.markdown("### ➕ Add New User")
    
    with st.form("add_user_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            username = st.text_input("Username", placeholder="Enter username")
            email = st.text_input("Email", placeholder="Enter email address")
            first_name = st.text_input("First Name", placeholder="Enter first name")
            last_name = st.text_input("Last Name", placeholder="Enter last name")
        
        with col2:
            # Get roles
            try:
                conn = get_conn()
                roles_df = conn.query("SELECT role_id, role_name FROM user_roles WHERE is_active = TRUE")
                role_options = {f"{row['role_name']}": row['role_id'] for _, row in roles_df.iterrows()}
                selected_role = st.selectbox("Role", list(role_options.keys()))
                
                # Get departments
                dept_df = conn.query("SELECT dept_id, dept_name FROM finance_departments ORDER BY dept_name")
                dept_options = {f"{row['dept_name']}": row['dept_id'] for _, row in dept_df.iterrows()}
                dept_options["No Department"] = None
                selected_dept = st.selectbox("Department", list(dept_options.keys()))
                
            except Exception as e:
                st.error(f"Error loading options: {str(e)}")
                return
        
        password = st.text_input("Password", type="password", placeholder="Enter password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm password")
        
        col1, col2 = st.columns(2)
        
        with col1:
            is_active = st.checkbox("Active User", value=True)
        
        with col2:
            is_verified = st.checkbox("Verified User", value=True)
        
        submitted = st.form_submit_button("➕ Add User", type="primary")
        
        if submitted:
            if not all([username, email, first_name, last_name, password]):
                st.error("❌ Please fill in all required fields.")
            elif password != confirm_password:
                st.error("❌ Passwords do not match.")
            else:
                try:
                    # Add user to database
                    add_user_to_database(
                        username, email, first_name, last_name, password,
                        role_options[selected_role], dept_options[selected_dept],
                        is_active, is_verified
                    )
                    st.success("✅ User added successfully!")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error adding user: {str(e)}")


def toggle_user_status(user_id: int, new_status: bool):
    """Toggle user active status."""
    try:
        conn = get_conn()
        
        conn.query("""
            UPDATE users 
            SET is_active = %(new_status)s, updated_at = CURRENT_TIMESTAMP
            WHERE user_id = %(user_id)s
        """, params={"new_status": new_status, "user_id": user_id})
        
        status_text = "activated" if new_status else "deactivated"
        st.success(f"✅ User {status_text} successfully!")
        
    except Exception as e:
        st.error(f"❌ Error updating user status: {str(e)}")


def end_user_session(session_id: str):
    """End a user session."""
    try:
        conn = get_conn()
        
        conn.query("""
            UPDATE user_sessions 
            SET is_active = FALSE
            WHERE session_id = %(session_id)s
        """, params={"session_id": session_id})
        
        st.success("✅ Session ended successfully!")
        
    except Exception as e:
        st.error(f"❌ Error ending session: {str(e)}")


def add_user_to_database(username: str, email: str, first_name: str, last_name: str, 
                        password: str, role_id: int, department_id: int, 
                        is_active: bool, is_verified: bool):
    """Add a new user to the database."""
    try:
        from src.auth import get_auth_manager
        
        conn = get_conn()
        
        # Hash password
        auth_manager = get_auth_manager()
        password_hash = auth_manager.hash_password(password)
        
        # Insert user
        conn.query("""
            INSERT INTO users (username, email, password_hash, first_name, last_name,
                             role_id, department_id, is_active, is_verified)
            VALUES (%(username)s, %(email)s, %(password_hash)s, %(first_name)s, %(last_name)s,
                    %(role_id)s, %(department_id)s, %(is_active)s, %(is_verified)s)
        """, params={
            "username": username, 
            "email": email, 
            "password_hash": password_hash, 
            "first_name": first_name, 
            "last_name": last_name,
            "role_id": role_id, 
            "department_id": department_id, 
            "is_active": is_active, 
            "is_verified": is_verified
        })
        
    except Exception as e:
        raise Exception(f"Database error: {str(e)}")


# Main execution
if __name__ == "__main__":
    render_user_management()
