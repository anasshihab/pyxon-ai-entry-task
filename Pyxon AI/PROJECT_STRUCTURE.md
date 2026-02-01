# Project Structure

```
pyxon-ai-entry-task/
│
├── 📄 README.md                      # Main documentation
├── 📄 QUICKSTART.md                  # Quick start guide
├── 📄 PULL_REQUEST_TEMPLATE.md       # PR template with details
├── 📄 requirements.txt               # Python dependencies
├── 📄 setup.py                       # Package setup
├── 📄 .gitignore                     # Git ignore rules
├── 📄 .env.example                   # Environment variables template
│
├── 🎮 app.py                         # Streamlit web demo
├── 💻 cli.py                         # Command-line interface
│
├── 📁 src/                           # Main source code
│   ├── __init__.py
│   │
│   ├── 📁 parser/                    # Document parser module
│   │   ├── __init__.py
│   │   ├── base_parser.py            # Base classes and data models
│   │   ├── pdf_parser.py             # PDF document parser
│   │   ├── docx_parser.py            # DOCX document parser
│   │   └── txt_parser.py             # TXT document parser
│   │
│   ├── 📁 chunking/                  # Text chunking module
│   │   ├── __init__.py
│   │   ├── fixed_chunking.py         # Fixed-size chunking
│   │   ├── dynamic_chunking.py       # Semantic chunking
│   │   └── strategy_selector.py      # Auto strategy selection
│   │
│   ├── 📁 storage/                   # Database storage module
│   │   ├── __init__.py
│   │   ├── vector_store.py           # ChromaDB integration
│   │   └── sql_store.py              # SQLite integration
│   │
│   ├── 📁 arabic/                    # Arabic language support
│   │   ├── __init__.py
│   │   └── arabic_handler.py         # Arabic text processing
│   │
│   └── 📁 rag/                       # RAG system module
│       ├── __init__.py
│       └── rag_system.py             # RAG implementation
│
├── 📁 benchmarks/                    # Benchmark suite
│   ├── run_benchmarks.py             # Main benchmark runner
│   └── arabic_test.py                # Arabic-specific tests
│
├── 📁 tests/                         # Unit tests
│   ├── __init__.py
│   └── test_parser.py                # Parser tests
│
└── 📁 data/                          # Data directory
    ├── 📁 sample/                    # Sample documents
    │   ├── sample_english.txt
    │   └── sample_arabic.txt
    │
    ├── 📁 uploads/                   # Uploaded documents
    ├── 📁 chroma_db/                 # Vector database (created at runtime)
    └── 📄 documents.db               # SQL database (created at runtime)
```

## Module Descriptions

### 🎯 Core Modules

#### `src/parser/`
- **Purpose:** Document parsing and text extraction
- **Components:**
  - `base_parser.py`: Abstract classes, Chunk/Metadata models
  - `pdf_parser.py`: PDF processing with PyPDF2
  - `docx_parser.py`: Word document processing
  - `txt_parser.py`: Plain text with encoding detection
- **Key Features:**
  - Multi-format support
  - Automatic language detection
  - Metadata extraction

#### `src/chunking/`
- **Purpose:** Intelligent text chunking
- **Components:**
  - `fixed_chunking.py`: Equal-size chunks with overlap
  - `dynamic_chunking.py`: Semantic boundary detection
  - `strategy_selector.py`: Automatic strategy selection
- **Key Features:**
  - Strategy auto-selection
  - Document analysis
  - Quality metrics

#### `src/storage/`
- **Purpose:** Dual database management
- **Components:**
  - `vector_store.py`: Semantic search with ChromaDB
  - `sql_store.py`: Structured queries with SQLite
- **Key Features:**
  - Hybrid retrieval
  - Metadata management
  - Efficient indexing

#### `src/arabic/`
- **Purpose:** Arabic language support
- **Components:**
  - `arabic_handler.py`: Comprehensive Arabic processing
- **Key Features:**
  - Diacritics handling
  - Text normalization
  - RTL support

#### `src/rag/`
- **Purpose:** RAG system implementation
- **Components:**
  - `rag_system.py`: Retrieval and generation interface
- **Key Features:**
  - Hybrid retrieval
  - Context aggregation
  - LLM-ready interface

### 🛠️ Tools & Utilities

#### `app.py` - Web Demo
- **Technology:** Streamlit
- **Features:**
  - Document upload
  - Real-time parsing
  - Search interface
  - Analytics dashboard

#### `cli.py` - Command Line
- **Technology:** Click + Rich
- **Commands:**
  - `parse`: Parse documents
  - `search`: Search content
  - `list-documents`: View all docs
  - `stats`: Database statistics
  - `benchmark`: Run tests

### 🧪 Testing & Benchmarking

#### `benchmarks/`
- Performance testing
- Accuracy evaluation
- Arabic-specific tests
- Quality metrics

#### `tests/`
- Unit tests
- Integration tests
- Coverage testing

## Data Flow

```
1. Upload Document
   ↓
2. Parser Selection (PDF/DOCX/TXT)
   ↓
3. Text Extraction
   ↓
4. Language Detection
   ↓
5. Content Analysis
   ↓
6. Strategy Selection (Fixed/Dynamic)
   ↓
7. Chunking
   ↓
8. Embedding Generation
   ↓
9. Storage (Vector DB + SQL DB)
   ↓
10. Ready for Retrieval
```

## Technology Stack

| Layer | Technology |
|-------|-----------|
| **Document Processing** | PyPDF2, python-docx, chardet |
| **NLP & Embeddings** | sentence-transformers, HuggingFace |
| **Vector Database** | ChromaDB |
| **SQL Database** | SQLite |
| **Arabic Support** | arabic-reshaper, python-bidi, pyarabic |
| **Web Interface** | Streamlit |
| **CLI** | Click, Rich |
| **Testing** | pytest |

## Key Design Patterns

1. **Factory Pattern:** DocumentParser selects appropriate parser
2. **Strategy Pattern:** Chunking strategy selection
3. **Repository Pattern:** VectorStore and SQLStore abstractions
4. **Builder Pattern:** Chunk and Metadata creation
5. **Facade Pattern:** RAGSystem simplifies complex operations

---

**Contact:** Anas Mohammad | anas.mohammad6673332@gmail.com | 00962786673332
