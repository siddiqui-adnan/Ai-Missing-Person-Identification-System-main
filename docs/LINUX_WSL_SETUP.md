# 🐧 Linux/WSL Setup Guide for Face Detection

This guide solves common OpenGL library errors on Linux and Windows Subsystem for Linux (WSL).

---

## ⚠️ Common Errors Solved

```
libGLESv2.so.2: cannot open shared object file: No such file or directory
libGL.so.1: cannot open shared object file
Face detection failed
```

---

## 🔧 Installation Steps

### Step 1: Update System Packages
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### Step 2: Install Required OpenGL Libraries

**For Ubuntu/Debian:**
```bash
sudo apt-get install -y \
  libgles2-mesa \
  libgles2-mesa-dev \
  libgl1-mesa-glx \
  libgl1-mesa-dev \
  libglib2.0-0 \
  libxext6 \
  libxrender1
```

**For Fedora/RHEL/CentOS:**
```bash
sudo dnf install -y \
  mesa-libGLES \
  mesa-libGLES-devel \
  libglvnd-glx \
  mesa-libGL-devel
```

**For Arch Linux:**
```bash
sudo pacman -S mesa lib32-mesa glib2
```

### Step 3: Install Python Build Dependencies
```bash
sudo apt-get install -y \
  build-essential \
  python3-dev \
  libssl-dev \
  libffi-dev
```

### Step 4: Install Python Dependencies
```bash
pip install -r requirements.txt
```

If `pip install` fails, try:
```bash
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --no-cache-dir
```

---

## ✅ Verification

Test if face detection works:

```bash
python -c "
import sys
sys.path.insert(0, '.')
from backend.utils.image_utils import detect_all_faces
import numpy as np

# Create a test image
test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
result = detect_all_faces(test_image)
print('✅ Face detection initialized successfully!')
print(f'   Result: {len(result)} faces detected')
"
```

Expected output:
```
✅ Face detection initialized successfully!
   Result: 0 faces detected
```

---

## 🚀 Running the Application

### On Linux/WSL Terminal:
```bash
python -m streamlit run Home.py
```

### On Windows (if using WSL):
1. Open WSL terminal
2. Navigate to project folder
3. Run the command above
4. Open browser to `http://localhost:8501`

---

## 🤔 Troubleshooting

### Issue: "libGLESv2.so.2 not found" still appears
**Solution:**
```bash
# Check if libraries are installed
ldconfig -p | grep GLES
ldconfig -p | grep GL

# Re-install if missing
sudo apt-get install --reinstall libgles2-mesa libgles2-mesa-dev
```

### Issue: "ModuleNotFoundError: No module named mediapipe"
**Solution:**
```bash
pip install --upgrade mediapipe
```

### Issue: "Face detection fails but no error message"
**Solution:** Use verbose mode:
```bash
export GLOG_minloglevel=0
export MEDIAPIPE_DISABLE_GPU=1
python -m streamlit run Home.py
```

### Issue: Very slow on WSL (High CPU usage)
**Cause:** Software rendering is CPU-intensive
**Solution Options:**
- Use GPU acceleration (if available) by removing `MEDIAPIPE_DISABLE_GPU`
- Run on native Linux (faster than WSL)
- Install GPU drivers for your system

---

## 📋 System Requirements Check

Run this script to verify your setup:

```bash
python -c "
import subprocess
import sys

print('🔍 Checking system dependencies...')
print()

# Check OpenGL libraries
libs = ['libGLESv2.so.2', 'libGL.so.1', 'libglib2.0.so.0']
for lib in libs:
    try:
        result = subprocess.run(['ldconfig', '-p'], capture_output=True, text=True)
        if lib in result.stdout:
            print(f'✅ {lib} - found')
        else:
            print(f'❌ {lib} - NOT found')
    except:
        print(f'⚠️  {lib} - unable to verify')

print()
print('Python Packages:')
try:
    import mediapipe
    print(f'✅ mediapipe {mediapipe.__version__} - installed')
except:
    print('❌ mediapipe - NOT installed')

try:
    import streamlit
    print(f'✅ streamlit {streamlit.__version__} - installed')
except:
    print('❌ streamlit - NOT installed')

try:
    import cv2
    print(f'✅ opencv-python - installed')
except:
    print('❌ opencv-python - NOT installed')
"
```

---

## 🚨 Still Having Issues?

If problems persist:

1. **Check exact error message:**
   ```bash
   python -m streamlit run Home.py 2>&1 | head -50
   ```

2. **Try reinstalling MediaPipe:**
   ```bash
   pip uninstall -y mediapipe
   pip install mediapipe --no-cache-dir
   ```

3. **Check Python version (need 3.8+):**
   ```bash
   python --version
   ```

4. **Test MediaPipe directly:**
   ```bash
   python scripts/test_all_components.py
   ```

---

## 📚 Related Documentation

- [MediaPipe Installation Guide](https://developers.google.com/mediapipe/framework/getting_started/install)
- [OpenGL on Linux](https://www.mesa3d.org/)
- [WSL2 GPU Support](https://docs.microsoft.com/en-us/windows/ai/directml/gpu-cuda-in-wsl)

---

**Last Updated:** May 2026
**Tested On:** Ubuntu 22.04, WSL2, Debian 12
