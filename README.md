# GnuPG EasyGui

![Issues](https://img.shields.io/github/issues/EddyDevProject/GnuPG-EasyGUI.svg)
![Build](https://app.travis-ci.com/EddyDevProject/GnuPG-EasyGUI.svg?branch=master)

Simple GUI for GnuPG

# Requirements
- numpy==1.23.1
- python-gnupg==0.4.9
- gnupg==2.3.1
- webbrowser (built-in)

# Setup
Install requirements using pip
 ```
pip install -r requirements.txt
```
or using make install

To open the program run from terminal
```
python main.py
```
Also install gnupg and tkinter if you don't have them already
Linux
```
sudo apt-get install gnupg
```
```
sudo apt-get install python3-tk
```
Windows
```
choco install gnupg
```
```
choco install python3-tk
```
MacOS
```
brew install gnupg
```
```
brew install python3-tk
```
# Generate Keys
To generate your keys click on the "Generate keys" button. You can decide to export them or view them later in the appropriate section.
# Import Keys
To import your keys click on the "Import keys" button.
# Encrypt File
To encrypt a file click on the "Encrypt File" button. You will be prompted for a recipients that matches the key of the person who sent you the file. A new file with the .gpg extension will be generated.
# Decrypt File
To decrypt a file click on the "Decrypt File" button. You will not be asked for anything as you must have already imported the key. A new file with the original extension will be generated.


