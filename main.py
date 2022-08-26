import os
import sys
from unicodedata import name
import gnupg as pg
import easygui as eg
import numpy as np


def menu():
    title = "GnuPG - Menu"
    msg = "Version: 0.1.1(Alpha)\nAuthor: EddyDev\n\nChoose an option"
    choices = ["Encrypt", "Decrypt", "Generate Keys", "Import Keys", "See Keys", "Quit"]
    choix = eg.buttonbox(msg=msg, title=title, choices=choices)
    if choix == "Encrypt":
        encrypt()
    elif choix == "Decrypt":
        decrypt()
    elif choix == "Generate Keys":
        generate_keys()
    elif choix == "Import Keys":
        import_keys()
    elif choix == "See Keys":
        see_keys()
    elif choix == "Quit":
        sys.exit()

def encrypt():
    """
    It opens a file, then asks the user to choose a recipient from a list of public keys, then encrypts
    the file with the chosen public key.
    """
    file = eg.fileopenbox(msg="Select file to encrypt", title="Encrypt")
    msg = "Choose a recipient"
    recipient = eg.enterbox(msg=msg, title="Encrypt")
    try:
        print("Recipient: " + recipient)
        fingerprint = gpg.list_keys(recipient)[0]['fingerprint']
        print("Fingerprint: " + fingerprint)
        gpg.encrypt_file(open(file, 'rb'), fingerprint, output=file + ".gpg")
        eg.msgbox(msg="File encrypted", title="Encrypt")
    except Exception as e:
        eg.msgbox(msg="Error: " + str(e), title="Encrypt")
        menu()
    menu()


def decrypt():
    """
    It opens a file, decrypts it, and then displays a message box.
    """
    file = eg.fileopenbox(msg="Select file to decrypt", title="Decrypt")
    try:
        gpg.decrypt_file(open(file, 'rb'), output=file[:-4])
    except Exception as e:
        eg.msgbox(msg="Error: " + str(e), title="Decrypt")
        menu()
    eg.msgbox(msg="File decrypted", title="Decrypt")  


def check_name(name):
    """
    It takes a name as an argument and returns True if the name is not in the list of keys, and False if
    it is
    
    :param name: The name of the person you want to encrypt the message for
    :return: a boolean value.
    """
    keys = np.array(gpg.list_keys())
    for i in range(len(keys)):
        all_word =  keys[i]['uids'][0].split()
        if name == all_word[0]:
            #print("1" + name + " == " +  keys[i]['uids'][0])
            return False
        #print("2" + name + " == " + keys[i]['uids'][0])
    return True
     
def generate_keys():
    name = eg.enterbox(msg="Enter name", title="Generate Keys")
    while not check_name(name):
        name = eg.enterbox(msg="Error alredy exists. enter name: ", title="Generate Keys")
    email = eg.enterbox(msg="Enter email", title="Generate Keys")
    comment = eg.enterbox(msg="Enter comment", title="Generate Keys")
    gpg.gen_key(gpg.gen_key_input(name_real=name, name_email=email, name_comment=comment))
    eg.msgbox(msg="Keys generated", title="Generate Keys")
    choix = eg.buttonbox("Do you want to export keys?", "Generate Keys", ("Yes", "No"))
    if choix == "Yes":
        export_keys()
    elif choix == "No":
        menu()


def export_keys():
    path = eg.diropenbox(msg="Select path to export keys", title="Export Keys")
    with open(path + "/public.key", 'w') as f:
        f.write(gpg.export_keys(gpg.list_keys()[0]['keyid']))
    with open(path + "/private.key", 'w') as f:
        f.write(gpg.export_keys(gpg.list_keys()[1]['keyid']))
    eg.msgbox(msg="Keys exported", title="Export Keys")
    choix = eg.buttonbox("Do you want to quit?", "Export Keys", ("Yes", "No"))
    if choix == "Yes":
        sys.exit()
    elif choix == "No":
        menu()

def delete_all_gpg_users():
    keys = np.array(gpg.list_keys())
    for i in range(len(keys)):
        gpg.delete_keys(keys[i]['keyid'])
    eg.msgbox(msg="All keys deleted", title="Delete All Keys")
    menu()


def see_keys():
    keys = np.array(gpg.list_keys())
    msg = "Public keys and Recipients:\n"
    for i in range(len(keys)):
        msg += "PUBLIC KEY: " + keys[i]['keyid'] + " RECIPIENTS: " + keys[i]['uids'][0] + "\n"
    choix = eg.buttonbox(msg=msg, title="See Keys", choices=["Delete All Keys", "Menu", "Raw Keys"])
    if choix == "Delete All Keys":
        delete_all_gpg_users()
    elif choix == "Menu":
        menu()
    elif choix == "Raw Keys":
        eg.msgbox(msg=str(gpg.list_keys()), title="See Keys")
        menu()

def import_keys():
    key = eg.fileopenbox(msg="Select key to import", title="Import Keys")
    gpg.import_keys(open(key, 'rb').read())
    eg.msgbox(msg="Key imported", title="Import Keys")
    eg.msgbox(msg="Imported keys: " + str(gpg.list_keys()), title="Import Keys")
    menu()


if __name__ == "__main__":
    gpg = pg.GPG()
    menu()


