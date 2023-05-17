import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import gnupg as pg
import numpy as np
import webbrowser

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
    window = tk.Tk()
    window.geometry("350x300")
    window.resizable(False, False)
    window.title("GnuPG - Menu")
    label = tk.Label(window, text="Version: 0.1.7(Alpha)\nAuthor: EddyDev\nLicense: MIT\n")
    link1 = tk.Label(window, text="Github Project", fg="red", cursor="hand2")
    label.pack()
    link1.bind("<Button-1>", lambda e: callback("https://github.com/EddyDevProject/GnuPG-EasyGUI"))
    link1.pack()

    choices = ["Encrypt", "Decrypt", "Generate Keys", "Import Keys", "See Keys", "Quit"]

    def handle_choice(choice):
        window.destroy()
        if choice == "Encrypt":
            encrypt()
        elif choice == "Decrypt":
            decrypt()
        elif choice == "Generate Keys":
            generate_keys()
        elif choice == "Import Keys":
            import_keys()
        elif choice == "See Keys":
            see_keys()
        elif choice == "Quit":
            sys.exit()

    for choice in choices:
        button = tk.Button(window, text=choice, command=lambda choice=choice: handle_choice(choice))
        button.pack()

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
            menu()
            return

        keys = gpg.list_keys()
        names = [key['uids'][0].split()[0] for key in keys]

        recipient = simpledialog.askstring("Encrypt", "Select recipient")
        if not recipient:
            show_alert("Encrypt", "Recipient not selected")
            menu()
            return

        print("Recipient: " + recipient)

        recipient_keys = [key for key in keys if key['uids'][0].split()[0] == recipient]
        if len(recipient_keys) == 0:
            show_alert("Encrypt", "Recipient not found")
            menu()
            return

        fingerprint = recipient_keys[0]['fingerprint']
        print("Fingerprint: " + fingerprint)

        encrypted_file = file + ".gpg"
        gpg.encrypt_file(open(file, 'rb'), fingerprint, output=encrypted_file)
        show_alert("Encrypt", "File encrypted")

    except Exception as e:
        show_alert("Encrypt", "Error: " + str(e))
    menu()

def decrypt():
    """
    It opens a file, decrypts it, and then displays a message box.
    """
    try:
        file = filedialog.askopenfilename(title="Select file to decrypt", filetypes=(("GPG files", "*.gpg"),))
        if not file:
            show_alert("Decrypt", "File not selected")
            menu()
            return

        outputFileName = file[:-4]
        outputExtension = outputFileName[-4:]

        i = 1
        while os.path.exists(outputFileName + outputExtension):
            i += 1
            outputFileName = outputFileName[:-1] + str(i)

        outputFileName += outputExtension

        with open(file, 'rb') as f:
            passphrase = ''
            if not gpg.decrypt_file(f, passphrase=''):
                passphrase = simpledialog.askstring("Decrypt", "Enter passphrase", show='*')

            gpg.decrypt_file(open(file, 'rb'), passphrase=passphrase, output=outputFileName)

        if os.path.exists(outputFileName):
            show_alert("Decrypt", "File decrypted and saved as " + outputFileName)
        else:
            show_alert("Decrypt", "File decrypted but not saved")

    except Exception as e:
        show_alert("Decrypt", "Error: " + str(e))
    menu()

def generate_keys():
    """
    Show window to generate keys with the name and email of the user and the passphrase and save it as a .asc file
    """
    window = tk.Tk()
    window.geometry("350x300")
    window.resizable(False, False)
    window.title("GnuPG - Generate Keys")

    def generate_keys_action():
        try:
            name = name_entry.get()
            email = email_entry.get()
            passphrase = passphrase_entry.get()

            if name == "" or email == "" or passphrase == "":
                show_alert("Generate Keys", "Fill all the fields")
                return

            input_data = gpg.gen_key_input(name_email=name + " <" + email + ">", passphrase=passphrase)
            key = gpg.gen_key(input_data)

            if key:
                with open(name + ".asc", 'w') as f:
                    f.write(gpg.export_keys(key.fingerprint))
                show_alert("Generate Keys", "Keys generated and saved as " + name + ".asc")
            else:
                show_alert("Generate Keys", "Error generating keys")

        except Exception as e:
            show_alert("Generate Keys", "Error: " + str(e))

    name_label = tk.Label(window, text="Name")
    name_label.pack()
    name_entry = tk.Entry(window)
    name_entry.pack()

    email_label = tk.Label(window, text="Email")
    email_label.pack()
    email_entry = tk.Entry(window)
    email_entry.pack()

    passphrase_label = tk.Label(window, text="Passphrase")
    passphrase_label.pack()
    passphrase_entry = tk.Entry(window, show="*")
    passphrase_entry.pack()

    button = tk.Button(window, text="Generate Keys", command=generate_keys_action)
    button.pack()
    back_button = tk.Button(window, text="Menu", command=lambda: [window.destroy(), menu()])
    back_button.pack()
    
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
    keys = np.array(gpg.list_keys())
    msg = "Public keys and Recipients:\n"
    for key in keys:
        msg += "PUBLIC KEY: " + key['keyid'] + " RECIPIENTS: " + key['uids'][0] + "\n"

    messagebox.showinfo("See Keys", msg)
    menu()

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

    menu()

if __name__ == "__main__":
    menu()
