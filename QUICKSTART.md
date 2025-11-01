# ⚡ Quick Start Guide

Get your Architecture Diagram Generator running in 5 minutes!

## 🎯 For Local Development

### 1. Install Dependencies

```bash
# Install Graphviz (required)
# Windows: Download from https://graphviz.org/download/
# macOS:
brew install graphviz
# Linux:
sudo apt-get install graphviz

# Install Python packages
pip install -r requirements.txt
```

### 2. Set Up API Key

```bash
# Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env

# Get API key from: https://makersuite.google.com/app/apikey
```

### 3. Run the App

```bash
streamlit run streamlit_app.py
```

Open browser to `http://localhost:8501` 🎉

---

## ☁️ For Streamlit Cloud Deployment

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "New app"
3. Select your repository
4. Set main file: `streamlit_app.py`
5. Click "Deploy"

### 3. Add API Key (Secrets)

In Streamlit Cloud app settings → Secrets:

```toml
GEMINI_API_KEY = "your_api_key_here"
```

Done! Your app is live! 🚀

---

## 💡 Example Prompts to Try

### Simple Microservices
```
Create a microservices architecture with API Gateway, 
3 microservices, and PostgreSQL database
```

### AWS Serverless
```
Serverless app with API Gateway, Lambda, DynamoDB, and S3
```

### Kubernetes
```
Kubernetes deployment with 3 pods, ingress, and Redis cache
```

---

## 🐛 Common Issues

### "Graphviz not found"
- Install Graphviz and add to PATH
- Restart terminal after installation

### "Invalid API key"
- Check API key in `.env` or Streamlit secrets
- No extra spaces or quotes

### App crashes on generate
- Check logs for specific errors
- Try simpler prompt first
- Verify all dependencies installed

---

## 📚 More Help

- Full README: [README.md](README.md)
- Deployment Guide: [DEPLOYMENT.md](DEPLOYMENT.md)
- Get API Key: [Google AI Studio](https://makersuite.google.com/app/apikey)

---

**Happy Diagramming!** 🎨

