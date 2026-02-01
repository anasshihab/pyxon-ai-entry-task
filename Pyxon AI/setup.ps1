# AI-Powered Document Parser Setup Script
# Run this script to set up the project for the first time

param(
    [switch]$SkipVenv = $false,
    [switch]$SkipInstall = $false
)

Write-Host "`n🚀 AI-Powered Document Parser - Setup Script" -ForegroundColor Cyan
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "📌 Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Python not found. Please install Python 3.9 or higher." -ForegroundColor Red
    exit 1
}
Write-Host "✅ Found: $pythonVersion" -ForegroundColor Green

# Create virtual environment
if (-not $SkipVenv) {
    Write-Host "`n📦 Creating virtual environment..." -ForegroundColor Yellow
    if (Test-Path "venv") {
        Write-Host "⚠️  Virtual environment already exists. Skipping..." -ForegroundColor Yellow
    } else {
        python -m venv venv
        Write-Host "✅ Virtual environment created" -ForegroundColor Green
    }
    
    # Activate virtual environment
    Write-Host "`n🔧 Activating virtual environment..." -ForegroundColor Yellow
    & "venv\Scripts\Activate.ps1"
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
}

# Install dependencies
if (-not $SkipInstall) {
    Write-Host "`n📥 Installing dependencies..." -ForegroundColor Yellow
    Write-Host "This may take a few minutes..." -ForegroundColor Gray
    pip install -r requirements.txt
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ Dependencies installed successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Failed to install dependencies" -ForegroundColor Red
        exit 1
    }
}

# Create necessary directories
Write-Host "`n📁 Creating data directories..." -ForegroundColor Yellow
$directories = @(
    "data\uploads",
    "data\chroma_db", 
    "data\sample",
    "logs"
)

foreach ($dir in $directories) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "  ✅ Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "  ⚠️  Already exists: $dir" -ForegroundColor Yellow
    }
}

# Create .env file
Write-Host "`n📝 Checking environment configuration..." -ForegroundColor Yellow
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "✅ Created .env file from template" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file already exists" -ForegroundColor Yellow
}

# Display next steps
Write-Host "`n`n🎉 Setup Complete!" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
Write-Host "📚 Quick Start Guide:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  1. Run the web demo:" -ForegroundColor White
Write-Host "     streamlit run app.py" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Use the CLI:" -ForegroundColor White
Write-Host "     python cli.py parse --file data\sample\sample_english.txt" -ForegroundColor Gray
Write-Host "     python cli.py search --query 'AI'" -ForegroundColor Gray
Write-Host ""
Write-Host "  3. Run tests:" -ForegroundColor White
Write-Host "     pytest tests/" -ForegroundColor Gray
Write-Host ""
Write-Host "  4. Run benchmarks:" -ForegroundColor White
Write-Host "     python benchmarks\run_benchmarks.py" -ForegroundColor Gray
Write-Host ""
Write-Host "📖 Documentation:" -ForegroundColor Cyan
Write-Host "   - README.md          : Main documentation" -ForegroundColor Gray
Write-Host "   - QUICKSTART.md      : Quick start guide" -ForegroundColor Gray
Write-Host "   - DEVELOPMENT.md     : Developer guide" -ForegroundColor Gray
Write-Host ""
Write-Host "📞 Contact: Anas Mohammad" -ForegroundColor Cyan
Write-Host "   Email: anas.mohammad6673332@gmail.com" -ForegroundColor Gray
Write-Host "   Phone: 00962786673332" -ForegroundColor Gray
Write-Host ""
Write-Host "=" * 60 -ForegroundColor Cyan
Write-Host ""
