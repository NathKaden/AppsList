# Makefile for AppsList

ifeq ($(OS),Windows_NT)
    VENV_BIN = .venv/Scripts
    CLEAN_CMD = if exist __pycache__ (rmdir /s /q __pycache__) & if exist functions\__pycache__ (rmdir /s /q functions\__pycache__) & if exist tests\__pycache__ (rmdir /s /q tests\__pycache__)
    RELEASE_CMD = powershell -Command "if (Test-Path release) { Remove-Item -Recurse -Force release }; New-Item -ItemType Directory -Path release | Out-Null; Copy-Item dist/AppsList.exe release/ | Out-Null; Copy-Item -Recurse assets release/ | Out-Null; Copy-Item -Recurse bdd release/ | Out-Null; if (Test-Path AppsList-Release.zip) { Remove-Item AppsList-Release.zip }; Compress-Archive -Path release/* -DestinationPath AppsList-Release.zip; Remove-Item -Recurse -Force release; Write-Host 'Release package AppsList-Release.zip created successfully!'"
else
    VENV_BIN = .venv/bin
    CLEAN_CMD = rm -rf __pycache__ functions/__pycache__ tests/__pycache__
    RELEASE_CMD = rm -rf release && mkdir release && cp dist/AppsList release/ && cp -r assets release/ && cp -r bdd release/ && rm -f AppsList-Release.zip && zip -r AppsList-Release.zip release/* && rm -rf release && echo 'Release package AppsList-Release.zip created successfully!'
endif

.PHONY: setup run clean test release

setup:
	python -m venv .venv
	$(VENV_BIN)/pip install -r requirements.txt

run:
	$(VENV_BIN)/python main.py

test:
	$(VENV_BIN)/python -m unittest discover -s tests

clean:
	$(CLEAN_CMD)

release:
	$(VENV_BIN)/pyinstaller --onefile --noconsole --icon=assets/medias/icon.jpg --name=AppsList main.py
	$(RELEASE_CMD)
