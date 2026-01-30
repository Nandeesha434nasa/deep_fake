import os
import io
import cv2
import uvicorn
import numpy as np
import tempfile
from typing import Dict
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from tensorflow.keras.models import load_model
from PIL import Image

app = FastAPI(title="Neural Sentinel", version="1.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Load Model ===
MODEL_PATH = "efficientnet_b4_COMPATIBLE.keras"
MODEL_INPUT_SIZE = (380, 380)

print(f"Loading model from {MODEL_PATH}...")
model = load_model(MODEL_PATH)
print("Model loaded successfully.")

@app.get("/health")
def health():
    return {"status": "online", "model_loaded": True}

# ================================
# PREDICTION ENDPOINT (IMAGE + VIDEO)
# ================================
@app.post("/detect")
async def detect(file: UploadFile = File(...)) -> Dict:
    """
    Handles Image and Video inputs.
    - Images: Processed directly.
    - Videos: First frame is extracted and analyzed.
    """
    
    # 1. Read file bytes
    contents = await file.read()
    img = None

    # 2. Check if file is a VIDEO
    if file.content_type.startswith("video") or file.filename.endswith((".mp4", ".mov", ".avi")):
        try:
            # Save video to a temporary file (OpenCV needs a file path)
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                tmp.write(contents)
                tmp_path = tmp.name

            # Extract the first frame using OpenCV
            cap = cv2.VideoCapture(tmp_path)
            ret, frame = cap.read()
            cap.release()
            
            # Delete the temp file
            os.unlink(tmp_path)

            if ret:
                # Convert OpenCV BGR to PIL RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
            else:
                return {"success": False, "error": "Could not extract frame from video"}
        except Exception as e:
            return {"success": False, "error": f"Video processing failed: {str(e)}"}
            
    # 3. Check if file is an IMAGE
    else:
        img = Image.open(io.BytesIO(contents)).convert("RGB")

    # 4. Preprocess & Predict
    if img is None:
        return {"success": False, "error": "Invalid file format"}

    # Resize to model input
    img = img.resize(MODEL_INPUT_SIZE, Image.BILINEAR)

    # Convert to tensor
    arr = np.asarray(img).astype(np.float32)
    batch = np.expand_dims(arr, axis=0)

    # Run Inference
    prediction_score = float(model.predict(batch)[0][0])
    label = "FAKE" if prediction_score >= 0.5 else "REAL"

    return {
        "success": True,
        "label": label,
        "probability_fake": prediction_score,
        "probability_real": 1 - prediction_score,
        "is_video_analysis": file.content_type.startswith("video")
    }

# Serve Static Files
@app.get("/")
def root():
    return FileResponse("index.html")

@app.get("/styles.css")
def styles():
    return FileResponse("styles.css")

@app.get("/script.js")
def script():
    return FileResponse("script.js")