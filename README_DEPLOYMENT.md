# Street Infrastructure Image Classifier API

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template)

High-accuracy AI-powered street infrastructure detection API for mobile apps and web dashboards.

## 🚀 Features

- **97.84% Accuracy** - ConvNeXtLarge model
- **6 Classes** - garbage, open_manhole, potholes, road_normal, streetlight_bad, streetlight_good
- **FastAPI** - High-performance async API
- **Priority Levels** - CRITICAL, HIGH, MEDIUM, LOW for dashboard integration
- **Batch Processing** - Process multiple images at once
- **CORS Enabled** - Ready for web/mobile integration

## 📦 Deployment

### Railway Deployment

1. **Fork this repository**

2. **Add Model File**
   - Download `final_model_98plus.keras` from Kaggle
   - Upload to Railway as persistent volume or external storage
   - Update `MODEL_PATH` in `api.py`

3. **Deploy to Railway**
   ```bash
   # Install Railway CLI
   npm install -g @railway/cli
   
   # Login
   railway login
   
   # Deploy
   railway up
   ```

4. **Environment Variables** (Set in Railway dashboard)
   ```
   PORT=8000
   ```

5. **Access API**
   - API: `https://your-app.railway.app`
   - Docs: `https://your-app.railway.app/docs`

### Alternative: Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements_api.txt .
RUN pip install --no-cache-dir -r requirements_api.txt

COPY api.py .
COPY saved_models/final_model_98plus.keras ./saved_models/

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:
```bash
docker build -t street-classifier-api .
docker run -p 8000:8000 street-classifier-api
```

## 🔌 API Endpoints

### Health Check
```http
GET /health
```

### Predict Single Image
```http
POST /predict
Content-Type: multipart/form-data

{
  "file": <image_file>
}
```

**Response:**
```json
{
  "success": true,
  "predicted_class": "potholes",
  "confidence": 98.45,
  "priority": "HIGH",
  "description": "Road pothole - Needs repair"
}
```

### Predict Batch (Max 10 images)
```http
POST /predict/batch
Content-Type: multipart/form-data

{
  "files": [<image_files>]
}
```

## 💻 Local Development

1. **Clone repository**
   ```bash
   git clone https://github.com/yourusername/street-classifier-api.git
   cd street-classifier-api
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements_api.txt
   ```

3. **Download model**
   - Place `final_model_98plus.keras` in `saved_models/` folder

4. **Run API**
   ```bash
   python api.py
   ```

5. **Test API**
   ```bash
   python test_api.py
   ```

## 📱 Mobile App Integration

### Flutter Example
```dart
import 'package:http/http.dart' as http;

Future<Map<String, dynamic>> predictImage(File imageFile) async {
  var request = http.MultipartRequest(
    'POST', 
    Uri.parse('https://your-api.railway.app/predict')
  );
  
  request.files.add(
    await http.MultipartFile.fromPath('file', imageFile.path)
  );
  
  var response = await request.send();
  var responseData = await response.stream.bytesToString();
  return jsonDecode(responseData);
}
```

### JavaScript/React Example
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('https://your-api.railway.app/predict', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => {
  console.log('Predicted:', data.predicted_class);
  console.log('Priority:', data.priority);
});
```

## 🎯 Priority Levels

| Class | Priority | Action |
|-------|----------|--------|
| open_manhole | CRITICAL | Immediate action required |
| potholes | HIGH | Repair needed soon |
| garbage | MEDIUM | Schedule cleanup |
| streetlight_bad | MEDIUM | Maintenance required |
| streetlight_good | LOW | No action |
| road_normal | LOW | No action |

## 📊 Model Details

- **Architecture:** ConvNeXtLarge
- **Parameters:** 197M
- **Image Size:** 384x384
- **Accuracy:** 97.84%
- **Training:** 3-stage gradual unfreezing

## 🔧 Configuration

### Change Port
```python
# api.py
uvicorn.run(app, host="0.0.0.0", port=8080)
```

### Enable CORS for Specific Domains
```python
# api.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-domain.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📝 Requirements

- Python 3.11+
- TensorFlow 2.16+
- FastAPI 0.104+
- See `requirements_api.txt` for full list

## 🐛 Troubleshooting

### Model File Not Found
- Download model from Kaggle or training output
- Place in `saved_models/` directory
- Check path in `api.py` (`MODEL_PATH`)

### Out of Memory
- Model is ~760MB, requires sufficient RAM
- Railway: Use at least 1GB RAM plan
- Reduce batch size if needed

### Slow Predictions
- Model optimized for GPU (optional)
- CPU inference takes 1-3 seconds per image
- Use batch endpoint for multiple images

## 📄 License

MIT License - Free for personal and commercial use

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📞 Support

- **Documentation:** See `API_USAGE.md`
- **Issues:** GitHub Issues
- **API Docs:** `https://your-api.railway.app/docs`

---

**Created:** December 2025  
**Model Accuracy:** 97.84%  
**Framework:** TensorFlow + FastAPI
