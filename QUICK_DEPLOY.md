# 🚀 Quick Deploy Commands

## GitHub Setup
```bash
cd E:\Image_classifier
git init
git add .
git commit -m "Initial commit: Street Infrastructure Classifier API"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/street-infrastructure-classifier.git
git push -u origin main
```

## Railway Deploy (Web)
1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Choose repository
4. Wait for auto-deploy
5. Upload model file (760MB) to `/app/saved_models/`

## Railway Deploy (CLI)
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

## Test Deployment
```bash
# Replace URL with your Railway URL
curl https://your-app.up.railway.app/health
curl https://your-app.up.railway.app/classes
```

## Open Docs
```
https://your-app.up.railway.app/docs
```

---

## Files Created ✅

- `.gitignore` - Excludes model/data/notebooks
- `Procfile` - Railway startup command
- `runtime.txt` - Python 3.11
- `Dockerfile` - Container config
- `README_DEPLOYMENT.md` - User docs
- `GITHUB_RAILWAY_GUIDE.md` - Full deployment guide
- `RAILWAY_DEPLOY.md` - Railway-specific instructions

## Next Steps

1. **Push to GitHub** - See `GITHUB_RAILWAY_GUIDE.md` Step 1
2. **Deploy to Railway** - See `GITHUB_RAILWAY_GUIDE.md` Step 2
3. **Upload Model** - See `GITHUB_RAILWAY_GUIDE.md` Step 3
4. **Test API** - See `GITHUB_RAILWAY_GUIDE.md` Step 4

---

**Model File:** `saved_models/final_model_98plus.keras` (760MB)
**Accuracy:** 97.84%
**API Framework:** FastAPI
**Deployment:** Railway
