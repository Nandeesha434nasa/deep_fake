🕵️‍♂️ Deepfake Detection System

An intelligent web-based system that detects manipulated (deepfake) images using a custom-trained EfficientNet-B4 deep learning model.
Includes a FastAPI backend + clean HTML/CSS/JS frontend.

🚀 Features
🔍 Deepfake Detection

Uses a trained EfficientNet-B4 model (efficientnet_b4_COMPATIBLE.keras)

Accepts image uploads

Classifies them as:

REAL

FAKE

Shows probability scores

🌐 Web-Based Interface

Upload images through a clean frontend UI

Results displayed instantly

⚡ FastAPI Backend

Lightweight, fast, asynchronous API server

Easily deployable on:

Render

AWS EC2

Railway

Local machine

🧠 Machine Learning Pipeline

Model trained on deepfake datasets

Preprocessing follows exact model input size 380 × 380

No manual normalization required (handled inside model)
