#!/usr/bin/env python3
"""
Authentication and User Management for Reflexta Analytics Platform
Secure user authentication with role-based access control.
"""

import hashlib
import secrets
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import streamlit as st
from src.db import get_conn


class AuthManager:
    """Authentication manager for user login, sessions, and permissions."""
    
    def __init__(self):
        """Initialize the authentication manager."""
        self.session_timeout = timedelta(hours=8)  # 8 hour session timeout
    
    def hash_password(self, password: str) -> str:
        """Hash a password using bcrypt."""
        try:
            import bcrypt
            salt = bcrypt.gensalt()
            return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
        except ImportError:
            # Fallback to hashlib if bcrypt is not available
            return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify a password against its hash."""
        try:
            import bcrypt
            return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
        except ImportError:
            # Fallback to hashlib if bcrypt is not available
            return hashlib.sha256(password.encode()).hexdigest() == hashed
    
    def authenticate_user(self, username: str, password: str) -> Optional[Dict[str, Any]]:
        """Authenticate a user with username and password."""
        try:
            conn = get_conn()
            
            # Get user data using Streamlit connection API
            query = """
                SELECT u.user_id, u.username, u.email, u.password_hash, u.first_name, u.last_name,
                       u.is_active, u.is_verified, u.role_id, u.department_id,
                       r.role_name, r.permissions,
                       d.dept_name as department_name
                FROM users u
                JOIN user_roles r ON u.role_id = r.role_id
                LEFT JOIN finance_departments d ON u.department_id = d.dept_id
                WHERE u.username = %(username)s AND u.is_active = TRUE
            """
            
            user_df = conn.query(query, params={"username": username})
            
            if user_df.empty:
                return None
            
            user_data = user_df.iloc[0].to_dict()
            
            if self.verify_password(password, user_data['password_hash']):
                # Create session
                session_id = self.create_session(user_data['user_id'])
                
                # Update last login
                conn.query("""
                    UPDATE users 
                    SET last_login = CURRENT_TIMESTAMP
                    WHERE user_id = %(user_id)s
                """, params={"user_id": user_data['user_id']})
                
                # Return user data without password
                user_data['session_id'] = session_id
                del user_data['password_hash']
                
                return user_data
            
            return None
            
        except Exception as e:
            st.error(f"Authentication error: {str(e)}")
            return None
    
    def create_session(self, user_id: int) -> str:
        """Create a new session for a user."""
        try:
            conn = get_conn()
            
            # Generate session ID
            session_id = str(uuid.uuid4())
            
            # Get client IP (simplified for Streamlit)
            ip_address = "127.0.0.1"  # Default for local development
            
            # Create session record
            conn.query("""
                INSERT INTO user_sessions (session_id, user_id, ip_address, expires_at, is_active)
                VALUES (%(session_id)s, %(user_id)s, %(ip_address)s, %(expires_at)s, TRUE)
            """, params={
                "session_id": session_id,
                "user_id": user_id,
                "ip_address": ip_address,
                "expires_at": datetime.now() + self.session_timeout
            })
            
            return session_id
            
        except Exception as e:
            st.error(f"Error creating session: {str(e)}")
            return None
    
    def validate_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Validate a session and return user data if valid."""
        try:
            conn = get_conn()
            
            # Check session validity
            query = """
                SELECT s.session_id, s.user_id, s.expires_at, s.is_active,
                       u.username, u.email, u.first_name, u.last_name, u.is_active as user_active,
                       r.role_name, r.permissions,
                       d.dept_name as department_name
                FROM user_sessions s
                JOIN users u ON s.user_id = u.user_id
                JOIN user_roles r ON u.role_id = r.role_id
                LEFT JOIN finance_departments d ON u.department_id = d.dept_id
                WHERE s.session_id = %(session_id)s 
                AND s.is_active = TRUE 
                AND s.expires_at > CURRENT_TIMESTAMP
                AND u.is_active = TRUE
            """
            
            session_df = conn.query(query, params={"session_id": session_id})
            
            if session_df.empty:
                return None
            
            session_data = session_df.iloc[0].to_dict()
            
            # Update last activity
            conn.query("""
                UPDATE user_sessions 
                SET last_activity = CURRENT_TIMESTAMP
                WHERE session_id = %(session_id)s
            """, params={"session_id": session_id})
            
            return session_data
            
        except Exception as e:
            st.error(f"Session validation error: {str(e)}")
            return None
    
    def logout_user(self, session_id: str) -> bool:
        """Logout a user by invalidating their session."""
        try:
            conn = get_conn()
            
            conn.query("""
                UPDATE user_sessions 
                SET is_active = FALSE
                WHERE session_id = %(session_id)s
            """, params={"session_id": session_id})
            
            return True
            
        except Exception as e:
            st.error(f"Logout error: {str(e)}")
            return False
    
    def check_permission(self, user_id: int, permission: str) -> bool:
        """Check if a user has a specific permission."""
        try:
            conn = get_conn()
            
            query = """
                SELECT r.permissions
                FROM users u
                JOIN user_roles r ON u.role_id = r.role_id
                WHERE u.user_id = %(user_id)s AND u.is_active = TRUE
            """
            
            user_df = conn.query(query, params={"user_id": user_id})
            
            if user_df.empty:
                return False
            
            permissions = user_df.iloc[0]['permissions']
            
            if isinstance(permissions, dict):
                return permissions.get(permission, False)
            
            return False
            
        except Exception as e:
            st.error(f"Permission check error: {str(e)}")
            return False
    
    def get_user_permissions(self, user_id: int) -> Dict[str, bool]:
        """Get all permissions for a user."""
        try:
            conn = get_conn()
            
            query = """
                SELECT r.permissions
                FROM users u
                JOIN user_roles r ON u.role_id = r.role_id
                WHERE u.user_id = %(user_id)s AND u.is_active = TRUE
            """
            
            user_df = conn.query(query, params={"user_id": user_id})
            
            if user_df.empty:
                return {}
            
            permissions = user_df.iloc[0]['permissions']
            
            if isinstance(permissions, dict):
                return permissions
            
            return {}
            
        except Exception as e:
            st.error(f"Error getting user permissions: {str(e)}")
            return {}
    
    def cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions and return count of cleaned sessions."""
        try:
            conn = get_conn()
            
            # Get count of expired sessions
            count_df = conn.query("""
                SELECT COUNT(*) as count
                FROM user_sessions
                WHERE expires_at < CURRENT_TIMESTAMP OR is_active = FALSE
            """)
            
            count = count_df.iloc[0]['count'] if not count_df.empty else 0
            
            # Clean up expired sessions
            conn.query("""
                DELETE FROM user_sessions
                WHERE expires_at < CURRENT_TIMESTAMP OR is_active = FALSE
            """)
            
            return count
            
        except Exception as e:
            st.error(f"Session cleanup error: {str(e)}")
            return 0


# Global auth manager instance
_auth_manager = None


def get_auth_manager() -> AuthManager:
    """Get the global authentication manager instance."""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager


def is_authenticated() -> bool:
    """Check if the current user is authenticated."""
    if 'authenticated' not in st.session_state:
        return False
    
    if not st.session_state.get('authenticated', False):
        return False
    
    # Validate session
    session_id = st.session_state.get('session_id')
    if not session_id:
        return False
    
    auth_manager = get_auth_manager()
    user_data = auth_manager.validate_session(session_id)
    
    if user_data:
        # Update session state with fresh user data
        st.session_state['user_data'] = user_data
        return True
    
    # Session is invalid, clear authentication
    st.session_state.clear()
    return False


def get_current_user() -> Optional[Dict[str, Any]]:
    """Get the current authenticated user data."""
    if not is_authenticated():
        return None
    
    return st.session_state.get('user_data')


def require_permission(permission: str):
    """Decorator to require a specific permission for a function."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if not is_authenticated():
                st.error("🔒 Authentication required")
                st.info("Please log in to access this feature.")
                return
            
            current_user = get_current_user()
            if not current_user:
                st.error("🔒 User session not found")
                return
            
            auth_manager = get_auth_manager()
            if not auth_manager.check_permission(current_user['user_id'], permission):
                st.error(f"🚫 Access denied. You don't have permission for: {permission}")
                st.info("Contact your administrator for access.")
                return
            
            return func(*args, **kwargs)
        return wrapper
    return decorator


def has_permission(permission: str) -> bool:
    """Check if the current user has a specific permission."""
    if not is_authenticated():
        return False
    
    current_user = get_current_user()
    if not current_user:
        return False
    
    auth_manager = get_auth_manager()
    return auth_manager.check_permission(current_user['user_id'], permission)


def get_user_role() -> Optional[str]:
    """Get the current user's role."""
    current_user = get_current_user()
    if current_user:
        return current_user.get('role_name')
    return None


def is_admin() -> bool:
    """Check if the current user is an administrator."""
    return get_user_role() == 'Administrator'


def is_manager() -> bool:
    """Check if the current user is a manager."""
    role = get_user_role()
    return role in ['Administrator', 'Manager']


def get_user_department() -> Optional[str]:
    """Get the current user's department."""
    current_user = get_current_user()
    if current_user:
        return current_user.get('department_name')
    return None