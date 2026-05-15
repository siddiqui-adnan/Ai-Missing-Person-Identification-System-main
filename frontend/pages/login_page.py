"""
Login page for the AI Missing Person Identification System
Handles authentication for Admin, Public, and Complainant users
"""
import streamlit as st
from datetime import datetime

from frontend.components.styles import get_login_page_styles
from frontend.components.utils import load_background_image, load_config
from config import Config, Messages
from backend.services.auth_service import UserAuth
from backend.utils.error_handler import log_user_action

# Enhanced features flag
try:
    from backend.utils.error_handler import log_user_action, check_session_timeout
    ENHANCED_FEATURES = True
except ImportError:
    ENHANCED_FEATURES = False


def render_login_page():
    """Render the login page with three access options"""
    
    # Load background image with caching
    bg_image_base64 = load_background_image()
    
    # Apply styles
    st.markdown(get_login_page_styles(bg_image_base64), unsafe_allow_html=True)

    # Main banner
    st.markdown("""
    <div class="main-container">
        <div class="login-banner" style="background: #ffffff !important; background-color: #ffffff !important;">
            <h1>🔍 AI MISSING PERSON IDENTIFICATION SYSTEM</h1>
            <p class="tagline">REUNITING FAMILIES THROUGH ADVANCED TECHNOLOGY</p>
            <span class="badge">Choose your login type below</span>
        </div>
    """, unsafe_allow_html=True)

    # Login Cards - Responsive layout
    col1, col2, col3 = st.columns([1, 1, 1])
    
    # Initialize session state for card expansion
    if "show_admin_form" not in st.session_state:
        st.session_state["show_admin_form"] = False
    if "show_public_form" not in st.session_state:
        st.session_state["show_public_form"] = False
    if "show_complainant_form" not in st.session_state:
        st.session_state["show_complainant_form"] = False
    
    with col1:
        render_admin_login_card()
    
    with col2:
        render_public_login_card()
    
    with col3:
        render_complainant_card()

    st.markdown("""
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_admin_login_card():
    """Render admin login card"""
    # Create clickable card
    if st.button("👮‍♂️\n\n**Admin Login**\n\nFor law enforcement and authorized personnel\n\n*Click to login*", 
                key="admin_card_btn", 
                use_container_width=True,
                type="secondary"):
        st.session_state["show_admin_form"] = not st.session_state["show_admin_form"]
        st.session_state["show_public_form"] = False
        st.session_state["show_complainant_form"] = False
        st.rerun()
    
    # Admin login form - only show if toggled
    if st.session_state["show_admin_form"]:
        try:
            with st.form("admin_login_form"):
                st.markdown("**Admin Credentials**")
                admin_username = st.text_input("Username", key="admin_username", autocomplete="off")
                admin_password = st.text_input("Password", type="password", key="admin_password", autocomplete="new-password")
                admin_submit = st.form_submit_button("Login")
                
                if admin_submit:
                    # Check login attempts (security feature)
                    if st.session_state.get("login_attempts", 0) >= Config.MAX_LOGIN_ATTEMPTS:
                        st.error(f"🔒 Too many failed attempts. Please try again in {Config.MAX_LOGIN_ATTEMPTS} minutes.")
                        if ENHANCED_FEATURES:
                            log_user_action("Max login attempts exceeded", admin_username)
                    elif admin_username == "mit" and admin_password == "123":
                        st.session_state["authentication_status"] = True
                        st.session_state["user_role"] = "Admin"
                        st.session_state["username"] = admin_username
                        st.session_state["name"] = "Gagandeep Singh"
                        st.session_state["login_status"] = True
                        st.session_state["user"] = admin_username
                        st.session_state["login_attempts"] = 0
                        st.session_state["last_activity"] = datetime.now()
                        
                        if ENHANCED_FEATURES:
                            log_user_action("Admin login", admin_username)
                        
                        st.success(Messages.LOGIN_SUCCESS)
                        
                        if admin_password == "123":
                            st.warning(Messages.DEFAULT_PASSWORD)
                        
                        st.rerun()
                    else:
                        st.session_state["login_attempts"] = st.session_state.get("login_attempts", 0) + 1
                        st.error(Messages.LOGIN_FAILED)
                        if ENHANCED_FEATURES:
                            log_user_action("Failed admin login attempt", admin_username)
        except Exception as e:
            st.error(f"Login error: {e}")


def render_public_login_card():
    """Render public user login/registration card"""
    # Create clickable card
    if st.button("👥\n\n**Public Access**\n\nReport sightings and help find missing persons\n\n*Click to register/login*", 
                key="public_card_btn", 
                use_container_width=True,
                type="secondary"):
        st.session_state["show_public_form"] = not st.session_state["show_public_form"]
        st.session_state["show_admin_form"] = False
        st.session_state["show_complainant_form"] = False
        st.rerun()
    
    # Public registration/login form - only show if toggled
    if st.session_state["show_public_form"]:
        try:
            user_auth = UserAuth()
            
            # Tab selection
            tab1, tab2, tab3, tab4 = st.tabs(["🔐 Login", "📝 Register", "✅ Verify", "🔑 Reset Password"])
            
            # LOGIN TAB
            with tab1:
                render_public_login_form(user_auth)
            
            # REGISTER TAB
            with tab2:
                render_public_register_form(user_auth)
            
            # VERIFY TAB
            with tab3:
                render_public_verify_form(user_auth)
            
            # RESET PASSWORD TAB
            with tab4:
                render_password_reset_form(user_auth)
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("If you're having trouble, please contact support.")


def render_public_login_form(user_auth):
    """Render public user login form"""
    with st.form("public_login_form"):
        st.markdown("**Login to Your Account**")
        login_email = st.text_input("Email", key="login_email", autocomplete="off")
        login_password = st.text_input("Password", type="password", key="login_password", autocomplete="new-password")
        login_submit = st.form_submit_button("Login")
        
        if login_submit:
            if not login_email or not login_password:
                st.error("Please enter both email and password")
            else:
                # Check login attempts (security feature)
                if st.session_state.get("login_attempts", 0) >= Config.MAX_LOGIN_ATTEMPTS:
                    st.error(f"🔒 Too many failed attempts. Please try again later.")
                    if ENHANCED_FEATURES:
                        log_user_action("Max login attempts exceeded", login_email)
                else:
                    success, message, user_data = user_auth.login_user(login_email, login_password)
                    
                    if success:
                        st.session_state["authentication_status"] = True
                        st.session_state["user_role"] = "Public"
                        st.session_state["username"] = user_data["email"]
                        st.session_state["name"] = user_data["name"]
                        st.session_state["phone"] = user_data.get("phone", "")
                        st.session_state["login_attempts"] = 0
                        st.session_state["last_activity"] = datetime.now()
                        
                        if ENHANCED_FEATURES:
                            log_user_action("Public login", login_email)
                        
                        st.success(message)
                        st.rerun()
                    else:
                        st.session_state["login_attempts"] = st.session_state.get("login_attempts", 0) + 1
                        st.error(message)
                        if ENHANCED_FEATURES:
                            log_user_action("Failed public login attempt", login_email)
    
    # Forgot password link
    st.markdown("---")
    st.markdown("**Forgot your password?** 👉 Go to the **'Reset Password'** tab above")


def render_public_register_form(user_auth):
    """Render public user registration form"""
    with st.form("public_register_form"):
        st.markdown("**Create New Account**")
        reg_name = st.text_input("Full Name", key="reg_name")
        reg_email = st.text_input("Email", key="reg_email", autocomplete="off")
        reg_phone = st.text_input("Phone Number", key="reg_phone", placeholder="+91 1234567890 or 1234567890")
        reg_password = st.text_input("Password", type="password", key="reg_password", autocomplete="new-password")
        reg_password_confirm = st.text_input("Confirm Password", type="password", key="reg_password_confirm", autocomplete="new-password")
        
        st.markdown("**Password Requirements:**")
        st.caption("• Minimum 6 characters")
        st.caption("• Use a strong, unique password")
        
        register_submit = st.form_submit_button("Register")
        
        if register_submit:
            # Validation
            if not reg_name or not reg_email or not reg_phone or not reg_password:
                st.error("Please fill in all fields including phone number")
            elif "@" not in reg_email or "." not in reg_email:
                st.error("Please enter a valid email address")
            elif len(reg_password) < 6:
                st.error("Password must be at least 6 characters long")
            elif reg_password != reg_password_confirm:
                st.error("Passwords do not match")
            else:
                # Validate phone number
                phone_clean = reg_phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "").replace("+", "")
                if not phone_clean.isdigit():
                    st.error("Phone number must contain only digits")
                elif len(phone_clean) < 10:
                    st.error("Phone number must be at least 10 digits")
                else:
                    # Register user with phone number
                    success, message, token = user_auth.register_user(reg_email, reg_password, reg_name, reg_phone)
                
                    if success:
                        st.success(message)
                        
                        if ENHANCED_FEATURES:
                            log_user_action("New user registered", reg_email)
                    else:
                        st.error(message)


def render_public_verify_form(user_auth):
    """Render email verification form"""
    with st.form("public_verify_form"):
        st.markdown("**Verify Your Account**")
        st.info("📧 Enter the 6-digit verification code sent to your email")
        verify_token = st.text_input("6-Digit Verification Code", key="verify_token", max_chars=6, placeholder="123456")
        verify_submit = st.form_submit_button("Verify Account")
        
        if verify_submit:
            if not verify_token:
                st.error("Please enter the 6-digit verification code")
            elif len(verify_token) != 6 or not verify_token.isdigit():
                st.error("Please enter a valid 6-digit code")
            else:
                success, message = user_auth.verify_user(verify_token)
                
                if success:
                    st.success(message)
                    st.balloons()
                    st.info("✅ You can now login using the 'Login' tab")
                    if ENHANCED_FEATURES:
                        log_user_action("Email verified", verify_token)
                else:
                    st.error(message)


def render_complainant_card():
    """Render complainant (public viewer) card"""
    # Create clickable card - directly redirect to cases page
    if st.button("👨‍👩‍👧‍👦\n\n**View Cases**\n\nFor family members and complainants\n\n*Click to view*", 
                key="complainant_card_btn", 
                use_container_width=True,
                type="secondary"):
        # Set session state to show complainant view (no login required)
        st.session_state["authentication_status"] = True
        st.session_state["user_role"] = "Complainant"
        st.session_state["username"] = "public_viewer"
        st.session_state["name"] = "Public Viewer"
        st.session_state["last_activity"] = datetime.now()
        
        if ENHANCED_FEATURES:
            log_user_action("Complainant cases viewed", "public_viewer")
        
        st.rerun()


def render_password_reset_form(user_auth):
    """Render password reset form"""
    st.markdown("**Reset Your Password**")
    st.info("🔑 Enter your email to receive a password reset code")
    
    # Initialize session state for reset flow
    if "reset_step" not in st.session_state:
        st.session_state["reset_step"] = "request"  # request, verify, complete
    if "reset_email" not in st.session_state:
        st.session_state["reset_email"] = ""
    
    # STEP 1: Request Reset Code
    if st.session_state["reset_step"] == "request":
        with st.form("request_reset_form"):
            reset_email = st.text_input("Email Address", key="reset_email_input", autocomplete="off")
            request_submit = st.form_submit_button("Send Reset Code")
            
            if request_submit:
                if not reset_email:
                    st.error("Please enter your email address")
                elif "@" not in reset_email or "." not in reset_email:
                    st.error("Please enter a valid email address")
                else:
                    success, message, token = user_auth.request_password_reset(reset_email)
                    
                    if success:
                        st.session_state["reset_step"] = "verify"
                        st.session_state["reset_email"] = reset_email
                        st.success(message)
                        st.info("📧 Check your email for the 6-digit reset code")
                        st.rerun()
                    else:
                        st.error(message)
    
    # STEP 2: Verify Code and Reset Password
    elif st.session_state["reset_step"] == "verify":
        st.success(f"📧 Reset code sent to: {st.session_state['reset_email']}")
        
        with st.form("verify_reset_form"):
            st.markdown("**Enter Reset Code and New Password**")
            reset_code = st.text_input("6-Digit Reset Code", key="reset_code_input", max_chars=6, placeholder="123456")
            new_password = st.text_input("New Password", type="password", key="new_password_input", autocomplete="new-password")
            confirm_password = st.text_input("Confirm New Password", type="password", key="confirm_password_input", autocomplete="new-password")
            
            st.markdown("**Password Requirements:**")
            st.caption("• Minimum 6 characters")
            st.caption("• Use a strong, unique password")
            
            col1, col2 = st.columns(2)
            
            with col1:
                reset_submit = st.form_submit_button("Reset Password", type="primary")
            
            with col2:
                cancel_reset = st.form_submit_button("Cancel")
            
            if reset_submit:
                if not reset_code:
                    st.error("Please enter the 6-digit reset code")
                elif len(reset_code) != 6 or not reset_code.isdigit():
                    st.error("Please enter a valid 6-digit code")
                elif not new_password:
                    st.error("Please enter a new password")
                elif len(new_password) < 6:
                    st.error("Password must be at least 6 characters long")
                elif new_password != confirm_password:
                    st.error("Passwords do not match")
                else:
                    # Reset password
                    success, message = user_auth.reset_password(reset_code, new_password)
                    
                    if success:
                        # Show prominent success message
                        st.markdown("---")
                        st.success("🎉 **Password Has Been Reset Successfully!**")
                        st.balloons()
                        st.markdown("""
                        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                    padding: 20px; border-radius: 10px; text-align: center; margin: 20px 0;'>
                            <h3 style='color: white; margin: 0;'>✅ Your password has been changed!</h3>
                            <p style='color: white; margin: 10px 0 0 0;'>You can now login with your new password</p>
                        </div>
                        """, unsafe_allow_html=True)
                        st.info("👉 Go to the **'Login'** tab above to sign in with your new password")
                        
                        if ENHANCED_FEATURES:
                            log_user_action("Password reset", st.session_state["reset_email"])
                        
                        # Reset state after a delay to show message
                        st.session_state["reset_step"] = "complete"
                        st.session_state["show_reset_success"] = True
                    else:
                        st.error(message)
            
            if cancel_reset:
                # Reset state
                st.session_state["reset_step"] = "request"
                st.session_state["reset_email"] = ""
                st.rerun()
    
    # STEP 3: Show success and allow return to login
    elif st.session_state["reset_step"] == "complete":
        st.markdown("---")
        st.success("🎉 **Password Has Been Reset Successfully!**")
        st.markdown("""
        <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 30px; border-radius: 10px; text-align: center; margin: 20px 0;'>
            <h2 style='color: white; margin: 0;'>✅ Password Changed!</h2>
            <p style='color: white; margin: 15px 0 0 0; font-size: 16px;'>Your password has been successfully reset</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.info("👉 Click the **'Login'** tab above to sign in with your new password")
        
        if st.button("🔐 Go to Login", type="primary", use_container_width=True):
            # Reset state
            st.session_state["reset_step"] = "request"
            st.session_state["reset_email"] = ""
            st.session_state["show_reset_success"] = False
            st.rerun()
