"""
Configuration management for the Missing Person Identification System
"""

import os
from pathlib import Path
from typing import Optional
import yaml


class Config:
    """Application configuration"""
    
    # Application Info
    APP_NAME = "AI Missing Person Identification System"
    APP_VERSION = "1.0.0"
    APP_URL = "http://localhost:8501"
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent  # Project root directory
    RESOURCES_DIR = BASE_DIR / "resources"
    BACKUPS_DIR = BASE_DIR / "backups"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./config/sqlite_database.db")
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key-in-production")
    SESSION_TIMEOUT_MINUTES = int(os.getenv("SESSION_TIMEOUT_MINUTES", "30"))
    MAX_LOGIN_ATTEMPTS = 5
    LOCKOUT_DURATION_MINUTES = 15
    
    # File Upload
    MAX_UPLOAD_SIZE_MB = 10
    ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/jpg", "image/png"]
    
    # Face Detection
    FACE_LANDMARKER_PATH = BASE_DIR / "config" / "face_landmarker.task"
    DEFAULT_MATCH_THRESHOLD = 3.0
    MIN_MATCH_THRESHOLD = 0.5
    MAX_MATCH_THRESHOLD = 5.0
    
    # Email (if configured)
    SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
    EMAIL_FROM = os.getenv("EMAIL_FROM", SMTP_USERNAME)
    
    # UI Settings
    ITEMS_PER_PAGE = 10
    MAP_DEFAULT_ZOOM = 5
    MAP_DEFAULT_CENTER = [20.5937, 78.9629]  # India center
    
    @classmethod
    def ensure_directories(cls):
        """Create necessary directories if they don't exist"""
        cls.RESOURCES_DIR.mkdir(exist_ok=True)
        cls.BACKUPS_DIR.mkdir(exist_ok=True)
        cls.LOGS_DIR.mkdir(exist_ok=True)
    
    @classmethod
    def load_login_config(cls) -> dict:
        """Load login configuration from YAML file"""
        config_path = cls.BASE_DIR / "login_config.yml"
        try:
            with open(config_path, 'r') as file:
                return yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file '{config_path}' not found")
    

    
    @classmethod
    def is_email_configured(cls) -> bool:
        """Check if email is properly configured"""
        return bool(cls.SMTP_USERNAME and cls.SMTP_PASSWORD)


# Create directories on import
Config.ensure_directories()


# UI Theme Configuration
class Theme:
    """UI theme colors and styles"""
    
    # Primary Colors
    PRIMARY_COLOR = "#1565c0"
    PRIMARY_DARK = "#0d47a1"
    PRIMARY_LIGHT = "#667eea"
    
    # Secondary Colors
    SECONDARY_COLOR = "#764ba2"
    ACCENT_COLOR = "#4ecdc4"
    
    # Status Colors
    SUCCESS_COLOR = "#27ae60"
    WARNING_COLOR = "#f39c12"
    ERROR_COLOR = "#e74c3c"
    INFO_COLOR = "#3498db"
    
    # Role Colors
    ADMIN_COLOR = "#ff6b6b"
    PUBLIC_COLOR = "#4ecdc4"
    
    # Background
    BACKGROUND_GRADIENT = "linear-gradient(135deg, rgba(102, 126, 234, 0.7) 0%, rgba(118, 75, 162, 0.7) 100%)"
    
    # Text
    TEXT_PRIMARY = "#1a237e"
    TEXT_SECONDARY = "#546e7a"
    TEXT_LIGHT = "#ffffff"
    
    # Shadows
    SHADOW_LIGHT = "0 4px 20px rgba(0, 0, 0, 0.15)"
    SHADOW_MEDIUM = "0 8px 32px rgba(0, 0, 0, 0.15)"
    SHADOW_HEAVY = "0 12px 40px rgba(0, 0, 0, 0.2)"


# Messages Configuration
class Messages:
    """Standard messages used throughout the application"""
    
    # Success Messages
    LOGIN_SUCCESS = "✅ Login successful! Welcome back."
    CASE_REGISTERED = "✅ Case registered successfully!"
    CASE_UPDATED = "✅ Case updated successfully!"
    CASE_DELETED = "✅ Case deleted successfully!"
    MATCH_FOUND = "🎉 Match found! Both records marked as 'Found'."
    
    # Error Messages
    LOGIN_FAILED = "❌ Invalid username or password. Please try again."
    NO_FACE_DETECTED = "👤 No face detected in the image. Please upload a clear photo with a visible face."
    UPLOAD_REQUIRED = "📷 Please upload a photo to continue."
    FIELDS_REQUIRED = "⚠️ Please fill in all required fields."
    DATABASE_ERROR = "🗄️ Database error occurred. Please try again."
    PERMISSION_DENIED = "🔒 You don't have permission to perform this action."
    SESSION_EXPIRED = "⏰ Your session has expired. Please login again."
    
    # Info Messages
    NO_CASES_FOUND = "ℹ️ No cases found."
    NO_MATCHES_FOUND = "🤷‍♂️ No matches found with current threshold. Try adjusting the threshold or adding more cases."
    PROCESSING = "⏳ Processing... Please wait."
    
    # Warning Messages
    CONFIRM_DELETE = "⚠️ Are you sure you want to delete this case? This action cannot be undone."
    CONFIRM_RESET = "⚠️ This will reset all found cases to 'Not Found'. Click again to confirm."
    DEFAULT_PASSWORD = "⚠️ You are using a default password. Please change it immediately for security."
