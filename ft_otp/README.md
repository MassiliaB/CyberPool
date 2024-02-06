# Ft_otp

A program that allows you to store an initial password in a file, and that is capable of generating a new one time password every time it is requested.

Usage :
```bash
$ echo -n "HERE IS A KEY MY FRIEND" > key.txt
$ ./ft_otp -g key.hex
Key was successfully saved in ft_otp.key.
$ ./ft_otp -k ft_otp.key
836492
```

• Option -g : The program receives as argument a hexadecimal key of at least 64 characters. The program stores this key safely in a file called ft_otp.key, which
is encrypted.
• Option -k : The program generates a new temporary password based on the key given as argument and prints it on the standard output.
