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

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✅ Virtual environment created"
else
    echo "✅ Virtual environment already exists"
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📦 Installing dependencies (this may take ~30 seconds)..."
pip3 install -q --upgrade pip
pip3 install -r requirements.txt

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
