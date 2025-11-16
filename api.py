# api.py
import os
import io
import uvicorn
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from tensorflow.keras.models import load_model
from PIL import Image

app = FastAPI(title="Neural Sentinel", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# === Load model ===
MODEL_PATH = "efficientnet_b4_COMPATIBLE.keras"
MODEL_INPUT_SIZE = (380, 380)

model = load_model(MODEL_PATH)


@app.get("/health")
def health():
    return {"status": "online", "model_loaded": True}


# ================================
# CLEAN + CORRECT DETECT ENDPOINT
# ================================
@app.post("/detect")
async def detect(file: UploadFile = File(...)):

    # Read file bytes
    contents = await file.read()

    # Load image
    img = Image.open(io.BytesIO(contents)).convert("RGB")

    # Resize to model input
    img = img.resize(MODEL_INPUT_SIZE, Image.BILINEAR)

    # Convert to float32 (DO NOT divide by 255)
    arr = np.asarray(img).astype(np.float32)

    # Make batch
    batch = np.expand_dims(arr, axis=0)

    # Predict (shape = (1,1))
    pred = float(model.predict(batch)[0][0])

    # Interpret output
    label = "FAKE" if pred >= 0.5 else "REAL"

    # Response
    return {
        "success": True,
        "label": label,
        "probability_fake": pred,
        "probability_real": 1 - pred
    }
@app.get("/")
def root():
    return FileResponse("index.html")

@app.get("/styles.css")
def styles():
    return FileResponse("styles.css")

@app.get("/script.js")
def script():
    return FileResponse("script.js")
