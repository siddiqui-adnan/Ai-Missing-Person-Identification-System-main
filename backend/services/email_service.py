"""
Message sender for Missing Person Identification System
Sends messages from missingpersonidentificationsys@gmail.com to complainant emails
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Import email config
try:
    from email_system.email_config import EmailConfig
except ImportError:
    # Fallback if email_config is not available
    class EmailConfig:
        def __init__(self):
            self.smtp_host = None
            self.smtp_port = 587
            self.smtp_user = None
            self.smtp_password = None
            self.notify_email = None
        def is_configured(self):
            return False
        def get_config(self):
            return {
                'smtp_host': self.smtp_host,
                'smtp_port': self.smtp_port,
                'smtp_user': self.smtp_user,
                'smtp_password': self.smtp_password,
                'notify_email': self.notify_email
            }

class MessageSender:
    """Handles sending messages from system email to complainants"""
    
    def __init__(self):
        self.system_email = "missingpersonidentificationsys@gmail.com"
        self.email_config = EmailConfig()
    
    def _load_email_config(self):
        """Load email configuration using EmailConfig class"""
        # Use the centralized EmailConfig class
        config = self.email_config.get_config()
        
        # Add debug logging
        print(f"[MessageSender] Email Config Check:")
        print(f"  - SMTP Host: {config['smtp_host']}")
        print(f"  - SMTP Port: {config['smtp_port']}")
        print(f"  - SMTP User: {config['smtp_user']}")
        print(f"  - Has Password: {bool(config['smtp_password'])}")
        print(f"  - Password Length: {len(config['smtp_password']) if config['smtp_password'] else 0}")
        
        # Try Streamlit secrets as additional fallback
        if not config['smtp_password']:
            try:
                import streamlit as st
                if hasattr(st, 'secrets') and 'email' in st.secrets:
                    config['smtp_host'] = st.secrets.get("email", {}).get("SMTP_HOST", config['smtp_host'])
                    config['smtp_port'] = int(st.secrets.get("email", {}).get("SMTP_PORT", config['smtp_port']))
                    config['smtp_user'] = st.secrets.get("email", {}).get("SMTP_USER", config['smtp_user'])
                    config['smtp_password'] = st.secrets.get("email", {}).get("SMTP_PASSWORD", config['smtp_password'])
                    if config['smtp_password']:
                        print("[MessageSender] Loaded config from Streamlit secrets")
            except Exception as e:
                print(f"[MessageSender] Could not load from Streamlit secrets: {e}")
        
        return config
    
    def send_case_update(self, recipient_email: str, 
                       case_name: str, status: str, message: str = "") -> bool:
        """Send case update notification to complainant"""
        
        if not recipient_email:
            print("[MessageSender] No recipient email provided")
            return False
        
        subject = f"Case Update - {case_name}"
        
        body = f"""Dear Complainant,

This is an update regarding your missing person case:

Case Details:
- Name: {case_name}
- Status: {status}
- Update: {message}

Please log in to the Missing Person Identification System to view full details:
http://localhost:8501

If you have any questions, please contact us at missingpersonidentificationsys@gmail.com

Thank you for using our system.

Best regards,
AI Missing Person Identification System Team
"""
        
        return self._send_email(recipient_email, subject, body)
    
    def send_match_notification(self, recipient_email: str, case_name: str, 
                           matched_person: str, location: str, 
                           confidence: str, case_id: str = None, 
                           registered_case_id: str = None, public_case_id: str = None) -> bool:
        """Send match notification to complainant with photo attachments"""
        
        if not recipient_email:
            print("[MessageSender] No recipient email provided")
            return False
        
        subject = f"MATCH FOUND - {case_name}"
        
        case_id_line = f"- Case ID: {case_id}\n" if case_id else ""
        
        body = f"""Dear Complainant,

We wish to inform you that a potential match has been identified for the missing person case you registered in our system.

**Match Details:**

* **Case ID:** {case_id}
* **Missing Person:** {case_name}
* **Matched Individual:** {matched_person}
* **Location:** {location}
* **Match Confidence:** {confidence}

This match has been evaluated as high confidence and requires your prompt attention and verification.

**Next Steps:**

1. Log in to Missing Person Identification System
2. Review match details and associated images carefully
3. If the match appears accurate, contact appropriate local authorities
4. Confirm or reject the match within the system

Access your account here:
http://localhost:8501

For any questions or assistance, please contact us at:
[missingpersonidentificationsys@gmail.com](mailto:missingpersonidentificationsys@gmail.com)

