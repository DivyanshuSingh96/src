import requests

# Your API endpoint for the image fetch
# url = "http://127.0.0.1:8000/image-upload/apiGET-Image/"
url = "http://127.0.0.1:8000/image-upload/apiGET-Image/41?is_encrypted=False"

# Send a GET request to fetch image data
response = requests.get(url)

# Check the response status and content
if response.status_code == 200:
    print("Response Data:", response.json())
else:
    print("Failed to retrieve data. Status Code:", response.status_code)
