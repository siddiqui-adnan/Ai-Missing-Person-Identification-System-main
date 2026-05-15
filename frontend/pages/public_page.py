"""
Public user page for reporting sightings
"""
import streamlit as st
from datetime import datetime

from frontend.components.styles import get_main_app_styles
from frontend.components.utils import format_time_12h
from config import Config
from backend.database import db_queries
from backend.utils.error_handler import log_user_action, check_session_timeout

def render_public_page():
    """Main public page renderer"""
    # Apply styles
    st.markdown(get_main_app_styles(), unsafe_allow_html=True)
    
    # Check session timeout
    try:
        if not check_session_timeout():
            st.error("⏰ Your session has expired. Please login again.")
            st.session_state.clear()
            st.rerun()
    except:
        pass  # If check_session_timeout not available
    
    # Render sidebar
    render_public_sidebar()
    
    # Main content - Professional header
    st.markdown("""
    <div style='background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); 
                padding: 2rem; border-radius: 12px; margin-bottom: 2rem; 
                box-shadow: 0 4px 16px rgba(0,0,0,0.1);'>
        <h1 style='color: white; margin: 0; font-size: 2.5rem;'>📝 Report a Sighting</h1>
        <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 1.1rem;'>
            Help us find missing persons by reporting sightings
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Report sighting form
    render_report_form()
    
    # Recent submissions
    st.markdown("---")
    st.markdown("""
    <div style='background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%); 
                padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
        <h3 style='color: white; margin: 0; font-size: 1.5rem;'>📊 Your Recent Submissions</h3>
    </div>
    """, unsafe_allow_html=True)
    render_recent_submissions()


def render_public_sidebar():
    """Render public user sidebar"""
    with st.sidebar:
        # Professional header
        st.markdown("""
        <div style='background: linear-gradient(135deg, #3498db 0%, #2980b9 100%); 
                    padding: 1.5rem; border-radius: 8px; margin-bottom: 1.5rem;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
            <h3 style='color: white; margin: 0; font-size: 1.3rem;'>👋 Welcome, Citizen</h3>
            <p style='color: rgba(255,255,255,0.9); margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
                Public Access
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # User information - Clean layout
        st.markdown("#### 👤 User Information")
        st.markdown(f"""
        <div style='background: #f5f7fa; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;'>
            <p style='margin: 0.5rem 0; font-size: 0.9rem;'><strong>Role:</strong> Public User</p>
            <p style='margin: 0.5rem 0; font-size: 0.9rem;'><strong>Username:</strong> {st.session_state.get('username', 'N/A')}</p>
            <p style='margin: 0.5rem 0; font-size: 0.9rem;'><strong>Name:</strong> {st.session_state.get('name', 'N/A')}</p>
            <p style='margin: 0.5rem 0; font-size: 0.9rem;'><strong>Phone:</strong> {st.session_state.get('phone', 'N/A')}</p>
            <p style='margin: 0.5rem 0; font-size: 0.9rem;'><strong>Status:</strong> ✅ Authenticated</p>
            <p style='margin: 0.5rem 0; font-size: 0.9rem;'><strong>Version:</strong> {Config.APP_VERSION}</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True, type="secondary"):
            try:
                log_user_action("Logout", st.session_state.get("username"))
            except:
                pass
            st.session_state["authentication_status"] = False
            st.session_state["user_role"] = None
            st.session_state.clear()
            st.rerun()


def render_report_form():
    """Render report sighting form"""
    
    import os
    import uuid
    import json
    from backend.utils.image_utils import image_obj_to_numpy, extract_face_mesh_landmarks
    from backend.models.data_models import PublicSubmissions
    from frontend.components.utils import get_indian_states_and_cities
    
    image_col, form_col = st.columns([1, 1.2], gap="large")
    save_flag = 0
    face_mesh = None
    face_detected = False
    unique_id = None
    
    with image_col:
        st.markdown("#### 📸 Upload Photo")
        image_obj = st.file_uploader(
            "Upload Photo", type=["jpg", "jpeg", "png"], key="public_submission_img", label_visibility="collapsed"
        )
        if image_obj:
            unique_id = str(uuid.uuid4())
            
            with st.spinner("Processing image..."):
                os.makedirs("./resources", exist_ok=True)
                uploaded_file_path = "./resources/" + unique_id + ".jpg"
                with open(uploaded_file_path, "wb") as f:
                    f.write(image_obj.read())
                
                image_obj.seek(0)
                st.image(image_obj, width=300, caption="Uploaded Photo")
                image_obj.seek(0)
                
                image_np = image_obj_to_numpy(image_obj)
                landmarks = extract_face_mesh_landmarks(image_np)

                if landmarks is not None:
                    face_mesh = landmarks
                    face_detected = True
                    st.success("✅ Face detected successfully!")
                else:
                    st.warning("⚠️ No face detected. Please upload a clear photo with a visible face.")

    with form_col:
        if face_detected:
            st.markdown("#### 📋 Report Details")
            
            # Person details
            st.markdown("**👤 Person Details**")
            col1, col2 = st.columns(2)
            with col1:
                person_name = st.text_input("Person's Name (if known)", key="pub_name")
            with col2:
                age_range = st.selectbox(
                    "Age Range",
                    ["Child (0-12)", "Teen (13-19)", "Young Adult (20-35)", "Adult (36-60)", "Senior (60+)"],
                    key="pub_age"
                )
            gender = st.selectbox("Gender", ["Male", "Female", "Other"], key="pub_gender")
            
            # Location details
            st.markdown("**📍 Location Details**")
            indian_states, state_cities = get_indian_states_and_cities()
            
            col1, col2 = st.columns(2)
            with col1:
                state = st.selectbox("State *", [""] + sorted(indian_states), key="pub_state")
            with col2:
                if state and state in state_cities:
                    city = st.selectbox("City *", [""] + sorted(state_cities[state]), key="pub_city")
                else:
                    city = st.text_input("City *", key="pub_city_text")
            
            location = st.text_input("Exact Location Sighted *", key="pub_location")
            date_sighted = st.date_input("Date Sighted", key="pub_date")
            description = st.text_area("Additional Description", key="pub_desc", height=80)
            
            # Contact information
            st.markdown("**📞 Your Contact Information**")
            col1, col2 = st.columns(2)
            with col1:
                contact_name = st.text_input("Your Name *", key="pub_contact_name")
            with col2:
                contact_mobile = st.text_input("Mobile Number *", key="pub_contact_mobile", max_chars=10)
            contact_email = st.text_input("Email Address *", key="pub_contact_email")
            
            if st.button("📤 Submit Report", type="primary", use_container_width=True):
                # Validation
                if not location or not city:
                    st.error("❌ Please provide location and city.")
                elif not contact_mobile or len(contact_mobile) != 10 or not contact_mobile.isdigit():
                    st.error("❌ Please provide a valid 10-digit mobile number.")
                elif not contact_email or "@" not in contact_email:
                    st.error("❌ Please provide a valid email address.")
                elif not contact_name:
                    st.error("❌ Please provide your name.")
                else:
                    try:
                        # Create submission
                        submission = PublicSubmissions(
                            id=unique_id,
                            submitted_by=contact_name,
                            name=person_name or "",
                            face_mesh=json.dumps(face_mesh),
                            location=location,
                            city=city,
                            state=state or "",
                            mobile=contact_mobile,
                            email=contact_email,
                            status="NF",
                            birth_marks=description or ""
                        )
                        
                        db_queries.new_public_case(submission)
                        st.success("✅ Your report has been submitted successfully!")
                        st.balloons()
                        st.info("Thank you for helping find missing persons. Law enforcement will review your submission.")
                        
                        try:
                            log_user_action("Public submission", st.session_state.get("username"))
                        except:
                            pass
                        
                        # Refresh to show in recent submissions
                        st.info("🔄 Scroll down to see your submission in 'Recent Submissions'.")
                        
                    except Exception as e:
                        st.error(f"❌ Error submitting report: {str(e)}")


def render_recent_submissions():
    """Render recent submissions"""
    try:
        # Get all public submissions (in a real implementation, filter by user)
        submissions = db_queries.fetch_public_cases(train_data=False, status="All")
        
        if not submissions:
            st.info("📭 You haven't submitted any reports yet.")
            return
        
        st.write(f"**Total Submissions:** {len(submissions)}")
        st.markdown("---")
        
        # Show recent submissions (limit to 10)
        for submission in submissions[:10]:
            status_emoji = "🟢" if submission.status == "F" else "🔴"
            status_text = "FOUND" if submission.status == "F" else "NOT FOUND"
            
            with st.expander(f"{status_emoji} {submission.location} - {status_text}", expanded=False):
                col_photo, col_details = st.columns([1, 2])
                
                with col_photo:
                    try:
                        st.image(
                            f"./resources/{submission.id}.jpg",
                            width=150,
                            caption="Sighting Photo",
                            use_container_width=False,
                        )
                    except Exception:
                        st.warning("📷 Image not available")
                
                with col_details:
                    if hasattr(submission, 'name') and submission.name:
                        st.write(f"**Name:** {submission.name}")
                    st.write(f"**Location:** {submission.location}")
                    if hasattr(submission, 'city') and submission.city:
                        st.write(f"**City:** {submission.city}")
                    if hasattr(submission, 'state') and submission.state:
                        st.write(f"**State:** {submission.state}")
                    st.write(f"**Submitted By:** {submission.submitted_by or 'Anonymous'}")
                    st.write(f"**Mobile:** {submission.mobile}")
                    st.write(f"**Submitted On:** {format_time_12h(submission.submitted_on)}")
                    st.write(f"**Status:** {status_text}")
                    
                    if submission.birth_marks:
                        st.write(f"**Description:** {submission.birth_marks}")
                    
                    # Delete button
                    if st.button(f"🗑️ Delete", key=f"delete_{submission.id}"):
                        try:
                            db_queries.delete_public_submission(submission.id)
                            st.success("✅ Submission deleted successfully!")
                            st.rerun()
                        except Exception as e:
                            st.error(f"❌ Error deleting submission: {str(e)}")
    
    except Exception as e:
        st.error(f"❌ Error loading submissions: {str(e)}")
