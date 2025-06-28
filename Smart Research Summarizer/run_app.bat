@echo off
echo Starting Smart Research Assistant...
echo.
echo Installing dependencies if needed...
"C:/Users/karthick raja/AppData/Local/Programs/Python/Python38/python.exe" -m pip install streamlit PyPDF2
echo.
echo The app will open at: http://localhost:8501
echo.
cd /d "%~dp0"
"C:/Users/karthick raja/AppData/Local/Programs/Python/Python38/python.exe" -m streamlit run app.py --server.port 8501 --server.address localhost
pause