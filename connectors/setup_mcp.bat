@echo off
REM QA OS - configure all MCP connectors (Selenium, snd-schema, selenium-framework-db).
REM Double-click, or run from a command prompt. Extra options: -ClaudeCode  -SkipDb  -SkipSelenium
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0setup_mcp.ps1" %*
pause
