# Makefile for AppsList

ifeq ($(OS),Windows_NT)
    VENV_BIN = .venv/Scripts
    CLEAN_CMD = if exist __pycache__ (rmdir /s /q __pycache__) & if exist functions\__pycache__ (rmdir /s /q functions\__pycache__) & if exist tests\__pycache__ (rmdir /s /q tests\__pycache__)
else
    VENV_BIN = .venv/bin
    CLEAN_CMD = rm -rf __pycache__ functions/__pycache__ tests/__pycache__
endif

.PHONY: setup run clean

setup:
	python -m venv .venv
	$(VENV_BIN)/pip install -r requirements.txt

run:
	$(VENV_BIN)/python main.py

clean:
	$(CLEAN_CMD)
