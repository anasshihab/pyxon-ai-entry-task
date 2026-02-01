# 🚀 Quick Start Guide

Welcome to the AI-Powered Document Parser! This guide will help you get started quickly.

## Installation (5 minutes)

### Step 1: Clone & Setup
```bash
# Clone the repository
git clone https://github.com/pyxon-ai/pyxon-ai-entry-task.git
cd pyxon-ai-entry-task

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

This will install all required packages including:
- Document parsers (PyPDF2, python-docx)
- NLP models (sentence-transformers)
- Databases (ChromaDB, SQLite)
- Arabic support (arabic-reshaper, python-bidi)
- Web interface (Streamlit)

## Running the Demo (2 minutes)

### Web Interface (Recommended)
```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

### Command Line Interface
```bash
# Parse a document
python cli.py parse --file data/sample/sample_english.txt

# Search documents
python cli.py search --query "machine learning"

# View statistics
python cli.py stats
```

## Usage Examples

### 1. Upload and Parse a Document

**Web Interface:**
1. Click "Upload & Parse" in sidebar
2. Upload your PDF, DOCX, or TXT file
3. Configure language and chunking strategy
4. Click "Parse Document"
5. View results and generated chunks

**CLI:**
```bash
python cli.py parse --file your_document.pdf --strategy auto --language en
```

### 2. Search Documents

**Web Interface:**
1. Click "Search & Retrieve" in sidebar
2. Enter your search query
3. Filter by language or document
4. View ranked results

**CLI:**
```bash
python cli.py search --query "artificial intelligence" --num-results 10
```

### 3. Test with Arabic

**Sample Arabic Document:**
```bash
python cli.py parse --file data/sample/sample_arabic.txt --language ar --preserve-diacritics
```

**Search in Arabic:**
```bash
python cli.py search --query "الذكاء الاصطناعي" --language ar
```

## Testing the System

### Run Sample Test
```bash
# Parse English sample
python cli.py parse --file data/sample/sample_english.txt

# Parse Arabic sample
python cli.py parse --file data/sample/sample_arabic.txt

# Search both
python cli.py search --query "AI"
```

### Run Benchmarks
```bash
# Full benchmark suite
python benchmarks/run_benchmarks.py

# Arabic-specific tests
python benchmarks/arabic_test.py
```

## Python API Example

```python
from src import DocumentParser, VectorStore, SQLStore, RAGSystem

# Initialize
parser = DocumentParser(language='en', strategy='auto')
vector_store = VectorStore()
sql_store = SQLStore()

# Parse document
result = parser.parse_with_chunking('document.pdf', chunk_size=512)

# Store
vector_store.add_chunks(result.chunks)
sql_store.add_document(result.metadata)
sql_store.add_chunks(result.chunks)

# Search
rag = RAGSystem(vector_store, sql_store)
response = rag.query("What is this document about?", k=5)

print(f"Found {len(response['sources'])} relevant chunks")
print(f"Context: {response['context'][:500]}...")
```

## Key Features to Try

### 1. Automatic Strategy Selection
Upload different types of documents and observe how the system automatically selects the best chunking strategy:
- **Structured documents** (reports, forms) → Fixed chunking
- **Variable content** (books, articles) → Dynamic chunking

### 2. Arabic Support
Test full Arabic support:
```python
from src.arabic import ArabicHandler

handler = ArabicHandler(preserve_diacritics=True)

# Test text with diacritics
text = "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ"
print(f"Diacritics count: {handler.count_diacritics(text)}")
print(f"Without diacritics: {handler.remove_diacritics(text)}")
```

### 3. Hybrid Search
The system combines semantic and keyword search for better results:
```python
results = rag.retriever.retrieve_hybrid(
    query="machine learning applications",
    k=5,
    alpha=0.7  # Weight for semantic vs keyword
)
```

## Troubleshooting

### Issue: Import errors
**Solution:** Make sure virtual environment is activated and all dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: ChromaDB errors
**Solution:** Delete the ChromaDB directory and restart
```bash
rm -rf data/chroma_db
```

### Issue: Arabic text not displaying correctly
**Solution:** Ensure terminal/browser supports UTF-8 encoding

### Issue: Slow parsing
**Solution:** For large documents, use smaller chunk sizes or process in batches

## Next Steps

1. **Explore the Code:** Check `src/` directory for implementation details
2. **Run Benchmarks:** See `benchmarks/` for performance tests
3. **Customize:** Modify chunking strategies, embedding models, or add new parsers
4. **Deploy:** Use the deployment guide to host on cloud platforms

## Support

**Developer:** Anas Mohammad
**Email:** anas.mohammad6673332@gmail.com
**Phone:** 00962786673332

## Resources

- [Full Documentation](README.md)
- [Architecture Details](PULL_REQUEST_TEMPLATE.md)
- [API Reference](docs/API.md) *(coming soon)*

---

🎉 **You're all set! Start parsing documents and exploring the system!**
