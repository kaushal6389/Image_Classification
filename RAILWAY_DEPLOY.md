# Railway Deployment Instructions

## 🚀 Quick Deploy to Railway

### Step 1: Prepare Repository

1. **Add model file to .gitignore** (already done)
   - Model file is too large for GitHub (760MB)
   - Will be uploaded separately to Railway

2. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo.git
   git push -u origin main
   ```

### Step 2: Deploy to Railway

1. **Go to Railway.app**
   - Sign up/login: https://railway.app

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Railway will auto-detect:**
   - ✅ Python project
   - ✅ requirements_api.txt
   - ✅ Procfile (web command)
   - ✅ runtime.txt (Python 3.11)

### Step 3: Upload Model File

**Option A: Railway Volume (Recommended)**
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# Create volume and upload model
railway volume create model-storage
railway volume add model-storage /app/saved_models
railway upload model-storage saved_models/final_model_98plus.keras
```

**Option B: External Storage (e.g., AWS S3, Google Cloud Storage)**
1. Upload model to cloud storage
2. Update `api.py` to download model on startup:
```python
import urllib.request

MODEL_URL = "https://your-storage-url/final_model_98plus.keras"
if not os.path.exists(MODEL_PATH):
    print("Downloading model...")
    urllib.request.urlretrieve(MODEL_URL, MODEL_PATH)
```

**Option C: Direct Upload (Small projects)**
1. Go to Railway project settings
2. Navigate to "Data" tab
3. Upload `final_model_98plus.keras` manually

### Step 4: Configure Environment Variables

In Railway dashboard:
```
PORT = 8000  (auto-set by Railway)
PYTHONUNBUFFERED = 1
```

### Step 5: Deploy

Railway will automatically:
- Install dependencies from `requirements_api.txt`
- Start API using command in `Procfile`
- Assign public URL

### Step 6: Verify Deployment

1. **Check logs** in Railway dashboard
2. **Test API endpoints:**
   ```bash
   # Replace with your Railway URL
   curl https://your-app.up.railway.app/health
   ```

3. **Open docs:**
   ```
   https://your-app.up.railway.app/docs
   ```

## 📊 Resource Requirements

**Minimum:**
- Memory: 1GB RAM (for model loading)
- CPU: 1 core
- Storage: 1GB (for model file)

**Recommended:**
- Memory: 2GB RAM
- CPU: 2 cores
- Storage: 2GB

**Railway Plans:**
- Free: $5 credit/month (enough for testing)
- Hobby: $5/month (better for production)

## 🔧 Post-Deployment Configuration

### Custom Domain
1. Go to Railway project settings
2. Click "Domains"
3. Add custom domain
4. Update DNS records

### Monitoring
- Railway provides built-in monitoring
- Check logs for errors
- Monitor API usage

### Scaling
- Railway auto-scales based on traffic
- For high traffic, upgrade plan

## 🐛 Common Issues

### Model File Not Found
```bash
# Check if model exists
railway run ls saved_models/

# Upload if missing
railway upload model-storage saved_models/final_model_98plus.keras
```

### Out of Memory
- Upgrade Railway plan to 2GB+ RAM
- Model requires ~1GB RAM to load

### Slow Startup
- First request may be slow (model loading)
- Subsequent requests will be fast
- Consider keeping API warm with periodic health checks

### Build Fails
```bash
# Check logs
railway logs

# Common fixes:
# 1. Verify requirements_api.txt has all dependencies
# 2. Check Python version in runtime.txt
# 3. Ensure Procfile command is correct
```

## 🔐 Security Best Practices

1. **API Key (Optional)**
   ```python
   # Add to api.py
   from fastapi import Header, HTTPException
   
   async def verify_api_key(x_api_key: str = Header(...)):
       if x_api_key != os.getenv("API_KEY"):
           raise HTTPException(status_code=401, detail="Invalid API Key")
   ```

2. **Rate Limiting**
   ```bash
   pip install slowapi
   ```
   ```python
   from slowapi import Limiter
   limiter = Limiter(key_func=get_remote_address)
   
   @app.post("/predict")
   @limiter.limit("10/minute")
   async def predict(...):
       ...
   ```

3. **CORS Configuration**
   - Limit to specific domains in production
   - Update in `api.py`

## 📱 Mobile App Connection

Update your mobile app API endpoint:
```
https://your-app.up.railway.app
```

Test from mobile app:
```javascript
const API_URL = 'https://your-app.up.railway.app';
```

## 💰 Cost Estimation

**Railway Pricing:**
- Hobby Plan: $5/month
- Usage: ~$0.01 per hour of uptime
- Bandwidth: Free for first 100GB

**Expected Monthly Cost:**
- Low traffic: $5-10
- Medium traffic: $10-20
- High traffic: $20-50

## 🎉 Deployment Checklist

- [ ] Push code to GitHub
- [ ] Create Railway project
- [ ] Upload model file
- [ ] Configure environment variables
- [ ] Deploy and verify
- [ ] Test all endpoints
- [ ] Set up custom domain (optional)
- [ ] Configure monitoring
- [ ] Update mobile app URL
- [ ] Test from mobile app

## 📚 Additional Resources

- Railway Docs: https://docs.railway.app
- FastAPI Docs: https://fastapi.tiangolo.com
- TensorFlow Serving: https://www.tensorflow.org/tfx/guide/serving

---

**Ready to deploy? Follow the steps above!** 🚀
