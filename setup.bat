@echo off
setlocal enabledelayedexpansion

echo Installing Python dependencies...
pip install -r requirements.txt
echo Python dependencies installed.

pause

:: Set the URL for the Gpg4win installer
set "url=https://files.gpg4win.org/gpg4win-4.1.0.exe"

:: Set the output path for the installer
set "output=C:\Temp\gpg4win.exe"

:: Check if the installer exists
if not exist "%output%" (
    echo Downloading Gpg4win installer...
    powershell -Command "Invoke-WebRequest -Uri '%url%' -OutFile '%output%'"
    echo Download completed.
) else (
    echo Gpg4win installer already exists.
)

:: Check if the installer exists after download attempt
if exist "%output%" (
    echo Installing Gpg4win...
    echo Please wait while the installation completes.
    
    start /wait "" "%output%" 
    echo Installation completed.
) else (
    echo Gpg4win installer not found or download failed.
)

:: Add GnuPG to the PATH environment variable
setx PATH "%PATH%;C:\Program Files (x86)\GnuPG\bin"

echo Please restart your system for changes to take effect.

endlocal
