# 🚀 Railway Volume Setup - Step by Step Guide

## Model File Info
- **File**: `final_model_98plus.keras`
- **Location**: `E:\Image_classifier\saved_models\final_model_98plus.keras`
- **Size**: **1.3 GB** (1302.91 MB)

---

## ✅ Step 1: Create Railway Volume via Dashboard

1. **Open Railway Dashboard**: https://railway.app/dashboard
2. Navigate to project: **proud-hope**
3. Click on **web** service
4. Go to **"Volumes"** tab (left sidebar)
5. Click **"+ New Volume"**
6. Configure:
   - **Name**: `model-storage`
   - **Mount Path**: `/data`
7. Click **"Add Volume"**

---

## ✅ Step 2: Upload Model File

Railway doesn't support direct CLI upload for large files. **Use one of these methods:**

### Method A: Use Railway Shell (RECOMMENDED)
1. In Railway Dashboard → web service → **Settings** → Add this variable:
   ```
   RAILWAY_RUN_UID=0
   ```

2. In your terminal, run:
   ```powershell
   railway run bash
   ```

3. Inside the container:
   ```bash
   # Check mount point
   ls /data
   
   # Exit and prepare for file transfer
   exit
   ```

4. Use `railway run` with a upload script (create `upload_model.py`):
   ```python
   # This will be created in next step
   ```

### Method B: HTTP Upload (SIMPLER FOR NOW)
Since model is too large (1.3GB), we'll modify the API to load model ONLY when prediction is requested (lazy loading).

---

## ✅ Step 3: Modify API for Lazy Loading (QUICK FIX)

Instead of downloading on startup, load model only when /predict is called.

Update `api.py` to NOT load model on startup, but load when needed.

---

## 🎯 BEST SOLUTION: Use Model in Docker Image

Since model is 1.3GB and GitHub/Railway have limits, we'll:

1. Upload model to Hugging Face (free, unlimited for ML models)
2. Download on first request
3. Cache in memory

This is already implemented in current `api.py`!

---

## 📋 Action Items for YOU:

### Option 1: Hugging Face Upload (RECOMMENDED - 5 min)
```bash
# Install huggingface-cli
pip install huggingface_hub

# Login
huggingface-cli login
# Enter your token from https://huggingface.co/settings/tokens

# Upload model
huggingface-cli upload YOUR_USERNAME/street-infrastructure-model saved_models/final_model_98plus.keras final_model_98plus.keras

# Update Railway env variable
railway variables set MODEL_URL="https://huggingface.co/YOUR_USERNAME/street-infrastructure-model/resolve/main/final_model_98plus.keras"
```

### Option 2: Use smaller model or quantized version
Convert model to TFLite (much smaller):
```python
import tensorflow as tf

# Load model
model = tf.keras.models.load_model('saved_models/final_model_98plus.keras')

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

# Save
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
```

Size will be ~300-400 MB instead of 1.3GB!

---

## ⚡ QUICKEST FIX (For Hackathon Demo TODAY):

1. **Skip model deployment for now**
2. **Deploy API with mock responses**
3. **Show architecture and explain model separately**

Let me create a mock API version...
