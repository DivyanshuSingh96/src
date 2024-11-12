from PIL import Image
import numpy as np
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from rsa_encryption import generate_rsa_keypair, hybrid_encrypt, hybrid_decrypt

# Function to convert text to binary (for hiding in the image)
def text_to_bin(text):
    binary = ''.join(format(byte, '08b') for byte in text)
    return binary

def embed_message_in_image(image_path, message, output_image_path):
    img = Image.open(image_path)
    img_data = np.array(img)

    binary_data = ''.join(format(byte, '08b') for byte in message) + '1010101010101010'  # Add a delimiter
    data_len = len(binary_data)

    if data_len > img_data.size:
        raise ValueError("Message is too large to fit in the image.")

    data_idx = 0
    for row in range(img_data.shape[0]):
        for col in range(img_data.shape[1]):
            if data_idx < data_len:
                for channel in range(3):  # RGB channels
                    pixel_val = img_data[row, col, channel]
                    # Modify the LSB (Least Significant Bit) to embed the message
                    img_data[row, col, channel] = (pixel_val & ~1) | int(binary_data[data_idx])
                    data_idx += 1
                    if data_idx >= data_len:
                        break

    output_img = Image.fromarray(img_data)
    output_img.save(output_image_path)

def extract_data_from_image(image_path):
    img = Image.open(image_path)
    img_data = np.array(img)

    binary_data = ''
    data_idx = 0
    for row in range(img_data.shape[0]):
        for col in range(img_data.shape[1]):
            for channel in range(3):  # RGB channels
                pixel_val = img_data[row, col, channel]
                binary_data += str(pixel_val & 1)
                data_idx += 1
                if data_idx >= img_data.size * 3:  # Assuming the entire image is used to store the message
                    break
        if data_idx >= img_data.size * 3:
            break

    # Find the delimiter
    delimiter_idx = binary_data.find('1010101010101010')
    if delimiter_idx == -1:
        raise ValueError("Delimiter not found in the image data.")

    # Extract the plaintext message
    plaintext_message = bytes([int(binary_data[i:i+8], 2) for i in range(0, delimiter_idx, 8)])

    # Extract the encrypted file data
    encrypted_file_data = bytes([int(binary_data[i:i+8], 2) for i in range(delimiter_idx + 16, len(binary_data), 8)])

    return plaintext_message, encrypted_file_data

if __name__ == "__main__":

    image_path = 'django-cloudflare-r2/src/utils/images/5633.jpg'
    output_image_path = 'django-cloudflare-r2/src/utils/images/5633_new2.png'

    private_key, public_key = generate_rsa_keypair()

    plaintext = b"This is the message to hide."

    embed_message_in_image(image_path=image_path, message=plaintext, output_image_path=output_image_path)
    print(f"Message is successfully saved!!!")

    iv, encrypted_file_data, tag, encrypted_aes_key, encrypted_aes_key_length = hybrid_encrypt(open(output_image_path, 'rb').read(), public_key)

    try:
        decrypted_image_data = hybrid_decrypt(encrypted_file_data, encrypted_aes_key, private_key, tag, iv)

        with open('django-cloudflare-r2/src/utils/images/5633_decrypted.png', 'wb') as f:
            f.write(decrypted_image_data)
        print("Decrypted image saved.")
    except ValueError as e:
        print(f"Error decrypting the image: {e}")
        exit(1)

    extracted_message, _ = extract_data_from_image('django-cloudflare-r2/src/utils/images/5633_decrypted.png')
    print("Extracted message:", extracted_message)
