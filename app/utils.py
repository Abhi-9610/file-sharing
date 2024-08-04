import os
from cryptography.fernet import Fernet

# Generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Encrypt the filename
def encrypt_filename(filename, key):
    f = Fernet(key)
    return f.encrypt(filename.encode()).decode()

# Decrypt the filename
def decrypt_filename(encrypted_filename, key):
    f = Fernet(key)
    return f.decrypt(encrypted_filename.encode()).decode()
