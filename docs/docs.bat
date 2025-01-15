@echo off
rem Change the current working directory to the directory of the batch script
cd /d %~dp0
cd ..

uv run --dev pdoc --docformat google --math --mermaid ak_requests -o docs