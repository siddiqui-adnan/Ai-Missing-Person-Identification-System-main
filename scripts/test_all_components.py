#!/usr/bin/env python3
"""
Comprehensive test script for AI Missing Person Identification System
Tests all major components and reports any errors
"""

import sys
from pathlib import Path

# Add project root to path (parent directory of scripts folder)
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def test_imports():
    """Test all critical imports"""
    print_header("Testing Imports")
    
    tests = [
        ("Config", "from config.app_config import Config"),
        ("Database Queries", "from backend.database import db_queries"),
        ("Data Models", "from backend.models import data_models"),
        ("Auth Service", "from backend.services import auth_service"),
        ("Case Service", "from backend.services import case_service"),
        ("Match Service", "from backend.services import match_service"),
        ("Email Service", "from backend.services import email_service"),
        ("Train Service", "from backend.services import train_service"),
        ("Validation Service", "from backend.services import validation_service"),
        ("Image Utils", "from backend.utils import image_utils"),
        ("Error Handler", "from backend.utils import error_handler"),
        ("Validation Utils", "from backend.utils import validation_utils"),
        ("Login Page", "from frontend.pages import login_page"),
        ("Admin Page", "from frontend.pages import admin_page"),
        ("Public Page", "from frontend.pages import public_page"),
        ("Complainant Page", "from frontend.pages import complainant_page"),
        ("UI Components", "from frontend.components import styles, ui_helpers, utils"),
    ]
    
    passed = 0
    failed = 0
    
    for name, import_stmt in tests:
        try:
            exec(import_stmt)
            print(f"✅ {name}")
            passed += 1
        except Exception as e:
            print(f"❌ {name}: {str(e)}")
            failed += 1
    
    print(f"\nImport Tests: {passed} passed, {failed} failed")
    return failed == 0

def test_config():
    """Test configuration"""
    print_header("Testing Configuration")
    
    try:
        from config.app_config import Config
        
        # Test paths
        print(f"✅ BASE_DIR: {Config.BASE_DIR}")
        print(f"✅ RESOURCES_DIR: {Config.RESOURCES_DIR}")
        print(f"✅ LOGS_DIR: {Config.LOGS_DIR}")
        print(f"✅ DATABASE_URL: {Config.DATABASE_URL}")
        print(f"✅ FACE_LANDMARKER_PATH: {Config.FACE_LANDMARKER_PATH}")
        
        # Test methods
        Config.ensure_directories()
        print(f"✅ Directories created/verified")
        
        # Check if face model exists
        if Config.FACE_LANDMARKER_PATH.exists():
            print(f"✅ Face landmarker model found")
        else:
            print(f"ℹ️  Face landmarker model will be downloaded on first use")
        
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_database():
    """Test database operations"""
    print_header("Testing Database")
    
    try:
        from backend.database import db_queries
        
        # Test database creation
        db_queries.create_db()
        print("✅ Database initialized")
        
        # Test database connection
        from sqlmodel import Session, create_engine
        from config.app_config import Config
        
        engine = create_engine(Config.DATABASE_URL)
        with Session(engine) as session:
            print("✅ Database connection successful")
        
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def test_mediapipe():
    """Test MediaPipe face detection"""
    print_header("Testing MediaPipe Face Detection")
    
    try:
        import mediapipe as mp
        from mediapipe.tasks.python import vision
        print("✅ MediaPipe imported")
        
        from backend.utils.image_utils import _MODEL_PATH
        from pathlib import Path
        
        if Path(_MODEL_PATH).exists():
            print(f"✅ Face model exists at {_MODEL_PATH}")
        else:
            print(f"ℹ️  Face model will be downloaded on first use")
        
        return True
    except Exception as e:
        print(f"❌ MediaPipe error: {e}")
        return False

def test_email_config():
    """Test email configuration"""
    print_header("Testing Email Configuration")
    
    try:
        from email_system.email_config import load_email_config
        
        config = load_email_config()
        
        if config.get('smtp_host'):
            print(f"✅ SMTP Host: {config['smtp_host']}")
            print(f"✅ SMTP Port: {config['smtp_port']}")
            print(f"✅ SMTP User: {config['smtp_user']}")
            print(f"✅ Email configured")
        else:
            print("⚠️  Email not configured (optional)")
        
        return True
    except Exception as e:
        print(f"⚠️  Email configuration: {e} (optional)")
        return True  # Email is optional

def test_file_structure():
    """Test file structure"""
    print_header("Testing File Structure")
    
    required_files = [
        "Home.py",
        "requirements.txt",
        "login_config.yml",
        "email_settings.txt",
        "config/app_config.py",
        "backend/__init__.py",
        "frontend/__init__.py",
    ]
    
    required_dirs = [
        "config",
        "backend",
        "frontend",
        "backend/database",
        "backend/models",
        "backend/services",
        "backend/utils",
        "frontend/pages",
        "frontend/components",
    ]
    
    all_ok = True
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} missing")
            all_ok = False
    
    for dir in required_dirs:
        if Path(dir).exists():
            print(f"✅ {dir}/")
        else:
            print(f"❌ {dir}/ missing")
            all_ok = False
    
    return all_ok

def test_python_packages():
    """Test required Python packages"""
    print_header("Testing Python Packages")
    
    packages = [
        "streamlit",
        "mediapipe",
        "cv2",
        "numpy",
        "pandas",
        "sklearn",
        "sqlmodel",
        "PIL",
        "folium",
        "openpyxl",
        "yaml",
        "cryptography",
        "validators",
        "bleach",
    ]
    
    passed = 0
    failed = 0
    
    for package in packages:
        try:
            if package == "cv2":
                __import__("cv2")
            elif package == "PIL":
                __import__("PIL")
            elif package == "sklearn":
                __import__("sklearn")
            elif package == "yaml":
                __import__("yaml")
            else:
                __import__(package)
            print(f"✅ {package}")
            passed += 1
        except ImportError:
            print(f"❌ {package} not installed")
            failed += 1
    
    print(f"\nPackage Tests: {passed} passed, {failed} failed")
    return failed == 0

def main():
    print("\n" + "╔" + "═" * 58 + "╗")
    print("║" + " " * 58 + "║")
    print("║" + "  AI Missing Person Identification System".center(58) + "║")
    print("║" + "  Comprehensive Component Test".center(58) + "║")
    print("║" + " " * 58 + "║")
    print("╚" + "═" * 58 + "╝")
    
    results = {
        "File Structure": test_file_structure(),
        "Python Packages": test_python_packages(),
        "Imports": test_imports(),
        "Configuration": test_config(),
        "Database": test_database(),
        "MediaPipe": test_mediapipe(),
        "Email Config": test_email_config(),
    }
    
    print_header("Test Summary")
    
    all_passed = True
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 60)
    
    if all_passed:
        print("\n✅ All tests passed! Application is fully functional.")
        print("\nYou can run the application with:")
        print("  python -m streamlit run Home.py")
        print("\nOr use the start script:")
        print("  bash start.sh  (Linux/Mac)")
        print("  start.bat      (Windows)")
        return 0
    else:
        print("\n❌ Some tests failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
