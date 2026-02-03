# Academic Project: Deepfake Detection System

A robust, full-stack web application designed to detect AI-manipulated media (deepfakes) using advanced computer vision and deep learning techniques. This system leverages a custom-trained **EfficientNet-B4** model to analyze images and video frames for forensic inconsistencies.

![Project Banner](https://img.shields.io/badge/Status-Active-success) ![Accuracy](https://img.shields.io/badge/Model%20Accuracy-92.5%25-blue) ![Python](https://img.shields.io/badge/Python-3.9%2B-yellow)

## 🚀 Key Features

* **State-of-the-Art Detection:** Utilizes an **EfficientNet-B4** Convolutional Neural Network (CNN) trained on diverse deepfake datasets.
* **Temporal Video Analysis:** Implements a **multi-frame sampling algorithm** to analyze video inputs at multiple intervals (0%, 20%, 40%, etc.), ensuring transient glitches and inconsistencies are detected.
* **Real-Time Inference:** Built on **FastAPI** for asynchronous, high-performance processing of high-resolution uploads.
* **Modern UI/UX:** Features a responsive, "Cyberpunk-themed" interface with real-time confidence visualizations and drag-and-drop support.
* **Environment Agnostic:** Architected with relative API paths for seamless deployment to cloud platforms (Render, AWS, Railway) or local environments.

## 🛠️ Technology Stack

* **Backend:** Python, FastAPI, Uvicorn
* **Deep Learning:** TensorFlow/Keras, EfficientNet-B4
* **Computer Vision:** OpenCV, Pillow (PIL), NumPy
* **Frontend:** HTML5, CSS3 (CSS Variables & Animations), Vanilla JavaScript

## 📂 Project Structure

```bash
deep_fake/
├── api.py                  # Main FastAPI application (Inference Logic & Video Sampling)
├── efficientnet_b4...keras # Pre-trained Deep Learning Model
├── requirements.txt        # Python dependencies
├── index.html              # Frontend Interface
├── styles.css              # Styling & Animations
├── script.js               # Client-side Logic (API communication)
└── README.md               # Project Documentation

## Installation & Setup

### Prerequisites
* Python 3.8 or higher
* pip (Python Package Manager)

### 1. Clone the Repository
```bash
git clone [https://github.com/nandeesha434nasa/deep_fake.git](https://github.com/nandeesha434nasa/deep_fake.git)
cd deep_fake

2. Install Dependencies
pip install -r requirements.txt

3.Run the Application
Start the FastAPI server using Uvicorn:
uvicorn api:app --reload

4. Access the Interface
Open your browser and navigate to: http://127.0.0.1:8000


Model Performance
The system was benchmarked against other common architectures during the research phase:

Model Architecture	Accuracy	Precision	Recall
EfficientNet-B4	    92.5%	    91.8%	    93.2%
Xception	        91.2%	    90.5%	    92.0%
Custom CNN          85.8%       84.2%       87.5%


Contributors
Academic Research Team (2025-26):

Nandeesha B (1MV23IC035) - Project Coordination & Full Stack Development

Nischay Upadhya P (1MV23IC039) - Model Implementation

Supreeth Gutti (1MV23IC058) - API Development

Kaushik Raju S (1MV23IC046) - Data Analysis
