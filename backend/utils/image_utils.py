import os
import sys
import urllib.request

# Set environment variables BEFORE importing any libraries
os.environ['OPENCV_IO_ENABLE_OPENEXR'] = '0'
os.environ['OPENCV_IO_ENABLE_JASPER'] = '0'
os.environ['OPENCV_VIDEOIO_PRIORITY_MSMF'] = '0'

# Force software rendering for MediaPipe to avoid GPU/OpenGL issues
os.environ['MEDIAPIPE_DISABLE_GPU'] = '1'
os.environ['GLOG_minloglevel'] = '2'  # Suppress MediaPipe warnings

# Software rendering configuration for better Linux/WSL compatibility
os.environ['MESA_GL_VERSION_OVERRIDE'] = '4.1'
os.environ['MESA_GLSL_VERSION_OVERRIDE'] = '410'
os.environ['LIBGL_ALWAYS_INDIRECT'] = '1'  # Force indirect rendering on Linux
os.environ['GALLIUM_DRIVER'] = 'llvmpipe'  # Use LLVM pipe for software rendering

import cv2
import PIL
import PIL.ImageDraw
import numpy as np
import streamlit as st

# Try to import mediapipe with fallback handling
try:
    import mediapipe as mp
    from mediapipe.tasks import python as mp_python
    from mediapipe.tasks.python import vision as mp_vision
    MEDIAPIPE_AVAILABLE = True
except Exception as e:
    MEDIAPIPE_AVAILABLE = False
    MEDIAPIPE_ERROR = str(e)

# Configure OpenCV to avoid GUI dependencies
cv2.setUseOptimized(True)

_MODEL_PATH = "config/face_landmarker.task"
_MODEL_URL = (
    "https://storage.googleapis.com/mediapipe-models/"
    "face_landmarker/face_landmarker/float16/1/face_landmarker.task"
)


def _ensure_model():
    if not os.path.exists(_MODEL_PATH):
        with st.spinner("Downloading face landmarker model (one-time, ~30 MB)..."):
            urllib.request.urlretrieve(_MODEL_URL, _MODEL_PATH)


def _ensure_model_silent():
    if not os.path.exists(_MODEL_PATH):
        urllib.request.urlretrieve(_MODEL_URL, _MODEL_PATH)


def _build_detector(num_faces: int = 5):
    if not MEDIAPIPE_AVAILABLE:
        st.error(f"❌ MediaPipe is not available: {MEDIAPIPE_ERROR}")
        st.error("This may be due to missing system libraries. Please check the troubleshooting section in README.md")
        raise RuntimeError(f"MediaPipe not available: {MEDIAPIPE_ERROR}")
    
    try:
        base_options = mp_python.BaseOptions(model_asset_path=_MODEL_PATH)
        options = mp_vision.FaceLandmarkerOptions(
            base_options=base_options,
            num_faces=num_faces,
            output_face_blendshapes=False,
            output_facial_transformation_matrixes=False,
        )
        return mp_vision.FaceLandmarker.create_from_options(options)
    except Exception as e:
        error_msg = str(e)
        if "libGLESv2" in error_msg or "libGL" in error_msg:
            st.error(f"❌ OpenGL library missing: {error_msg}")
            st.info("**Quick Fix:** Run this command in your terminal:")
            st.code("sudo apt-get update && sudo apt-get install -y libgles2-mesa libgles2-mesa-dev libgl1-mesa-glx", language="bash")
            st.error("After installation, restart the application.")
        else:
            st.error(f"Failed to initialize face detector: {error_msg}")
            st.error("This may be due to missing system libraries. Please check the troubleshooting section in README.md")
        raise e


def _normalize_image(image: np.ndarray) -> np.ndarray:
    if image.dtype != np.uint8:
        image = image.astype(np.uint8)
    if image.ndim == 2:
        image = np.stack([image] * 3, axis=-1)
    elif image.shape[2] == 4:
        image = image[:, :, :3]
    return image


def image_obj_to_numpy(image_obj) -> np.ndarray:
    """Convert a Streamlit-uploaded image object to an RGB numpy array."""
    image = PIL.Image.open(image_obj).convert("RGB")
    return np.array(image)


def detect_all_faces(image: np.ndarray, max_faces: int = 5):
    """
    Detect up to max_faces in an image.

    Returns a list of dicts, one per detected face:
        {
            "landmarks": [x1,y1,z1, x2,y2,z2, ...],   # flattened, normalised
            "bbox": (x_min, y_min, x_max, y_max),      # pixel coords
        }
    Returns an empty list if no faces are found.
    """
    _ensure_model()
    image = _normalize_image(image)
    h, w = image.shape[:2]

    try:
        detector = _build_detector(num_faces=max_faces)
        if not MEDIAPIPE_AVAILABLE:
            return []
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
        result = detector.detect(mp_image)
        detector.close()
    except Exception as e:
        error_msg = str(e)
        if "libGLESv2" in error_msg or "libGL" in error_msg:
            st.error("❌ **Face detection failed due to missing OpenGL libraries**")
            st.info("""
**Quick Fix for Linux/WSL:**
```bash
sudo apt-get update && sudo apt-get install -y libgles2-mesa libgles2-mesa-dev libgl1-mesa-glx libglib2.0-0
```
After installation, restart the application.

**For detailed troubleshooting:**
See `docs/LINUX_WSL_SETUP.md` for comprehensive setup instructions.
            """)
        else:
            st.error(f"❌ Face detection failed: {error_msg}")
            st.warning("""
This may be due to missing system libraries. If you're on Linux/WSL:
1. Check `docs/LINUX_WSL_SETUP.md` for detailed setup instructions
2. Run the verification script: `python scripts/verify_setup.py`
            """)
        return []

    faces = []
    for lm_list in result.face_landmarks:
        xs = [lm.x * w for lm in lm_list]
        ys = [lm.y * h for lm in lm_list]
        padding = 0.08 * max(w, h)
        bbox = (
            max(0, int(min(xs) - padding)),
            max(0, int(min(ys) - padding)),
            min(w, int(max(xs) + padding)),
            min(h, int(max(ys) + padding)),
        )
        landmarks_flat = [coord for lm in lm_list for coord in (lm.x, lm.y, lm.z)]
        faces.append({"landmarks": landmarks_flat, "bbox": bbox})
    return faces


