# Define variables
VENV_NAME = .venv
PYTHON = $(VENV_NAME)/bin/python
PIP = $(VENV_NAME)/bin/pip

# Default target to create a virtual environment
all: install

# Create a virtual environment if not already created
$(VENV_NAME)/bin/activate: requirements.txt
	python3 -m venv $(VENV_NAME)
	$(PIP) install -r requirements.txt

# Install dependencies in the virtual environment
install: $(VENV_NAME)/bin/activate
	$(PIP) install -r requirements.txt

# Run tests (for example, using pytest)
# test: $(VENV_NAME)/bin/activate
# 	$(VENV_NAME)/bin/python -m pytest


# Clean up (remove the virtual environment)
clean:
	rm -rf $(VENV_NAME)

compile: $(VENV_NAME)/bin/activate
	$(VENV_NAME)/bin/python compile.py

.PHONY: compile
