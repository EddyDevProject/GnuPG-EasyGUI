# GnuPG - EasyGUI

![Issues](https://img.shields.io/github/issues/EddyDevProject/GnuPG-EasyGUI.svg)
![Build](https://app.travis-ci.com/EddyDevProject/GnuPG-EasyGUI.svg?branch=master)

A user-friendly graphical interface for managing GnuPG (GPG) operations, including file encryption/decryption and key management. This application has been modernized with a `CustomTkinter` UI for a better user experience.

## Key Features

*   **Modern User Interface:** Built with `CustomTkinter` for a contemporary look and feel.
*   **File Encryption & Decryption:** Securely encrypt files for specific recipients and decrypt files using your GPG keys and passphrase.
*   **Efficient Large File Handling:** Optimized for memory efficiency when encrypting and decrypting large files.
*   **GPG Key Pair Generation:** Easily generate new GPG key pairs (public and private).
*   **Key Import:** Import GPG public keys from files.
*   **Key Listing:** View details of all GPG keys in your keyring (Recipient, Key ID, Fingerprint).
*   **Update Checker:** Built-in functionality to check for new application versions from the GitHub repository.

## Requirements

1.  **Python 3.x:** Ensure you have Python 3 installed.
2.  **GnuPG (GPG):** GnuPG must be installed on your system and accessible via the `gpg` command in your system's PATH.

    *   **Linux:**
        ```bash
        sudo apt-get update
        sudo apt-get install gnupg
        ```
    *   **macOS:**
        ```bash
        brew install gnupg
        ```
    *   **Windows:**
        *   Download and install Gpg4win from [gpg4win.org](https://www.gpg4win.org/). This package includes GnuPG, Kleopatra (a certificate manager), and GpgOL (an Outlook plugin). Ensure `gpg.exe` is in your system PATH.
        *   Alternatively, via Chocolatey (ensure Chocolatey is installed):
            ```powershell
            choco install gpg4win
            ```
            Or for just the GnuPG command line tools:
            ```powershell
            choco install gnupg
            ```

3.  **Python Libraries:** These will be installed via `requirements.txt`.
    *   `customtkinter`
    *   `numpy`
    *   `python-gnupg`
    *   `tk` (usually comes with Python, but listed for clarity)
    *   `requests`

## How to Run

1.  **Clone the Repository (Optional):**
    If you haven't downloaded the project files yet:
    ```bash
    git clone https://github.com/EddyDevProject/GnuPG-EasyGUI.git
    cd GnuPG-EasyGUI
    ```

2.  **Install Dependencies:**
    Navigate to the project directory in your terminal and run:
    ```bash
    pip install -r requirements.txt
    ```
    *Note: On some systems, you might need to use `pip3` instead of `pip`.*

3.  **Run the Application:**
    ```bash
    python main.py
    ```
    *Note: On some systems, you might need to use `python3` instead of `python`.*

## Usage Overview

*   **Generate Keys:** Click "Generate Keys," fill in your details (Name, Email, Passphrase), and save the exported public key (`.asc` file) to a location of your choice.
*   **See Keys:** View a list of all GPG keys currently in your keyring.
*   **Import Keys:** Import GPG keys from `.asc` files or other key file formats.
*   **Encrypt File:** Select a file to encrypt and choose a recipient from your list of public keys. The encrypted file will be saved with a `.gpg` extension.
*   **Decrypt File:** Select a `.gpg` file to decrypt. You will be prompted for the passphrase associated with your private key. The decrypted file will be saved with `_decrypted` appended to its original name (before the extension).
*   **Update:** Check if a newer version of the application is available.

## License

This project is licensed under the MIT License.

## Author & Contributors

*   **Author:** EddyDev ([EddyDevProject on GitHub](https://github.com/EddyDevProject))
*   **Contributors:**
    *   Federica Capobianco ([federicaCapobianco on GitHub](https://github.com/federicaCapobianco))
    *   (And other contributors via pull requests and suggestions)
