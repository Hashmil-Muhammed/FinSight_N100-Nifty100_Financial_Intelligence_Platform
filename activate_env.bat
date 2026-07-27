@echo off
echo ===================================================
echo Ingesting Nifty 100 Financial Intelligence Platform
echo Activating Virtual Environment...
echo ===================================================

:: Switch to G Drive and navigate to Workspace
G:
cd "G:\My Drive\WorkSpace\Bluestock_Fintech_Data_Analyst_Intern\Intership at BlueStock\Nifty100_Capstone_Project"

:: Activate the virtual environment
call .venv\Scripts\activate.bat

echo.
echo Status: Environment Activated Successfully!
echo Ready for Sprint 1 Development.
echo ===================================================

:: Keep the CMD window open and active
cmd /k