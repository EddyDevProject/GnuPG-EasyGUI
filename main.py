import os
import sys
import tkinter as tk
import customtkinter
from tkinter import filedialog, messagebox, simpledialog
import gnupg as pg
import numpy as np
import webbrowser
import requests

version = "0.2.7"

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

def get_system_os():
    if sys.platform.startswith('win'):
        return "win"
    elif sys.platform.startswith('linux'):
        return "linux"
    elif sys.platform.startswith('darwin'):
        return "mac"
    else:
        return None
    
if(get_system_os() == "win"):
     gpg = pg.GPG(gpgbinary=r"C:\\Program Files (x86)\\GnuPG\bin\\gpg.exe")
else:
    gpg = pg.GPG()



def show_alert(title, message):
    messagebox.showinfo(title, message)

def callback(url):
   webbrowser.open_new_tab(url)

def menu():
    """
    It displays a menu with buttons and when you click on one of them, it calls the corresponding
    function.
    """
    window = customtkinter.CTk()
    window.geometry("350x450") # Increased height for better spacing
    window.resizable(False, False)
    window.title("GnuPG - Menu")

    # Main frame for better organization
    main_frame = customtkinter.CTkFrame(window)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    text = "Version: " + version
    text += "\nAuthor: EddyDev"
    text += "\nLicense: MIT"
    text += "\nContributors: "
    label = customtkinter.CTkLabel(main_frame, text=text)
    label.pack(pady=(0, 5))

    contr = customtkinter.CTkLabel(main_frame, text="- Fegderica Capobianco", text_color="orange", cursor="hand2")
    contr.bind("<Button-1>", lambda e: callback("https://github.com/federicaCapobianco"))
    contr.pack(pady=2)

    link1 = customtkinter.CTkLabel(main_frame, text="Github Project", text_color="red", cursor="hand2")
    link1.bind("<Button-1>", lambda e: callback("https://github.com/EddyDevProject/GnuPG-EasyGUI"))
    link1.pack(pady=(2, 15)) # Added padding below

    choices = ["Encrypt", "Decrypt", "Generate Keys", "Import Keys", "See Keys", "Update", "Quit"]

    def handle_choice(choice):
        if choice == "Encrypt":
            encrypt()
        elif choice == "Decrypt":
            decrypt()
        elif choice == "Generate Keys":
            window.destroy()
            generate_keys()
        elif choice == "Import Keys":
            import_keys()
        elif choice == "See Keys":
            window.destroy()
            see_keys()
        elif choice == "Update":
            window.destroy()
            see_repo_update()
        elif choice == "Quit":
            window.destroy()
            sys.exit()

    for choice in choices:
        button = customtkinter.CTkButton(main_frame, text=choice, command=lambda choice=choice: handle_choice(choice))
        button.pack(pady=5, fill="x") # Added padding and fill x

    window.mainloop()

