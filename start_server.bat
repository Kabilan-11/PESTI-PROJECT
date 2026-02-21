@echo off
echo ========================================
echo AgriChem Solutions - Backend Server
echo ========================================
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting Flask server...
echo Server will be available at: http://localhost:5000
echo Admin Dashboard: admin.html
echo.
python app.py
pause
