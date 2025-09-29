#!/usr/bin/env python3
"""
Authentication System for Reflexta Analytics Platform
Comprehensive user authentication with login, registration, and session management.
"""

from __future__ import annotations

import hashlib
import secrets
import streamlit as st
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import pandas as pd
from .db import get_conn


class UserAuth:
    """User authentication and session management."""
    
    def __init__(self):
        self.session_timeout = 24 * 60 * 60  # 24 hours in seconds
        self.initialize_session()
    
    def initialize_session(self) -> None:
        """Initialize authentication session state."""
        if 'auth' not in st.session_state:
            st.session_state.auth = {
                'is_authenticated': False,
                'user_id': None,
                'username': None,
                'email': None,
                'role': None,
                'login_time': None,
                'last_activity': None
            }
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256 with salt."""
        salt = secrets.token_hex(16)
        password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}:{password_hash}"
    
    def verify_password(self, password: str, stored_hash: str) -> bool:
        """Verify password against stored hash."""
        try:
            salt, password_hash = stored_hash.split(':')
            computed_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return computed_hash == password_hash
        except ValueError:
            return False
    
    def create_user(self, username: str, email: str, password: str, role: str = 'user') -> Dict[str, Any]:
        """Create a new user account."""
        try:
            conn = get_conn()
            
            # Check if user already exists
            existing_user = conn.query(
                "SELECT id FROM users WHERE username = :username OR email = :email",
                params={"username": username, "email": email}
            )
            
            if not existing_user.empty:
                return {'success': False, 'message': 'Username or email already exists'}
            
            # Hash password
            password_hash = self.hash_password(password)
            
            # Insert new user
            result = conn.query("""
                INSERT INTO users (username, email, password_hash, role, created_at, is_active)
                VALUES (:username, :email, :password_hash, :role, :created_at, :is_active)
                RETURNING id
            """, params={
                "username": username, 
                "email": email, 
                "password_hash": password_hash, 
                "role": role, 
                "created_at": datetime.now(), 
                "is_active": True
            })
            
            if not result.empty:
                user_id = result.iloc[0]['id']
                return {
                    'success': True, 
                    'message': 'User created successfully',
                    'user_id': user_id
                }
            else:
                return {'success': False, 'message': 'Failed to create user'}
            
        except Exception as e:
            return {'success': False, 'message': f'Error creating user: {str(e)}'}
    
    def authenticate_user(self, username: str, password: str) -> Dict[str, Any]:
        """Authenticate user login."""
        try:
            conn = get_conn()
            
            # Get user data
            user_data = conn.query("""
                SELECT id, username, email, password_hash, role, is_active, last_login
                FROM users 
                WHERE username = :username OR email = :email
            """, params={"username": username, "email": username})
            
            if user_data.empty:
                return {'success': False, 'message': 'Invalid username or password'}
            
            user_row = user_data.iloc[0]
            user_id = user_row['id']
            db_username = user_row['username']
            email = user_row['email']
            password_hash = user_row['password_hash']
            role = user_row['role']
            is_active = user_row['is_active']
            
            # Check if user is active
            if not is_active:
                return {'success': False, 'message': 'Account is deactivated'}
            
            # Verify password
            if not self.verify_password(password, password_hash):
                return {'success': False, 'message': 'Invalid username or password'}
            
            # Update last login
            conn.query(
                "UPDATE users SET last_login = :last_login WHERE id = :user_id",
                params={"last_login": datetime.now(), "user_id": user_id}
            )
            
            # Set session data
            st.session_state.auth.update({
                'is_authenticated': True,
                'user_id': user_id,
                'username': db_username,
                'email': email,
                'role': role,
                'login_time': datetime.now(),
                'last_activity': datetime.now()
            })
            
            return {
                'success': True,
                'message': 'Login successful',
                'user_data': {
                    'user_id': user_id,
                    'username': db_username,
                    'email': email,
                    'role': role
                }
            }
            
        except Exception as e:
            return {'success': False, 'message': f'Authentication error: {str(e)}'}
    
    def logout_user(self) -> None:
        """Logout current user."""
        st.session_state.auth.update({
            'is_authenticated': False,
            'user_id': None,
            'username': None,
            'email': None,
            'role': None,
            'login_time': None,
            'last_activity': None
        })
        st.rerun()
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return st.session_state.auth.get('is_authenticated', False)
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current user data."""
        if self.is_authenticated():
            return {
                'user_id': st.session_state.auth.get('user_id'),
                'username': st.session_state.auth.get('username'),
                'email': st.session_state.auth.get('email'),
                'role': st.session_state.auth.get('role'),
                'login_time': st.session_state.auth.get('login_time'),
                'last_activity': st.session_state.auth.get('last_activity')
            }
        return None
    
    def check_session_timeout(self) -> bool:
        """Check if session has timed out."""
        if not self.is_authenticated():
            return False
        
        last_activity = st.session_state.auth.get('last_activity')
        if not last_activity:
            return True
        
        time_diff = (datetime.now() - last_activity).total_seconds()
        return time_diff > self.session_timeout
    
    def update_activity(self) -> None:
        """Update last activity timestamp."""
        if self.is_authenticated():
            st.session_state.auth['last_activity'] = datetime.now()
    
    def has_role(self, required_role: str) -> bool:
        """Check if user has required role."""
        if not self.is_authenticated():
            return False
        
        user_role = st.session_state.auth.get('role')
        role_hierarchy = {
            'admin': ['admin', 'manager', 'user'],
            'manager': ['manager', 'user'],
            'user': ['user']
        }
        
        return required_role in role_hierarchy.get(user_role, [])
    
    def get_user_permissions(self) -> List[str]:
        """Get user permissions based on role."""
        role = st.session_state.auth.get('role', 'user')
        
        permissions = {
            'admin': [
                'view_dashboard', 'view_finance', 'view_procurement', 'view_analytics',
                'view_database', 'manage_users', 'view_reports', 'export_data',
                'admin_settings', 'system_config'
            ],
            'manager': [
                'view_dashboard', 'view_finance', 'view_procurement', 'view_analytics',
                'view_database', 'view_reports', 'export_data'
            ],
            'user': [
                'view_dashboard', 'view_finance', 'view_procurement', 'view_analytics'
            ]
        }
        
        return permissions.get(role, permissions['user'])


