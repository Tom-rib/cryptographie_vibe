.PHONY: help install setup setup-serveur setup-client test run client clean lint format docs

# Check if we're in virtual environment
VENV_PYTHON := venv/bin/python3
VENV_PIP := venv/bin/pip3

help:
	@echo "╔════════════════════════════════════════════════════════════════╗"
	@echo "║           CRYPTO VIBENESS - Project Management                ║"
	@echo "╚════════════════════════════════════════════════════════════════╝"
	@echo ""
	@echo "QUICK START:"
	@echo "  make setup          Setup everything (creates venv, installs deps)"
	@echo "  make setup-serveur  Setup and start server (for testing)"
	@echo "  make setup-client   Setup and start client (for testing)"
	@echo "  make test           Run all tests"
	@echo ""
	@echo "AVAILABLE TARGETS:"
	@echo "  make install        Install dependencies (in venv)"
	@echo "  make run            Run the IRC server"
	@echo "  make test           Run all tests"
	@echo "  make test-jour1p1   Test JOUR1_PARTIE1 (Chat)"
	@echo "  make test-jour1p2   Test JOUR1_PARTIE2 (Auth MD5)"
	@echo "  make test-jour2p1   Test JOUR2_PARTIE1 (Bcrypt)"
	@echo "  make test-jour2p2   Test JOUR2_PARTIE2 (AES-256)"
	@echo "  make test-jour3p1   Test JOUR3_PARTIE1 (RSA Keys)"
	@echo "  make test-jour3p2   Test JOUR3_PARTIE2 (E2EE + Signatures)"
	@echo "  make clean          Clean cache and temp files"
	@echo "  make clean-all      Clean cache, temp files, and venv"
	@echo "  make lint           Run linter (pylint)"
	@echo "  make format         Format code (black)"
	@echo "  make deps-update    Update requirements.txt"
	@echo "  make docs           Display documentation"
	@echo ""

setup:
	@echo "🔧 Setting up project..."
	@echo "🔍 Checking system dependencies..."
	@if ! python3 -m venv --help > /dev/null 2>&1; then \
		echo "⚠️  python3-venv not found. Installing..."; \
		if command -v apt-get > /dev/null; then \
			sudo apt-get update && sudo apt-get install -y python3-venv; \
		else \
			echo "❌ Could not install python3-venv automatically."; \
			echo "   Please install manually: sudo apt install python3-venv"; \
			exit 1; \
		fi \
	fi
	@if [ ! -d "venv" ]; then \
		echo "📦 Creating virtual environment..."; \
		python3 -m venv venv; \
		echo "✅ Virtual environment created"; \
	fi
	@echo "📦 Installing dependencies..."
	@. venv/bin/activate && pip3 install --upgrade pip && pip3 install -r requirements.txt
	@echo "✅ Setup complete! Ready to use."
	@echo ""
	@echo "Next steps:"
	@echo "  source venv/bin/activate"
	@echo "  make test"

setup-serveur: setup
	@echo ""
	@echo "🚀 Starting IRC server..."
	@. venv/bin/activate && python3 src/server.py

setup-client: setup
	@echo ""
	@echo "💻 Starting IRC client..."
	@. venv/bin/activate && python3 src/client.py

install:
	@echo "📦 Installing dependencies..."
	@if [ -f "venv/bin/activate" ]; then \
		. venv/bin/activate && pip3 install -r requirements.txt; \
	else \
		echo "❌ Virtual environment not found. Run: make setup"; \
		exit 1; \
	fi
	@echo "✅ Dependencies installed"

test:
	@echo "🧪 Running all validation tests..."
	@. venv/bin/activate && python3 tests/validate_jour1_partie1.py
	@. venv/bin/activate && python3 tests/validate_jour1_partie2.py
	@. venv/bin/activate && python3 tests/validate_jour2_partie1.py
	@. venv/bin/activate && python3 tests/validate_jour2_partie2.py
	@. venv/bin/activate && python3 tests/validate_jour3_partie1.py
	@. venv/bin/activate && python3 tests/validate_jour3_partie2.py
	@echo "✅ All tests completed"

test-jour1p1:
	@echo "🧪 Testing JOUR1_PARTIE1 (Chat)..."
	@. venv/bin/activate && python3 tests/validate_jour1_partie1.py

test-jour1p2:
	@echo "🧪 Testing JOUR1_PARTIE2 (Auth MD5)..."
	@. venv/bin/activate && python3 tests/validate_jour1_partie2.py

test-jour2p1:
	@echo "🧪 Testing JOUR2_PARTIE1 (Bcrypt)..."
	@. venv/bin/activate && python3 tests/validate_jour2_partie1.py

test-jour2p2:
	@echo "🧪 Testing JOUR2_PARTIE2 (AES-256)..."
	@. venv/bin/activate && python3 tests/validate_jour2_partie2.py

test-jour3p1:
	@echo "🧪 Testing JOUR3_PARTIE1 (RSA Keys)..."
	@. venv/bin/activate && python3 tests/validate_jour3_partie1.py

test-jour3p2:
	@echo "🧪 Testing JOUR3_PARTIE2 (E2EE + Signatures)..."
	@. venv/bin/activate && python3 tests/validate_jour3_partie2.py

run:
	@echo "🚀 Starting IRC server..."
	python3 src/server.py

client:
	@echo "💻 Starting IRC client..."
	python3 src/client.py

clean:
	@echo "🧹 Cleaning cache and temp files..."
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .coverage
	rm -rf htmlcov/
	rm -f *.log
	@echo "✅ Cleaned"

clean-all: clean
	@echo "🧹 Cleaning everything including venv..."
	rm -rf venv/
	@echo "✅ Full clean completed"

lint:
	@echo "🔍 Linting Python code..."
	python3 -m pylint src/ tests/ --disable=missing-docstring,too-few-public-methods,line-too-long || true
	@echo "✅ Linting complete"

format:
	@echo "✨ Formatting code with black..."
	python3 -m black src/ tests/ --quiet
	@echo "✅ Formatting complete"

deps-update:
	@echo "📝 Updating requirements.txt..."
	pip3 freeze > requirements.txt
	@echo "✅ requirements.txt updated"

docs:
	@echo "📚 Available Documentation:"
	@echo ""
	@echo "Quick Start:"
	@echo "  cat COMMENCER_ICI.md"
	@echo ""
	@echo "Full Project Overview:"
	@echo "  cat README.md"
	@echo ""
	@echo "Project Status:"
	@echo "  cat PROJECT_STATE.md"
	@echo ""
	@echo "All Stages:"
	@echo "  JOUR1_PARTIE1: cat JOUR1_PARTIE1.md"
	@echo "  JOUR1_PARTIE2: cat JOUR1_PARTIE2.md"
	@echo "  JOUR2_PARTIE1: cat JOUR2_PARTIE1.md"
	@echo "  JOUR2_PARTIE2: cat JOUR2_PARTIE2.md"
	@echo "  JOUR3_PARTIE1: cat JOUR3_PARTIE1.md"
	@echo "  JOUR3_PARTIE2: cat JOUR3_PARTIE2.md"
	@echo ""

.DEFAULT_GOAL := help
