#!/bin/bash

# AI-Powered Document Parser Setup Script
# Run this script to set up the project for the first time

echo ""
echo "🚀 AI-Powered Document Parser - Setup Script"
echo "============================================================"
echo ""

# Check Python version
echo "📌 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.9 or higher."
    exit 1
fi
echo "✅ Found: $(python3 --version)"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists. Skipping..."
else
    python3 -m venv venv
    echo "✅ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "🔧 Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
echo "This may take a few minutes..."
pip install -r requirements.txt
if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Create necessary directories
echo ""
echo "📁 Creating data directories..."
directories=("data/uploads" "data/chroma_db" "data/sample" "logs")

for dir in "${directories[@]}"; do
    if [ ! -d "$dir" ]; then
        mkdir -p "$dir"
        echo "  ✅ Created: $dir"
    else
        echo "  ⚠️  Already exists: $dir"
    fi
done

# Create .env file
echo ""
echo "📝 Checking environment configuration..."
if [ ! -f ".env" ]; then
    cp .env.example .env
    echo "✅ Created .env file from template"
else
    echo "⚠️  .env file already exists"
fi

# Display next steps
echo ""
echo ""
echo "🎉 Setup Complete!"
echo "============================================================"
echo ""
echo "📚 Quick Start Guide:"
echo ""
echo "  1. Run the web demo:"
echo "     streamlit run app.py"
echo ""
echo "  2. Use the CLI:"
echo "     python cli.py parse --file data/sample/sample_english.txt"
echo "     python cli.py search --query 'AI'"
echo ""
echo "  3. Run tests:"
echo "     pytest tests/"
echo ""
echo "  4. Run benchmarks:"
echo "     python benchmarks/run_benchmarks.py"
echo ""
echo "📖 Documentation:"
echo "   - README.md          : Main documentation"
echo "   - QUICKSTART.md      : Quick start guide"
echo "   - DEVELOPMENT.md     : Developer guide"
echo ""
echo "📞 Contact: Anas Mohammad"
echo "   Email: anas.mohammad6673332@gmail.com"
echo "   Phone: 00962786673332"
echo ""
echo "============================================================"
echo ""
