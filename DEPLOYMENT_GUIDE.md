# 🚀 How to Deploy Your Analysis Online

You have 2 options: **Streamlit Cloud** (interactive) or **GitHub Pages** (static).

---

## Option 1: Streamlit Cloud (RECOMMENDED) ⭐

### What you get:
- ✅ Interactive charts (hover, zoom, pan)
- ✅ Beautiful web interface
- ✅ Free hosting
- ✅ URL: `your-app.streamlit.app`
- ✅ Updates automatically when you push to GitHub

### Steps to deploy:

#### 1. Create GitHub repository

```bash
cd /Users/konstantinosfotiou/Documents/mariye

# Initialize git if not already done
git init

# Create .gitignore
echo "*.png
*.csv
__pycache__/
.DS_Store
divorce_analysis.py
article_analysis.py" > .gitignore

# Add files
git add app.py requirements.txt OHJE_MARIOKSELLE.md api.md
git commit -m "Initial commit: Marriage divorce analysis app"

# Create repo on GitHub (do this in browser: github.com/new)
# Then connect it:
git remote add origin https://github.com/YOUR_USERNAME/mariye.git
git branch -M main
git push -u origin main
```

#### 2. Deploy to Streamlit Cloud

1. Go to: **https://share.streamlit.io/**
2. Sign in with GitHub
3. Click **"New app"**
4. Select:
   - **Repository:** `YOUR_USERNAME/mariye`
   - **Branch:** `main`
   - **Main file path:** `app.py`
5. Click **"Deploy"**

**Done!** Your app will be live at: `https://YOUR_USERNAME-mariye.streamlit.app`

⏱️ Takes ~2-3 minutes to deploy

---

## Option 2: GitHub Pages (Simple Static Version)

If you want a simpler static page (no Python running), I can create an HTML version.

### Pros:
- ✅ Very simple
- ✅ Fast loading
- ✅ Free hosting

### Cons:
- ❌ No interactivity
- ❌ Just displays images

Would you like me to create this too? Just ask!

---

## Option 3: Observable (Data Visualization Focus)

If you want super fancy interactive data viz:
- https://observablehq.com/
- Uses JavaScript
- Great for embedding

---

## 🎯 My Recommendation

**Use Streamlit Cloud** - it's perfect for this project:
- Your analysis is in Python
- Interactive charts are better than static images
- Free and easy to deploy
- Professional looking
- Can update data easily

---

## 🔄 How to Update Your Deployed App

Once deployed, just:

```bash
cd /Users/konstantinosfotiou/Documents/mariye

# Make changes to app.py
# Then:
git add app.py
git commit -m "Updated analysis"
git push

# Streamlit Cloud will automatically redeploy!
```

---

## 🧪 Test Locally First

Before deploying, test it locally:

```bash
cd /Users/konstantinosfotiou/Documents/mariye
streamlit run app.py
```

Opens at: http://localhost:8501

---

## 📱 Share Your App

Once deployed, just share the URL:
- `https://your-app.streamlit.app`

Anyone can access it (no login needed)!

---

## 💡 Tips

1. **Keep it in sync:**
   - Don't push large files (*.png, *.csv already in .gitignore)
   - Only push code files

2. **Update data:**
   - Edit the `data` dictionary in `app.py`
   - Push changes
   - Auto-deploys

3. **Custom domain:**
   - Streamlit Cloud allows custom domains (free tier limited)
   - Or use GitHub Pages with your own domain

---

## 🆘 Need Help?

**Streamlit Docs:** https://docs.streamlit.io/  
**Deployment Guide:** https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app

Let me know if you need help with any step!

