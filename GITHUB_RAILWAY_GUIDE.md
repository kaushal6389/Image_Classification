# GitHub & Railway Deployment Guide

## 📋 Pre-Deployment Checklist

✅ `.gitignore` - Configured (excludes model, data, notebooks)
✅ `Procfile` - Railway startup command
✅ `runtime.txt` - Python 3.11 specification
✅ `requirements_api.txt` - API dependencies
✅ `api.py` - FastAPI application (PORT env variable)
✅ `Dockerfile` - Container configuration
✅ `README_DEPLOYMENT.md` - User documentation

## 🚀 Step 1: Push to GitHub

### Initialize Git Repository

```bash
# Navigate to project folder
cd E:\Image_classifier

# Initialize git (if not already done)
git init

# Add all files
git add .

# Check what will be committed (verify .gitignore working)
git status

# You should NOT see:
# - saved_models/*.keras files
# - data/ folder
# - *.ipynb files
# - __pycache__/

# Commit
git commit -m "Initial commit: Street Infrastructure Classifier API"

# Create main branch
git branch -M main
```

### Create GitHub Repository

1. Go to https://github.com
2. Click "New repository"
3. Name: `street-infrastructure-classifier`
4. Description: `AI-powered street infrastructure detection API (97.84% accuracy)`
5. Public or Private (your choice)
6. **DON'T** initialize with README (we already have files)
7. Click "Create repository"

### Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/street-infrastructure-classifier.git

# Push code
git push -u origin main
```

## 🚂 Step 2: Deploy to Railway

### Option A: Railway Web Dashboard (Easiest)

1. **Go to Railway**
   - Visit: https://railway.app
   - Sign up with GitHub account

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `street-infrastructure-classifier`

3. **Railway Auto-Detects:**
   - ✅ Python project
   - ✅ `requirements_api.txt` (dependencies)
   - ✅ `Procfile` (start command)
   - ✅ `runtime.txt` (Python 3.11)

4. **Configure Settings**
   - Go to "Settings" tab
   - **Memory**: Set to 2GB (model requires ~1GB)
   - **Build Command**: Auto-detected (`pip install -r requirements_api.txt`)
   - **Start Command**: Auto-detected from Procfile (`uvicorn api:app --host 0.0.0.0 --port $PORT`)

5. **Deploy**
   - Click "Deploy"
   - Wait 3-5 minutes for build
   - Railway will provide URL: `https://your-app.up.railway.app`

### Option B: Railway CLI (Advanced)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Initialize project
railway init

# Link to Railway project
railway link

# Deploy
railway up
```

## 📦 Step 3: Upload Model File

**IMPORTANT:** Model file (~760MB) is too large for GitHub. Upload separately to Railway.

### Method 1: Railway Volume (Recommended)

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and link project
railway login
railway link

# Create persistent volume
railway volume create model-storage

# Mount volume
railway volume add model-storage /app/saved_models

# Upload model file
railway run cp saved_models/final_model_98plus.keras /app/saved_models/
```

### Method 2: Direct Upload via Web Interface

1. Go to Railway dashboard
2. Click on your project
3. Go to "Data" tab
4. Click "Upload Files"
5. Upload `saved_models/final_model_98plus.keras`
6. Restart deployment

### Method 3: Cloud Storage (AWS S3/Google Cloud)

Upload model to S3/GCS and modify `api.py`:

```python
import urllib.request
import os

# Add this before model loading
MODEL_URL = "https://your-storage.s3.amazonaws.com/final_model_98plus.keras"
if not os.path.exists(MODEL_PATH):
    print("📥 Downloading model from cloud storage...")
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
    print("✅ Model downloaded")
```

## ✅ Step 4: Verify Deployment

### Check Logs

Railway Dashboard → Your Project → Logs

Look for:
```
✅ Model loaded successfully
🚀 STARTING STREET INFRASTRUCTURE CLASSIFIER API
📊 Model: final_model_98plus.keras (97.84% accuracy)
```

### Test API Endpoints

```bash
# Replace YOUR_APP_URL with actual Railway URL

# Health check
curl https://your-app.up.railway.app/health

# Expected: {"status": "healthy", "model_loaded": true, ...}

# Get classes
curl https://your-app.up.railway.app/classes

# Interactive docs
# Open in browser: https://your-app.up.railway.app/docs
```

### Test from Python

```python
import requests

API_URL = "https://your-app.up.railway.app"

# Health check
response = requests.get(f"{API_URL}/health")
print(response.json())

# Predict
with open("test_image.jpg", "rb") as f:
    files = {"file": f}
    response = requests.post(f"{API_URL}/predict", files=files)
    print(response.json())
```

