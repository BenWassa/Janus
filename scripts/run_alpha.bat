@echo off
cd /d "C:\Users\benjamin.haddon\Documents\Janus"
echo Starting Janus Alpha Build...
echo.
python dist/janus_v2-alpha/src/engine.py --telemetry outputs/user_session.json
echo.
echo Game finished. Press any key to close this window.
pause >nul
