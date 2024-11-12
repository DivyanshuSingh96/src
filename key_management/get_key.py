import requests

url = "http://127.0.0.1:8000/api/apiGet"

key = "newgreatlife"
final_val = f"{url}/?key={key}"

request = requests.get(final_val)
print(request)