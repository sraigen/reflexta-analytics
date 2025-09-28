from __future__ import annotations

import streamlit as st
from src.db_analysis import analyze_database, get_table_info, get_table_sample
from src.db import health_check

st.set_page_config(page_title="Database Analysis", layout="wide")

# Professional header with company branding
try:
    import base64
    with open("logo.png", "rb") as logo_file:
        logo_base64 = base64.b64encode(logo_file.read()).decode()
    
    st.markdown(f"""
    <div class="main-header">
        <div style="display: flex; align-items: center; justify-content: center; margin-bottom: 1rem;">
            <img src="data:image/png;base64,{logo_base64}" alt="Reflexta Data Intelligence" class="company-logo" style="height: 60px; margin-right: 25px; vertical-align: middle;">
            <div style="text-align: left;">
                <h1 style="margin: 0; font-size: 2.2rem; font-weight: 700; line-height: 1.2;">Database Analysis</h1>
                <p style="margin: 0.3rem 0 0 0; font-size: 1.1rem; opacity: 0.9; font-weight: 300;">Reflexta Data Intelligence</p>
            </div>
        </div>
        <p style="margin: 0; text-align: center; font-size: 1rem; opacity: 0.9;">Explore your database structure and data</p>
    </div>
    """, unsafe_allow_html=True)
except FileNotFoundError:
    st.markdown("""
    <div class="main-header">
        <h1>Database Analysis</h1>
        <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9; font-weight: 300;">Reflexta Data Intelligence</p>
        <p>Explore your database structure and data</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar with company logo
with st.sidebar:
    # Company logo in sidebar
    try:
        with open("logo.png", "rb") as logo_file:
            logo_base64 = base64.b64encode(logo_file.read()).decode()
        
        st.markdown(f"""
        <div class="sidebar-logo">
            <img src="data:image/png;base64,{logo_base64}" alt="Reflexta Data Intelligence" style="height: 40px; margin-bottom: 0.5rem;">
            <h3>Reflexta Data Intelligence</h3>
            <p>Database Analysis</p>
        </div>
        """, unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown("""
        <div class="sidebar-logo">
            <h3>Reflexta Data Intelligence</h3>
            <p>Database Analysis</p>
        </div>
        """, unsafe_allow_html=True)

if not health_check():
    st.error("❌ Database connection failed. Please check your connection settings.")
    st.stop()

# Analyze database
with st.spinner("Analyzing database structure..."):
    analysis = analyze_database()

if "error" in analysis:
    st.error(f"❌ Analysis failed: {analysis['error']}")
    st.stop()

# Database Overview
st.markdown('<div class="section-header">📊 Database Overview</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Tables", analysis["table_count"])
with col2:
    st.metric("Views", analysis["view_count"])
with col3:
    st.metric("Total Objects", analysis["table_count"] + analysis["view_count"])
with col4:
    st.metric("Status", "✅ Connected")

# Tables Section
st.markdown('<div class="section-header">📋 Tables</div>', unsafe_allow_html=True)

if not analysis["tables"].empty:
    st.dataframe(analysis["tables"], use_container_width=True, hide_index=True)
    
    # Table details
    selected_table = st.selectbox("Select a table to analyze:", analysis["tables"]["tablename"].tolist())
    
    if selected_table:
        st.markdown(f"#### 📊 Analyzing: {selected_table}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Table info
            info = get_table_info(selected_table)
            if "error" not in info:
                st.metric("Row Count", f"{info['row_count']:,}")
                st.dataframe(info["columns"], use_container_width=True, hide_index=True)
        
        with col2:
            # Sample data
            st.markdown("**Sample Data:**")
            sample = get_table_sample(selected_table, 10)
            if not sample.empty:
                st.dataframe(sample, use_container_width=True, hide_index=True)
            else:
                st.info("No data available or table is empty")
else:
    st.info("No tables found in the database.")

# Views Section
st.markdown('<div class="section-header">👁️ Views</div>', unsafe_allow_html=True)

if not analysis["views"].empty:
    st.dataframe(analysis["views"], use_container_width=True, hide_index=True)
else:
    st.info("No views found in the database.")

# Recommendations
st.markdown('<div class="section-header">💡 Recommendations</div>', unsafe_allow_html=True)

if analysis["table_count"] == 0:
    st.warning("⚠️ No tables found. Consider creating sample data or importing your existing data.")
    st.info("💡 **Next Steps:**\n1. Create Finance and Procurement tables\n2. Import sample data\n3. Set up views for analytics")
else:
    st.success("✅ Database structure detected. Ready for dashboard development!")
    st.info("💡 **Available for Dashboard Development:**\n1. Finance module dashboards\n2. Procurement analytics\n3. Cross-module insights")
