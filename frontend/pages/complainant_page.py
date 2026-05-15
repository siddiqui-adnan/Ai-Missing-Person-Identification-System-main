"""
Complainant page for viewing cases (no login required)
"""
import streamlit as st
from datetime import datetime

from frontend.components.styles import get_main_app_styles
from frontend.components.utils import format_time_12h
from config import Config
from backend.database import db_queries
from backend.utils.error_handler import log_user_action

def render_complainant_page():
    """Main complainant page renderer"""
    # Apply styles
    st.markdown(get_main_app_styles(), unsafe_allow_html=True)
    
    # Render sidebar
    render_complainant_sidebar()
    
    # Main content - Professional header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); 
                padding: 2rem; border-radius: 12px; margin-bottom: 2rem; 
                box-shadow: 0 4px 16px rgba(0,0,0,0.1);'>
        <h1 style='color: white; margin: 0; font-size: 2.5rem;'>👨‍👩‍👧‍👦 Missing Person Cases</h1>
        <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;'>
            Browse all registered missing person cases
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.info("📋 Browse all registered missing person cases. No login required.")
    
    # View all cases
    render_all_cases_view()


def render_complainant_sidebar():
    """Render complainant sidebar"""
    with st.sidebar:
        # Professional header
        st.markdown("""
        <div style='background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); 
                    padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem;'>👋 Welcome, Citizen</h3>
            <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
                Public Viewer
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # User information - Clean layout
        st.markdown("#### 📋 Access Information")
        st.markdown(f"""
        <div style='background: #f5f7fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
            <p style='margin: 0.5rem 0; font-size: 0.9rem;'><strong>Role:</strong> Public Viewer</p>
            <p style='margin: 0.5rem 0; font-size: 0.9rem;'><strong>Access:</strong> Read-Only</p>
            <p style='margin: 0.5rem 0; font-size: 0.9rem;'><strong>Status:</strong> ✅ Active</p>
            <p style='margin: 0.5rem 0; font-size: 0.9rem;'><strong>Version:</strong> {Config.APP_VERSION}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Back to login button
        if st.button("🚪 Back to Login", use_container_width=True, type="secondary"):
            log_user_action("Logout", st.session_state.get("username"))
            st.session_state["authentication_status"] = False
            st.session_state["user_role"] = None
            st.session_state.clear()
            st.rerun()


def render_all_cases_view():
    """Render all cases view for complainants"""
    try:
        # Get all registered cases and public submissions
        all_registered_cases = db_queries.get_all_registered_cases()
        all_public_submissions = db_queries.fetch_public_cases(train_data=False, status="All")
        
        # Filter options - Professional layout
        st.markdown("### 🔍 Filter & Search")
        col1, col2 = st.columns(2)
        with col1:
            status_filter = st.selectbox(
                "Filter by Status",
                ["All", "Not Found", "Found"]
            )
        
        with col2:
            search_term = st.text_input("🔍 Search by name or location", "")
        
        st.markdown("---")
        
        # Filter registered cases
        filtered_registered = all_registered_cases
        if status_filter == "Not Found":
            filtered_registered = [c for c in all_registered_cases if c.status == "NF"]
        elif status_filter == "Found":
            filtered_registered = [c for c in all_registered_cases if c.status == "F"]
        
        if search_term:
            filtered_registered = [
                c for c in filtered_registered 
                if search_term.lower() in c.name.lower() 
                or (c.city and search_term.lower() in c.city.lower())
                or (c.address and search_term.lower() in c.address.lower())
            ]
        
        # Filter public submissions
        filtered_public = all_public_submissions
        if status_filter == "Not Found":
            filtered_public = [c for c in all_public_submissions if c.status == "NF"]
        elif status_filter == "Found":
            filtered_public = [c for c in all_public_submissions if c.status == "F"]
        
        if search_term:
            filtered_public = [
                c for c in filtered_public 
                if (hasattr(c, 'name') and c.name and search_term.lower() in c.name.lower())
                or (c.location and search_term.lower() in c.location.lower())
                or (hasattr(c, 'city') and c.city and search_term.lower() in c.city.lower())
            ]
        
        # Statistics - Professional cards
        total_cases = len(filtered_registered) + len(filtered_public)
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); 
                    padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <p style='color: white; margin: 0; font-size: 1.1rem;'>
                📊 Showing <strong>{total_cases}</strong> cases 
                (<strong>{len(filtered_registered)}</strong> Admin + <strong>{len(filtered_public)}</strong> Public)
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # ========================================
        # SECTION 1: ADMIN REGISTERED CASES
        # ========================================
        st.markdown(f"## 🏢 Admin Registered Cases ({len(filtered_registered)})")
        st.info("These are official missing person cases registered by law enforcement.")
        
        if not filtered_registered:
            st.info("📭 No admin registered cases match your criteria.")
        else:
            for case in filtered_registered:
                # Status indicator
                if case.status == "NF":
                    status_color = "🔴"
                    status_text = "NOT FOUND"
                else:
                    status_color = "🟢"
                    status_text = "FOUND"
                
                with st.expander(f"{status_color} {case.name} - {case.city or 'Unknown City'} ({status_text})", expanded=False):
                    # Three-column layout: Photo (left), Personal/Location (middle), Contact/Marks/Case Info (right)
                    col_photo, col_middle, col_right = st.columns([1, 2, 2])
                    
                    with col_photo:
                        try:
                            st.image(
                                f"./resources/{case.id}.jpg",
                                width=250,
                                caption=case.name,
                                use_container_width=True,
                            )
                        except Exception:
                            st.warning("📷 Image not available")
                    
                    with col_middle:
                        st.markdown("### 👤 Personal Information")
                        st.write(f"**Name:** {case.name}")
                        st.write(f"**Father's Name:** {case.father_name or 'Not provided'}")
                        st.write(f"**Age:** {case.age or 'Unknown'}")
                        
                        st.markdown("### 📍 Location Information")
                        st.write(f"**Last Seen:** {case.last_seen}")
                        st.write(f"**City:** {case.city or 'Not provided'}")
                        st.write(f"**State:** {case.state or 'Not provided'}")
                        st.write(f"**Address:** {case.address or 'Not provided'}")
                    
                    with col_right:
                        st.markdown("### 📞 Contact Information")
                        st.write(f"**Complainant:** {case.complainant_name or 'Not provided'}")
                        st.write(f"**Mobile:** {case.complainant_mobile or 'Not provided'}")
                        st.write(f"**Email:** {case.complainant_email or 'Not provided'}")
                        
                        if case.birth_marks:
                            st.markdown("### 🔍 Identifying Marks")
                            st.write(case.birth_marks)
                        
                        st.markdown("### 📅 Case Information")
                        st.write(f"**Registered On:** {format_time_12h(case.submitted_on) if case.submitted_on else 'Unknown'}")
                        st.write(f"**Status:** {status_text}")
                    
                    # Description at the bottom (full width) if available
                    if case.description:
                        st.markdown("---")
                        st.markdown("### 📝 Description")
                        st.write(case.description)
                    
                    # Found status message at the bottom
                    if case.status == "F" and case.matched_with:
                        st.markdown("---")
                        st.success(f"✅ This person has been found! (Matched with: {case.matched_with})")
        
        st.markdown("---")
        
        # ========================================
        # SECTION 2: PUBLIC SUBMISSIONS
        # ========================================
        st.markdown(f"## 👥 Public Submission Cases ({len(filtered_public)})")
        st.info("These are sightings reported by members of the public.")
        
        if not filtered_public:
            st.info("📭 No public submissions match your criteria.")
        else:
            for case in filtered_public:
                # Status indicator
                if case.status == "NF":
                    status_color = "🔴"
                    status_text = "NOT FOUND"
                else:
                    status_color = "🟢"
                    status_text = "FOUND"
                
                # Get name or location for title
                case_name = case.name if (hasattr(case, 'name') and case.name) else 'Unknown Person'
                case_location = case.location or 'Unknown Location'
                
                with st.expander(f"{status_color} {case_name} - {case_location} ({status_text})", expanded=False):
                    # Three-column layout: Photo (left), Personal/Location (middle), Contact/Marks/Case Info (right)
                    col_photo, col_middle, col_right = st.columns([1, 2, 2])
                    
                    with col_photo:
                        try:
                            st.image(
                                f"./resources/{case.id}.jpg",
                                width=250,
                                caption=case_name,
                                use_container_width=True,
                            )
                        except Exception:
                            st.warning("📷 Image not available")
                    
                    with col_middle:
                        st.markdown("### 👤 Person Information")
                        if hasattr(case, 'name') and case.name:
                            st.write(f"**Name:** {case.name}")
                        else:
                            st.write(f"**Name:** Unknown")
                        
                        st.markdown("### 📍 Sighting Information")
                        st.write(f"**Location Sighted:** {case.location}")
                        if hasattr(case, 'city') and case.city:
                            st.write(f"**City:** {case.city}")
                        if hasattr(case, 'state') and case.state:
                            st.write(f"**State:** {case.state}")
                    
                    with col_right:
                        st.markdown("### 📞 Submitted By")
                        st.write(f"**Name:** {case.submitted_by or 'Anonymous'}")
                        st.write(f"**Mobile:** {case.mobile}")
                        if hasattr(case, 'email') and case.email:
                            st.write(f"**Email:** {case.email}")
                        
                        if hasattr(case, 'birth_marks') and case.birth_marks:
                            st.markdown("### 🔍 Description/Remarks")
                            st.write(case.birth_marks)
                        
                        st.markdown("### 📅 Submission Information")
                        if hasattr(case, 'submitted_on') and case.submitted_on:
                            st.write(f"**Submitted On:** {format_time_12h(case.submitted_on)}")
                        st.write(f"**Status:** {status_text}")
                    
                    # Found status message at the bottom
                    if case.status == "F":
                        st.markdown("---")
                        st.success(f"✅ This sighting has been verified and matched!")
        
        if not filtered_registered and not filtered_public:
            st.info("🔍 No cases match your search criteria.")
    
    except Exception as e:
        st.error(f"❌ Error loading cases: {str(e)}")
        st.info("Please try refreshing the page or contact support.")
