@echo off
cd /d "C:\Users\benjamin.haddon\Documents\Janus"
echo Starting Janus Alpha Build (Developer Mode)...
echo.
python dist/janus_v2-alpha/src/engine.py --telemetry log.json --debug
echo.
echo Game finished. Press any key to close this window.
pause >nul
