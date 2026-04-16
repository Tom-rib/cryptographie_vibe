.PHONY: help install setup setup-serveur setup-client test run client clean clean-venv clean-all lint format docs

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
	@echo "  make clean-venv     Remove virtual environment (to reset)"
	@echo "  make clean-all      Clean cache, temp files, and venv"
	@echo "  make lint           Run linter (pylint)"
	@echo "  make format         Format code (black)"
	@echo "  make deps-update    Update requirements.txt"
	@echo "  make docs           Display documentation"
	@echo ""

setup:
	@echo "🔧 Setting up project..."
	@echo "🔍 Checking and installing system dependencies..."
	@if ! python3 -m venv --help > /dev/null 2>&1; then \
		echo "⚠️  python3-venv not found. Installing..."; \
		if command -v apt-get > /dev/null; then \
			echo "📦 Running: sudo apt-get update..."; \
			sudo apt-get update || true; \
			echo "📦 Running: sudo apt-get install -y python3-venv..."; \
			sudo apt-get install -y python3-venv || (echo "❌ apt-get install failed. Trying apt-get install --fix-missing..."; sudo apt-get install --fix-missing -y python3-venv) || (echo "❌ Could not install python3-venv"; echo "   Try manually: sudo apt-get update && sudo apt-get install -y python3-venv"; exit 1); \
		else \
			echo "❌ apt-get not found. Please install python3-venv manually."; \
			exit 1; \
		fi; \
		echo "✅ python3-venv installed"; \
	else \
		echo "✅ python3-venv is available"; \
	fi
	@if [ -d "venv" ]; then \
		if [ ! -f "venv/bin/activate" ]; then \
			echo "⚠️  Virtual environment is incomplete. Removing..."; \
			rm -rf venv; \
		else \
			if ! venv/bin/python3 -c "import sys; sys.exit(0)" > /dev/null 2>&1; then \
				echo "⚠️  Virtual environment is corrupted. Removing..."; \
				rm -rf venv; \
			else \
				echo "✅ Existing venv is OK"; \
			fi \
		fi \
	fi
	@if [ ! -d "venv" ]; then \
		echo "📦 Creating virtual environment..."; \
		python3 -m venv venv || (echo "❌ Failed to create venv"; exit 1); \
		if [ ! -f "venv/bin/python3" ]; then \
			echo "❌ venv/bin/python3 not found after creation"; \
			exit 1; \
		fi; \
		if [ ! -f "venv/bin/activate" ]; then \
			echo "❌ venv/bin/activate not found after creation"; \
			exit 1; \
		fi; \
		echo "✅ Virtual environment created"; \
	fi
	@echo "📦 Installing dependencies..."
	@if ! venv/bin/python3 -m pip --version > /dev/null 2>&1; then \
		echo "⚠️  pip is missing. Installing with ensurepip..."; \
		venv/bin/python3 -m ensurepip --upgrade || (echo "❌ Failed to install pip"; exit 1); \
	fi
	@venv/bin/python3 -m pip install --upgrade pip setuptools wheel && venv/bin/python3 -m pip install -r requirements.txt
	@echo "✅ Setup complete! Ready to use."
	@echo ""
	@echo "Next steps:"
	@echo "  source venv/bin/activate"
	@echo "  make test"

setup-serveur: setup
	@echo ""
	@echo "🚀 Starting IRC server..."
	@venv/bin/python3 src/server.py

setup-client: setup
	@echo ""
	@echo "💻 Starting IRC client..."
	@venv/bin/python3 src/client.py

install:
	@echo "📦 Installing dependencies..."
	@if [ -f "venv/bin/python3" ]; then \
		venv/bin/python3 -m pip install -r requirements.txt; \
	else \
		echo "❌ Virtual environment not found. Run: make setup"; \
		exit 1; \
	fi
	@echo "✅ Dependencies installed"

test:
	@echo "🧪 Running all validation tests..."
	@venv/bin/python3 tests/validate_jour1_partie1.py
	@venv/bin/python3 tests/validate_jour1_partie2.py
	@venv/bin/python3 tests/validate_jour2_partie1.py
	@venv/bin/python3 tests/validate_jour2_partie2.py
	@venv/bin/python3 tests/validate_jour3_partie1.py
	@venv/bin/python3 tests/validate_jour3_partie2.py
	@echo "✅ All tests completed"

test-jour1p1:
	@echo "🧪 Testing JOUR1_PARTIE1 (Chat)..."
	@venv/bin/python3 tests/validate_jour1_partie1.py

test-jour1p2:
	@echo "🧪 Testing JOUR1_PARTIE2 (Auth MD5)..."
	@venv/bin/python3 tests/validate_jour1_partie2.py

test-jour2p1:
	@echo "🧪 Testing JOUR2_PARTIE1 (Bcrypt)..."
	@venv/bin/python3 tests/validate_jour2_partie1.py

test-jour2p2:
	@echo "🧪 Testing JOUR2_PARTIE2 (AES-256)..."
	@venv/bin/python3 tests/validate_jour2_partie2.py

test-jour3p1:
	@echo "🧪 Testing JOUR3_PARTIE1 (RSA Keys)..."
	@venv/bin/python3 tests/validate_jour3_partie1.py

test-jour3p2:
	@echo "🧪 Testing JOUR3_PARTIE2 (E2EE + Signatures)..."
	@venv/bin/python3 tests/validate_jour3_partie2.py

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

clean-venv:
	@echo "🧹 Removing virtual environment..."
	rm -rf venv/
	@echo "✅ Virtual environment removed"
	@echo "Run 'make setup' to create a fresh environment"

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
