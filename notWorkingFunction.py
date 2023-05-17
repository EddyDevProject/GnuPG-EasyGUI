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
