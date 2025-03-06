#!/bin/bash

# Check if Homebrew is already installed
if command -v brew >/dev/null 2>&1; then
    echo "Homebrew already installed."
else
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    if command -v brew >/dev/null 2>&1; then
        echo "Homebrew installed successfully."
    else
        echo "Homebrew installation failed."
        exit 1
    fi
fi

# Install gnupg
if command -v gpg >/dev/null 2>&1; then
    echo "GnuPG already installed."
else
    echo "Installing GnuPG..."
    brew install gnupg
    if command -v gpg >/dev/null 2>&1; then
        echo "GnuPG installed successfully."
    else
        echo "GnuPG installation failed."
        exit 1
    fi
fi

# Check if Python 3 is already installed
if command -v python3 >/dev/null 2>&1; then
    echo "Python already installed."
else
    echo "Installing Python..."
    brew install python3
    if command -v python3 >/dev/null 2>&1; then
        echo "Python installed successfully."
    else
        echo "Python installation failed."
        exit 1
    fi
fi

# Install python3-tk
if command -v python3-tk >/dev/null 2>&1; then
    echo "Python3-tk already installed."
else
    echo "Installing Python3-tk..."
    brew install python3-tk
    if command -v python3-tk >/dev/null 2>&1; then
        echo "Python3-tk installed successfully."
    else
        echo "Python3-tk installation failed."
        exit 1
    fi
fi


# Check if pip is already installed
if command -v pip3 >/dev/null 2>&1; then
    echo "Pip already installed."
else
    echo "Installing pip..."
    # trying to install pip as a module instead of a package
    python3 -m ensurepip --default-pip
    if command -v pip3 >/dev/null 2>&1; then
        echo "Pip installed successfully."
    else
        echo "Pip installation failed."
        exit 1
    fi
fi

# Install requirements
echo "Installing requirements from requirements.txt..."
pip3 install -r requirements.txt

# Run the main script
echo "Running main.py..."
python3 main.py

exit 0
