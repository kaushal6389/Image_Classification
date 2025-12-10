"""
FastAPI - Street Infrastructure Classifier API
Deploy ML model for mobile app and web dashboard integration
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
import numpy as np
import tensorflow as tf
from tensorflow import keras
import io
import os
from datetime import datetime
from typing import Optional
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
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(SCRIPT_DIR, 'saved_models', 'final_model_98plus.keras')
IMG_SIZE = 384
CLASS_NAMES = ['garbage', 'open_manhole', 'potholes', 'road_normal', 'streetlight_bad', 'streetlight_good']

# Class descriptions for dashboard
CLASS_DESCRIPTIONS = {
    'garbage': 'Garbage/litter on street',
    'open_manhole': 'Uncovered manhole - Safety hazard',
    'potholes': 'Road pothole - Needs repair',
    'road_normal': 'Normal road condition',
    'streetlight_bad': 'Broken/non-functional streetlight',
    'streetlight_good': 'Working streetlight'
}

# Priority levels for dashboard
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
logger.info("Loading ML model...")
try:
    model = keras.models.load_model(MODEL_PATH)
    model_size = os.path.getsize(MODEL_PATH) / (1024*1024)
    logger.info(f"✅ Model loaded: {model_size:.1f} MB, Params: {model.count_params():,}")
except Exception as e:
    logger.error(f"❌ Error loading model: {e}")
    raise

# =============================================================================
# FASTAPI APP
# =============================================================================
app = FastAPI(
    title="Street Infrastructure Classifier API",
    description="AI-powered street infrastructure detection for mobile apps and dashboards",
    version="1.0.0"
)

# CORS configuration for web/mobile app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def preprocess_image(image: Image.Image) -> np.ndarray:
    """Preprocess image for model prediction"""
    # Convert to RGB
    if image.mode != 'RGB':
        image = image.convert('RGB')
    
    # Resize
    image = image.resize((IMG_SIZE, IMG_SIZE))
    
    # Convert to array and normalize
    img_array = np.array(image) / 255.0
    img_batch = np.expand_dims(img_array, axis=0)
    
    return img_batch

def predict_infrastructure(image: Image.Image) -> dict:
    """Predict infrastructure class from image"""
    try:
        # Preprocess
        img_batch = preprocess_image(image)
        
        # Predict
        predictions = model.predict(img_batch, verbose=0)
        pred_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][pred_idx])
        predicted_class = CLASS_NAMES[pred_idx]
        
        # Get all class probabilities
        all_predictions = {
            cls: float(prob) 
            for cls, prob in zip(CLASS_NAMES, predictions[0])
        }
        
        # Sort by probability
        sorted_predictions = dict(sorted(all_predictions.items(), key=lambda x: x[1], reverse=True))
        
        return {
            'success': True,
            'predicted_class': predicted_class,
            'confidence': confidence,
            'description': CLASS_DESCRIPTIONS[predicted_class],
            'priority': CLASS_PRIORITY[predicted_class],
            'all_probabilities': sorted_predictions,
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "message": "Street Infrastructure Classifier API",
        "version": "1.0.0",
        "model": "ConvNeXtLarge (97.84% accuracy)",
        "endpoints": {
            "predict": "/predict - Upload image for classification",
            "health": "/health - Check API health",
            "classes": "/classes - Get available classes",
            "docs": "/docs - Interactive API documentation"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "model_loaded": model is not None,
        "timestamp": datetime.now().isoformat()
    }

@app.get("/classes")
async def get_classes():
    """Get all available classes with descriptions"""
    return {
        "classes": [
            {
                "name": cls,
                "description": CLASS_DESCRIPTIONS[cls],
                "priority": CLASS_PRIORITY[cls]
            }
            for cls in CLASS_NAMES
        ],
        "total": len(CLASS_NAMES)
    }

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    include_all_probabilities: Optional[bool] = True
):
    """
    Predict infrastructure class from uploaded image
    
    Args:
        file: Image file (jpg, jpeg, png, bmp)
        include_all_probabilities: Include probabilities for all classes
    
    Returns:
        JSON with prediction results
    """
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        logger.info(f"Processing image: {file.filename}, Size: {image.size}")
        
        # Predict
        result = predict_infrastructure(image)
        
        # Format response
        response = {
            "success": True,
            "filename": file.filename,
            "predicted_class": result['predicted_class'],
            "confidence": round(result['confidence'] * 100, 2),  # As percentage
            "description": result['description'],
            "priority": result['priority'],
            "timestamp": result['timestamp']
        }
        
        if include_all_probabilities:
            response['all_predictions'] = {
                cls: round(prob * 100, 2) 
                for cls, prob in result['all_probabilities'].items()
            }
        
        logger.info(f"Prediction: {result['predicted_class']} ({result['confidence']:.2%})")
        
        return JSONResponse(content=response)
        
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/predict/batch")
async def predict_batch(files: list[UploadFile] = File(...)):
    """
    Predict multiple images at once
    
    Args:
        files: List of image files
    
    Returns:
        JSON with results for all images
    """
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 images allowed per batch")
    
    results = []
    
    for file in files:
        try:
            # Validate file type
            if not file.content_type.startswith('image/'):
                results.append({
                    "filename": file.filename,
                    "success": False,
                    "error": "Not an image file"
                })
                continue
            
            # Read and predict
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            result = predict_infrastructure(image)
            
            results.append({
                "filename": file.filename,
                "success": True,
                "predicted_class": result['predicted_class'],
                "confidence": round(result['confidence'] * 100, 2),
                "priority": result['priority']
            })
            
        except Exception as e:
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    return {
        "total_images": len(files),
        "processed": len([r for r in results if r['success']]),
        "failed": len([r for r in results if not r['success']]),
        "results": results
    }

# =============================================================================
# RUN SERVER
# =============================================================================
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("PORT", 8000))
    
    print("\n" + "="*70)
    print("🚀 STARTING STREET INFRASTRUCTURE CLASSIFIER API")
    print("="*70)
    print(f"📊 Model: final_model_98plus.keras (97.84% accuracy)")
    print(f"🌐 API URL: http://localhost:{port}")
    print(f"📚 Docs: http://localhost:{port}/docs")
    print(f"🔍 Health: http://localhost:{port}/health")
    print("="*70 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
