// ============================================
// NEURAL SENTINEL - DEEPFAKE DETECTION SYSTEM
// ============================================

const API_URL = 'http://127.0.0.1:8000/detect';
let selectedFile = null;

// ============================================
// DOM ELEMENTS
// ============================================
const elements = {
    uploadZone: document.getElementById('uploadZone'),
    fileInput: document.getElementById('fileInput'),
    uploadContent: document.getElementById('uploadContent'),
    filePreview: document.getElementById('filePreview'),
    previewImage: document.getElementById('previewImage'),
    previewVideo: document.getElementById('previewVideo'),
    fileName: document.getElementById('fileName'),
    removeFile: document.getElementById('removeFile'),
    analyzeButton: document.getElementById('analyzeButton'),
    processingStages: document.getElementById('processingStages'),
    resultsContainer: document.getElementById('resultsContainer'),
    errorContainer: document.getElementById('errorContainer'),
    analyzeAnother: document.getElementById('analyzeAnother'),
    tryAgain: document.getElementById('tryAgain')
};

// ============================================
// INITIALIZATION
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    setupFileUpload();
    setupSmoothScroll();
});

// ============================================
// FILE UPLOAD LOGIC (FIXED)
// ============================================
function setupFileUpload() {
    // 1. FIX: Ensure clicking the box opens the file selector
    elements.uploadZone.addEventListener('click', (e) => {
        // Prevent triggering if clicking the "remove" button
        if (e.target === elements.removeFile) return;
        elements.fileInput.click();
    });
    
    // 2. Handle File Selection
    elements.fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFile(e.target.files[0]);
        }
    });
    
    // 3. Drag and Drop Support
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        elements.uploadZone.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    // Visual Cues for Dragging
    ['dragenter', 'dragover'].forEach(eventName => {
        elements.uploadZone.addEventListener(eventName, () => {
            elements.uploadZone.classList.add('dragover');
        });
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        elements.uploadZone.addEventListener(eventName, () => {
            elements.uploadZone.classList.remove('dragover');
        });
    });
    
    elements.uploadZone.addEventListener('drop', (e) => {
        const file = e.dataTransfer.files[0];
        handleFile(file);
    });
    
    // Remove File Button
    elements.removeFile.addEventListener('click', (e) => {
        e.stopPropagation(); // Stop the click from re-opening the file selector
        resetUpload();
    });
    
    // Button Listeners
    elements.analyzeButton.addEventListener('click', analyzeFile);
    elements.analyzeAnother.addEventListener('click', resetUpload);
    elements.tryAgain.addEventListener('click', resetUpload);
}

// ============================================
// HANDLE FILE (Images + Video)
// ============================================
function handleFile(file) {
    if (!file) return;
    
    // Allow Images AND Videos
    const validTypes = ['image/jpeg', 'image/png', 'image/jpg', 'video/mp4', 'video/quicktime', 'video/x-msvideo'];
    
    // Check type or extension as a backup
    if (!validTypes.includes(file.type) && !file.name.match(/\.(jpg|jpeg|png|mp4|mov|avi)$/i)) {
        showError('Invalid file type. Please upload JPG, PNG images or MP4 videos.');
        return;
    }
    
    selectedFile = file;
    
    // UI Updates
    elements.uploadContent.style.display = 'none';
    elements.filePreview.style.display = 'block';
    elements.fileName.textContent = file.name;
    
    // Preview Logic
    const fileURL = URL.createObjectURL(file);
    
    if (file.type.startsWith('video') || file.name.endsWith('.mp4')) {
        // Video Preview
        elements.previewVideo.src = fileURL;
        elements.previewVideo.style.display = 'block';
        elements.previewImage.style.display = 'none';
    } else {
        // Image Preview
        elements.previewImage.src = fileURL;
        elements.previewImage.style.display = 'block';
        elements.previewVideo.style.display = 'none';
    }
    
    // Enable analyze button
    elements.analyzeButton.disabled = false;
}

