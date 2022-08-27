# GnuPG EasyGui

[![API](https://img.shields.io/badge/Telegram%20Bot%20API-November%2020%2C%202020-36ade1.svg)](https://core.telegram.org/bots/api)
![PHP](https://img.shields.io/badge/php-%3E%3D5.6-8892bf.svg)
![Build](https://travis-ci.com/EddyDevProject/Amazon-Ref-Links-Generator-Bot.svg?branch=main)

Simple GUI for GnuPG

# Requirements
- easygui==0.98.3
- numpy==1.23.1
- python-gnupg==0.4.9

# Setup
Install requirements using pip
 ```
pip install -r requirements.txt
```
To open the program run from terminal
```
python main.py
```
# Generate Keys
To generate your keys click on the "Generate keys" button. You can decide to export them or view them later in the appropriate section.
# Import Keys
To import your keys click on the "Import keys" button.
# Encrypt File
To encrypt a file click on the "Encrypt File" button. You will be prompted for a recipients that matches the key of the person who sent you the file. A new file with the .gpg extension will be generated.
# Decrypt File
To decrypt a file click on the "Decrypt File" button. You will not be asked for anything as you must have already imported the key. A new file with the original extension will be generated.


