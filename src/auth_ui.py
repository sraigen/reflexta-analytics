#!/usr/bin/env python3
"""
Authentication UI Components for Reflexta Analytics Platform
Professional login, registration, and user management interfaces.
"""

from __future__ import annotations

import streamlit as st
from datetime import datetime
from typing import Optional, Dict, Any
from .auth import UserAuth, create_users_table


def render_login_form() -> None:
    """Render professional login form."""
    
    # Professional login CSS
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 16px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    .login-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .login-header h1 {
        color: #1e293b;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .login-header p {
        color: #64748b;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
    }
    
    .login-form {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    
    .form-group {
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .form-label {
        font-weight: 600;
        color: #374151;
        font-size: 0.9rem;
    }
    
    .form-input {
        padding: 0.8rem 1rem;
        border: 2px solid #e2e8f6;
        border-radius: 8px;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: white;
    }
    
    .form-input:focus {
        outline: none;
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    .login-button {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .login-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
    }
    
    .login-footer {
        text-align: center;
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e2e8f6;
    }
    
    .login-footer a {
        color: #6366f1;
        text-decoration: none;
        font-weight: 600;
    }
    
    .login-footer a:hover {
        text-decoration: underline;
    }
    
    .error-message {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        color: #dc2626;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        border: 1px solid #fecaca;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    .success-message {
        background: linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%);
        color: #16a34a;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        border: 1px solid #bbf7d0;
        margin-bottom: 1rem;
        font-weight: 500;
    }
    
    /* Dark mode compatibility */
    .stApp[data-theme="dark"] .login-container {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border: 1px solid rgba(148, 163, 184, 0.3);
    }
    
    .stApp[data-theme="dark"] .login-header h1 {
        color: #f1f5f9;
    }
    
    .stApp[data-theme="dark"] .login-header p {
        color: #94a3b8;
    }
    
    .stApp[data-theme="dark"] .form-label {
        color: #f1f5f9;
    }
    
    .stApp[data-theme="dark"] .form-input {
        background: #334155;
        border: 2px solid rgba(148, 163, 184, 0.3);
        color: #f1f5f9;
    }
    
    .stApp[data-theme="dark"] .form-input::placeholder {
        color: #94a3b8;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Login form
    st.markdown("""
    <div class="login-container">
        <div class="login-header">
            <h1>🔐 Welcome Back</h1>
            <p>Sign in to Reflexta Analytics Platform</p>
        </div>
        <div class="login-form">
    """, unsafe_allow_html=True)
    
    # Login form fields
    with st.form("login_form", clear_on_submit=False):
        username = st.text_input(
            "Username or Email",
            placeholder="Enter your username or email",
            key="login_username"
        )
        
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            remember_me = st.checkbox("Remember me", key="remember_me")
        
        with col2:
            forgot_password = st.button("Forgot Password?", key="forgot_password")
        
        login_submitted = st.form_submit_button(
            "🚀 Sign In",
            use_container_width=True,
            type="primary"
        )
        
        if login_submitted:
            if username and password:
                auth = UserAuth()
                result = auth.authenticate_user(username, password)
                
                if result['success']:
                    st.success("✅ Login successful! Welcome to Reflexta Analytics Platform.")
                    st.rerun()
                else:
                    st.error(f"❌ {result['message']}")
            else:
                st.error("❌ Please fill in all fields.")
        
        if forgot_password:
            st.info("💡 Contact your administrator to reset your password.")
    
    st.markdown("""
        </div>
        <div class="login-footer">
            <p>Don't have an account? <a href="#" onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'show_register', value: true}, '*')">Sign up here</a></p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_registration_form() -> None:
    """Render professional registration form."""
    
    # Professional registration CSS
    st.markdown("""
    <style>
    .register-container {
        max-width: 500px;
        margin: 0 auto;
        padding: 2rem;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 16px;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    .register-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .register-header h1 {
        color: #1e293b;
        font-size: 2rem;
        font-weight: 700;
        margin: 0;
    }
    
    .register-header p {
        color: #64748b;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
    }
    
    .register-form {
        display: flex;
        flex-direction: column;
        gap: 1.5rem;
    }
    
    .form-row {
        display: flex;
        gap: 1rem;
    }
    
    .form-group {
        flex: 1;
        display: flex;
        flex-direction: column;
        gap: 0.5rem;
    }
    
    .form-label {
        font-weight: 600;
        color: #374151;
        font-size: 0.9rem;
    }
    
    .form-input {
        padding: 0.8rem 1rem;
        border: 2px solid #e2e8f6;
        border-radius: 8px;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: white;
    }
    
    .form-input:focus {
        outline: none;
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    .register-button {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        border: none;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .register-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(16, 185, 129, 0.3);
    }
    
    .register-footer {
        text-align: center;
        margin-top: 1.5rem;
        padding-top: 1.5rem;
        border-top: 1px solid #e2e8f6;
    }
    
    .register-footer a {
        color: #6366f1;
        text-decoration: none;
        font-weight: 600;
    }
    
    .register-footer a:hover {
        text-decoration: underline;
    }
    
    .password-requirements {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        color: #92400e;
        padding: 0.8rem 1rem;
        border-radius: 8px;
        border: 1px solid #fbbf24;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
    
    .password-requirements ul {
        margin: 0.5rem 0 0 1rem;
        padding: 0;
    }
    
    .password-requirements li {
        margin: 0.2rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Registration form
    st.markdown("""
    <div class="register-container">
        <div class="register-header">
            <h1>📝 Create Account</h1>
            <p>Join Reflexta Analytics Platform</p>
        </div>
        <div class="register-form">
    """, unsafe_allow_html=True)
    
    # Password requirements
    st.markdown("""
    <div class="password-requirements">
        <strong>Password Requirements:</strong>
        <ul>
            <li>At least 8 characters long</li>
            <li>Contains uppercase and lowercase letters</li>
            <li>Contains at least one number</li>
            <li>Contains at least one special character</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Registration form fields
    with st.form("register_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        
        with col1:
            first_name = st.text_input(
                "First Name",
                placeholder="Enter your first name",
                key="register_first_name"
            )
        
        with col2:
            last_name = st.text_input(
                "Last Name",
                placeholder="Enter your last name",
                key="register_last_name"
            )
        
        username = st.text_input(
            "Username",
            placeholder="Choose a username",
            key="register_username"
        )
        
        email = st.text_input(
            "Email",
            placeholder="Enter your email address",
            key="register_email"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Create a password",
                key="register_password"
            )
        
        with col2:
            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                placeholder="Confirm your password",
                key="register_confirm_password"
            )
        
        role = st.selectbox(
            "Role",
            ["user", "manager", "admin"],
            key="register_role",
            help="Select your role. Admin roles require approval."
        )
        
        terms_accepted = st.checkbox(
            "I agree to the Terms of Service and Privacy Policy",
            key="terms_accepted"
        )
        
        register_submitted = st.form_submit_button(
            "🚀 Create Account",
            use_container_width=True,
            type="primary"
        )
        
        if register_submitted:
            if all([first_name, last_name, username, email, password, confirm_password]):
                if password != confirm_password:
                    st.error("❌ Passwords do not match.")
                elif not terms_accepted:
                    st.error("❌ Please accept the terms and conditions.")
                else:
                    # Validate password strength
                    if len(password) < 8:
                        st.error("❌ Password must be at least 8 characters long.")
                    else:
                        auth = UserAuth()
                        result = auth.create_user(username, email, password, role)
                        
                        if result['success']:
                            st.success("✅ Account created successfully! You can now log in.")
                            st.info("💡 Your account is pending approval. Contact your administrator for access.")
                        else:
                            st.error(f"❌ {result['message']}")
            else:
                st.error("❌ Please fill in all fields.")
    
    st.markdown("""
        </div>
        <div class="register-footer">
            <p>Already have an account? <a href="#" onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'show_login', value: true}, '*')">Sign in here</a></p>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_user_profile() -> None:
    """Render user profile and settings."""
    
    auth = UserAuth()
    user_data = auth.get_current_user()
    
    if not user_data:
        st.error("🔒 Please log in to view your profile.")
        return
    
    st.markdown("## 👤 User Profile")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.markdown("### Profile Information")
        
        # Display user information
        st.markdown(f"**Username:** {user_data['username']}")
        st.markdown(f"**Email:** {user_data['email']}")
        st.markdown(f"**Role:** {user_data['role'].title()}")
        st.markdown(f"**Login Time:** {user_data['login_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        # User permissions
        permissions = auth.get_user_permissions()
        st.markdown("### Permissions")
        for permission in permissions:
            st.markdown(f"✅ {permission.replace('_', ' ').title()}")
    
    with col2:
        st.markdown("### Account Settings")
        
        # Change password
        with st.expander("🔐 Change Password", expanded=False):
            with st.form("change_password_form"):
                current_password = st.text_input(
                    "Current Password",
                    type="password",
                    key="current_password"
                )
                
                new_password = st.text_input(
                    "New Password",
                    type="password",
                    key="new_password"
                )
                
                confirm_new_password = st.text_input(
                    "Confirm New Password",
                    type="password",
                    key="confirm_new_password"
                )
                
                if st.form_submit_button("Update Password"):
                    if new_password == confirm_new_password:
                        st.success("✅ Password updated successfully!")
                    else:
                        st.error("❌ Passwords do not match.")
        
        # Session information
        with st.expander("📊 Session Information", expanded=False):
            st.markdown(f"**Session Start:** {user_data['login_time'].strftime('%Y-%m-%d %H:%M:%S')}")
            st.markdown(f"**Last Activity:** {user_data['last_activity'].strftime('%Y-%m-%d %H:%M:%S')}")
            st.markdown(f"**Session Timeout:** 24 hours")
            
            if st.button("🔄 Refresh Session"):
                auth.update_activity()
                st.success("✅ Session refreshed!")
                st.rerun()
        
        # Logout
        if st.button("🚪 Logout", type="secondary"):
            auth.logout_user()
            st.success("✅ Logged out successfully!")
            st.rerun()


def render_auth_guard() -> None:
    """Render authentication guard for protected routes."""
    
    auth = UserAuth()
    
    # Check if user is authenticated
    if not auth.is_authenticated():
        st.markdown("""
        <div style="text-align: center; padding: 4rem 2rem;">
            <h1 style="color: #1e293b; margin-bottom: 1rem;">🔒 Authentication Required</h1>
            <p style="color: #64748b; font-size: 1.1rem; margin-bottom: 2rem;">
                Please log in to access the Reflexta Analytics Platform.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Show login form
        render_login_form()
        return False
    
    # Check session timeout
    if auth.check_session_timeout():
        st.error("⏰ Session expired. Please log in again.")
        auth.logout_user()
        return False
    
    # Update activity
    auth.update_activity()
    
    return True


def render_auth_navbar() -> None:
    """Render authentication navbar with user info and logout."""
    
    auth = UserAuth()
    
    if auth.is_authenticated():
        user_data = auth.get_current_user()
        
        # Create navbar
        st.markdown("""
        <style>
        .auth-navbar {
            background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 25%, #16213e 50%, #0f3460 75%, #533483 100%);
            padding: 1rem 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            color: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.3);
        }
        
        .auth-navbar-left {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .auth-navbar-right {
            display: flex;
            align-items: center;
            gap: 1rem;
        }
        
        .user-info {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
        }
        
        .user-name {
            font-weight: 600;
            font-size: 1rem;
        }
        
        .user-role {
            font-size: 0.8rem;
            opacity: 0.8;
        }
        
        .logout-btn {
            background: rgba(255, 255, 255, 0.2);
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-decoration: none;
        }
        
        .logout-btn:hover {
            background: rgba(255, 255, 255, 0.3);
            transform: translateY(-1px);
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div class="auth-navbar">
            <div class="auth-navbar-left">
                <h2 style="margin: 0; font-size: 1.5rem;">📊 Reflexta Analytics Platform</h2>
            </div>
            <div class="auth-navbar-right">
                <div class="user-info">
                    <div class="user-name">👤 {user_data['username']}</div>
                    <div class="user-role">{user_data['role'].title()}</div>
                </div>
                <a href="#" onclick="window.parent.postMessage({{type: 'streamlit:setComponentValue', key: 'logout', value: true}}, '*')" class="logout-btn">
                    🚪 Logout
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Handle logout
        if st.session_state.get('logout'):
            auth.logout_user()
            st.success("✅ Logged out successfully!")
            st.rerun()
