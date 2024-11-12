from PIL import Image
import requests
from io import BytesIO

# Your API endpoint for the image upload
url = "http://127.0.0.1:8000/image-upload/apiPOST-Image/"

# The image file path you want to upload
image_path = "E:/Python/Django Projects/Django Projects/Project 19/django-cloudflare-r2/src/images/5633.jpg"

# Form data payload
data = {
    "title": "Great Anime",
    "content": "Awesome Anime",
    "author": "Divyanshu Singh",
}

# Open and process the image with Pillow
with open(image_path, "rb") as image_file:
    image = Image.open(image_file)
    
    # Optional: You can resize, compress, or convert the image
    image = image.convert("RGB")  # Ensures image is in a compatible format
    
    # Save the processed image into a bytes buffer
    img_byte_arr = BytesIO()
    image.save(img_byte_arr, format="JPEG")  # You can change the format if necessary
    img_byte_arr.seek(0)  # Go to the start of the BytesIO buffer

    # Send the POST request with the image file and data
    files = {"image_file": ("image.jpg", img_byte_arr, "image/jpeg")}  # Update MIME type if needed
    response = requests.post(url, data=data, files=files)

# Check the response status and content
print("Status Code:", response.status_code)
print("Response Content:", response.json())
