#!/bin/bash

# Crypto Vibeness Setup Script
# One command to set everything up!

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║        CRYPTO VIBENESS - Automatic Setup Script               ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
echo "🐍 Checking Python version..."
python3 --version || (echo "❌ Python3 not found. Please install Python 3.9 or higher." && exit 1)

# Check if python3-venv is installed
echo "🔍 Checking and installing system dependencies..."
if ! python3 -m venv --help > /dev/null 2>&1; then
    echo "⚠️  python3-venv not found. Installing..."
    if command -v apt-get > /dev/null; then
        echo "📦 Running: sudo apt-get update..."
        sudo apt-get update || true
        
        echo "📦 Running: sudo apt-get install -y python3-venv..."
        if ! sudo apt-get install -y python3-venv; then
            echo "⚠️  First attempt failed. Trying with --fix-missing..."
            if ! sudo apt-get install --fix-missing -y python3-venv; then
                echo "❌ Failed to install python3-venv"
                echo "Try manually: sudo apt-get update && sudo apt-get install -y python3-venv"
                exit 1
            fi
        fi
        echo "✅ python3-venv installed"
    else
        echo "❌ apt-get not found. Please install python3-venv manually."
        exit 1
    fi
else
    echo "✅ python3-venv is available"
fi

# Remove corrupted venv if it exists
if [ -d "venv" ]; then
    echo "🔍 Checking existing virtual environment..."
    if ! venv/bin/python3 -c "import sys; sys.exit(0)" > /dev/null 2>&1; then
        echo "⚠️  Virtual environment is corrupted. Removing..."
        deactivate 2>/dev/null || true
        rm -rf venv
    else
        echo "✅ Existing venv is OK"
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv || (echo "❌ Failed to create venv" && exit 1)
    
    if [ ! -f "venv/bin/python3" ]; then
        echo "❌ venv/bin/python3 not found after creation"
        exit 1
    fi
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Verify and install pip if needed
echo "🔍 Checking pip in virtual environment..."
if ! python3 -m pip --version > /dev/null 2>&1; then
    echo "⚠️  pip is missing. Installing with ensurepip..."
    python3 -m ensurepip --upgrade || (echo "❌ Failed to install pip with ensurepip"; exit 1)
fi

# Install/upgrade pip, setuptools, wheel
echo "📦 Upgrading pip, setuptools, and wheel..."
python3 -m pip install --upgrade pip setuptools wheel || (echo "❌ Failed to upgrade pip tools"; exit 1)

# Install dependencies
echo "📦 Installing dependencies (this may take ~30 seconds)..."
python3 -m pip install -r requirements.txt || (echo "❌ Failed to install dependencies"; exit 1)

# Verify installation
echo "✅ Installation complete!"
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    SETUP SUCCESSFUL ✅                        ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo ""
echo "1. Activate virtual environment (each terminal session):"
echo "   source venv/bin/activate"
echo ""
echo "2. Run tests to verify everything:"
echo "   make test"
echo ""
echo "3. Start manual testing:"
echo "   Terminal 1: make run"
echo "   Terminal 2: python3 src/client.py"
echo "   Terminal 3: python3 src/client.py"
echo ""
echo "4. Follow the manual testing guide:"
echo "   cat MANUAL_TESTING.md"
echo ""
echo "📚 Documentation:"
echo "   make help        Show all available commands"
echo "   make docs        Show documentation files"
echo ""
