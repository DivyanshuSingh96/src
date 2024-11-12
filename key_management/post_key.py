import requests
from decouple import config as env_config

url = "http://127.0.0.1:8000/api/apiPost"
# url = "https://cipher-cloud.divyanshu-singh.workers.dev"

public_key = "vlkajlksjfdlkfldsfsksadjflksajkfd0"
private_key = "ksahfkjsdhkjfsdfslakjdhfkjasdhfkjhasdakjf"

message = "helasdfsdflo"
image_url = "https://64646f9b5ea8571f2ced7edbd8036eb4.r2.cloudflarestorage.com/csp/media/images/0/7cc327da-a0b9-11ef-a973-d843aeb854c8.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ec9cfb9b2a842510c277484e30881b81%2F20241112%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241112T054641Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=3dbc77115aabeb9f9555264ea37fe1d2c29fa09883aa54bc988415f2f1da40ea"

kv_data = {
    "key": f"({public_key}, {private_key})",
    "keyId": f"({message}, {image_url})",  # placeholder until image URL is fetched
}

headers = {
    "Content-Type": "multipart/form-data",
    # "Authorization": f"Bearer {env_config('CLOUDFLARE_API_KEY')}",  # If your Cloudflare Worker requires authorization
}

response = requests.post(url, json=[kv_data], headers=headers)
print(response.status_code)