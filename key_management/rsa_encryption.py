from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from aes_encryption import generate_aes_key, encrypt_file_with_aes_gcm, decrypt_file_with_aes_gcm

def generate_rsa_keypair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

rsa_keys = generate_rsa_keypair()
# print(rsa_keys)

def encrypt_aes_key_with_rsa(aes_key, public_key):
    rsa_key = RSA.import_key(public_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    encrypted_aes_key = cipher_rsa.encrypt(aes_key)
    return encrypted_aes_key

def decrypt_aes_key_with_rsa(encrypted_aes_key, private_key):
    rsa_key = RSA.import_key(private_key)
    cipher_rsa = PKCS1_OAEP.new(rsa_key)
    aes_key = cipher_rsa.decrypt(encrypted_aes_key)
    return aes_key

# aes_key = generate_aes_key()

plaintext = b"Hello Everyone"
# encrypt_aes = encrypt_file_with_aes_gcm(plaintext, aes_key)

# print(f"Generated AES Key - {aes_key}\n")
# print(f"Initialization Vector (IV) - {encrypt_aes[0]}\n")

# aes_rsa_encrypt = encrypt_aes_key_with_rsa(encrypt_aes[1], rsa_keys[1])
# print(f"AES encryption with RSA - {aes_rsa_encrypt}\n")

# aes_rsa_decrypt = decrypt_aes_key_with_rsa(aes_rsa_encrypt, rsa_keys[0])
# print(f"AES decryption with RSA - {aes_rsa_decrypt}")

# def hybrid_encrypt(file_data, public_key):
#     # Step 1: Generate a random AES key (for 256-bit encryption)
#     aes_key = generate_aes_key()  # 256-bit AES key

#     # Step 2: Encrypt the file data with AES
#     iv, encrypted_file_data, tag = encrypt_file_with_aes_gcm(file_data, aes_key)

#     # Step 3: Encrypt the AES key with RSA
#     encrypted_aes_key = encrypt_aes_key_with_rsa(aes_key, public_key)

#     # Return encrypted AES key, IV, and encrypted file data
#     return iv, encrypted_file_data, tag, encrypted_aes_key

def hybrid_encrypt(file_data, public_key):
    # Step 1: Generate a random AES key (for 256-bit encryption)
    aes_key = generate_aes_key()  # 256-bit AES key

    # Step 2: Encrypt the file data with AES
    iv, encrypted_file_data, tag = encrypt_file_with_aes_gcm(file_data, aes_key)

    # Step 3: Encrypt the AES key with RSA
    encrypted_aes_key = encrypt_aes_key_with_rsa(aes_key, public_key)

    # Return encrypted AES key, IV, encrypted file data, and the length of the encrypted AES key
    return iv, encrypted_file_data, tag, encrypted_aes_key, len(encrypted_aes_key)

def hybrid_decrypt(encrypted_file_data, encrypted_aes_key, private_key, tag, iv):
    # Step 1: Decrypt the AES key using RSA
    aes_key = decrypt_aes_key_with_rsa(encrypted_aes_key, private_key)
    
    # Step 2: Decrypt the file data using AES
    decrypted_file_data = decrypt_file_with_aes_gcm(encrypted_file_data, tag, aes_key, iv)

    return decrypted_file_data

# iv, encrypted_file_data, tag, encrypted_aes_key = hybrid_encrypt(plaintext, rsa_keys[1])
# print(iv, encrypted_file_data, tag, encrypted_aes_key)

# decrypted_text = hybrid_decrypt(encrypted_file_data, encrypted_aes_key, rsa_keys[0], tag, iv)
# print(decrypted_text)