## 🔧 Step 5: Configure Environment Variables

Railway Dashboard → Your Project → Variables

```env
PORT=8000              # Auto-set by Railway
PYTHONUNBUFFERED=1     # Better logging
TF_CPP_MIN_LOG_LEVEL=2 # Reduce TensorFlow warnings
```

## 📱 Step 6: Update Mobile App

Update your mobile app's API endpoint:

```javascript
// Before
const API_URL = 'http://localhost:8000';

// After
const API_URL = 'https://your-app.up.railway.app';
```

## 🐛 Troubleshooting

### Issue: Build Fails

**Solution:**
```bash
# Check logs
railway logs

# Common fixes:
# 1. Verify requirements_api.txt has correct versions
# 2. Check Procfile syntax
# 3. Ensure runtime.txt has valid Python version
```

### Issue: Model Not Found

**Error:** `Model file not found: final_model_98plus.keras`

**Solutions:**
1. Upload model file using Railway Volume
2. Check file path in `api.py`
3. Verify model file uploaded to correct location

```bash
# Check if file exists
railway run ls saved_models/
```

### Issue: Out of Memory

**Error:** `MemoryError` or `OOM`

**Solutions:**
1. Upgrade Railway plan to 2GB+ RAM
2. Check Railway dashboard → Settings → Memory
3. Model requires minimum 1GB RAM

### Issue: Slow First Request

**Expected Behavior:**
- First request: 5-10 seconds (model loading)
- Subsequent requests: 1-2 seconds

**Solution:**
- Keep API warm with periodic health checks
- Set up monitoring/ping service

### Issue: CORS Errors from Web App

**Error:** `Access-Control-Allow-Origin`

**Solution:** Update `api.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📊 Monitoring & Maintenance

### Railway Monitoring

Railway Dashboard provides:
- ✅ CPU/Memory usage
- ✅ Request logs
- ✅ Build logs
- ✅ Crash detection
- ✅ Auto-restart

### Custom Domain (Optional)

1. Railway Dashboard → Your Project → Settings
2. Click "Domains"
3. Add custom domain: `api.yourdomain.com`
4. Update DNS records:
   ```
   Type: CNAME
   Name: api
   Value: your-app.up.railway.app
   ```

### Scaling

Railway auto-scales based on:
- Request volume
- Memory usage
- CPU usage

**For high traffic:**
- Upgrade to Pro plan ($20/month)
- Enable horizontal scaling
- Use CDN for static assets

## 💰 Cost Estimation

### Railway Pricing

**Hobby Plan ($5/month):**
- 500 hours uptime
- $0.01/hour beyond limit
- 100GB bandwidth
- Perfect for: Low-medium traffic

**Pro Plan ($20/month):**
- Unlimited hours
- Priority support
- Better resources
- Perfect for: Production apps

**Expected Monthly Cost:**
- Development/Testing: $5-10
- Small production: $10-20
- Medium traffic: $20-40

## ✅ Post-Deployment Checklist

- [ ] GitHub repository created and pushed
- [ ] Railway project deployed
- [ ] Model file uploaded (760MB)
- [ ] API health check passes
- [ ] All endpoints tested (/predict, /batch, /health, /classes)
- [ ] Interactive docs working (https://your-app.up.railway.app/docs)
- [ ] Mobile app updated with new URL
- [ ] CORS configured for frontend domains
- [ ] Custom domain added (optional)
- [ ] Monitoring set up
- [ ] Team members added (if applicable)

## 🎉 Success! Your API is Live

**Share these URLs:**
- 🌐 API: `https://your-app.up.railway.app`
- 📖 Docs: `https://your-app.up.railway.app/docs`
- 💚 Health: `https://your-app.up.railway.app/health`

**Test from anywhere:**
```bash
curl https://your-app.up.railway.app/health
```

**Mobile App Integration:**
```dart
// Flutter
final apiUrl = 'https://your-app.up.railway.app';
```

```javascript
// React Native
const API_URL = 'https://your-app.up.railway.app';
```

---

## 📚 Additional Resources

- **Railway Docs:** https://docs.railway.app
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **API Usage Guide:** See `API_USAGE.md`
- **Deployment README:** See `README_DEPLOYMENT.md`

## 🆘 Need Help?

1. Check Railway logs first
2. Review this guide's troubleshooting section
3. Check API documentation at `/docs`
4. Test endpoints with provided scripts
5. Verify model file uploaded correctly

---

**Ready to deploy? Start with Step 1!** 🚀
