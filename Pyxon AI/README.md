# 🚀 AI-Powered Document Parser with RAG Integration

A production-ready document parser designed for Retrieval-Augmented Generation (RAG) systems with intelligent chunking, Arabic language support, and comprehensive benchmarking.

## 🌐 Live Demo

**🔗 Try it now:** [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pyxon-ai-demo.streamlit.app)

> **Demo URL**: https://pyxon-ai-demo.streamlit.app  
> **Status**: 🟢 Live  
> **Uptime**: 24/7

### Quick Demo Guide:
1. **Upload** a PDF, DOCX, or TXT file (try Arabic text!)
2. **Choose** chunking strategy (Auto/Fixed/Dynamic)
3. **Search** your documents with natural language queries
4. **View** analytics and performance metrics

## ✨ Features

### 📄 Document Processing
- **Multi-format support**: PDF, DOCX, TXT
- **Intelligent chunking**: Automatic selection between fixed and dynamic strategies
- **Semantic analysis**: Understanding document structure, topics, and key concepts
- **Arabic language support**: Full support including diacritics (harakat/tashkeel)

### 🗄️ Storage
- **Vector Database**: ChromaDB for semantic search
- **SQL Database**: SQLite for structured queries and metadata
- **Hybrid retrieval**: Semantic + keyword-based search

### 📊 Advanced Features
- **Graph RAG**: Knowledge graph generation for improved retrieval
- **RAPTOR**: Recursive Abstractive Processing for hierarchical chunking
- **Benchmark suite**: Comprehensive evaluation metrics
- **RAG-ready**: Seamless integration with LLMs

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Document Input                        │
│                (PDF, DOCX, TXT)                         │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│              Document Parser                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │   PDF    │  │   DOCX   │  │   TXT    │             │
│  └──────────┘  └──────────┘  └──────────┘             │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│            Content Analyzer                              │
│  • Semantic Analysis                                     │
│  • Topic Extraction                                      │
│  • Strategy Selection                                    │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│          Chunking Engine                                 │
│  ┌──────────────┐    ┌──────────────┐                  │
│  │    Fixed     │    │   Dynamic    │                  │
│  │   Chunking   │    │   Chunking   │                  │
│  └──────────────┘    └──────────────┘                  │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│            Storage Layer                                 │
│  ┌─────────────────┐    ┌─────────────────┐            │
│  │   Vector DB     │    │    SQL DB       │            │
│  │   (ChromaDB)    │    │   (SQLite)      │            │
│  └─────────────────┘    └─────────────────┘            │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│              RAG Interface                               │
│  • Semantic Retrieval                                    │
│  • Hybrid Search                                         │
│  • LLM Integration                                       │
└─────────────────────────────────────────────────────────┘
```

## 🛠️ Technology Stack

- **Document Processing**: PyPDF2, python-docx, chardet
- **NLP & Embeddings**: 
  - HuggingFace transformers
  - sentence-transformers (all-MiniLM-L6-v2)
  - Arabic: CAMeLBERT, multilingual models
- **Vector DB**: ChromaDB
- **SQL DB**: SQLite
- **Chunking**: LangChain, custom algorithms
- **Web Framework**: Streamlit
- **Arabic NLP**: arabic-reshaper, python-bidi, AraBERT

## 📦 Installation

### Prerequisites
- Python 3.9 or higher
- pip package manager
- Git

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/pyxon-ai/pyxon-ai-entry-task.git
cd pyxon-ai-entry-task
```

2. **Create a virtual environment**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Download required models**
```bash
python scripts/download_models.py
```

## 🚀 Quick Start

### Run the Web Demo
```bash
streamlit run app.py
```
Access the demo at `http://localhost:8501`

### Command Line Interface
```bash
# Parse a single document
python cli.py parse --file document.pdf --strategy auto

# Parse with specific strategy
python cli.py parse --file document.docx --strategy dynamic

# Benchmark a document
python cli.py benchmark --file document.pdf
```

### Python API
```python
from src.parser import DocumentParser
from src.storage import VectorStore, SQLStore

# Initialize parser
parser = DocumentParser(
    language='ar',  # Arabic support
    strategy='auto'  # Auto-select chunking strategy
)

# Parse document
result = parser.parse('document.pdf')

# Store in databases
vector_store = VectorStore()
sql_store = SQLStore()

vector_store.add_chunks(result.chunks)
sql_store.add_metadata(result.metadata)

# Retrieve similar chunks
results = vector_store.search("ما هي الأهداف الرئيسية؟", k=5)
```

## 📊 Benchmark Suite

Run comprehensive benchmarks:

