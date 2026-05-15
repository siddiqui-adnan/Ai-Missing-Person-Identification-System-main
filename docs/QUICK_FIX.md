# ⚡ Quick Fix - OpenGL Library Errors

If you see these errors, you're in the right place:
```
libGLESv2.so.2: cannot open shared object file
libGL.so.1: cannot open shared object file
Face detection failed
```

---

## 🚀 One-Command Fix (Linux/WSL)

```bash
sudo apt-get update && sudo apt-get install -y libgles2-mesa libgles2-mesa-dev libgl1-mesa-glx libglib2.0-0 libxext6 libxrender1
```

Then restart your application:
```bash
python -m streamlit run Home.py
```

---

## ✅ Verify It Works

Run this command:
```bash
python scripts/verify_setup.py
```

You should see: **✅ All checks passed!**

---

## 📋 If That Doesn't Work

1. **Check your Linux distribution:**
   ```bash
   lsb_release -a
   # or
   cat /etc/os-release
   ```

2. **Follow the full guide:** [docs/LINUX_WSL_SETUP.md](docs/LINUX_WSL_SETUP.md)

3. **Test MediaPipe specifically:**
   ```bash
   python scripts/test_all_components.py
   ```

---

## 🐧 Linux Distribution Specific

### Ubuntu/Debian
```bash
sudo apt-get update
sudo apt-get install -y libgles2-mesa libgles2-mesa-dev libgl1-mesa-glx libglib2.0-0
```

### Fedora/RHEL/CentOS
```bash
sudo dnf install -y mesa-libGLES mesa-libGLES-devel libglvnd-glx mesa-libGL-devel
```

### Arch Linux
```bash
sudo pacman -S mesa lib32-mesa glib2
```

---

## 💡 Pro Tips

- **For WSL2:** GPU support is available - see full guide for setup
- **For slow performance:** Your system is using CPU rendering (normal after fix)
- **For older Linux:** Try installing `mesa-utils` package first

---

## 🆘 Still Stuck?

1. Run: `python scripts/verify_setup.py` - copy the full output
2. Check: `docs/LINUX_WSL_SETUP.md` - section "Still Having Issues"
3. Check: GitHub issues or documentation for your specific Linux version

**You're almost there!** 🎉
