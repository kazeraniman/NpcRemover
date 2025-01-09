@echo off
rem This turns off every command being written out instead of executed immediately.

rem Setting up the container to hold all of the python dependencies needed to run the script.
echo "Setting up environment for the dependencies..."
if not exist venv (
    py -m venv venv
    if not %errorlevel% == 0 (
        python -m venv venv
        if %errorlevel% == 0 (
            echo "Error: Unable to create environment."
            pause
            exit \b 1
        )
    )

    echo "Environment created.".
) else (
    echo "Environment already exists".
)

rem Enter the environment and install any dependencies as needed.
echo "Installing dependencies..."
venv\Scripts\pip install -r requirements.txt
echo "Dependencies installed."

echo "Launching the app..."
rem Run the script to launch the app.
venv\Scripts\python.exe src\main.py
