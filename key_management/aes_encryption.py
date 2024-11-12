import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def generate_aes_key():
    key = os.urandom(32)
    return key

def encrypt_file_with_aes_gcm(file_data, aes_key):
    nonce = get_random_bytes(12)  # 12-byte IV for GCM
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(file_data)
    return nonce, ciphertext, tag

def decrypt_file_with_aes_gcm(ciphertext, tag, aes_key, nonce):
    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    return decrypted_data

if __name__ == "__main__":
    plaintext = b"Hello Everyone"
    aes_key = generate_aes_key()
    # # print(aes_key)

    encrypt_data = encrypt_file_with_aes_gcm(plaintext, aes_key)
    print(encrypt_data)

    decrypt_data = decrypt_file_with_aes_gcm(encrypt_data[1], encrypt_data[2], aes_key, encrypt_data[0])
    print(decrypt_data)