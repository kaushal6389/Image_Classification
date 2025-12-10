# 🚀 Railway Deployment - Complete Setup Guide

## 📋 Prerequisites
- Railway CLI installed (`npm install -g @railway/cli` or download from https://railway.app/cli)
- Model file: `saved_models/final_model_98plus.keras` (1.3GB)
- Railway account logged in (`railway login`)

---

## ✅ Step 1: Create Railway Volume

```powershell
# Link to your project (if not already linked)
railway link

# Create a new volume
railway volume add
```

**Configuration:**
- **Name**: `model-storage`
- **Mount Path**: `/data`

---

## ✅ Step 2: Upload Model to Volume

### Option A: Using Railway Dashboard (Recommended)

1. Go to Railway Dashboard: https://railway.app/dashboard
2. Select project: **proud-hope**
3. Go to **"Volumes"** tab
4. Click on **model-storage** volume
5. Click **"Upload Files"** button
6. Upload: `E:\Image_classifier\saved_models\final_model_98plus.keras`
7. Verify file appears as: `/data/final_model_98plus.keras`

### Option B: Using Railway CLI (if available in future)

```powershell
# Navigate to saved_models folder
cd E:\Image_classifier\saved_models

# Upload file to volume
railway volume upload model-storage final_model_98plus.keras
```

---

## ✅ Step 3: Attach Volume to Service

```powershell
# Attach volume to web service
railway volume attach model-storage --service web
```

**Verify mount path**: `/data`

---

## ✅ Step 4: Set Environment Variable (Optional)

```powershell
# If using custom path, set environment variable
railway variables set VOLUME_PATH=/data
```

---

## ✅ Step 5: Deploy

```powershell
# Clean deploy
railway up

# Or redeploy current deployment
railway redeploy
```

---

## 🧪 Step 6: Verify Deployment

### Check Health Endpoint

```powershell
# Get your service URL
railway domain

# Test health endpoint
curl https://your-service.railway.app/health
```

**Expected Response:**
```json
{
  "status": "healthy",
  "model": {
    "loaded": true,
    "path": "/data/final_model_98plus.keras",
    "size_mb": 1300.0,
    "parameters": 197000000
  },
  "timestamp": "2025-12-10T..."
}
```

### Check Logs

```powershell
railway logs
```

**Look for:**
```
📂 Using model from Railway volume: /data/final_model_98plus.keras
📦 Model file size: 1300.0 MB
✅ Model loaded successfully!
   Parameters: 197,000,000
```

---

## 🎯 Step 7: Test API

### Interactive Docs
Visit: `https://your-service.railway.app/docs`

### Test Prediction

```powershell
# Upload test image
curl -X POST "https://your-service.railway.app/predict" `
  -F "file=@path/to/test/image.jpg"
```

---

## 🔧 Troubleshooting

### Model Not Found
```
❌ MODEL NOT FOUND!
Expected location: /data/final_model_98plus.keras
```

**Solution:**
1. Check volume is attached: `railway volume list`
2. Verify mount path is `/data`
3. Confirm file exists in volume via Dashboard
4. Restart service: `railway restart`

### Model Load Error
```
❌ Error loading model: ...
```

**Solution:**
1. Verify file integrity (correct upload)
2. Check file size matches original (1.3GB)
3. Re-upload model file
4. Check logs: `railway logs`

### Memory Issues
If container runs out of memory:

```powershell
# Upgrade service plan or optimize model
railway settings
```

---

## 📊 Current Setup Summary

✅ **Repository**: https://github.com/kaushal6389/Image_Classification  
✅ **Project**: proud-hope  
✅ **Service**: web  
✅ **Volume**: model-storage → /data  
✅ **Model**: final_model_98plus.keras (1.3GB)  
✅ **API Framework**: FastAPI + Uvicorn  
✅ **Python**: 3.11  
✅ **TensorFlow**: 2.16.1  

---

## 🎉 Success Checklist

- [ ] Volume created and attached
- [ ] Model uploaded to volume
- [ ] Service deployed successfully
- [ ] Health check returns `"loaded": true`
- [ ] `/predict` endpoint works
- [ ] No errors in logs
- [ ] API docs accessible at `/docs`

---

## 📞 Quick Commands Reference

```powershell
# Check status
railway status

# View logs
railway logs --tail 100

# List volumes
railway volume list

# Restart service
railway restart

# Open dashboard
railway open
```
