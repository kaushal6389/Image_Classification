"""
FastAPI - Street Infrastructure Classifier API
Deploy ML model for mobile app and web dashboard integration
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow import keras
import io
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Disable TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
tf.get_logger().setLevel('ERROR')

# =============================================================================
# CONFIGURATION
# =============================================================================
IMG_SIZE = 384
CLASS_NAMES = ['garbage', 'open_manhole', 'potholes', 'road_normal', 'streetlight_bad', 'streetlight_good']

# Railway Volume path for model storage
VOLUME_PATH = os.getenv("VOLUME_PATH", "/data")
MODEL_FILENAME = "final_model_98plus.keras"
MODEL_PATH = os.path.join(VOLUME_PATH, MODEL_FILENAME)

# Class metadata
CLASS_DESCRIPTIONS = {
    'garbage': 'Garbage/litter on street',
    'open_manhole': 'Uncovered manhole - Safety hazard',
    'potholes': 'Road pothole - Needs repair',
    'road_normal': 'Normal road condition',
    'streetlight_bad': 'Broken/non-functional streetlight',
    'streetlight_good': 'Working streetlight'
}

CLASS_PRIORITY = {
    'open_manhole': 'CRITICAL',
    'potholes': 'HIGH',
    'garbage': 'MEDIUM',
    'streetlight_bad': 'MEDIUM',
    'streetlight_good': 'LOW',
    'road_normal': 'LOW'
}

# =============================================================================
# LOAD MODEL
# =============================================================================
model = None
model_status = "NOT_LOADED"
model_error = None

if os.path.exists(MODEL_PATH):
    try:
        logger.info(f"📥 Loading model from: {MODEL_PATH}")
        file_size_mb = os.path.getsize(MODEL_PATH) / (1024 * 1024)
        logger.info(f"📦 Model size: {file_size_mb:.1f} MB")
        
        model = keras.models.load_model(MODEL_PATH)
        model_status = "LOADED"
        logger.info(f"✅ Model loaded successfully!")
        logger.info(f"   Params: {model.count_params():,}")
    except Exception as e:
        model_status = "ERROR"
        model_error = str(e)
        logger.error(f"❌ Model loading failed: {e}")
else:
    model_status = "NOT_FOUND"
    model_error = f"Model file not found at {MODEL_PATH}"
    logger.warning(f"⚠️  {model_error}")
    logger.warning(f"⚠️  Upload model to Railway volume first!")

# =============================================================================
# FASTAPI APP
# =============================================================================
app = FastAPI(
    title="Street Infrastructure Classifier API",
    description="AI street infrastructure detection for mobile apps",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def preprocess_image(image: Image.Image) -> np.ndarray:
    """Preprocess image for model prediction"""
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    image = image.resize((IMG_SIZE, IMG_SIZE))
    img_array = np.array(image) / 255.0
    img_batch = np.expand_dims(img_array, axis=0)
    
    return img_batch

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Street Infrastructure Classifier API", "status": "running"}

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_status": model_status,
        "model_error": model_error,
        "classes": CLASS_NAMES,
        "image_size": IMG_SIZE
    }

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    """
    Predict infrastructure class from uploaded image
    
    Returns:
    - class_name: Predicted class
    - confidence: Confidence score (0-100)
    - priority: Priority level (CRITICAL, HIGH, MEDIUM, LOW)
    - description: Class description
    """
    
    if model is None:
        raise HTTPException(status_code=503, detail=f"Model not available: {model_error}")
    
    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Preprocess
        img_batch = preprocess_image(image)
        
        # Predict
        predictions = model.predict(img_batch, verbose=0)
        class_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][class_idx]) * 100
        
        class_name = CLASS_NAMES[class_idx]
        
        return {
            "class": class_name,
            "confidence": round(confidence, 2),
            "priority": CLASS_PRIORITY.get(class_name, "LOW"),
            "description": CLASS_DESCRIPTIONS.get(class_name, "Unknown"),
            "all_predictions": {
                CLASS_NAMES[i]: round(float(predictions[0][i]) * 100, 2)
                for i in range(len(CLASS_NAMES))
            }
        }
    
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=400, detail=f"Prediction failed: {str(e)}")

@app.post("/predict/batch")
async def predict_batch(files: list[UploadFile] = File(...)):
    """Batch prediction for multiple images"""
    
    if model is None:
        raise HTTPException(status_code=503, detail=f"Model not available: {model_error}")
    
    results = []
    
    try:
        for file in files:
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            
            img_batch = preprocess_image(image)
            predictions = model.predict(img_batch, verbose=0)
            class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][class_idx]) * 100
            
            class_name = CLASS_NAMES[class_idx]
            
            results.append({
                "filename": file.filename,
                "class": class_name,
                "confidence": round(confidence, 2),
                "priority": CLASS_PRIORITY.get(class_name, "LOW"),
                "description": CLASS_DESCRIPTIONS.get(class_name, "Unknown")
            })
        
        return {
            "total": len(results),
            "processed": len(results),
            "results": results
        }
    
    except Exception as e:
        logger.error(f"Batch prediction error: {e}")
        raise HTTPException(status_code=400, detail=f"Batch prediction failed: {str(e)}")

@app.get("/classes")
async def get_classes():
    """Get available classes and their info"""
    return {
        "classes": [
            {
                "name": class_name,
                "description": CLASS_DESCRIPTIONS.get(class_name),
                "priority": CLASS_PRIORITY.get(class_name)
            }
            for class_name in CLASS_NAMES
        ]
    }

# =============================================================================
# SERVER
# =============================================================================
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    
    print("\n" + "="*70)
    print("🚀 STARTING STREET INFRASTRUCTURE CLASSIFIER API")
    print("="*70)
    print(f"🌐 API URL: http://localhost:{port}")
    print(f"📚 Docs: http://localhost:{port}/docs")
    print(f"🏥 Health: http://localhost:{port}/health")
    print(f"📊 Model: {model_status}")
    print("="*70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
