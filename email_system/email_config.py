"""
Email configuration for the Missing Person Identification System
"""

import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class EmailConfig:
    """Email configuration management"""
    
    def __init__(self):
        # Default Gmail SMTP settings (can be overridden)
        self.smtp_host = os.environ.get("SMTP_HOST", "smtp.gmail.com")
        self.smtp_port = int(os.environ.get("SMTP_PORT", "587"))
        self.smtp_user = os.environ.get("SMTP_USER", "")
        self.smtp_password = os.environ.get("SMTP_PASSWORD", "")
        self.notify_email = os.environ.get("NOTIFY_EMAIL", "")
        
        # Load from config file if environment variables not set
        self._load_from_file()
    
    def _load_from_file(self):
        """Load email configuration from config file"""
        # Multiple path locations to check
        current_dir = os.path.dirname(__file__)
        parent_dir = os.path.dirname(current_dir)
        
        config_paths = [
            # Root directory paths
            os.path.join(parent_dir, "email_settings.txt"),
            os.path.join(current_dir, "email_settings.txt"),
            # Current working directory paths
            os.path.join(os.getcwd(), "email_settings.txt"),
            os.path.join(os.getcwd(), "email_system", "email_settings.txt"),
            # Config directory paths (alternative)
            os.path.join(parent_dir, "config", "email_settings.txt"),
            os.path.join(os.getcwd(), "config", "email_settings.txt"),
            # Absolute path fallback
            "email_settings.txt",
        ]
        
        config_file = None
        for path in config_paths:
            abs_path = os.path.abspath(path)
            if os.path.exists(abs_path):
                config_file = abs_path
                break
        
        if config_file:
            try:
                with open(config_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and '=' in line and not line.startswith('#'):
                            key, value = line.split('=', 1)
                            key = key.strip().upper()
                            value = value.strip()
                            
                            if key == "SMTP_HOST" and not self.smtp_host:
                                self.smtp_host = value
                            elif key == "SMTP_PORT" and not os.environ.get("SMTP_PORT"):
                                self.smtp_port = int(value)
                            elif key == "SMTP_USER" and not self.smtp_user:
                                self.smtp_user = value
                            elif key == "SMTP_PASSWORD" and not self.smtp_password:
                                self.smtp_password = value
                            elif key == "NOTIFY_EMAIL" and not self.notify_email:
                                self.notify_email = value
            except Exception as e:
                print(f"[EmailConfig] Error loading email config: {e}")
    
    def is_configured(self) -> bool:
        """Check if email is properly configured"""
        return bool(self.smtp_host and self.smtp_user and self.smtp_password)
    
    def get_config(self) -> dict:
        """Get email configuration as dictionary"""
        return {
            'smtp_host': self.smtp_host,
            'smtp_port': self.smtp_port,
            'smtp_user': self.smtp_user,
            'smtp_password': self.smtp_password,
            'notify_email': self.notify_email
        }
    
    def create_config_file(self, smtp_host: str, smtp_user: str, smtp_password: str, 
                          smtp_port: int = 587, notify_email: str = ""):
        """Create email configuration file"""
        config_content = f"""# Email Configuration for Missing Person Identification System
# Edit these settings with your email provider details

# SMTP Server Settings
SMTP_HOST={smtp_host}
SMTP_PORT={smtp_port}
SMTP_USER={smtp_user}
SMTP_PASSWORD={smtp_password}

# Default notification email (optional)
NOTIFY_EMAIL={notify_email}

# Common SMTP settings:
# Gmail: smtp.gmail.com:587
# Outlook: smtp-mail.outlook.com:587
# Yahoo: smtp.mail.yahoo.com:587
"""
        
        with open("email_settings.txt", 'w') as f:
            f.write(config_content)
        
        print("Email configuration file created: email_settings.txt")
        print("Please edit this file with your actual email settings.")

# Global email config instance
email_config = EmailConfig()
