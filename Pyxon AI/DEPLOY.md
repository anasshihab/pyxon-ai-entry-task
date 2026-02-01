# 🚀 Deployment Guide - Streamlit Cloud

## Quick Deploy (5 minutes)

### Step 1: Prepare Your Repository

1. **Make sure your repository is the one you want to deploy from:**
   ```
   https://github.com/anasshihab/pyxon-ai-entry-task.git
   ```

2. **Ensure these files are in your repo:**
   - ✅ `app.py` (main Streamlit app)
   - ✅ `requirements.txt` (dependencies)
   - ✅ `README.md` (with demo link)
   - ✅ `.gitignore` (excluding data/, .venv/)

### Step 2: Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud:**
   - Visit: https://share.streamlit.io/
   - Sign in with your GitHub account

2. **Create New App:**
   - Click "New app" button
   - Fill in:
     - **Repository**: `anasshihab/pyxon-ai-entry-task`
     - **Branch**: `main` (or `master`)
     - **Main file path**: `app.py`
   - Click "Deploy"!

3. **Wait for Deployment:**
   - First deployment takes 5-10 minutes
   - Installing dependencies
   - Downloading models
   - Starting app

4. **Get Your URL:**
   - Your app will be live at something like:
   - `https://anasshihab-pyxon-ai-entry-task-app-xxxxx.streamlit.app`
   - Or choose a custom URL: `https://pyxon-ai-demo.streamlit.app`

### Step 3: Update README

Once deployed, update your README.md with the actual URL:

1. Open `README.md`
2. Find the Live Demo section (line ~8)
3. Replace `https://pyxon-ai-demo.streamlit.app` with your actual URL
4. Commit and push:
   ```bash
   git add README.md
   git commit -m "Update demo URL"
   git push
   ```

### Step 4: Create Pull Request

1. **Go to the original repository:**
   ```
   https://github.com/pyxon-ai/pyxon-ai-entry-task
   ```

2. **Click "Fork" (if you haven't already)**

3. **Create Pull Request:**
   - Click "New Pull Request"
   - Base repository: `pyxon-ai/pyxon-ai-entry-task`
   - Head repository: `anasshihab/pyxon-ai-entry-task`
   - Click "Create Pull Request"

4. **Fill in PR Details:**
   - Title: "Pyxon AI Entry Task - Anas Mohammad"
   - Description: Use the template from `PULL_REQUEST_TEMPLATE.md`
   - Include:
     - ✅ Contact info (email, phone)
     - ✅ Demo URL
     - ✅ Implementation summary
     - ✅ Architecture details
     - ✅ Questions/assumptions

5. **Submit!**

---

## 📝 Example PR Description

```markdown
# Pyxon AI Entry Task Submission

## Contact Information
📧 **Email:** anas.mohammad6673332@gmail.com  
📱 **Phone:** 00962786673332

## Live Demo
🔗 **Demo URL:** https://your-actual-demo-url.streamlit.app

## Implementation Summary
This solution provides a complete AI-powered document parser with:
- ✅ Multi-format support (PDF, DOCX, TXT)
- ✅ Intelligent chunking (fixed & dynamic strategies)
- ✅ Dual database system (ChromaDB + SQLite)
- ✅ Full Arabic language support with diacritics
- ✅ RAG system integration
- ✅ Comprehensive benchmarking

## Key Features
1. **Smart Chunking**: Automatically selects best strategy
2. **Arabic Support**: Full harakat/tashkeel preservation
3. **Hybrid Search**: Semantic + keyword retrieval
4. **Web Interface**: User-friendly Streamlit app
5. **CLI Tool**: Command-line interface included

## Architecture
- Parser layer: Handles PDF, DOCX, TXT
- Chunking layer: Fixed & dynamic strategies
- Storage layer: Vector (ChromaDB) + SQL (SQLite)
- RAG layer: Retrieval-augmented generation ready

## Technologies
- Python 3.9+
- Streamlit (UI)
- ChromaDB (Vector DB)
- SQLite (SQL DB)
- sentence-transformers (Embeddings)
- Arabic NLP libraries

## How to Run Locally
```bash
git clone https://github.com/anasshihab/pyxon-ai-entry-task.git
cd pyxon-ai-entry-task
pip install -r requirements.txt
streamlit run app.py
```

## Questions & Assumptions
1. **Deployment**: Deployed on Streamlit Cloud for easy access
2. **Models**: Using sentence-transformers for embeddings
3. **Arabic**: Full support with optional diacritic preservation
4. **Scale**: Optimized for 100-1000 documents

Looking forward to your feedback!

**Anas Mohammad**  
📧 anas.mohammad6673332@gmail.com  
📱 00962786673332
```

---

## ✅ Deployment Checklist

Before submitting:
- [ ] Code is pushed to your GitHub repo
- [ ] App is deployed to Streamlit Cloud
- [ ] Demo URL is working
- [ ] README has demo link
- [ ] All features are working online
- [ ] Arabic text displays correctly  
- [ ] Tested uploading documents
- [ ] Search functionality works
- [ ] PR is created with all details
- [ ] Contact information is included

---

## 🎯 Expected Results

### Your deployed app should:
1. ✅ Load without errors
2. ✅ Allow file uploads (PDF/DOCX/TXT)
3. ✅ Display Arabic text correctly (RTL)
4. ✅ Search documents with queries
5. ✅ Show analytics dashboard
6. ✅ Handle errors gracefully

### Performance:
- First load: ~30-60 seconds (model download)
- Subsequent loads: ~5-10 seconds
- Upload & process: ~2-5 seconds per document

---

## 🆘 Troubleshooting

### Issue: App crashes on startup
**Solution**: Check Streamlit Cloud logs for errors

### Issue: Models not downloading
**Solution**: Streamlit Cloud has internet access, models auto-download

### Issue: Out of memory
**Solution**: Use smaller embedding models in requirements.txt

### Issue: Slow loading
**Solution**: Normal for first load; subsequent loads are faster

---

## 📞 Need Help?

**Developer**: Anas Mohammad  
**Email**: anas.mohammad6673332@gmail.com  
**Phone**: 00962786673332

---

Good luck with your deployment! 🚀