def encrypt():
    """
    It opens a file, then asks the user to choose a recipient from a list of public keys, then encrypts
    the file with the chosen public key.
    """
    try:
        file = filedialog.askopenfilename(title="Select file to encrypt")
        if not file:
            show_alert("Encrypt", "File not selected")
            return

        keys = gpg.list_keys()
        names = [key['uids'][0].split()[0] for key in keys]

        recipient = simpledialog.askstring("Encrypt", "Select recipient")
        if not recipient:
            show_alert("Encrypt", "Recipient not selected")
            return

        print("Recipient: " + recipient)
        print("Names: " + str(names))
        recipient_keys = [key for key in keys if key['uids'][0].split()[0] == recipient]
        if len(recipient_keys) == 0:
            show_alert("Encrypt", "Recipient not found")
            return

        fingerprint = recipient_keys[0]['fingerprint']
        print("Fingerprint: " + fingerprint)

       
        output_path = os.path.dirname(file) 
        output_file_filename = os.path.basename(file) + ".gpg"
        encrypted_file = os.path.join(output_path, output_file_filename)

        
        with open(file, 'rb') as f:
            # Initial attempt to encrypt, always_trust=False is default and recommended
            # to ensure GPG uses its configured trust model.
            stream_status = gpg.encrypt_file(f, recipients=[fingerprint], output=encrypted_file)

            encryption_successful = False
            if stream_status.ok:
                encryption_successful = True
            # Check for specific trust-related errors. GPG error messages can be localized.
            # Common English phrases: "not certified", "not trusted", "unusable public key"
            # It's hard to cover all languages. A more robust way would be to parse GPG status codes if available,
            # but python-gnupg's status object doesn't directly expose fine-grained trust error codes easily.
            # For now, we check common phrases in stderr.
            elif "not trusted" in str(stream_status.stderr).lower() or \
                 "unusable public key" in str(stream_status.stderr).lower() or \
                 "not certified" in str(stream_status.stderr).lower():
                
                # If encryption failed due to trust, remove potentially incomplete encrypted file
                if os.path.exists(encrypted_file):
                    try:
                        os.remove(encrypted_file)
                    except OSError as e:
                        print(f"Error removing partially encrypted file: {e}") # Log or handle as needed

                response = messagebox.askquestion("Encrypt - Key Not Trusted", 
                                                  f"The key for '{recipient}' ({fingerprint}) is not trusted, or its certification is not established.\n\n"
                                                  "GPG Error: " + str(stream_status.stderr).splitlines()[0] + "\n\n"
                                                  "Do you want to permanently trust this key (TRUST_ULTIMATE) and attempt encryption again?")
                if response == "yes":
                    trust_result = gpg.trust_keys(fingerprint, "TRUST_ULTIMATE")
                    # print(f"Trust result: {trust_result.status} {trust_result.stderr}") # For debugging
                    
                    f.seek(0)  # IMPORTANT: Reset file stream to the beginning
                    retry_status = gpg.encrypt_file(f, recipients=[fingerprint], output=encrypted_file)
                    if retry_status.ok:
                        encryption_successful = True
                    else:
                        show_alert("Encrypt", "Encryption failed after trusting key: " + str(retry_status.stderr))
                        # Attempt to remove partially encrypted file if retry failed
                        if os.path.exists(encrypted_file):
                            try: os.remove(encrypted_file)
                            except OSError: pass
                else:
                    show_alert("Encrypt", "Encryption cancelled: Key not trusted by user.")
            else:
                # Handle other non-trust related encryption errors
                show_alert("Encrypt", "Error encrypting file: " + str(stream_status.stderr))
                # Attempt to remove partially encrypted file on other errors too
                if os.path.exists(encrypted_file):
                    try: os.remove(encrypted_file)
                    except OSError: pass
        
        if encryption_successful:
            show_alert("Encrypt", "File encrypted and saved as " + encrypted_file)
        # else: 
            # If encryption_successful is False, an alert should have already been shown.
            # No further message needed here unless there's a specific unhandled case.

    except Exception as e:
        show_alert("Encrypt", "Error: " + str(e))
            

def decrypt():
    """
    Opens a selected encrypted file and prompts the user to enter the passphrase to decrypt it.
    """
    try:
        file = filedialog.askopenfilename(title="Select file to decrypt")
        if not file:
            show_alert("Decryption", "File not selected")
            return

        passphrase = simpledialog.askstring("Decryption", "Enter the passphrase", show="*")
        if not passphrase:
            show_alert("Decryption", "Passphrase not entered")
            return

        # Determine decrypted_file_path first
        decrypted_file_path = file[:-4] # Original logic for path
        # Ensure the file has an extension before trying to split and remove it
        if '.' in os.path.basename(decrypted_file_path) and not decrypted_file_path.endswith('.'):
            base, ext = os.path.splitext(decrypted_file_path)
            decrypted_file_path = base + "_decrypted" + ext
        else: # Handle files with no extension or ending with a dot
            decrypted_file_path += "_decrypted"

        with open(file, 'rb') as f:
            status = gpg.decrypt_file(f, passphrase=passphrase, output=decrypted_file_path)

            if not status.ok:
                tips = "Tips: \n"
                tips += "1. Check if the passphrase is correct.\n"
                tips += "2. Check if the file is actually encrypted.\n"
                tips += "3. Check if the file is a valid .gpg file format.\n"
                tips += "4. Try moving the file to a simpler path (e.g., Desktop)."
                error_message = "Error decrypting the file."
                if status.stderr:
                    error_message += "\nDetails: " + str(status.stderr)
                error_message += "\n\n" + tips
                show_alert("Decryption", error_message)
                # Attempt to remove partially decrypted file if decryption failed
                if os.path.exists(decrypted_file_path):
                    try:
                        os.remove(decrypted_file_path)
                    except OSError as e:
                        print(f"Error removing partial file {decrypted_file_path}: {e}")
                return

        show_alert("Decryption", "File decrypted and saved as " + decrypted_file_path)

    except Exception as e:
        show_alert("Decryption", "Error: " + str(e))



