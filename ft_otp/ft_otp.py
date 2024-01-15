import sys
import hashlib
import hmac
import math
import time
import hashlib
import os

def is_hex_string(string):
    try:
        int(string, 16)
        return True
    except ValueError:
        return False

def encryptKey(key: str):
    hash_object = hashlib.sha256()
    hash_object.update(key.encode())
    hash_password = hash_object.hexdigest()
    with open("ft_otp.key", "w") as keyfile:
        keyfile.write(hash_password)
    print("Key was successfully saved in ft_otp.key")

def passwdGen(len: int = 6):
    with open("ft_otp.key", "r") as keyfile:
        file = keyfile.read()
    current_time = math.floor(time.time())
    step = 30
    t = math.floor(current_time / step)
    hash_value = hmac.new(
        bytes(file, encoding="utf-8"),
        t.to_bytes(length=8, byteorder="big"),
        hashlib.sha256,
    ).digest()
    return trunc(hash_value, len)

def trunc(hash_value: hmac.HMAC, length: int) -> str:
    bitstring = bin(int(hash_value.hex(), base=16))
    last_four_bits = bitstring[-4:]
    offset = int(last_four_bits, base=2)
    chosen_32_bits = bitstring[offset * 8 : offset * 8 + 32]
    full_totp = str(int(chosen_32_bits, base=2))
    return full_totp[-length:]

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 script.py <-k|-g>")
        sys.exit(1)

    option = sys.argv[1]
    file = sys.argv[2]

    if option == "-g":
        if os.path.isfile(file):
            with open(file, "r") as file:
                hex_content = file.read().strip()
                if is_hex_string(hex_content) and len(hex_content) >= 64:
                    encryptKey(hex_content)
                else:
                    print("Error: key must be 64 hexadecimal characters.")
        else:
            print(f"Error: File {file} does not exist.")
    elif option == "-k":
        if os.path.isfile("ft_otp.key") and os.path.basename(file) == "ft_otp.key":
            tempPasswd = passwdGen()
            print(f"Temporary Password: {tempPasswd}")
        else:
            print("Error: send the ft_otp.key file")
            sys.exit(1)
    else:
        print("Error: Invalid option, please use -k or -g")
        sys.exit(1)
if __name__ == "__main__":
    main()