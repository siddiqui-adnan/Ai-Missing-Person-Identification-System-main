"""
User Authentication and Registration System
Handles user registration, email verification, and login
"""

import sqlite3
import hashlib
import secrets
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Optional, Tuple
import os

# Import email validator
try:
    from backend.utils.validation_utils import EmailValidator
    EMAIL_VALIDATION_AVAILABLE = True
except ImportError:
    EMAIL_VALIDATION_AVAILABLE = False
    print("Warning: Email validation not available")

class UserAuth:
    def __init__(self, db_path="config/sqlite_database.db"):
        self.db_path = db_path
        self.create_users_table()
    
    def create_users_table(self):
        """Create users table if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS public_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                name TEXT,
                phone_number TEXT,
                verification_token TEXT,
                is_verified INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP,
                reset_token TEXT,
                reset_token_expiry TIMESTAMP
            )
        """)
        
        conn.commit()
        conn.close()
    
    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def generate_verification_token(self) -> str:
        """Generate a random 6-digit verification code"""
        return str(random.randint(100000, 999999))
    
    def register_user(self, email: str, password: str, name: str = "", phone: str = "") -> Tuple[bool, str, Optional[str]]:
        """
        Register a new user with email validation
        Returns: (success, message, verification_token)
        """
        try:
            # Basic email format validation
            if "@" not in email or "." not in email:
                return False, "Invalid email format", None
            
            # Advanced email validation (if available)
            if EMAIL_VALIDATION_AVAILABLE:
                is_valid, validation_message = EmailValidator.validate_email(email, check_domain=True)
                if not is_valid:
                    return False, f"❌ {validation_message}", None
            
            # Check if user already exists
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT email, is_verified FROM public_users WHERE email = ?", (email,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                email_exists, is_verified = existing_user
                conn.close()
                
                if is_verified:
                    return False, "Email already registered and verified. Please login.", None
                else:
                    return False, "Email already registered but not verified. Please check your email for the verification code or use 'Verify Email' tab.", None
            
            # Hash password and generate verification token
            password_hash = self.hash_password(password)
            verification_token = self.generate_verification_token()
            
            # Insert new user with phone number
            cursor.execute("""
                INSERT INTO public_users (email, password_hash, name, phone_number, verification_token, is_verified)
                VALUES (?, ?, ?, ?, ?, 0)
            """, (email, password_hash, name, phone, verification_token))
            
            conn.commit()
            conn.close()
            
            # Try to send verification email
            email_sent = self.send_verification_email(email, verification_token)
            
            # Always return token for display (whether email sent or not)
            if email_sent:
                return True, "✅ Registration successful! Check your email for the 6-digit verification code.", verification_token
            else:
                return True, "✅ Registration successful! Check your email for the 6-digit verification code.", verification_token
        
        except Exception as e:
            return False, f"Registration error: {str(e)}", None
    
    def send_verification_email(self, email: str, token: str) -> bool:
        """
        Send verification email to user
        Returns: True if email sent successfully
        """
        try:
            # Load email configuration from email_settings.txt first, then environment variables
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = "missingpersonidentificationsys@gmail.com"
            sender_password = ""
            
            # Try to load from email_settings.txt
            config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "email_settings.txt")
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line and '=' in line and not line.startswith('#'):
                                key, value = line.split('=', 1)
                                key = key.strip().upper()
                                value = value.strip()
                                
                                if key == "SMTP_HOST" and value:
                                    smtp_server = value
                                elif key == "SMTP_PORT" and value:
                                    smtp_port = int(value)
                                elif key == "SMTP_USER" and value:
                                    sender_email = value
                                elif key == "SMTP_PASSWORD" and value:
                                    sender_password = value
                except Exception as e:
                    print(f"Error loading email_settings.txt: {e}")
            
            # Override with environment variables if set
            smtp_server = os.getenv("SMTP_SERVER", smtp_server)
            smtp_port = int(os.getenv("SMTP_PORT", str(smtp_port)))
            sender_email = os.getenv("SMTP_USERNAME") or os.getenv("SMTP_USER") or sender_email
            sender_password = os.getenv("SMTP_PASSWORD") or sender_password
            
            if not sender_password or sender_password == "your-app-password":
                print("❌ Warning: SMTP_PASSWORD not configured properly")
                print(f"Please update email_settings.txt with a valid Gmail App Password")
                return False
            
            if not sender_email or sender_email == "your-email@gmail.com":
                print("❌ Warning: SMTP_USER not configured properly")
                return False
            
            # Create email message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Your Verification Code - AI Missing Person System"
            message["From"] = f"AI Missing Person System <{sender_email}>"
            message["To"] = email
            
            # Email body with 6-digit code
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
                    <div style="max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                        <div style="text-align: center; margin-bottom: 30px;">
                            <h1 style="color: #1a237e; margin: 0;">🔍 AI Missing Person System</h1>
                            <p style="color: #667eea; font-size: 14px; margin-top: 5px;">Reuniting Families Through Advanced Technology</p>
                        </div>
                        
                        <h2 style="color: #1a237e; margin-bottom: 20px;">Welcome!</h2>
                        <p style="color: #333; font-size: 16px; line-height: 1.6;">
                            Thank you for registering with AI Missing Person Identification System. 
                            To complete your registration, please verify your email address.
                        </p>
                        
                        <p style="color: #333; font-size: 16px; line-height: 1.6;">
                            <strong>Website:</strong> <a href="http://localhost:8501" style="color: #1a237e; text-decoration: none;">http://localhost:8501</a>
                        </p>
                        
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; margin: 30px 0; text-align: center;">
                            <p style="color: white; margin: 0 0 10px 0; font-size: 14px; font-weight: 600;">YOUR VERIFICATION CODE</p>
                            <div style="background: white; padding: 20px; border-radius: 8px; display: inline-block;">
                                <span style="font-size: 42px; font-weight: bold; color: #1a237e; letter-spacing: 8px;">{token}</span>
                            </div>
                        </div>
                        
                        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; margin: 20px 0;">
                            <p style="margin: 0; color: #333; font-size: 14px;"><strong>How to verify:</strong></p>
                            <ol style="margin: 10px 0 0 0; padding-left: 20px; color: #666; font-size: 14px;">
                                <li>Go to the login page</li>
                                <li>Click on "Verify Email" tab</li>
                                <li>Enter the 6-digit code above</li>
                                <li>Click "Verify" button</li>
                            </ol>
                        </div>
                        
                        <p style="color: #999; font-size: 12px; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                            <strong>Security Note:</strong> This code will expire in 24 hours. If you didn't register for this account, 
                            please ignore this email or contact support if you have concerns.
                        </p>
                        
                        <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                            <p style="color: #999; font-size: 11px; margin: 0;">
                                AI Missing Person Identification System<br>
                                Helping reunite families with missing loved ones
                            </p>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            message.attach(MIMEText(html, "html"))
            
            # Send email to the USER's email address (not system email)
            print(f"Attempting to send verification code to: {email}")
            print(f"From: {sender_email}")
            print(f"Code: {token}")
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
            
            print(f"✅ Verification email sent successfully to {email}")
            return True
        
        except smtplib.SMTPAuthenticationError as e:
            print(f"❌ SMTP Authentication Error: {str(e)}")
            print("Please check your Gmail App Password is correct")
            return False
        except smtplib.SMTPException as e:
            print(f"❌ SMTP Error: {str(e)}")
            return False
        except Exception as e:
            print(f"❌ Email sending error: {str(e)}")
            return False
    
    def verify_user(self, token: str) -> Tuple[bool, str]:
        """
        Verify user account with token
        Returns: (success, message)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT email, is_verified FROM public_users 
                WHERE verification_token = ?
            """, (token,))
            
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return False, "Invalid verification token"
            
            email, is_verified = result
            
            if is_verified:
                conn.close()
                return False, "Account already verified"
            
            # Update user as verified
            cursor.execute("""
                UPDATE public_users 
                SET is_verified = 1, verification_token = NULL
                WHERE verification_token = ?
            """, (token,))
            
            conn.commit()
            conn.close()
            
            return True, "Account verified successfully! You can now login."
        
        except Exception as e:
            return False, f"Verification error: {str(e)}"
    
    def login_user(self, email: str, password: str) -> Tuple[bool, str, Optional[dict]]:
        """
        Login user with email and password
        Returns: (success, message, user_data)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            
            cursor.execute("""
                SELECT id, email, name, phone_number, is_verified, last_login
                FROM public_users
                WHERE email = ? AND password_hash = ?
            """, (email, password_hash))
            
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return False, "Invalid email or password", None
            
            user_id, email, name, phone_number, is_verified, last_login = result
            
            if not is_verified:
                conn.close()
                return False, "Please verify your email before logging in", None
            
            # Update last login
            cursor.execute("""
                UPDATE public_users
                SET last_login = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (user_id,))
            
            conn.commit()
            conn.close()
            
            user_data = {
                "id": user_id,
                "email": email,
                "name": name or email.split("@")[0],
                "phone": phone_number or "",
                "last_login": last_login
            }
            
            return True, "Login successful!", user_data
        
        except Exception as e:
            return False, f"Login error: {str(e)}", None
    
    def check_email_exists(self, email: str) -> bool:
        """Check if email is already registered"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("SELECT email FROM public_users WHERE email = ?", (email,))
            result = cursor.fetchone()
            
            conn.close()
            return result is not None
        
        except Exception:
            return False
    
    def request_password_reset(self, email: str) -> Tuple[bool, str, Optional[str]]:
        """
        Request password reset - generates token and sends email
        Returns: (success, message, reset_token)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if email exists
            cursor.execute("SELECT email, is_verified FROM public_users WHERE email = ?", (email,))
            result = cursor.fetchone()
            
            if not result:
                conn.close()
                return False, "Email not found in our system", None
            
            email_db, is_verified = result
            
            if not is_verified:
                conn.close()
                return False, "Please verify your email first before resetting password", None
            
            # Generate 6-digit reset token
            reset_token = self.generate_verification_token()
            
            # Set expiry to 1 hour from now
            expiry_time = datetime.now() + timedelta(hours=1)
            
            # Update user with reset token
            cursor.execute("""
                UPDATE public_users 
                SET reset_token = ?, reset_token_expiry = ?
                WHERE email = ?
            """, (reset_token, expiry_time, email))
            
            conn.commit()
            conn.close()
            
            # Send reset email
            email_sent = self.send_password_reset_email(email, reset_token)
            
            if email_sent:
                return True, "Password reset code sent to your email", reset_token
            else:
                return True, "Password reset code generated. Check your email.", reset_token
        
        except Exception as e:
            return False, f"Error requesting password reset: {str(e)}", None
    
    def send_password_reset_email(self, email: str, token: str) -> bool:
        """
        Send password reset email to user
        Returns: True if email sent successfully
        """
        try:
            # Load email configuration
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = "missingpersonidentificationsys@gmail.com"
            sender_password = ""
            
            # Try to load from email_settings.txt
            config_file = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "email_settings.txt")
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line and '=' in line and not line.startswith('#'):
                                key, value = line.split('=', 1)
                                key = key.strip().upper()
                                value = value.strip()
                                
                                if key == "SMTP_HOST" and value:
                                    smtp_server = value
                                elif key == "SMTP_PORT" and value:
                                    smtp_port = int(value)
                                elif key == "SMTP_USER" and value:
                                    sender_email = value
                                elif key == "SMTP_PASSWORD" and value:
                                    sender_password = value
                except Exception as e:
                    print(f"Error loading email_settings.txt: {e}")
            
            # Override with environment variables if set
            smtp_server = os.getenv("SMTP_SERVER", smtp_server)
            smtp_port = int(os.getenv("SMTP_PORT", str(smtp_port)))
            sender_email = os.getenv("SMTP_USERNAME") or os.getenv("SMTP_USER") or sender_email
            sender_password = os.getenv("SMTP_PASSWORD") or sender_password
            
            if not sender_password or sender_password == "your-app-password":
                print("❌ Warning: SMTP_PASSWORD not configured properly")
                return False
            
            if not sender_email or sender_email == "your-email@gmail.com":
                print("❌ Warning: SMTP_USER not configured properly")
                return False
            
            # Create email message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Password Reset Code - AI Missing Person System"
            message["From"] = f"AI Missing Person System <{sender_email}>"
            message["To"] = email
            
            # Email body with 6-digit code
            html = f"""
            <html>
                <body style="font-family: Arial, sans-serif; padding: 20px; background-color: #f5f5f5;">
                    <div style="max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 10px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);">
                        <div style="text-align: center; margin-bottom: 30px;">
                            <h1 style="color: #1a237e; margin: 0;">🔍 AI Missing Person System</h1>
                            <p style="color: #667eea; font-size: 14px; margin-top: 5px;">Reuniting Families Through Advanced Technology</p>
                        </div>
                        
                        <h2 style="color: #1a237e; margin-bottom: 20px;">Password Reset Request</h2>
                        <p style="color: #333; font-size: 16px; line-height: 1.6;">
                            We received a request to reset your password. Use the code below to reset your password.
                        </p>
                        
                        <p style="color: #333; font-size: 16px; line-height: 1.6;">
                            <strong>Website:</strong> <a href="http://localhost:8501" style="color: #1a237e; text-decoration: none;">http://localhost:8501</a>
                        </p>
                        
                        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 30px; border-radius: 10px; margin: 30px 0; text-align: center;">
                            <p style="color: white; margin: 0 0 10px 0; font-size: 14px; font-weight: 600;">YOUR PASSWORD RESET CODE</p>
                            <div style="background: white; padding: 20px; border-radius: 8px; display: inline-block;">
                                <span style="font-size: 42px; font-weight: bold; color: #1a237e; letter-spacing: 8px;">{token}</span>
                            </div>
                        </div>
                        
                        <div style="background: #f8f9fa; padding: 20px; border-radius: 8px; border-left: 4px solid #667eea; margin: 20px 0;">
                            <p style="margin: 0; color: #333; font-size: 14px;"><strong>How to reset your password:</strong></p>
                            <ol style="margin: 10px 0 0 0; padding-left: 20px; color: #666; font-size: 14px;">
                                <li>Go to the login page</li>
                                <li>Click on "Forgot Password" button</li>
                                <li>Enter the 6-digit code above</li>
                                <li>Enter your new password</li>
                                <li>Click "Reset Password" button</li>
                            </ol>
                        </div>
                        
                        <div style="background: #fff3cd; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107; margin: 20px 0;">
                            <p style="margin: 0; color: #856404; font-size: 13px;">
                                <strong>⚠️ Security Alert:</strong> This code will expire in 1 hour. If you didn't request this password reset, 
                                please ignore this email and your password will remain unchanged.
                            </p>
                        </div>
                        
                        <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #eee;">
                            <p style="color: #999; font-size: 11px; margin: 0;">
                                AI Missing Person Identification System<br>
                                Helping reunite families with missing loved ones
                            </p>
                        </div>
                    </div>
                </body>
            </html>
            """
            
            message.attach(MIMEText(html, "html"))
            
            print(f"Attempting to send password reset code to: {email}")
            print(f"From: {sender_email}")
            print(f"Code: {token}")
            
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(message)
            
            print(f"✅ Password reset email sent successfully to {email}")
            return True
        
        except Exception as e:
            print(f"❌ Password reset email error: {str(e)}")
            return False
    
    def verify_reset_token(self, token: str) -> Tuple[bool, str, Optional[str]]:
        """
        Verify reset token is valid and not expired
        Returns: (success, message, email)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT email, reset_token_expiry FROM public_users 
                WHERE reset_token = ?
            """, (token,))
            
            result = cursor.fetchone()
            conn.close()
            
            if not result:
                return False, "Invalid reset code", None
            
            email, expiry_str = result
            
            # Check if token expired
            expiry_time = datetime.fromisoformat(expiry_str)
            if datetime.now() > expiry_time:
                return False, "Reset code has expired. Please request a new one.", None
            
            return True, "Reset code verified", email
        
        except Exception as e:
            return False, f"Error verifying reset code: {str(e)}", None
    
    def reset_password(self, token: str, new_password: str) -> Tuple[bool, str]:
        """
        Reset password using valid token
        Returns: (success, message)
        """
        try:
            # Verify token first
            is_valid, message, email = self.verify_reset_token(token)
            
            if not is_valid:
                return False, message
            
            # Hash new password
            password_hash = self.hash_password(new_password)
            
            # Update password and clear reset token
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE public_users 
                SET password_hash = ?, reset_token = NULL, reset_token_expiry = NULL
                WHERE reset_token = ?
            """, (password_hash, token))
            
            conn.commit()
            conn.close()
            
            return True, "Password reset successfully! You can now login with your new password."
        
        except Exception as e:
            return False, f"Error resetting password: {str(e)}"
    
    def get_all_users(self) -> list:
        """
        Get all registered users for admin management
        Returns: List of user dictionaries
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, email, name, phone_number, is_verified, created_at, last_login
                FROM public_users
                ORDER BY created_at DESC
            """)
            
            users = []
            for row in cursor.fetchall():
                users.append({
                    "id": row[0],
                    "email": row[1],
                    "name": row[2] or "N/A",
                    "phone": row[3] or "N/A",
                    "verified": "Yes" if row[4] else "No",
                    "created_at": row[5],
                    "last_login": row[6] or "Never"
                })
            
            conn.close()
            return users
        
        except Exception as e:
            print(f"Error getting users: {str(e)}")
            return []
    
    def delete_user(self, user_id: int) -> Tuple[bool, str]:
        """
        Delete/unregister a user from the system
        Returns: (success, message)
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Get user email before deletion for confirmation
            cursor.execute("SELECT email FROM public_users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            if not result:
                conn.close()
                return False, "User not found"
            
            user_email = result[0]
            
            # Delete user and all their submissions (correct table name: publicsubmissions)
            cursor.execute("DELETE FROM publicsubmissions WHERE submitted_by = ?", (user_email,))
            cursor.execute("DELETE FROM public_users WHERE id = ?", (user_id,))
            
            conn.commit()
            conn.close()
            
            return True, f"User {user_email} has been successfully unregistered"
        
        except Exception as e:
            return False, f"Error deleting user: {str(e)}"
    
    def get_user_stats(self) -> dict:
        """
        Get statistics about registered users
        Returns: Dictionary with user statistics
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Total users
            cursor.execute("SELECT COUNT(*) FROM public_users")
            total_users = cursor.fetchone()[0]
            
            # Verified users
            cursor.execute("SELECT COUNT(*) FROM public_users WHERE is_verified = 1")
            verified_users = cursor.fetchone()[0]
            
            # Users registered today
            cursor.execute("SELECT COUNT(*) FROM public_users WHERE DATE(created_at) = DATE('now')")
            today_users = cursor.fetchone()[0]
            
            # Users with recent login (last 7 days)
            cursor.execute("""
                SELECT COUNT(*) FROM public_users 
                WHERE last_login >= DATE('now', '-7 days')
            """)
            active_users = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                "total_users": total_users,
                "verified_users": verified_users,
                "unverified_users": total_users - verified_users,
                "today_users": today_users,
                "active_users": active_users,
                "verification_rate": round((verified_users / total_users * 100), 1) if total_users > 0 else 0
            }
        
        except Exception as e:
            print(f"Error getting user stats: {str(e)}")
            return {
                "total_users": 0,
                "verified_users": 0,
                "unverified_users": 0,
                "today_users": 0,
                "active_users": 0,
                "verification_rate": 0
            }
