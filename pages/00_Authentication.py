#!/usr/bin/env python3
"""
Authentication Page for Reflexta Analytics Platform
Login, registration, and user management interface.
"""

from __future__ import annotations

import streamlit as st
from src.auth import UserAuth, create_users_table
from src.auth_ui import render_login_form, render_registration_form, render_user_profile


# Page configuration
st.set_page_config(
    page_title="Authentication - Reflexta Analytics",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize authentication
auth = UserAuth()
create_users_table()

# Professional CSS for authentication page
st.markdown("""
<style>
    .auth-page-container {
        min-height: 100vh;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f6 100%);
        padding: 2rem;
    }
    
    .auth-page-header {
        text-align: center;
        margin-bottom: 3rem;
    }
    
    .auth-page-header h1 {
        color: #1e293b;
        font-size: 3rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    .auth-page-header p {
        color: #64748b;
        font-size: 1.2rem;
        margin: 1rem 0 0 0;
    }
    
    .auth-tabs {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }
    
    .auth-tab {
        background: white;
        border: 2px solid #e2e8f6;
        padding: 1rem 2rem;
        border-radius: 12px 12px 0 0;
        cursor: pointer;
        transition: all 0.3s ease;
        font-weight: 600;
        color: #64748b;
    }
    
    .auth-tab.active {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white;
        border-color: #6366f1;
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
    }
    
    .auth-tab:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    }
    
    .auth-content {
        background: white;
        border-radius: 0 12px 12px 12px;
        padding: 2rem;
        box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
        border: 2px solid #e2e8f6;
        border-top: none;
    }
    
    /* Dark mode compatibility */
    .stApp[data-theme="dark"] .auth-page-container {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
    }
    
    .stApp[data-theme="dark"] .auth-page-header h1 {
        color: #f1f5f9;
    }
    
    .stApp[data-theme="dark"] .auth-page-header p {
        color: #94a3b8;
    }
    
    .stApp[data-theme="dark"] .auth-tab {
        background: #334155;
        border: 2px solid rgba(148, 163, 184, 0.3);
        color: #f1f5f9;
    }
    
    .stApp[data-theme="dark"] .auth-content {
        background: #1e293b;
        border: 2px solid rgba(148, 163, 184, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for auth tabs
if 'auth_tab' not in st.session_state:
    st.session_state.auth_tab = 'login'

# Check if user is already authenticated
if auth.is_authenticated():
    st.markdown("""
    <div class="auth-page-container">
        <div class="auth-page-header">
            <h1>🔐 Authentication</h1>
            <p>User Management and Account Settings</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show user profile
    render_user_profile()
    
    # Add logout button
    if st.button("🚪 Logout", type="secondary"):
        auth.logout_user()
        st.success("✅ Logged out successfully!")
        st.rerun()
else:
    # Show authentication page
    st.markdown("""
    <div class="auth-page-container">
        <div class="auth-page-header">
            <h1>🔐 Welcome to Reflexta Analytics</h1>
            <p>Enterprise-Grade Business Intelligence Platform</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Create tab navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        <div class="auth-tabs">
            <div class="auth-tab active" onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'auth_tab', value: 'login'}, '*')">
                🔐 Sign In
            </div>
            <div class="auth-tab" onclick="window.parent.postMessage({type: 'streamlit:setComponentValue', key: 'auth_tab', value: 'register'}, '*')">
                📝 Sign Up
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Handle tab switching
    if st.session_state.get('auth_tab') == 'login':
        st.markdown("""
        <div class="auth-content">
        """, unsafe_allow_html=True)
        
        render_login_form()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    elif st.session_state.get('auth_tab') == 'register':
        st.markdown("""
        <div class="auth-content">
        """, unsafe_allow_html=True)
        
        render_registration_form()
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Handle tab switching via JavaScript
    st.markdown("""
    <script>
    // Handle tab switching
    document.addEventListener('DOMContentLoaded', function() {
        const tabs = document.querySelectorAll('.auth-tab');
        tabs.forEach(tab => {
            tab.addEventListener('click', function() {
                // Remove active class from all tabs
                tabs.forEach(t => t.classList.remove('active'));
                // Add active class to clicked tab
                this.classList.add('active');
            });
        });
    });
    </script>
    """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #666;">
    <h3>Reflexta Data Intelligence</h3>
    <p>Empowering businesses with intelligent data analytics and insights</p>
    <p style="margin-top: 0.5rem; font-size: 0.8rem; opacity: 0.7;">
        Enterprise Analytics Platform • Real-time Business Intelligence • Advanced Data Visualization
    </p>
</div>
""", unsafe_allow_html=True)
