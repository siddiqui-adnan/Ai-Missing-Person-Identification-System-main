#!/usr/bin/env python3
"""
System diagnostics and verification script for Linux/WSL face detection setup.
Run this to verify all dependencies are properly installed.
"""

import sys
import subprocess
import os
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8+"""
    print("🔍 Python Version Check")
    version = sys.version_info
    required = (3, 8)
    if version >= required:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (Required: 3.8+)")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor} (Required: 3.8+)")
        return False


def check_system_libraries():
    """Check if required OpenGL libraries are installed"""
    print("\n🔍 System Libraries Check (Linux/WSL Only)")
    
    if sys.platform != 'linux':
        print("   ⓘ Not on Linux/WSL - skipping")
        return True
    
    libraries = {
        'libGLESv2.so.2': 'OpenGL ES 2.0',
        'libGL.so.1': 'OpenGL Core',
        'libglib2.0.so.0': 'GLib 2.0',
        'libxrender.so.1': 'X Render',
    }
    
    all_found = True
    for lib_name, lib_desc in libraries.items():
        try:
            result = subprocess.run(
                ['ldconfig', '-p'],
                capture_output=True,
                text=True,
                timeout=5
            )
            if lib_name in result.stdout:
                print(f"   ✅ {lib_name:20} - {lib_desc}")
            else:
                print(f"   ❌ {lib_name:20} - {lib_desc} (NOT FOUND)")
                all_found = False
        except Exception as e:
            print(f"   ⚠️  {lib_name:20} - Unable to verify")
    
    return all_found


def check_python_packages():
    """Check if required Python packages are installed"""
    print("\n🔍 Python Packages Check")
    
    packages = {
        'streamlit': 'Web UI framework',
        'mediapipe': 'Face detection & tracking',
        'opencv-python': 'Image processing',
        'numpy': 'Numerical computing',
        'pandas': 'Data manipulation',
        'pillow': 'Image library',
        'sqlmodel': 'Database ORM',
    }
    
    all_found = True
    for package_name, description in packages.items():
        try:
            __import__(package_name)
            
            # Try to get version
            try:
                if package_name == 'pillow':
                    import PIL
                    version = PIL.__version__
                elif package_name == 'sqlmodel':
                    import sqlmodel
                    version = sqlmodel.__version__
                else:
                    module = __import__(package_name)
                    version = getattr(module, '__version__', 'unknown')
            except:
                version = 'installed'
            
            print(f"   ✅ {package_name:20} - {description:25} ({version})")
        except ImportError:
            print(f"   ❌ {package_name:20} - {description:25} (NOT INSTALLED)")
            all_found = False
    
    return all_found


def check_mediapipe_setup():
    """Test if MediaPipe can be initialized"""
    print("\n🔍 MediaPipe Face Detection Test")
    
    try:
        # Try importing MediaPipe
        import mediapipe as mp
        from mediapipe.tasks import python as mp_python
        from mediapipe.tasks.python import vision as mp_vision
        
        print("   ✅ MediaPipe imports successful")
        
        # Check if model file exists
        model_path = Path('config/face_landmarker.task')
        if model_path.exists():
            print(f"   ✅ Model file exists: {model_path} ({model_path.stat().st_size / 1024 / 1024:.1f} MB)")
        else:
            print(f"   ⓘ Model file will be downloaded on first use: {model_path}")
        
        # Try to create detector (without image)
        try:
            from backend.utils.image_utils import _build_detector
            detector = _build_detector(num_faces=1)
            detector.close()
            print("   ✅ Face detector initialization successful")
            return True
        except Exception as e:
            error_msg = str(e)
            if 'libGL' in error_msg or 'libGLES' in error_msg:
                print(f"   ❌ OpenGL library error: {error_msg}")
                print("      Run: sudo apt-get install -y libgles2-mesa libgles2-mesa-dev libgl1-mesa-glx")
                return False
            else:
                print(f"   ⚠️  {error_msg}")
                return False
    
    except ImportError as e:
        print(f"   ❌ MediaPipe import failed: {e}")
        print("      Run: pip install mediapipe")
        return False
    except Exception as e:
        print(f"   ❌ Unexpected error: {e}")
        return False


def check_environment_variables():
    """Display relevant environment variables"""
    print("\n🔍 Environment Variables (for debugging)")
    
    env_vars = [
        'MEDIAPIPE_DISABLE_GPU',
        'MESA_GL_VERSION_OVERRIDE',
        'MESA_GLSL_VERSION_OVERRIDE',
        'LIBGL_ALWAYS_INDIRECT',
        'GALLIUM_DRIVER',
    ]
    
    for var in env_vars:
        value = os.environ.get(var, '(not set)')
        print(f"   {var:30} = {value}")


def check_disk_space():
    """Check if there's enough disk space"""
    print("\n🔍 Disk Space Check")
    
    try:
        import shutil
        total, used, free = shutil.disk_usage('.')
        free_gb = free / (1024 ** 3)
        
        if free_gb > 1:
            print(f"   ✅ Free disk space: {free_gb:.1f} GB (OK)")
            return True
        else:
            print(f"   ⚠️  Free disk space: {free_gb:.2f} GB (Low - may cause issues)")
            return False
    except Exception as e:
        print(f"   ⓘ Unable to check disk space: {e}")
        return True


def main():
    """Run all checks"""
    print("=" * 70)
    print("🔧 AI Missing Person System - Setup Verification")
    print("=" * 70)
    
    checks = [
        check_python_version,
        check_system_libraries,
        check_python_packages,
        check_mediapipe_setup,
        check_disk_space,
    ]
    
    results = []
    for check in checks:
        try:
            result = check()
            results.append(result)
        except Exception as e:
            print(f"\n❌ Error during check: {e}")
            results.append(False)
    
    check_environment_variables()
    
    print("\n" + "=" * 70)
    if all(results):
        print("✅ All checks passed! You're ready to run the application:")
        print("   python -m streamlit run Home.py")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
        print("   For Linux/WSL: See docs/LINUX_WSL_SETUP.md")
        sys.exit(1)
    print("=" * 70)


if __name__ == '__main__':
    main()