# Distinct colours for up to 5 faces (unselected state)
_FACE_COLORS = [
    (255, 200, 0),  # yellow
    (0, 180, 255),  # cyan
    (255, 100, 0),  # orange
    (180, 0, 255),  # purple
    (255, 0, 150),  # pink
]
_SELECTED_COLOR = (50, 220, 80)  # green
_UNSELECTED_DIM = (160, 160, 160)  # grey when another face is selected


def draw_face_boxes(
    image_numpy: np.ndarray, faces: list, selected_idx: int = None
) -> PIL.Image.Image:
    """
    Draw labelled bounding boxes around detected faces.

    - Single face: one green box labelled "Face detected"
    - Multiple faces, nothing selected: each box gets a distinct colour + number
    - Multiple faces, one selected: selected = bright green, others = grey + number
    """
    img = PIL.Image.fromarray(_normalize_image(image_numpy))
    draw = PIL.ImageDraw.Draw(img)
    n = len(faces)

    for i, face in enumerate(faces):
        x0, y0, x1, y1 = face["bbox"]
        box_w = max(1, (x1 - x0) // 200 + 2)  # line width scales with box size

        if n == 1:
            color = _SELECTED_COLOR
            label = "Face detected"
        elif selected_idx is None:
            color = _FACE_COLORS[i % len(_FACE_COLORS)]
            label = f"Face {i + 1}"
        elif i == selected_idx:
            color = _SELECTED_COLOR
            label = f"Face {i + 1} (selected)"
        else:
            color = _UNSELECTED_DIM
            label = f"Face {i + 1}"

        # Draw rounded-corner-ish box with a slightly thicker outline
        for offset in range(box_w):
            draw.rectangle(
                [x0 - offset, y0 - offset, x1 + offset, y1 + offset],
                outline=color,
            )

        # Label background + text
        font_size = max(12, (y1 - y0) // 8)
        text_x, text_y = x0, max(0, y0 - font_size - 4)
        draw.rectangle(
            [
                text_x,
                text_y,
                text_x + len(label) * font_size // 2 + 8,
                text_y + font_size + 4,
            ],
            fill=color,
        )
        draw.text((text_x + 4, text_y + 2), label, fill=(0, 0, 0))

    return img


# ── Single-face helper (kept for mobile_app compatibility) ────────────────────


def extract_face_mesh_landmarks(image: np.ndarray):
    """
    Extract face mesh landmarks for exactly one face.
    Shows a Streamlit error if none found. Returns None on failure.
    """
    faces = detect_all_faces(image, max_faces=1)
    if not faces:
        st.error(
            "❌ No face detected in this image.\n\n"
            "**Tips for a better result:**\n"
            "- Ensure the face is clearly visible and not obscured\n"
            "- Use good lighting — avoid dark or back-lit photos\n"
            "- Use a front-facing photo where possible"
        )
        return None
    return faces[0]["landmarks"]


# ── Frame-level helper (video) ────────────────────────────────────────────────


def extract_face_mesh_from_frame(frame_rgb: np.ndarray):
    """Silent version for batch/video use. Returns landmarks or None."""
    _ensure_model_silent()
    frame_rgb = _normalize_image(frame_rgb)
    try:
        detector = _build_detector(num_faces=1)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        result = detector.detect(mp_image)
        detector.close()
        if result.face_landmarks:
            lm_list = result.face_landmarks[0]
            return [coord for lm in lm_list for coord in (lm.x, lm.y, lm.z)]
        return None
    except Exception:
        return None


def _cosine_distance(a: list, b: list) -> float:
    a, b = np.array(a), np.array(b)
    denom = np.linalg.norm(a) * np.linalg.norm(b)
    if denom == 0:
        return 1.0
    return 1.0 - float(np.dot(a, b) / denom)


def extract_unique_faces_from_video(
    video_path: str,
    frame_interval: int = 15,
    similarity_threshold: float = 0.05,
):
    """
    Extract unique face landmarks from a video file.
    Returns list of (landmarks, frame_rgb) tuples — one per unique face.
    """
    _ensure_model_silent()
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        return []

    unique_faces = []
    frame_idx = 0
    while True:
        ret, frame_bgr = cap.read()
        if not ret:
            break
        if frame_idx % frame_interval == 0:
            frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
            landmarks = extract_face_mesh_from_frame(frame_rgb)
            if landmarks is not None:
                is_duplicate = any(
                    _cosine_distance(landmarks, ex_lm) < similarity_threshold
                    for ex_lm, _ in unique_faces
                )
                if not is_duplicate:
                    unique_faces.append((landmarks, frame_rgb))
        frame_idx += 1

    cap.release()
    return unique_faces