def generate_keys():
    """
    Show window to generate keys with the name and email of the user and the passphrase and save it as a .asc file
    """
    window = customtkinter.CTk()
    window.geometry("400x350") # Adjusted size for better layout
    window.resizable(False, False)
    window.title("GnuPG - Generate Keys")

    main_frame = customtkinter.CTkFrame(window)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def generate_keys_action():
        try:
            name = name_entry.get()
            email = email_entry.get()
            passphrase = passphrase_entry.get()

            if name == "" or email == "" or passphrase == "":
                show_alert("Generate Keys", "Fill all the fields")
                return

            input_data = gpg.gen_key_input(name_real=name, name_email=email, passphrase=passphrase)
            key = gpg.gen_key(input_data)

            if key:
                # Ask user where to save the file
                file_path = filedialog.asksaveasfilename(defaultextension=".asc",
                                                           initialfile=name + ".asc",
                                                           title="Save Key As",
                                                           filetypes=(("ASC files", "*.asc"),
                                                                      ("All files", "*.*")))
                if file_path:
                    with open(file_path, 'w') as f:
                        f.write(gpg.export_keys(key.fingerprint))
                    show_alert("Generate Keys", "Keys generated and saved as " + file_path)
                else:
                    show_alert("Generate Keys", "Key generation cancelled by user.")
            else:
                show_alert("Generate Keys", "Error generating keys")

        except Exception as e:
            show_alert("Generate Keys", "Error: " + str(e))

    name_label = customtkinter.CTkLabel(main_frame, text="Name")
    name_label.pack(pady=(0,2))
    name_entry = customtkinter.CTkEntry(main_frame, width=250)
    name_entry.pack(pady=(0,10))

    email_label = customtkinter.CTkLabel(main_frame, text="Email")
    email_label.pack(pady=(0,2))
    email_entry = customtkinter.CTkEntry(main_frame, width=250)
    email_entry.pack(pady=(0,10))

    passphrase_label = customtkinter.CTkLabel(main_frame, text="Passphrase")
    passphrase_label.pack(pady=(0,2))
    passphrase_entry = customtkinter.CTkEntry(main_frame, show="*", width=250)
    passphrase_entry.pack(pady=(0,20))

    button = customtkinter.CTkButton(main_frame, text="Generate Keys", command=generate_keys_action)
    button.pack(pady=10)
    back_button = customtkinter.CTkButton(main_frame, text="Menu", command=lambda: [window.destroy(), menu()])
    back_button.pack(pady=5)
    
    window.mainloop()

def delete_all_gpg_users():
    """
    It deletes all the keys in the keyring
    """
    keys = np.array(gpg.list_keys())
    for key in keys:
        gpg.delete_keys(key['keyid'])
    messagebox.showinfo("Delete All Keys", "All keys deleted")
    menu()

def see_keys():
    """
    It displays a list of all the public keys and their recipients
    """
    window = customtkinter.CTk()
    window.geometry("700x450") # Adjusted height
    window.title("GnuPG - See Keys")

    main_frame = customtkinter.CTkFrame(window)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    title_label = customtkinter.CTkLabel(main_frame, text="Available GPG Keys", font=("", 16, "bold"))
    title_label.pack(pady=(0, 10))

    scrollable_frame = customtkinter.CTkScrollableFrame(main_frame, height=300)
    scrollable_frame.pack(fill="x", expand=True)

    keys = np.array(gpg.list_keys())
    if len(keys) == 0:
        no_keys_label = customtkinter.CTkLabel(scrollable_frame, text="No keys found in your keyring.")
        no_keys_label.pack(pady=20)
    else:
        for key in keys:
            key_info = f"Recipient: {key['uids'][0]}\nKey ID: {key['keyid']}\nFingerprint: {key['fingerprint']}\n"
            key_label = customtkinter.CTkLabel(scrollable_frame, text=key_info, justify="left")
            key_label.pack(pady=5, anchor="w")
            separator = customtkinter.CTkFrame(scrollable_frame, height=2, fg_color="gray70") # Visual separator
            separator.pack(fill="x", pady=5)


    back_button = customtkinter.CTkButton(main_frame, text="Menu", command=lambda: [window.destroy(), menu()])
    back_button.pack(pady=20)

    window.mainloop()

def import_keys():
    """
    It asks the user to select a key to import, and if the user selects a key, it imports it
    """
    file_path = filedialog.askopenfilename(title="Select key to import", filetypes=[("All Files", "*.*")])

    if file_path:
        with open(file_path, 'rb') as file:
            import_result = gpg.import_keys(file.read())

        # check if the key was imported
        if import_result.count == 1:
            message = "Key imported"
        else:
            message = "Key not imported"

        show_alert("Import Keys", message)
    else:
        show_alert("Import Keys", "No key selected")

def compare_versions(data, version):
    """
    It compares two versions and returns True if the data is greater than the version
    """
    data = data.split(".")
    version = version.split(".")
    for i in range(len(data)):
        if int(data[i]) > int(version[i]):
            return True
    return False

def see_repo_update():
    """
    See if there is an update in the repository https://github.com/EddyDevProject/GnuPG-EasyGUI
    """
    try:
        data = requests.get("https://raw.githubusercontent.com/EddyDevProject/GnuPG-EasyGUI/master/version.txt").text
        if compare_versions(data, version):
            show_alert("Update", "There is an update available")
            menu()
        else:
            show_alert("Update", "There is no update available")
            menu()

    except Exception as e:
        show_alert("Update", "Error: " + str(e))


if __name__ == "__main__":
    try:
        menu()
    except Exception as e:
        show_alert("Error", str(e))

