import os
import sys
import gnupg as pg
import easygui as eg
import numpy as np


def menu():
    title = "GnuPG - Menu"
    msg = "Version: 0.1(Alpha)\nAuthor: EddyDev\n\nChoose an option"
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
    file = eg.fileopenbox(msg="Select file to encrypt", title="Encrypt")
    recipient = eg.enterbox(msg="Enter recipient", title="Encrypt")
    if recipient in str(gpg.list_keys()):
        gpg.encrypt_file(open(file, 'rb'), recipients=[recipient], output=file + ".gpg")
        eg.msgbox(msg="File encrypted", title="Encrypt")
    else:
        eg.msgbox(msg="Error: Wrong recipient", title="Encrypt")
        menu()
    menu()


def decrypt():
    file = eg.fileopenbox(msg="Select file to decrypt", title="Decrypt")
    try:
        gpg.decrypt_file(open(file, 'rb'), output=file[:-4])
    except:
        eg.msgbox(msg="Error: Wrong key", title="Decrypt")
        menu()
    eg.msgbox(msg="File decrypted", title="Decrypt")   


def generate_keys():
    name = eg.enterbox(msg="Enter name", title="Generate Keys")
    email = eg.enterbox(msg="Enter email", title="Generate Keys")
    comment = eg.enterbox(msg="Enter comment", title="Generate Keys")
    gpg.gen_key(gpg.gen_key_input(name_real=name, name_email=email, name_comment=comment))
    eg.msgbox(msg="\nPublic key: " + gpg.list_keys()[-2]['keyid'] + "\nPrivate key: " + gpg.list_keys()[-1]['keyid'] + "\nRecipients: " + str(gpg.list_keys()[-2]['uids']), title="Generate Keys")
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


def see_keys():
    keys = np.array(gpg.list_keys())
    msg = "Public keys and Recipients:\n"
    for i in range(len(keys)):
        msg += "PUBLIC KEY: " + keys[i]['keyid'] + " RECIPIENTS: " + keys[i]['uids'][0] + "\n"
    eg.msgbox(msg=msg, title="See Keys")
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