function resetUpload() {
    selectedFile = null;
    elements.fileInput.value = '';
    elements.uploadContent.style.display = 'block';
    elements.filePreview.style.display = 'none';
    elements.previewImage.src = '';
    elements.previewVideo.src = '';
    elements.analyzeButton.disabled = true;
    elements.processingStages.style.display = 'none';
    elements.resultsContainer.style.display = 'none';
    elements.errorContainer.style.display = 'none';
}

// ============================================
// ANALYSIS LOGIC
// ============================================
async function analyzeFile() {
    if (!selectedFile) return;
    
    // UI State: Processing
    elements.analyzeButton.querySelector('.button-text').style.display = 'none';
    elements.analyzeButton.querySelector('.button-loader').style.display = 'block';
    elements.analyzeButton.disabled = true;
    elements.processingStages.style.display = 'flex';
    elements.resultsContainer.style.display = 'none';
    elements.errorContainer.style.display = 'none';
    
    // Fake Progress Animation (Makes it look like it's "thinking")
    await animateStage('upload', 500);
    await animateStage('detection', 800);
    
    // Prepare Data
    const formData = new FormData();
    formData.append('file', selectedFile);
    
    try {
        await animateStage('analysis', 1000);
        
        // Call Backend
        const response = await fetch(API_URL, {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            throw new Error(`Server Error: ${response.status}`);
        }
        
        const result = await response.json();
        
        await animateStage('results', 500);
        
        if (result.success) {
            displayResults(result);
        } else {
            showError(result.error || 'Analysis failed.');
        }
        
    } catch (error) {
        console.error(error);
        showError('Could not connect to server. Is the backend running?');
    } finally {
        // Reset Button State
        elements.analyzeButton.querySelector('.button-text').style.display = 'block';
        elements.analyzeButton.querySelector('.button-loader').style.display = 'none';
    }
}

// ============================================
// UI HELPERS
// ============================================
async function animateStage(stageName, duration) {
    const stage = document.querySelector(`[data-stage="${stageName}"]`);
    if (!stage) return;
    
    stage.classList.add('active');
    
    // Connector animation
    const prevStage = stage.previousElementSibling?.previousElementSibling;
    if (prevStage && prevStage.nextElementSibling) {
        prevStage.nextElementSibling.classList.add('active');
    }
    
    await new Promise(r => setTimeout(r, duration));
    
    stage.classList.remove('active');
    stage.classList.add('completed');
}

function displayResults(result) {
    elements.processingStages.style.display = 'none';
    elements.resultsContainer.style.display = 'block';
    
    const { label, probability_fake, probability_real } = result;
    const confidence = Math.max(probability_fake, probability_real);
    
    // Update Text
    const badge = document.getElementById('resultBadge');
    badge.textContent = label;
    badge.className = `result-badge ${label.toLowerCase()}`;
    
    document.getElementById('classification').textContent = label;
    document.getElementById('classification').style.color = label === 'REAL' ? '#00ff88' : '#ff3366';
    
    document.getElementById('realProb').textContent = (probability_real * 100).toFixed(1) + '%';
    document.getElementById('fakeProb').textContent = (probability_fake * 100).toFixed(1) + '%';
    
    // Update Circle Meter
    const confidenceValue = document.getElementById('confidenceValue');
    animateNumber(confidenceValue, 0, confidence * 100, 1500);
    
    const circle = document.getElementById('confidenceCircle');
    // 534 is the circumference of the SVG circle
    const offset = 534 - (confidence * 534);
    circle.style.strokeDashoffset = offset;
    
    // Color the circle based on result
    circle.style.stroke = label === 'REAL' ? '#00ff88' : '#ff3366';
}

function showError(msg) {
    elements.processingStages.style.display = 'none';
    elements.resultsContainer.style.display = 'none';
    elements.errorContainer.style.display = 'block';
    document.getElementById('errorMessage').textContent = msg;
}

function animateNumber(element, start, end, duration) {
    let startTimestamp = null;
    const step = (timestamp) => {
        if (!startTimestamp) startTimestamp = timestamp;
        const progress = Math.min((timestamp - startTimestamp) / duration, 1);
        element.textContent = Math.floor(progress * (end - start) + start) + '%';
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
}

function setupSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) target.scrollIntoView({ behavior: 'smooth' });
        });
    });
}