#!/bin/bash


if command -v brew >/dev/null 2>&1; then
    echo "Homebrew already installed."
else
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    if command -v brew >/dev/null 2>&1; then
        echo "Homebrew installed successfully."
    else
        echo "Homebrew installation failed."
        exit 1
    fi
fi


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


if command -v pip3 >/dev/null 2>&1; then
    echo "Pip already installed."
else
    echo "Installing pip..."
    brew install pip3
    if command -v pip3 >/dev/null 2>&1; then
        echo "Pip installed successfully."
    else
        echo "Pip installation failed."
        exit 1
    fi
fi

pip3 install -r requirements.txt

python3 main.py

exit 0
