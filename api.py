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

#Helper Function for Prediction
def predict_single_frame(img: Image.Image) -> float:
    """
    Preprocesses a single PIL image and returns the 'fake' probability (0.0 to 1.0).
    """
    # Resize to model input
    img = img.resize(MODEL_INPUT_SIZE, Image.BILINEAR)
    
    # Convert to tensor
    arr = np.asarray(img).astype(np.float32)
    batch = np.expand_dims(arr, axis=0)
    
    # Run Inference
    # Assuming the model returns a single value (sigmoid output)
    # If using softmax (2 outputs), use prediction[0][1] for 'fake' class
    prediction_score = float(model.predict(batch, verbose=0)[0][0])
    return prediction_score

# ================================
# PREDICTION ENDPOINT (IMAGE + VIDEO)
# ================================
@app.post("/detect")
async def detect(file: UploadFile = File(...)) -> Dict:
    """
    Handles Image and Video inputs.
    - Images: Processed directly.
    - Videos: Analyzes multiple frames (temporal sampling) and averages the score.
    """
    
    contents = await file.read()
    probabilities = []
    frames_analyzed = 0

    # === VIDEO PROCESSING ===
    if file.content_type.startswith("video") or file.filename.endswith((".mp4", ".mov", ".avi")):
        try:
            # Save video to temp file
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
                tmp.write(contents)
                tmp_path = tmp.name

            cap = cv2.VideoCapture(tmp_path)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Analyze 5 frames evenly distributed across the video
            num_frames_to_check = 5
            step = max(1, total_frames // num_frames_to_check)
            
            for i in range(0, total_frames, step):
                # Stop if we have checked enough frames
                if len(probabilities) >= num_frames_to_check:
                    break
                    
                cap.set(cv2.CAP_PROP_POS_FRAMES, i)
                ret, frame = cap.read()
                
                if ret:
                    # Convert BGR (OpenCV) to RGB (PIL)
                    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    pil_img = Image.fromarray(frame_rgb)
                    
                    # Predict using helper
                    score = predict_single_frame(pil_img)
                    probabilities.append(score)
                    frames_analyzed += 1

            cap.release()
            os.unlink(tmp_path)

            if not probabilities:
                return {"success": False, "error": "Could not extract any frames from video"}

        except Exception as e:
            return {"success": False, "error": f"Video processing failed: {str(e)}"}
            
    # === IMAGE PROCESSING ===
    else:
        try:
            img = Image.open(io.BytesIO(contents)).convert("RGB")
            score = predict_single_frame(img)
            probabilities.append(score)
            frames_analyzed = 1
        except Exception as e:
            return {"success": False, "error": f"Image processing failed: {str(e)}"}

    # === AGGREGATE RESULTS ===
    # Calculate average probability across all frames
    avg_fake_prob = sum(probabilities) / len(probabilities)
    label = "FAKE" if avg_fake_prob >= 0.5 else "REAL"

    return {
        "success": True,
        "label": label,
        "probability_fake": avg_fake_prob,
        "probability_real": 1 - avg_fake_prob,
        "frames_analyzed": frames_analyzed,
        "is_video_analysis": frames_analyzed > 1
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