def create_users_table() -> None:
    """Create users table if it doesn't exist."""
    try:
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
        
        # Check if any users exist
        user_count_result = conn.query("SELECT COUNT(*) as count FROM users")
        user_count = user_count_result.iloc[0]['count'] if not user_count_result.empty else 0
        
        # Create default admin user if no users exist
        if user_count == 0:
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
        
    except Exception as e:
        st.error(f"Error creating users table: {str(e)}")


def require_auth(func):
    """Decorator to require authentication for functions."""
    def wrapper(*args, **kwargs):
        auth = UserAuth()
        
        # Check if user is authenticated
        if not auth.is_authenticated():
            st.error("🔒 Authentication required. Please log in to access this feature.")
            st.stop()
        
        # Check session timeout
        if auth.check_session_timeout():
            st.error("⏰ Session expired. Please log in again.")
            auth.logout_user()
            st.stop()
        
        # Update activity
        auth.update_activity()
        
        return func(*args, **kwargs)
    return wrapper


def require_role(required_role: str):
    """Decorator to require specific role for functions."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            auth = UserAuth()
            
            if not auth.is_authenticated():
                st.error("🔒 Authentication required.")
                st.stop()
            
            if not auth.has_role(required_role):
                st.error(f"🚫 Access denied. {required_role.title()} role required.")
                st.stop()
            
            auth.update_activity()
            return func(*args, **kwargs)
        return wrapper
    return decorator


def require_permission(permission: str):
    """Decorator to require specific permission for functions."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            auth = UserAuth()
            
            if not auth.is_authenticated():
                st.error("🔒 Authentication required.")
                st.stop()
            
            user_permissions = auth.get_user_permissions()
            if permission not in user_permissions:
                st.error(f"🚫 Access denied. {permission.replace('_', ' ').title()} permission required.")
                st.stop()
            
            auth.update_activity()
            return func(*args, **kwargs)
        return wrapper
    return decorator