**Important:** Please ensure that this match is verified with local authorities before taking any further action.

Sincerely,
**AI Missing Person Identification System Team**
"""
        
        # Prepare attachments
        attachments = []
        
        # Add registered case photo if available
        if registered_case_id:
            reg_photo_path = f"./resources/{registered_case_id}.jpg"
            if os.path.exists(reg_photo_path):
                attachments.append((reg_photo_path, f"registered_case_{registered_case_id}.jpg"))
                print(f"[MessageSender] Added registered case photo: {reg_photo_path}")
        
        # Add public submission photo if available
        if public_case_id:
            pub_photo_path = f"./resources/{public_case_id}.jpg"
            if os.path.exists(pub_photo_path):
                attachments.append((pub_photo_path, f"public_submission_{public_case_id}.jpg"))
                print(f"[MessageSender] Added public submission photo: {pub_photo_path}")
        
        # Send email with attachments
        return self._send_email_with_attachments(recipient_email, subject, body, attachments)
    
    def send_system_notification(self, recipient_email: str, title: str, message: str) -> bool:
        """Send general system notification"""
        
        if not recipient_email:
            print("[MessageSender] No recipient email provided")
            return False
        
        subject = f"Notification - {title}"
        
        body = f"""Dear User,

{title}

{message}

If you have any questions, please contact us at missingpersonidentificationsys@gmail.com

Best regards,
AI Missing Person Identification System Team
"""
        
        return self._send_email(recipient_email, subject, body)
    
    def send_email_with_attachment(self, recipient_email: str, subject: str, message: str, 
                                   attachment_path: str = None, attachment_name: str = None) -> bool:
        """Send email with optional attachment"""
        
        if not recipient_email:
            print("[MessageSender] No recipient email provided")
            return False
        
        body = f"""Dear User,

{message}

If you have any questions, please contact us at missingpersonidentificationsys@gmail.com

