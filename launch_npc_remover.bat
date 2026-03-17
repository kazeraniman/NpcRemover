@echo off
rem This turns off every command being written out instead of executed immediately.

rem Change to the folder of this file. This gets around running as Administrator putting us in System32. You shouldn't need to run as Administrator except to get around Smart App Control anyway.
cd /d "%~dp0"

rem Setting up the container to hold all of the python dependencies needed to run the script.
echo Setting up environment for the dependencies...
if not exist venv (
    py -m venv venv
    if errorlevel 1 (
        python -m venv venv
        if errorlevel 1 (
            echo:
            echo Error: Unable to create environment. Please check that you have Python3 installed and try again.
            pause
            exit \b 1
        )
    )

    echo Environment created.
) else (
    echo Environment already exists.
)

rem Enter the environment and install any dependencies as needed.
echo:
echo Installing dependencies...
venv\Scripts\pip install -r requirements.txt
if errorlevel 1 (
    echo:
    echo Error: Unable to install dependencies.
    pause
    exit \b 1
)
echo Dependencies installed.

echo:
echo Launching the app...
rem Change the working directory of the script so the different files can find each other.
set PYTHONPATH=%~dp0

rem Run the script to launch the app.
venv\Scripts\python.exe src\main.py
if errorlevel 1 (
    echo:
    echo Error: Unable to launch the app.
    pause
    exit \b 1
)

rem Pause to give time to read any error messages.
pause
