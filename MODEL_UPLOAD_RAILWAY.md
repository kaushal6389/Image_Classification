# 📦 Model Upload to Railway - Step by Step Guide

## ⚠️ Important: Model file (760MB) को Railway पर upload करना है

GitHub पर code है, लेकिन model file बहुत बड़ी है (760MB), इसलिए अलग से upload करनी होगी।

---

## 🚀 Method 1: Railway CLI (Command Line)

### Step 1: Railway CLI Install करो

```powershell
# Node.js installed होना चाहिए (check करो)
node --version

# Railway CLI install करो
npm install -g @railway/cli
```

### Step 2: Railway में Login करो

```powershell
# Login command
railway login
```

- Browser खुलेगा
- GitHub account से login करो
- "Authorize Railway" पर click करो
- Terminal में success message आएगा

### Step 3: Project को Link करो

```powershell
# अपने project folder में जाओ
cd E:\Image_classifier

# Railway project link करो
railway link
```

- Terminal में list दिखेगी आपकी Railway projects की
- Arrow keys से अपनी project select करो
- Enter press करो

### Step 4: Model File Upload करो

**Option A: Direct Copy (Recommended)**

```powershell
# Model file को Railway पर copy करो
railway run powershell -Command "New-Item -ItemType Directory -Force -Path '/app/saved_models'; Copy-Item 'saved_models/final_model_98plus.keras' '/app/saved_models/'"
```

**Option B: Using Volume (Persistent Storage)**

```powershell
# Volume create करो
railway volume create model-storage

# Volume mount करो
railway volume add model-storage /app/saved_models

# Model upload करो
railway run powershell -Command "Copy-Item 'saved_models/final_model_98plus.keras' '/app/saved_models/'"
```

### Step 5: Verify Upload

```powershell
# Check करो file upload हुई या नहीं
railway run ls /app/saved_models/

# Output में दिखना चाहिए:
# final_model_98plus.keras
```

### Step 6: Restart Deployment

```powershell
# Railway app restart करो
railway restart
```

---

## 🌐 Method 2: Railway Dashboard (Web Interface)

अगर CLI से problem आए तो ये simple method use करो:

### Step 1: Railway Dashboard खोलो
1. Go to: https://railway.app
2. अपनी project खोलो: `Image_Classification`

### Step 2: Settings में जाओ
1. Left sidebar में "Settings" click करो
2. Scroll करो "Volumes" section तक

### Step 3: Volume Create करो
1. "Add Volume" button click करो
2. Volume Name: `model-storage`
3. Mount Path: `/app/saved_models`
4. "Create Volume" click करो

### Step 4: Model Upload करो
दो तरीके हैं:

**Option A: Railway CLI से (Simpler)**
```powershell
cd E:\Image_classifier
railway login
railway link
railway volume upload model-storage saved_models/final_model_98plus.keras /saved_models/
```

**Option B: Manual FTP/SFTP** (यदि CLI काम न करे)
1. Railway dashboard में "Connect" button ढूंढो
2. SFTP credentials copy करो
3. FileZilla या WinSCP use करके upload करो

---

## ✅ Verification Steps

### 1. Check Logs
```powershell
railway logs
```

देखो ये message आता है:
```
✅ Model loaded: 760.0 MB, Params: 197,000,000
🚀 STARTING STREET INFRASTRUCTURE CLASSIFIER API
```

### 2. Test Health Endpoint
```powershell
# Railway URL के साथ test करो
curl https://your-app.up.railway.app/health
```

Expected Response:
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model_size_mb": 760.0,
  "model_params": 197000000
}
```

---

## 🐛 Common Issues & Solutions

### Issue 1: Railway CLI Install नहीं हो रहा

**Solution:**
```powershell
# Node.js check करो
node --version

# अगर Node.js नहीं है, install करो
# Download from: https://nodejs.org/

# फिर Railway CLI install करो
npm install -g @railway/cli
```

### Issue 2: Model Upload Failed / Timeout

**Solution:**
```powershell
# Smaller chunks में upload करो
# या Railway dashboard से directly upload करो
```

### Issue 3: Model File Not Found Error

**Solution:**
Check paths:
```powershell
# Local path check करो
ls saved_models/

# Railway पर path check करो
railway run ls /app/saved_models/
```

### Issue 4: Permission Denied

**Solution:**
```powershell
# Railway से logout और फिर login करो
railway logout
railway login
```

---

## 📊 Expected Timeline

- **Railway CLI Install:** 2-3 minutes
- **Login & Link:** 1-2 minutes
- **Model Upload:** 5-10 minutes (depends on internet speed)
- **Deployment Restart:** 2-3 minutes
- **Total Time:** ~15-20 minutes

---

## 🎯 Final Checklist

- [ ] Railway CLI installed (`railway --version`)
- [ ] Logged in to Railway (`railway login`)
- [ ] Project linked (`railway link`)
- [ ] Model file uploaded (760MB)
- [ ] Deployment restarted (`railway restart`)
- [ ] Health check passes (`/health` endpoint)
- [ ] API working (`/predict` endpoint)

---

## 💡 Pro Tips

1. **Fast Upload:** Use stable WiFi connection
2. **Verify First:** Check model file locally before upload
   ```powershell
   ls -l saved_models/final_model_98plus.keras
   ```
3. **Monitor Logs:** Keep `railway logs` running during deployment
4. **Test Locally:** Test API locally before Railway deployment
   ```powershell
   python api.py
   ```

---

## 📞 Need Help?

**Railway Docs:** https://docs.railway.app/reference/cli-api
**Project GitHub:** https://github.com/kaushal6389/Image_Classification

---

## ✨ Success Message

जब model upload हो जाए और API start हो जाए:

```
✅ Model loaded successfully
🚀 STARTING STREET INFRASTRUCTURE CLASSIFIER API
📊 Model: final_model_98plus.keras (97.84% accuracy)
🌐 API URL: https://your-app.up.railway.app
📚 Docs: https://your-app.up.railway.app/docs
```

**Tab खोलो:** `https://your-app.up.railway.app/docs` - Interactive API documentation!

---

**Ready? Start with Step 1!** 🚀
