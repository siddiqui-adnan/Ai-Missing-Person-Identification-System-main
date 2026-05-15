"""
AI Missing Person Identification System
Version 1.0.0 - Public Web Application
Entry Point - Refactored Architecture

This is the main entry point that routes to appropriate pages based on authentication status.
All business logic has been moved to backend services.
All UI components have been moved to frontend pages and components.
"""

import streamlit as st
import sys
from pathlib import Path

# Configure Streamlit page FIRST (must be the first Streamlit command)
st.set_page_config(
    page_title="AI Missing Person Identification System",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': """
        # AI Missing Person Identification System
        
        A comprehensive web application for missing person identification using AI-powered face recognition.
        
        **Features:**
        - Face recognition matching
        - Public submission portal
        - Admin management system
        - Real-time case tracking
        - Email notifications
        - Interactive maps
        
        **Version:** 1.0.0
        **Status:** Running Locally
        """
    }
)

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Add project root to path
sys.path.append(str(Path(__file__).parent))

# Import configuration
from config import Config

# Initialize database
from backend.database import db_queries

@st.cache_resource
def init_database():
    """Initialize database tables"""
    db_queries.create_db()
    return True

init_database()

# Initialize session state
if "login_status" not in st.session_state:
    from datetime import datetime
    st.session_state.update({
        "login_status": False,
        "user_role": None,
        "login_attempts": 0,
        "last_activity": datetime.now()
    })

# Route to appropriate page based on authentication status
if not st.session_state.get("authentication_status"):
    # Show login page
    from frontend.pages.login_page import render_login_page
    render_login_page()
    
elif st.session_state.get("authentication_status"):
    user_role = st.session_state.get("user_role")
    
    if user_role == "Admin":
        # Show admin dashboard
        from frontend.pages.admin_page import render_admin_page
        render_admin_page()
        
    elif user_role == "Public":
        # Show public submission page
        from frontend.pages.public_page import render_public_page
        render_public_page()
        
    elif user_role == "Complainant":
        # Show complainant view page
        from frontend.pages.complainant_page import render_complainant_page
        render_complainant_page()

# Add footer for public deployment - only on entrance page (not authenticated, not on login forms)
if not st.session_state.get("authentication_status", False) and not st.session_state.get("show_admin_form", False) and not st.session_state.get("show_public_form", False) and not st.session_state.get("show_complainant_form", False):
    st.markdown("---")
    st.markdown("""
<div style='text-align: center; padding: 25px; background: linear-gradient(135deg, rgba(102, 126, 234, 0.85) 0%, rgba(118, 75, 162, 0.85) 100%); border-radius: 15px; margin-top: 30px; backdrop-filter: blur(10px); box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2); border: 1px solid rgba(255, 255, 255, 0.2);'>
    <h4 style='color: white; margin: 0; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>🔍 AI Missing Person Identification System</h4>
    <p style='color: rgba(255,255,255,0.95); margin: 10px 0 0 0; font-size: 14px;'>Deployed on Streamlit Cloud | Version 1.0.0 | Reuniting Families Through Technology</p>
    <p style='color: rgba(255,255,255,0.9); margin: 5px 0 0 0; font-size: 12px;'>🌐 Publicly Accessible | 🔒 Secure | 📱 Mobile Responsive</p>
    <hr style='border: none; border-top: 1px solid rgba(255,255,255,0.4); margin: 20px 0;'>
    <h4 style='color: white; margin: 0 0 10px 0; font-size: 16px; text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);'>📞 Contact & Support</h4>
    <p style='color: rgba(255,255,255,0.95); margin: 0 0 15px 0; font-size: 13px;'>Need help? Get in touch with us</p>
    <div style='display: flex; justify-content: center; align-items: center; gap: 30px; flex-wrap: wrap; margin: 0 auto;'>
        <p style='color: rgba(255,255,255,0.98); margin: 8px 0; font-size: 13px; text-align: center;'><strong><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="vertical-align: middle; margin-right: 4px;"><path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline></svg> Email:</strong> <a href='mailto:missingpersonidentificationsys@gmail.com' style='color: white; text-decoration: none; font-weight: 500; transition: all 0.3s ease;'>missingpersonidentificationsys@gmail.com</a></p>
        <p style='color: rgba(255,255,255,0.98); margin: 8px 0; font-size: 13px; text-align: center;'><strong><svg xmlns="http://www.w3.org/2000/svg" width="14" height="14" viewBox="0 0 24 24" fill="white" style="vertical-align: middle; margin-right: 4px;"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg> Instagram:</strong> <a href='https://www.instagram.com/ai_mpis/' target='_blank' style='color: white; text-decoration: none; font-weight: 500; transition: all 0.3s ease;'>@ai_mpis</a></p>
    </div>
    <p style='color: rgba(255,255,255,0.8); font-size: 11px; margin: 15px 0 0 0;'>We're here to help you reunite families. Feel free to reach out for any questions or support.</p>
</div>
""", unsafe_allow_html=True)