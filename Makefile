# Makefile for SuperSales Analysis Streamlit Application

.PHONY: run install clean help

# Default port for Streamlit
PORT = 8503

# Default target
.DEFAULT_GOAL := help

# Run the Streamlit application
run:
	streamlit run main.py --server.port=$(PORT)

# Install dependencies
install:
	pip install -r requirements.txt

# Clean up cache files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".streamlit" -exec rm -rf {} +
	find . -type d -name ".ipynb_checkpoints" -exec rm -rf {} +

# Display help information
help:
	@echo "SuperSales Analysis Makefile Commands:"
	@echo "  make run         - Run the Streamlit application (default port: 8503)"
	@echo "  make run PORT=8000 - Run the Streamlit application on a specific port"
	@echo "  make install     - Install required dependencies"
	@echo "  make clean       - Clean up cache files"
	@echo "  make help        - Display this help message"