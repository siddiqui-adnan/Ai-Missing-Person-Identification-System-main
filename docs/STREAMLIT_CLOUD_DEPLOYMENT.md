# 🚀 Streamlit Cloud Deployment Guide

This guide covers deploying the AI Missing Person Identification System on Streamlit Cloud.

---

## ✅ Prerequisites

1. GitHub account with repository containing the code
2. Streamlit Cloud account (free tier available at streamlit.io)
3. All files in version control (`.git` is tracked)

---

## 📋 Deployment Checklist

### 1. Verify Local Files Are Correct

Ensure these files exist in your repository root:

```bash
cat packages.txt
cat requirements.txt
ls -la .streamlit/config.toml
```

### 2. Commit All Changes

```bash
git add -A
git commit -m "Configure for Streamlit Cloud deployment"
git push origin main
```

### 3. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository and `Home.py` as the main file
4. Click "Deploy"

You should see: **Your app is running** in 2-3 minutes

---

## 🔧 Key Configuration Files

### `packages.txt`
System-level dependencies (installed before Python packages):

```
libglib2.0-0
libsm6
libxext6
libxrender-dev
libgomp1
libgl1-mesa-glx
python3-opencv
```

These are required for:
- OpenCV (cv2) to function
- MediaPipe face detection
- Image processing libraries

### `requirements.txt`
Python packages with version ranges (not exact pins):

```
streamlit>=1.28.0,<2.0
opencv-python-headless>=4.8.0,<5.0
mediapipe>=0.10.0,<1.0
pandas>=2.1.0,<3.0
...
```

**Why version ranges?** Streamlit Cloud needs flexibility to find compatible binary wheels for the Ubuntu environment.

### `.streamlit/config.toml`
Streamlit configuration for cloud:

```toml
[server]
headless = true
port = 8501
enableXsrfProtection = true
enableCORS = false
```

**Note:** Removed `serverAddress = "localhost"` (local-only setting)

---

## 🐛 Common Deployment Issues

### Issue 1: "installer returned a non-zero exit code"

**Cause:** Package versions can't be found on cloud platform

**Solution:**
- Use version ranges: `package>=X.Y.Z,<X+1` instead of exact pins
- Remove unused packages from requirements.txt
- Verify packages.txt has all system dependencies

### Issue 2: "libGL.so.1 not found" or "libGLESv2 not found"

**Cause:** Missing system libraries for OpenCV/MediaPipe

**Solution:** Check `packages.txt` includes:
```
libgl1-mesa-glx
libglib2.0-0
```

### Issue 3: "ModuleNotFoundError: No module named cv2"

**Cause:** OpenCV failed to import due to missing system libs

**Solution:**
1. Verify `packages.txt` exists at repository root
2. Verify using `opencv-python-headless` (not `opencv-python`)
3. Check requirements.txt has: `opencv-python-headless>=4.8.0,<5.0`

### Issue 4: Memory error or timeout during deployment

**Cause:** Installing too many heavy packages

**Solution:**
- Remove unused dependencies (cryptography, validators, bleach, jinja2)
- Use minimal Streamlit (>1.28.0)
- Reduce numpy/pandas version specificity

---

## 📊 Deployment Stages

```
1. Repository connected ✅
   └─ Install build tools & system packages (from packages.txt)

2. System dependencies installed ✅
   └─ Install Python packages (from requirements.txt)

3. Python packages installed ✅
   └─ Download assets (face_landmarker.task model)

4. App booting ✅
   └─ Run Home.py startup script

5. App running 🎉
   └─ Your app is live!
```

Each stage logs to: **"Manage app" → View logs** in Streamlit Cloud

---

## 🔍 Debugging Deployment

### View Live Logs
1. Go to your app on Streamlit Cloud
2. Click "Manage app" (top right, three dots)
3. Click "View logs"
4. Look for errors at the "App running" stage

### Check Package Installation
The logs will show:
```
Installing dependencies from requirements.txt
Installing system packages from packages.txt
```

If you see "Collecting [package]" but no "Successfully installed", that's the problem.

### Test Locally First
Before deploying, test on your local machine:

```bash
# Simulate cloud environment
python -m pip install -r requirements.txt
python -m streamlit run Home.py
```

If it works locally but not on cloud, check:
1. `packages.txt` is in repository root
2. `.streamlit/config.toml` has no local-only settings
3. `requirements.txt` uses version ranges

---

## ✨ Optimization Tips

### 1. Cold Start Performance
- Models cache after first deployment
- First launch is slowest (downloads face_landmarker.task)
- Subsequent launches are ~2-3 seconds

### 2. Reduce Deployment Time
- Smaller requirements = faster deployment
- Remove unused packages
- Use compatible versions that have precompiled wheels

### 3. Monitor Resource Usage
- Streamlit Cloud free tier has memory limits
- Face detection is CPU-intensive but shouldn't timeout
- If slow: Consider caching results with `@st.cache_data`

---

## 📝 Manual Configuration

If auto-deployment fails:

1. **Create packages.txt:**
```bash
echo "libglib2.0-0" > packages.txt
echo "libsm6" >> packages.txt
echo "libxext6" >> packages.txt
echo "libgl1-mesa-glx" >> packages.txt
```

2. **Create .streamlit/config.toml:**
```bash
mkdir -p .streamlit
cat > .streamlit/config.toml << 'EOF'
[server]
headless = true
port = 8501
EOF
```

3. **Update requirements.txt:**
```bash
# Remove: jinja2, cryptography, validators, bleach
# Change exact versions to ranges (>=1.0.0,<2.0)
```

4. **Commit & Push:**
```bash
git add -A
git commit -m "Fix cloud deployment"
git push
```

---

## 🚀 Deployment Success Checklist

- [ ] All files pushed to GitHub
- [ ] `packages.txt` exists in repository root
- [ ] `.streamlit/config.toml` exists
- [ ] `requirements.txt` uses version ranges
- [ ] No local-only paths in code
- [ ] No hardcoded credentials (use environment variables)
- [ ] Face detection works on local machine
- [ ] App launches without errors

---

## 📚 Useful Resources

- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-cloud)
- [Streamlit Config Reference](https://docs.streamlit.io/library/advanced-features/configuration)
- [MediaPipe on Cloud](https://developers.google.com/mediapipe/framework/getting_started/install)

---

**Last Updated:** May 2026  
**For Issues:** Check app logs on Streamlit Cloud → Manage app → View logs
