@echo off
cd /d "C:\Users\benjamin.haddon\Documents\Janus"
echo Starting Janus Alpha Build (Developer Mode)...
echo.
python dist/src/engine.py --telemetry outputs/debug_session.json --debug
echo.
echo Game finished. Press any key to close this window.
pause >nul
