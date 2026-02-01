# 🎓 Development Guide

Complete guide for developers working on the AI Document Parser project.

## 📋 Table of Contents

1. [Setup Development Environment](#setup)
2. [Code Architecture](#architecture)
3. [Adding New Features](#features)
4. [Testing Guidelines](#testing)
5. [Contributing](#contributing)
6. [Deployment](#deployment)

## 🛠️ Setup Development Environment {#setup}

### Prerequisites
- Python 3.9+
- Git
- Virtual environment tool
- Text editor/IDE

### Initial Setup
```bash
# Clone repository
git clone https://github.com/pyxon-ai/pyxon-ai-entry-task.git
cd pyxon-ai-entry-task

# Set up virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Install in development mode
pip install -e .
```

### Development Tools
```bash
# Install development tools
pip install black flake8 mypy pytest-cov

# Format code
black src/

# Lint code
flake8 src/

# Type check
mypy src/
```

## 🏗️ Code Architecture {#architecture}

### Design Principles

1. **Modularity**: Each module has a single responsibility
2. **Extensibility**: Easy to add new parsers, chunking strategies
3. **Testability**: All components are unit-testable
4. **Type Safety**: Comprehensive type hints

### Adding a New Parser

```python
# src/parser/new_parser.py
from .base_parser import BaseParser, ParseResult, DocumentMetadata

class NewFormatParser(BaseParser):
    """Parser for new document format"""
    
    def parse(self, file_path: str) -> ParseResult:
        # Implementation
        pass
    
    def extract_text(self, file_path: str) -> str:
        # Implementation
        pass
```

Register in `src/parser/__init__.py`:
```python
from .new_parser import NewFormatParser

# Add to DocumentParser
self.parsers = {
    '.newformat': NewFormatParser(language, preserve_diacritics)
}
```

### Adding a New Chunking Strategy

```python
# src/chunking/new_strategy.py
from typing import List
from ..parser.base_parser import Chunk

class NewChunkingStrategy:
    """New chunking approach"""
    
    def chunk(self, text: str, document_id: str) -> List[Chunk]:
        # Implementation
        chunks = []
        # ... chunking logic
        return chunks
```

Register in `src/chunking/__init__.py`.

### Adding a New Storage Backend

```python
# src/storage/new_store.py
from typing import List, Dict, Any
from ..parser.base_parser import Chunk

class NewStore:
    """New storage backend"""
    
    def add_chunks(self, chunks: List[Chunk]) -> Dict[str, int]:
        # Implementation
        pass
    
    def search(self, query: str, k: int) -> List[Dict[str, Any]]:
        # Implementation
        pass
```

## ✨ Adding New Features {#features}

### Feature Development Workflow

1. **Create Feature Branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Implement Feature**
- Write code in appropriate module
- Add type hints
- Write docstrings
- Follow naming conventions

3. **Add Tests**
```python
# tests/test_your_feature.py
def test_your_feature():
    # Test implementation
    assert True
```

4. **Update Documentation**
- Update README if needed
- Add to CHANGELOG
- Update type stubs

5. **Commit & Push**
```bash
git add .
git commit -m "feat: add new feature"
git push origin feature/your-feature-name
```

### Example: Adding OCR Support

```python
# src/parser/ocr_parser.py
import pytesseract
from PIL import Image
from .pdf_parser import PDFParser

class OCRPDFParser(PDFParser):
    """PDF parser with OCR for scanned documents"""
    
    def __init__(self, language: str = 'en', preserve_diacritics: bool = True):
        super().__init__(language, preserve_diacritics)
        self.ocr_enabled = True
    
    def extract_text(self, file_path: str) -> str:
        # Try normal extraction first
        text = super().extract_text(file_path)
        
        # If no text, use OCR
        if not text.strip():
            text = self._ocr_extract(file_path)
        
        return text
    
    def _ocr_extract(self, file_path: str) -> str:
        # Convert PDF to images and OCR
        # Implementation here
        pass
```

## 🧪 Testing Guidelines {#testing}

### Test Structure

```python
# tests/test_module.py
import pytest
from src.module import YourClass

class TestYourClass:
    """Test suite for YourClass"""
    
    def setup_method(self):
        """Setup before each test"""
        self.instance = YourClass()
    
    def test_basic_functionality(self):
        """Test basic feature"""
        result = self.instance.method()
        assert result is not None
    
    def test_edge_cases(self):
        """Test edge cases"""
        with pytest.raises(ValueError):
            self.instance.method(invalid_input)
```

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/test_parser.py

# With coverage
pytest --cov=src tests/

# Verbose
pytest -v

# Stop on first failure
pytest -x
```

### Test Coverage Goals

- **Core modules**: >80% coverage
- **Critical paths**: 100% coverage
- **Edge cases**: Comprehensive coverage

## 📝 Code Style Guide

### Python Style

Follow PEP 8 with these specifics:

```python
# Imports
from typing import List, Dict, Any, Optional
import standard_library
import third_party
from . import local_module

# Constants
MAX_CHUNK_SIZE = 1024
DEFAULT_LANGUAGE = 'en'

# Class names: PascalCase
class DocumentParser:
    pass

# Function names: snake_case
def parse_document(file_path: str) -> ParseResult:
    pass

# Variable names: snake_case
chunk_size = 512
is_arabic = False

# Type hints everywhere
def process(data: List[str], count: int = 10) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    return result
```

### Docstring Format

```python
def function_name(param1: str, param2: int = 0) -> bool:
    """
    Brief description of function
    
    Longer description if needed. Explain the purpose, behavior,
    and any important details.
    
    Args:
        param1: Description of param1
        param2: Description of param2 (default: 0)
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When validation fails
        IOError: When file access fails
        
    Example:
        >>> function_name("test", 5)
        True
    """
    pass
```

## 🚀 Deployment {#deployment}

### Local Development

```bash
# Run web app
streamlit run app.py

# Run CLI
python cli.py --help
```

### Docker Deployment

```dockerfile
# Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

Build and run:
```bash
docker build -t doc-parser .
docker run -p 8501:8501 doc-parser
```

### Streamlit Cloud

1. Push to GitHub
2. Connect repository to Streamlit Cloud
3. Configure settings
4. Deploy

### AWS/Azure Deployment

See separate deployment guides in `docs/deployment/`

## 📊 Performance Optimization

### Profiling

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# Your code here
parser.parse(file_path)

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)
```

### Optimization Tips

1. **Batch Processing**: Process chunks in batches
2. **Caching**: Cache embeddings and frequent queries
3. **Async Operations**: Use async for I/O operations
4. **Database Indexes**: Ensure proper indexing
5. **Memory Management**: Stream large files

## 🐛 Debugging

### Logging

```python
from loguru import logger

# Configure logging
logger.add("logs/app.log", rotation="500 MB")

# Use in code
logger.info("Processing document {}", document_id)
logger.error("Failed to parse: {}", error)
```

### Common Issues

**Issue**: Slow chunk processing
**Solution**: Increase batch size, use multiprocessing

**Issue**: Memory errors with large files
**Solution**: Stream file, process in chunks

**Issue**: ChromaDB persistence errors
**Solution**: Check permissions, reset database

## 📚 Resources

### Documentation
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [sentence-transformers](https://www.sbert.net/)

### Learning
- RAG systems: LangChain documentation
- Vector databases: Pinecone blog
- Arabic NLP: CAMeL Tools documentation

## 👥 Contributing {#contributing}

### Contribution Guidelines

1. Fork the repository
2. Create feature branch
3. Make changes
4. Add tests
5. Update documentation
6. Submit pull request

### PR Checklist

- [ ] Code follows style guide
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Type hints added
- [ ] No linting errors
- [ ] Performance tested

## 📞 Support

**Developer**: Anas Mohammad
**Email**: anas.mohammad6673332@gmail.com
**Phone**: 00962786673332

---

**Happy Coding! 🎉**