```bash
# Run all benchmarks
python benchmarks/run_all.py

# Run specific benchmarks
python benchmarks/accuracy_test.py
python benchmarks/chunking_quality.py
python benchmarks/performance_test.py
python benchmarks/arabic_test.py
```

### Metrics Evaluated
- **Retrieval Accuracy**: Precision, Recall, F1-score
- **Chunking Quality**: Semantic coherence, boundary accuracy
- **Performance**: Processing speed, memory usage, scalability
- **Arabic Support**: Text handling, diacritics preservation

## 🌐 Arabic Language Support

The system provides comprehensive Arabic language support:

- ✅ Right-to-left text directionality
- ✅ Arabic character encoding (UTF-8)
- ✅ Diacritics (harakat/tashkeel) preservation
- ✅ Arabic-specific NLP models (CAMeLBERT, AraBERT)
- ✅ Proper tokenization and text normalization

Example:
```python
# Parse Arabic document with diacritics
parser = DocumentParser(language='ar', preserve_diacritics=True)
result = parser.parse('arabic_document.pdf')

# Search with Arabic queries
results = vector_store.search("مَا هِيَ الأَهْدَافُ الرَّئِيسِيَّةُ؟")
```

## 🧪 Testing

Run tests:
```bash
# All tests
pytest

# Specific test suites
pytest tests/test_parser.py
pytest tests/test_chunking.py
pytest tests/test_arabic.py
pytest tests/test_storage.py

# With coverage
pytest --cov=src tests/
```

## 📈 Chunking Strategies

### Fixed Chunking
- **Use case**: Uniform documents (reports, forms, structured content)
- **Strategy**: Equal-sized chunks with overlap
- **Parameters**: chunk_size=512, overlap=50

### Dynamic Chunking
- **Use case**: Variable structure (books, articles, mixed content)
- **Strategy**: Semantic boundaries, topic modeling
- **Parameters**: Adaptive based on content analysis

### Auto Selection
The system automatically selects the best strategy based on:
- Document structure uniformity
- Content density
- Topic coherence
- Semantic variance

## 🔗 RAG Integration

The parser is designed for seamless RAG integration:

```python
from src.rag import RAGSystem

# Initialize RAG system
rag = RAGSystem(
    vector_store=vector_store,
    sql_store=sql_store,
    llm_model='gpt-4'
)

# Query with context retrieval
response = rag.query(
    question="What are the main objectives?",
    language="en"
)

# Arabic query
response = rag.query(
    question="ما هي الأهداف الرئيسية؟",
    language="ar"
)
```

## 📂 Project Structure

```
pyxon-ai-entry-task/
├── src/
│   ├── parser/
│   │   ├── __init__.py
│   │   ├── pdf_parser.py
│   │   ├── docx_parser.py
│   │   ├── txt_parser.py
│   │   └── base_parser.py
│   ├── chunking/
│   │   ├── __init__.py
│   │   ├── fixed_chunking.py
│   │   ├── dynamic_chunking.py
│   │   └── strategy_selector.py
│   ├── analyzer/
│   │   ├── __init__.py
│   │   ├── semantic_analyzer.py
│   │   └── topic_extractor.py
│   ├── storage/
│   │   ├── __init__.py
│   │   ├── vector_store.py
│   │   └── sql_store.py
│   ├── arabic/
│   │   ├── __init__.py
│   │   ├── normalizer.py
│   │   └── diacritics_handler.py
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── retriever.py
│   │   └── rag_system.py
│   └── utils/
│       ├── __init__.py
│       └── helpers.py
├── benchmarks/
│   ├── run_all.py
│   ├── accuracy_test.py
│   ├── chunking_quality.py
│   ├── performance_test.py
│   └── arabic_test.py
├── tests/
│   ├── test_parser.py
│   ├── test_chunking.py
│   ├── test_arabic.py
│   └── test_storage.py
├── scripts/
│   └── download_models.py
├── data/
│   ├── sample/
│   └── benchmarks/
├── app.py
├── cli.py
├── requirements.txt
├── setup.py
└── README.md
```

## 🎯 Future Improvements

- [ ] Multi-modal support (images, tables)
- [ ] Advanced Graph RAG features
- [ ] Real-time document streaming
- [ ] Cloud deployment (AWS/Azure)
- [ ] More language support
- [ ] Enhanced RAPTOR implementation
- [ ] Query optimization
- [ ] Caching layer

## 📞 Contact Information

**Email**: anas.mohammad6673332@gmail.com  
**Phone**: 00962786673332

## 📝 License

MIT License

## 🙏 Acknowledgments

- HuggingFace for transformer models
- ChromaDB team for vector database
- LangChain for chunking utilities
- Arabic NLP community

---

**Built with ❤️ for Pyxon AI Entry Task**
--