Best regards,
AI Missing Person Identification System Team
"""
        
        return self._send_email(recipient_email, subject, body, attachment_path, attachment_name)
    
    def _send_email(self, recipient_email: str, subject: str, body: str, 
                   attachment_path: str = None, attachment_name: str = None) -> bool:
        """Internal email sending method with optional attachment support"""
        
        try:
            # Load email configuration dynamically
            config = self._load_email_config()
            
            print(f"[MessageSender] Email Config Check:")
            print(f"  - SMTP Host: {config['smtp_host']}")
            print(f"  - SMTP Port: {config['smtp_port']}")
            print(f"  - SMTP User: {config['smtp_user']}")
            print(f"  - Has Password: {bool(config['smtp_password'])}")
            print(f"  - Password Length: {len(config['smtp_password']) if config['smtp_password'] else 0}")
            
            if not config['smtp_password']:
                print("[MessageSender] ❌ SMTP_PASSWORD not configured")
                print("[MessageSender] Please update email_settings.txt with your Gmail App Password")
                return False
            
            # Create message
            msg = MIMEMultipart()
            msg["From"] = config['smtp_user']
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))
            
            # Add attachment if provided
            if attachment_path and os.path.exists(attachment_path):
                try:
                    with open(attachment_path, "rb") as attachment:
                        part = MIMEBase("application", "octet-stream")
                        part.set_payload(attachment.read())
                    
                    encoders.encode_base64(part)
                    
                    # Use provided name or extract from path
                    filename = attachment_name if attachment_name else os.path.basename(attachment_path)
                    part.add_header(
                        "Content-Disposition",
                        f"attachment; filename= {filename}",
                    )
                    
                    msg.attach(part)
                    print(f"[MessageSender] Attached file: {filename}")
                except Exception as e:
                    print(f"[MessageSender] Warning: Failed to attach file: {e}")
                    # Continue sending email without attachment
            
            # Send email
            print(f"[MessageSender] Attempting to send email to {recipient_email}")
            print(f"[MessageSender] Using SMTP: {config['smtp_host']}:{config['smtp_port']}")
            print(f"[MessageSender] From: {config['smtp_user']}")
            print(f"[MessageSender] Subject: {subject}")
            
            with smtplib.SMTP(config['smtp_host'], config['smtp_port'], timeout=30) as server:
                server.set_debuglevel(0)  # Set to 1 for verbose SMTP debugging
                server.ehlo()
                print("[MessageSender] Starting TLS...")
                server.starttls()
                server.ehlo()
                print("[MessageSender] Logging in...")
                server.login(config['smtp_user'], config['smtp_password'])
                print("[MessageSender] Sending message...")
                server.sendmail(config['smtp_user'], recipient_email, msg.as_string())
            
            print(f"[MessageSender] ✅ Email sent successfully to {recipient_email}: {subject}")
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"[MessageSender] ❌ Failed to send email: {error_msg}")
            
            # Provide specific error guidance
            if "535" in error_msg or "BadCredentials" in error_msg or "Username and Password not accepted" in error_msg:
                print("[MessageSender] Authentication failed - Please check Gmail App Password")
                print("[MessageSender] Make sure you're using an App Password, not your regular Gmail password")
                print("[MessageSender] Update email_settings.txt with correct password")
            elif "530" in error_msg or "Authentication" in error_msg:
                print("[MessageSender] Authentication required - Please check email settings")
            elif "550" in error_msg or "access denied" in error_msg.lower():
                print("[MessageSender] Access denied - Check email permissions")
            elif "SMTP" in error_msg or "Connection" in error_msg:
                print("[MessageSender] SMTP connection failed - Check email server settings and internet connection")
            else:
                    print(f"[MessageSender] Warning: Attachment file not found: {attachment_path}")
            
            # Send email
            print(f"[MessageSender] Attempting to send email to {recipient_email}")
            print(f"[MessageSender] Using SMTP: {config['smtp_host']}:{config['smtp_port']}")
            print(f"[MessageSender] From: {config['smtp_user']}")
            print(f"[MessageSender] Subject: {subject}")
            print(f"[MessageSender] Attachments: {len(attachments)} files")
            
            with smtplib.SMTP(config['smtp_host'], config['smtp_port'], timeout=30) as server:
                server.set_debuglevel(0)  # Set to 1 for verbose SMTP debugging
                server.ehlo()
                print("[MessageSender] Starting TLS...")
                server.starttls()
                server.ehlo()
                print("[MessageSender] Logging in...")
                server.login(config['smtp_user'], config['smtp_password'])
                print("[MessageSender] Sending message...")
                server.sendmail(config['smtp_user'], recipient_email, msg.as_string())
            
            print(f"[MessageSender] ✅ Email sent successfully to {recipient_email}: {subject}")
            return True
            
        except Exception as e:
            error_msg = str(e)
            print(f"[MessageSender] ❌ Failed to send email: {error_msg}")
            
            # Provide specific error guidance
            if "535" in error_msg or "BadCredentials" in error_msg or "Username and Password not accepted" in error_msg:
                print("[MessageSender] Authentication failed - Please check Gmail App Password")
                print("[MessageSender] Make sure you're using an App Password, not your regular Gmail password")
                print("[MessageSender] Update email_settings.txt with correct password")
            elif "530" in error_msg or "Authentication" in error_msg:
                print("[MessageSender] Authentication required - Please check email settings")
            elif "550" in error_msg or "access denied" in error_msg.lower():
                print("[MessageSender] Access denied - Check email permissions")
            elif "SMTP" in error_msg or "Connection" in error_msg:
                print("[MessageSender] SMTP connection failed - Check email server settings and internet connection")
            else:
                print("[MessageSender] General email error - Check network and configuration")
            
            import traceback
            print(f"[MessageSender] Full traceback:")
            traceback.print_exc()
            
            return False

def test_email_config(self):
    """Test email configuration and return status"""
    try:
        config = self._load_email_config()
        
        status = {
            'configured': False,
            'smtp_host': config['smtp_host'],
            'smtp_port': config['smtp_port'],
            'smtp_user': config['smtp_user'],
            'has_password': bool(config['smtp_password']),
            'error': None
        }
        
        if not config['smtp_password']:
            status['error'] = "SMTP password not configured"
            return status
        
        # Try to connect to SMTP server
        with smtplib.SMTP(config['smtp_host'], config['smtp_port'], timeout=10) as server:
            server.ehlo()
            server.starttls()
            server.login(config['smtp_user'], config['smtp_password'])
        
        status['configured'] = True
        return status
        
    except Exception as e:
        return {
            'configured': False,
            'error': str(e),
            'smtp_host': config.get('smtp_host', 'Unknown'),
            'smtp_port': config.get('smtp_port', 'Unknown'),
            'smtp_user': config.get('smtp_user', 'Unknown'),
            'has_password': bool(config.get('smtp_password'))
        }

# Global message sender instance
message_sender = MessageSender()
