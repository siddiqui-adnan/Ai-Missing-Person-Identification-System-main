"""
Error handling and logging utilities for the Missing Person Identification System
"""

import logging
import traceback
import re
import html
import shutil
from datetime import datetime
from functools import wraps
from pathlib import Path
import streamlit as st

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


class AppError(Exception):
    """Base exception class for application errors"""
    def __init__(self, message, error_code=None):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class DatabaseError(AppError):
    """Exception for database-related errors"""
    pass


class AuthenticationError(AppError):
    """Exception for authentication-related errors"""
    pass


class ValidationError(AppError):
    """Exception for data validation errors"""
    pass


class FaceDetectionError(AppError):
    """Exception for face detection errors"""
    pass


def handle_errors(func):
    """
    Decorator to handle errors gracefully in Streamlit functions
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except DatabaseError as e:
            logger.error(f"Database error in {func.__name__}: {str(e)}")
            st.error(f"🗄️ Database Error: {e.message}")
            st.info("Please try again or contact support if the issue persists.")
        except AuthenticationError as e:
            logger.warning(f"Authentication error in {func.__name__}: {str(e)}")
            st.error(f"🔐 Authentication Error: {e.message}")
        except ValidationError as e:
            logger.warning(f"Validation error in {func.__name__}: {str(e)}")
            st.warning(f"⚠️ Validation Error: {e.message}")
        except FaceDetectionError as e:
            logger.error(f"Face detection error in {func.__name__}: {str(e)}")
            st.error(f"👤 Face Detection Error: {e.message}")
            st.info("Please ensure the photo contains a clear, front-facing face.")
        except Exception as e:
            logger.error(f"Unexpected error in {func.__name__}: {str(e)}\n{traceback.format_exc()}")
            st.error(f"❌ An unexpected error occurred: {str(e)}")
    return wrapper


def log_user_action(action, user=None, details=None):
    """
    Log user actions for audit trail
    
    Args:
        action (str): Description of the action
        user (str): Username performing the action
        details (dict): Additional details about the action
    """
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "user": user or "anonymous",
        "details": details or {}
    }
    logger.info(f"User Action: {log_entry}")


def validate_image(image_obj):
    """
    Validate uploaded image
    
    Args:
        image_obj: Streamlit uploaded file object
        
    Returns:
        bool: True if valid, raises ValidationError otherwise
    """
    if image_obj is None:
        raise ValidationError("No image uploaded")
    
    # Check file size (max 10MB)
    if image_obj.size > 10 * 1024 * 1024:
        raise ValidationError("Image size must be less than 10MB")
    
    # Check file type
    allowed_types = ['image/jpeg', 'image/jpg', 'image/png']
    if image_obj.type not in allowed_types:
        raise ValidationError("Only JPG, JPEG, and PNG images are allowed")
    
    return True


def sanitize_input(text):
    """
    Sanitize user input to prevent injection attacks
    
    Args:
        text (str): Input text to sanitize
        
    Returns:
        str: Sanitized text
    """
    if not text:
        return text
    
    # Remove potentially dangerous characters
    sanitized = html.escape(text)
    
    return sanitized


def check_session_timeout():
    """
    Check if user session has timed out
    
    Returns:
        bool: True if session is valid, False if timed out
    """
    if "last_activity" not in st.session_state:
        st.session_state["last_activity"] = datetime.now()
        return True
    
    # Default timeout: 30 minutes
    timeout_minutes = 30
    last_activity = st.session_state["last_activity"]
    time_diff = (datetime.now() - last_activity).total_seconds() / 60
    
    if time_diff > timeout_minutes:
        logger.info(f"Session timeout for user: {st.session_state.get('username', 'unknown')}")
        return False
    
    # Update last activity
    st.session_state["last_activity"] = datetime.now()
    return True


def create_backup(db_path="config/sqlite_database.db"):
    """
    Create a backup of the database
    
    Args:
        db_path (str): Path to the database file
    """
    try:
        backup_dir = Path("backups")
        backup_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"backup_{timestamp}.db"
        
        shutil.copy2(db_path, backup_path)
        logger.info(f"Database backup created: {backup_path}")
        return str(backup_path)
    except Exception as e:
        logger.error(f"Failed to create backup: {str(e)}")
        raise DatabaseError(f"Failed to create database backup: {str(e)}")


def get_system_health():
    """
    Check system health and return status
    
    Returns:
        dict: System health information
    """
    health = {
        "status": "healthy",
        "checks": {}
    }
    
    # Check database
    db_path = Path("config/sqlite_database.db")
    health["checks"]["database"] = {
        "exists": db_path.exists(),
        "size_mb": round(db_path.stat().st_size / (1024 * 1024), 2) if db_path.exists() else 0
    }
    
    # Check face landmarker model
    model_path = Path("config/face_landmarker.task")
    health["checks"]["face_model"] = {
        "exists": model_path.exists(),
        "size_mb": round(model_path.stat().st_size / (1024 * 1024), 2) if model_path.exists() else 0
    }
    
    # Check resources directory
    resources_path = Path("resources")
    health["checks"]["resources"] = {
        "exists": resources_path.exists(),
        "image_count": len(list(resources_path.glob("*.jpg"))) if resources_path.exists() else 0
    }
    
    # Determine overall status
    if not health["checks"]["database"]["exists"]:
        health["status"] = "critical"
    elif not health["checks"]["face_model"]["exists"]:
        health["status"] = "warning"
    
    return health
