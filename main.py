import os
from random import choices
import sys
import gnupg as pg
import easygui as eg
import numpy as np

def menu():
    """
    It displays a menu with buttons and when you click on one of them, it calls the corresponding
    function.
    """
    title = "GnuPG - Menu"
    msg = "Version: 0.1.2(Alpha)\nAuthor: EddyDev\n\nChoose an option"
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
        outputFileName = file[:-4]
        if os.path.exists(outputFileName):
            i = 1
            while os.path.exists(outputFileName + str(i)):
                i += 1
            outputFileName += str(i)
        gpg.decrypt_file(open(file, 'rb'), output=outputFileName)
        if os.path.exists(outputFileName):
            eg.msgbox(msg="File decrypted and saved as " + outputFileName, title="Decrypt")
        else:
            eg.msgbox(msg="File decrypted but not saved", title="Decrypt")
    except Exception as e:
        eg.msgbox(msg="Error: " + str(e), title="Decrypt")
        menu() 


def check_name(name):
    """
    It takes a name as an argument and returns True if the name is not in the list of keys, and False if
    it is
    
    :param name: The name of the person you want to encrypt the message for
    :return: a boolean value.
    """
    keys = np.array(gpg.list_keys())
    if name == "":
        return False
    for i in range(len(keys)):
        all_word =  keys[i]['uids'][0].split()
        if name == all_word[0]:
            #print("1" + name + " == " +  keys[i]['uids'][0])
            return False
        #print("2" + name + " == " + keys[i]['uids'][0])
    return True

def generate_keys():
    msg = "Function temporarily disabled."
    msg += "\nYou can generate your own keys from the terminal."
    msg += "\ngpg --gen-key <- this will generate keys for you"
    msg += "\ngpg --export --armor NAMECHOSEN > pub.key <- export your keys in pub.key"
    msg += "\n\nIf you want to contribute to the development you can modify/fix the function generate_keys_old()"
    choices = ["CMD for Windows", "Terminal for Linux", "Close"]
    choix = eg.buttonbox(msg=msg, title="Generate Keys", choices=choices)
    if choix == "CMD for Windows":
        os.system("start cmd")
    elif choix == "Terminal for Linux":
        os.system("gnome-terminal")
    elif choix == "Close":
        menu()
     
def generate_keys_old():
    """
    It asks the user for a name, email and comment, then checks if the name is already in use, then
    generates a key with the given name, email and comment
    """
    
    try:
        multichoise = ["Name*", "Email", "Comment"]
        values = eg.multenterbox(msg="Enter name, email and comment (* required)", title="Generate Keys", fields=multichoise)
        name = values[0]
        email = values[1]
        comment = values[2]
        while not check_name(name):
            name = eg.enterbox(msg="Error alredy exists or is empty, enter name: ", title="Generate Keys")
        
        try:
            if(name != "" and name is not None):
                #print("Name: " + name)
                go = gpg.gen_key(gpg.gen_key_input(name_real=name, name_email=email, name_comment=comment))
                if go:
                    eg.msgbox(msg="Keys generated", title="Generate Keys")
                    choix = eg.buttonbox("Do you want to export keys?", "Generate Keys", ("Yes", "No"))
                    if choix == "Yes":
                        export_keys()
                    elif choix == "No":
                        menu()
                else:
                    menu()
            else:
                menu()
        except Exception as e:
            eg.msgbox(msg="Error: " + str(e), title="Generate Keys")
            menu()
    except TypeError as e:
        menu()
        


def export_keys():
    """
    It exports the keys to a directory of your choice
    """
    #bug: //TODO: #1 last key is not exported and private key is not exported

    path = eg.diropenbox(msg="Select path to export keys", title="Export Keys")
    with open(path + "/public.key", 'w') as f:
        f.write(gpg.export_keys(gpg.list_keys()[-1]['keyid']))
    with open(path + "/private.key", 'w') as f:
        f.write(gpg.export_keys(gpg.list_keys()[-1]['keyid']), secret=True)
    eg.msgbox(msg="Keys exported", title="Export Keys")
    choix = eg.buttonbox("Do you want to quit?", "Export Keys", ("Yes", "No"))
    if choix == "Yes":
        sys.exit()
    elif choix == "No":
        menu()

def delete_all_gpg_users():
    """
    It deletes all the keys in the keyring
    """
    keys = np.array(gpg.list_keys())
    for i in range(len(keys)):
        gpg.delete_keys(keys[i]['keyid'])
    eg.msgbox(msg="All keys deleted", title="Delete All Keys")
    menu()


def see_keys():
    """
    It displays a list of all the public keys and their recipients
    """
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
    """
    It asks the user to select a key to import, and if the user selects a key, it imports it
    """
    key = eg.fileopenbox(msg="Select key to import", title="Import Keys")
    if key == None:
        eg.msgbox(msg="No key selected", title="Import Keys")
        menu()
    gpg.import_keys(open(key, 'rb').read())
    eg.msgbox(msg="Key imported", title="Import Keys")
    menu()


if __name__ == "__main__":
    gpg = pg.GPG()
    menu()
    




