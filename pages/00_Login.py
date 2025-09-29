#!/usr/bin/env python3
"""
Login Page for Reflexta Analytics Platform
Secure user authentication and session management.
"""

import streamlit as st
from datetime import datetime
from src.auth import get_auth_manager, is_authenticated, get_current_user


def render_login_page():
    """Render the login page with professional styling."""
    
    # Page configuration
    st.set_page_config(
        page_title="Login - Reflexta Analytics",
        page_icon="🔐",
        layout="centered",
        initial_sidebar_state="collapsed"
    )
    
    # Professional login CSS
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 20px;
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
        margin-bottom: 0.5rem;
    }
    
    .login-header p {
        color: #64748b;
        font-size: 1rem;
        margin: 0;
    }
    
    .login-form {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid rgba(148, 163, 184, 0.1);
    }
    
    .form-group {
        margin-bottom: 1.5rem;
    }
    
    .form-label {
        display: block;
        color: #374151;
        font-weight: 600;
        margin-bottom: 0.5rem;
        font-size: 0.9rem;
    }
    
    .form-input {
        width: 100%;
        padding: 0.75rem 1rem;
        border: 2px solid #e5e7eb;
        border-radius: 8px;
        font-size: 1rem;
        transition: all 0.3s ease;
        background: #f9fafb;
    }
    
    .form-input:focus {
        outline: none;
        border-color: #6366f1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
        background: white;
    }
    
    .login-button {
        width: 100%;
        padding: 0.75rem 1rem;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border: none;
        border-radius: 8px;
        font-size: 1rem;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        margin-top: 1rem;
    }
    
    .login-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
    }
    
    .demo-credentials {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border: 1px solid rgba(251, 191, 36, 0.3);
        border-radius: 8px;
        padding: 1rem;
        margin-top: 1.5rem;
    }
    
    .demo-credentials h4 {
        color: #92400e;
        margin: 0 0 0.5rem 0;
        font-size: 0.9rem;
    }
    
    .demo-credentials p {
        color: #92400e;
        margin: 0;
        font-size: 0.8rem;
    }
    
    .error-message {
        background: #fef2f2;
        border: 1px solid #fecaca;
        color: #dc2626;
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
    
    .success-message {
        background: #f0fdf4;
        border: 1px solid #bbf7d0;
        color: #16a34a;
        padding: 0.75rem;
        border-radius: 8px;
        margin-bottom: 1rem;
        font-size: 0.9rem;
    }
    
    .company-footer {
        text-align: center;
        margin-top: 2rem;
        padding-top: 1rem;
        border-top: 1px solid rgba(148, 163, 184, 0.2);
    }
    
    .company-footer h3 {
        color: #1e293b;
        font-size: 1.2rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
    }
    
    .company-footer p {
        color: #64748b;
        font-size: 0.9rem;
        margin: 0;
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
    
    .stApp[data-theme="dark"] .login-form {
        background: #1e293b;
        border: 1px solid rgba(148, 163, 184, 0.3);
    }
    
    .stApp[data-theme="dark"] .form-label {
        color: #f1f5f9;
    }
    
    .stApp[data-theme="dark"] .form-input {
        background: #334155;
        border: 2px solid rgba(148, 163, 184, 0.3);
        color: #f1f5f9;
    }
    
    .stApp[data-theme="dark"] .form-input:focus {
        background: #475569;
        border-color: #6366f1;
    }
    
    .stApp[data-theme="dark"] .company-footer h3 {
        color: #f1f5f9;
    }
    
    .stApp[data-theme="dark"] .company-footer p {
        color: #94a3b8;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Check if user is already authenticated
    if is_authenticated():
        st.success("✅ You are already logged in!")
        st.info("Navigate to the main dashboard to continue.")
        
        if st.button("🏠 Go to Dashboard", use_container_width=True):
            st.switch_page("app.py")
        
        return
    
    # Login form
    st.markdown("""
    <div class="login-container">
        <div class="login-header">
            <h1>🔐 Welcome Back</h1>
            <p>Sign in to Reflexta Analytics Platform</p>
        </div>
        
        <div class="login-form">
    """, unsafe_allow_html=True)
    
    # Initialize auth manager
    auth_manager = get_auth_manager()
    
    # Login form
    with st.form("login_form", clear_on_submit=False):
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        username = st.text_input(
            "Username",
            placeholder="Enter your username",
            key="login_username"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="form-group">', unsafe_allow_html=True)
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            key="login_password"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            login_clicked = st.form_submit_button(
                "🔐 Sign In",
                use_container_width=True,
                type="primary"
            )
        
        with col2:
            if st.form_submit_button("🔄 Clear", use_container_width=True):
                st.rerun()
    
    # Handle login
    if login_clicked:
        if not username or not password:
            st.error("❌ Please enter both username and password.")
        else:
            with st.spinner("🔐 Authenticating..."):
                user_data = auth_manager.authenticate_user(username, password)
                
                if user_data:
                    # Store user data in session state
                    st.session_state['user_data'] = user_data
                    st.session_state['session_id'] = user_data.get('session_id')
                    st.session_state['authenticated'] = True
                    
                    st.success(f"✅ Welcome back, {user_data['first_name']}!")
                    st.info(f"Role: {user_data['role_name']} | Department: {user_data.get('department_name', 'N/A')}")
                    
                    # Redirect to main app
                    st.markdown("""
                    <script>
                    setTimeout(function() {
                        window.location.href = '/';
                    }, 2000);
                    </script>
                    """, unsafe_allow_html=True)
                    
                else:
                    st.error("❌ Invalid username or password. Please try again.")
    
    # Demo credentials
    st.markdown("""
    <div class="demo-credentials">
        <h4>🎯 Demo Credentials</h4>
        <p><strong>Admin:</strong> username: admin, password: admin123</p>
        <p><strong>Demo User:</strong> username: demo, password: admin123</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Company footer
    st.markdown("""
    <div class="company-footer">
        <h3>Reflexta Data Intelligence</h3>
        <p>Enterprise Analytics Platform • Secure Authentication • Professional Access Control</p>
    </div>
    """, unsafe_allow_html=True)


def render_logout_page():
    """Render logout confirmation page."""
    
    st.markdown("## 🔐 Logout Confirmation")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("✅ Yes, Logout", use_container_width=True, type="primary"):
            # Get auth manager
            auth_manager = get_auth_manager()
            
            # Logout user
            session_id = st.session_state.get('session_id')
            if session_id:
                auth_manager.logout_user(session_id)
            
            # Clear session state
            st.session_state.clear()
            
            st.success("✅ Successfully logged out!")
            st.info("You have been logged out of the system.")
            
            # Redirect to login
            st.markdown("""
            <script>
            setTimeout(function() {
                window.location.href = '/Login';
            }, 2000);
            </script>
            """, unsafe_allow_html=True)
    
    with col2:
        if st.button("❌ Cancel", use_container_width=True):
            st.switch_page("app.py")


# Main execution
if __name__ == "__main__":
    render_login_page()
