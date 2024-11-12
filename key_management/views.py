import logging
import json
import os
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from PIL import Image
import numpy as np

import requests
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from imageUpload.forms import ImagePostForm
from django.http import JsonResponse
from rest_framework.decorators import parser_classes, renderer_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer

# from key_management.aes_encryption import generate_aes_key, encrypt_file_with_aes_gcm, decrypt_file_with_aes_gcm
# from key_management.rsa_encryption import generate_rsa_keypair
# from key_management.steganography_encrypt_decrypt import embed_message_in_image

from rest_framework import serializers
from decouple import config as env_config

# from aes_encryption import generate_aes_key, encrypt_file_with_aes_gcm, decrypt_file_with_aes_gcm
# from rsa_encryption import generate_rsa_keypair
# from steganography_encrypt_decrypt import embed_message_in_image, extract_data_from_image, generate_rsa_keypair, hybrid_decrypt, hybrid_encrypt
from imageViewer.services import upload_image_to_cloudflare

from .serializers import TaskSerializer, EncryptedImageSerializer
from .models import Task, EncryptedImage

class UploadKey(APIView):
    def post(self, request):
        # Log the received data for debugging
        logger.debug("Received POST request data: %s", request.data)

        # Use serializer to validate request data
        serializer = TaskSerializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Invalid data received: {serializer.errors}")
            return Response({"error": "Invalid data format", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # Extract validated data
        data = serializer.validated_data

        # Cloudflare Worker URL
        CLOUDFLARE_WORKER_URL = env_config("CLOUDFLARE_WORKER_URL")

        try:
            # Forward data to Cloudflare Worker
            logger.info("Forwarding data to Cloudflare Worker...")
            # headers = {
            #     "Content-Type": "application/json",
            #     "Authorization": f"Bearer {env_config('WORKERS_API_TOKEN')}"  # If your Cloudflare Worker requires authorization
            # }
            response = requests.post(CLOUDFLARE_WORKER_URL, json=[data])#, headers=headers)

            # Log Cloudflare response status and text for debugging
            logger.debug(f"Cloudflare Worker Response: Status: {response.status_code}, Text: {response.text}")

            # Check if the response from Cloudflare is successful
            if response.status_code == 200:
                logger.info("Key-value pair uploaded successfully to Cloudflare Worker")
                return Response({"message": "Key-value pair uploaded successfully"}, status=status.HTTP_200_OK)
            else:
                logger.error(f"Error from Cloudflare Worker: Status: {response.status_code}, Response: {response.text}")
                return Response({"error": "Error uploading data to Cloudflare Worker"}, status=response.status_code)

        except requests.RequestException as e:
            # Log any exceptions that occur during the request to Cloudflare Worker
            logger.error(f"Exception occurred while forwarding data to Cloudflare Worker: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetKey(APIView):
    def get(self, request):
        key = request.query_params.get('key')
        logging.debug("Received GET request for key_id: %s", key)

        CLOUDFLARE_WORKER_URL = env_config("CLOUDFLARE_WORKER_URL")

        if key:
            response = requests.get(f"{CLOUDFLARE_WORKER_URL}?key={key}")
            # response = "key_id"

            response_json = json.loads(response.text)
            key = response_json["key"]
            value = response_json["value"]

            json_dict = {
                "key": key,
                "keyId": value
            }

            if response.status_code == 200:
                logging.info("Key retrieved successfully")
                return Response(json_dict, status=status.HTTP_200_OK)
            else:
                logging.error(f"Error retrieving key, Status: {response.status_code}, Response: {response.text}")
                return Response({"message": "Error retrieving key"}, status=response.status_code)

        logging.warning("Key ID required but not provided")
        return Response({"message": "Key ID required"}, status=status.HTTP_400_BAD_REQUEST)

# def upload_image_view(request):
#     if request.method == 'POST':
#         form = ImagePostForm(request.POST, request.FILES)
#         if form.is_valid():
#             image_file = form.cleaned_data['image_file']
#             plaintext = b"This is the message to hide."

#             # Embed the message in the image
#             output_image_path = 'path/to/save/encrypted_image.png'
#             embed_message_in_image(image_file.path, plaintext, output_image_path)

#             # Encrypt the image
#             private_key, public_key = generate_rsa_keypair()
#             iv, encrypted_image_data, tag, encrypted_aes_key, _ = hybrid_encrypt(open(output_image_path, 'rb').read(), public_key)

#             # Save the data for later retrieval or display
#             request.session['private_key'] = private_key.export_key().decode()
#             request.session['public_key'] = public_key.export_key().decode()

#             return redirect('display_image')  # Redirect to display the image page

#     else:
#         form = ImagePostForm()
#     return render(request, 'upload_image.html', {'form': form})

KEYS_UPLOAD_API_URL = "http://cryptic-cloud.vercel.app/api/apiPost"  # API for uploading keys
IMAGE_UPLOAD_API_URL = "http://cryptic-cloud.vercel.app/image-upload/apiPOST-Image"  # API for uploading image

@api_view(["POST"])
def upload_encrypted_image(request):
    if request.method == "POST":
        # Extract data from the incoming request
        public_key = request.data.get("public_key")
        private_key = request.data.get("private_key")
        title = request.data.get("title")
        author = request.data.get("author")
        message = request.data.get("message")
        image_url = request.data.get("image_url")  # Image (this might be a URL or base64 data)
        is_encrypted = request.data.get("is_encrypted", True)

        # Validate input data
        if not all([public_key, private_key, title, author, message, image_url]):
            return Response({"message": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

        # Step 1: Upload the keys to the keys API
        kv_data = {
            "key": f"({public_key}, {private_key})",
            "keyId": f"({message}, {image_url})",  # placeholder until image URL is fetched
        }

        try:
            kv_response = requests.post(KEYS_UPLOAD_API_URL, json=[kv_data], headers={"Content-Type": "application/json"})
            kv_response.raise_for_status()  # Raise an HTTPError for bad responses (4xx, 5xx)
        except requests.exceptions.RequestException as e:
            print(f"Error uploading keys: {e}")
            return Response({"message": f"Failed to upload keys to Cloudflare KV: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Step 2: Upload the image to the image upload API
        image_payload = {
            "title": title,
            "author": author,
            "image_url": image_url,
            "is_encrypted": is_encrypted,
        }

        try:
            image_response = requests.post(IMAGE_UPLOAD_API_URL, json=image_payload, headers={"Content-Type": "application/json"})
            image_response.raise_for_status()  # Raise an HTTPError for bad responses
        except requests.exceptions.RequestException as e:
            print(f"Error uploading image: {e}")
            return Response({"message": f"Failed to upload image to the server: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Get the image URL from the response (assuming the response contains image_url)
        image_url = image_response.json().get("image_url")
        print(image_url)
        if not image_url:
            return Response({"message": "Image URL not returned from image upload API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Now update the key ID with the real image URL
        # kv_data[0]["keyId"] = f"({message}, {image_url})"
        
        # # POST the updated kv_data to save the keys with the image URL
        # try:
        #     kv_response_updated = requests.post(KEYS_UPLOAD_API_URL, json=[kv_data], headers={"Content-Type": "application/json"})
        #     kv_response_updated.raise_for_status()  # Raise an HTTPError for bad responses
        # except requests.exceptions.RequestException as e:
        #     print(f"Error updating keys with image URL: {e}")
        #     return Response({"message": f"Failed to update keys with the image URL: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Step 3: Now save the image metadata to your database
        data_info = {
            "title": title,
            "author": author,
            "image_url": image_url,
            "is_encrypted": is_encrypted,
            "message": message,
            "public_key": public_key,
            "private_key": private_key
        }

        # Assuming you have the EncryptedImageSerializer defined as per your model
        serializer = EncryptedImageSerializer(data=data_info)
        if serializer.is_valid():
            serializer.save()
        else:
            print(f"Validation error: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Successfully uploaded image and encrypted data"}, status=status.HTTP_201_CREATED)


# @api_view(["POST"])
# def upload_encrypted_image(request):
#     if request.method == "POST":
#         # Extract data from the incoming request
#         public_key = request.data.get("public_key")
#         private_key = request.data.get("private_key")
#         title = request.data.get("title")
#         author = request.data.get("author")
#         message = request.data.get("message")
#         image_data = request.data.get("image_file")  # Image (this might be a URL or base64 data)
#         is_encrypted = request.data.get("is_encrypted", True)

#         # Step 1: Upload the keys to the keys API
#         kv_data = {
#             "key": f"({public_key}, {private_key})",
#             "keyId": f"({message}, placeholder_image_url)",  # placeholder until image URL is fetched
#         }

#         # POST request to upload keys
#         kv_response = requests.post(KEYS_UPLOAD_API_URL, json=[kv_data], headers={"Content-Type": "application/json"})
#         if kv_response.status_code != 200:
#             return Response({"message": "Failed to upload keys to Cloudflare KV"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # Step 2: Upload the image to the image upload API
#         image_payload = {
#             "image": image_data,  # Image data
#             "is_encrypted": is_encrypted,  # Boolean to indicate if the image is encrypted
#         }

#         # POST request to upload the image
#         image_response = requests.post(IMAGE_UPLOAD_API_URL, json=image_payload, headers={"Content-Type": "application/json"})
#         if image_response.status_code != 200:
#             return Response({"message": "Failed to upload image to the server"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # Get the image URL from the response (assuming the response contains image_url)
#         image_url = image_response.json().get("image_url")

#         # Now update the key ID with the real image URL
#         kv_data[0]["keyId"] = f"({message}, {image_url})"
        
#         # POST the updated kv_data to save the keys with the image URL
#         kv_response_updated = requests.post(KEYS_UPLOAD_API_URL, json=[kv_data], headers={"Content-Type": "application/json"})
#         if kv_response_updated.status_code != 200:
#             return Response({"message": "Failed to update keys with the image URL"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         # Step 3: Now save the image metadata to your database
#         # Create a dictionary to save the image metadata
#         data_info = {
#             "title": title,
#             "author": author,
#             "image_url": image_url,
#             "is_encrypted": is_encrypted,
#         }

#         # Here we assume you have an `EncryptedImage` model to store this data.
#         # You can use a serializer to save this in your database.
#         # Assuming `EncryptedImageSerializer` exists:

#         # EncryptedImageSerializer should be implemented in your `serializers.py` file
#         serializer = EncryptedImageSerializer(data=data_info)
#         if serializer.is_valid():
#             serializer.save()
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response({"message": "Successfully uploaded image and encrypted data"}, status=status.HTTP_201_CREATED)

# @api_view(["POST"])
# @renderer_classes([JSONRenderer, BrowsableAPIRenderer])
# @parser_classes([MultiPartParser, FormParser])
# def upload_encrypted_image(request):
#     if request.method == "POST":
#         data = request.json()
#         image_data = data.get("image_file")
#         public_key = data.get("public_key")
#         private_key = data.get("private_key")
#         title = data.get("title")
#         author = data.get("author")
#         message = data.get("message")
#         is_encrypted = data.get("is_encrypted")

#         # Send encrypted image to Cloudflare R2
#         image_url = upload_image_to_cloudflare(image_data, is_encrypted=True)
        
#         # Save keys to Cloudflare KV
#         kv_data = [{
#             "key": f"({public_key}, {private_key})",
#             "keyId": f"({message}, {image_url})",
#         }]

#         data_info = {
#             "title": title,
#             "author": author,
#             "image_url": image_url,
#             "is_encrypted": is_encrypted,
#         }

#         save_keys_to_kv(kv_data)
#         save_data_info(data_info)

#         return JsonResponse({"message": "Successfully uploaded and encrypted"})

# def save_keys_to_kv(kv_data):
#     kv_api = "http://127.0.0.1:8000/api/apiPost"

#     # Headers for the request
#     headers = {
#         'Content-Type': 'application/json'
#     }

#     # Sending POST request
#     response = requests.post(kv_api, headers=headers, json=kv_data)

#     # Print the response
#     if response.status_code == 200:
#         print("Success:", response.json())
#     else:
#         print("Failed:", response.status_code, response.text)

# def save_data_info(data_info):
#     data_api = "http://127.0.0.1:8000/image-upload/apiPOST-Image"
    
#     # Headers for the request
#     headers = {
#         'Content-Type': 'application/json'
#     }

#     # Sending POST request
#     response = requests.post(data_api, headers=headers, json=data_info)

#     # Print the response
#     if response.status_code == 200:
#         print("Success:", response.json())
#     else:
#         print("Failed:", response.status_code, response.text)

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

def generate_rsa_keypair():
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

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

def display_image_view(request, pk, is_encrypted=False):
    # Generate RSA keys
    public_key, private_key = generate_rsa_keypair()

    # Define API URL for fetching images
    api_url = f'http://cryptic-cloud.vercel.app/image-upload/apiGET-Image/{pk}?is_encrypted={is_encrypted}'

    try:
        # Fetch the image from the API
        response = requests.get(api_url)
        print(response)
        response.raise_for_status()
        image_data = response.json()
        print(image_data)
        image_url = image_data.get('cloudflare_path', 'path/to/default_image.png')  # Fallback image URL

        # Fetch image bytes from URL
        image_bytes = requests.get(image_url).content

        # Encrypt image with steganography if requested
        if is_encrypted:
            encrypted_image_data = embed_message_in_image(image_bytes, public_key)
            # Upload the encrypted image to Cloudflare to get a URL
            encrypted_image_url = upload_image_to_cloudflare(encrypted_image_data, is_encrypted=True)

            # Hybrid encryption of image data
            iv, encrypted_file_data, tag, encrypted_aes_key, encrypted_aes_key_length = hybrid_encrypt(image_bytes, public_key)

            try:
                decrypted_image_data = hybrid_decrypt(encrypted_file_data, encrypted_aes_key, private_key, tag, iv)

                # Save the decrypted image
                with open('django-cloudflare-r2/src/utils/images/5633_decrypted.png', 'wb') as f:
                    f.write(decrypted_image_data)
                
                # Upload the decrypted image to Cloudflare
                upload_image_to_cloudflare(decrypted_image_data, is_encrypted=True)

                print("Decrypted image saved and uploaded.")
            except ValueError as e:
                print(f"Error decrypting the image: {e}")
                return render(request, 'Frontend/error.html', {'error': 'Error decrypting the image'})

        else:
            encrypted_image_url = image_url

    except requests.RequestException as e:
        print(f"Error fetching image URL: {e}")
        encrypted_image_url = 'path/to/default_image.png'  # Fallback if API call fails

    # Pass the generated keys and image URL to the template context
    context = {
        'public_key': public_key,
        'private_key': private_key,
        'image_url': encrypted_image_url,
    }

    return render(request, 'Frontend/display_image.html', context)


# def display_image_view(request, pk, is_encrypted=False):
#     # Generate RSA keys
#     public_key, private_key = generate_rsa_keypair()

#     # Define API URL for fetching images
#     api_url = f'http://127.0.0.1:8000/image-upload/apiGET-Image/{pk}?is_encrypted={is_encrypted}'

#     try:
#         # Fetch the image from the API
#         response = requests.get(api_url)
#         response.raise_for_status()
#         image_data = response.json()
#         image_url = image_data.get('image_url', 'path/to/default_image.png')  # Fallback image URL

#         # Encrypt image with steganography if requested
#         if is_encrypted:
#             encrypted_image_url = embed_message_in_image(image_url, public_key)
#             upload_image_to_cloudflare(encrypted_image_url, is_encrypted=True)

#             iv, encrypted_file_data, tag, encrypted_aes_key, encrypted_aes_key_length = hybrid_encrypt(open(image_url, 'rb').read(), public_key)

#             try:
#                 decrypted_image_data = hybrid_decrypt(encrypted_file_data, encrypted_aes_key, private_key, tag, iv)

#                 with open('django-cloudflare-r2/src/utils/images/5633_decrypted.png', 'wb') as f:
#                     val = f.write(decrypted_image_data)
#                     upload_image_to_cloudflare(val, is_encrypted=True)
#                 print("Decrypted image saved.")
#             except ValueError as e:
#                 print(f"Error decrypting the image: {e}")
#                 exit(1)

#         else:
#             encrypted_image_url = image_url

#     except requests.RequestException as e:
#         print(f"Error fetching image URL: {e}")
#         encrypted_image_url = 'path/to/default_image.png'  # Fallback if API call fails

#     # Pass the generated keys and image URL to the template context
#     context = {
#         'public_key': public_key,
#         'private_key': private_key,
#         'image_url': encrypted_image_url,
#     }

#     return render(request, 'Frontend/display_image.html', context)
