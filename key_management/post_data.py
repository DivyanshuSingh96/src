import requests
import json

# API endpoint
# url = 'http://127.0.0.1:8000/api/apiEncrypt/'

# # Data to send in the POST request
# data = {
#     'image_file': 'https://64646f9b5ea8571f2ced7edbd8036eb4.r2.cloudflarestorage.com/csp/media/images/0/90d977e9-a07e-11ef-8c65-d843aeb854c8.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ec9cfb9b2a842510c277484e30881b81%2F20241111%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241111T224454Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=0d2eb72c201d5a97fc98b3cb31438101bc4d9c819d892ff9fda88448e074113f',  # Replace with actual image URL
#     'public_key': 'your-public-key-here',
#     'private_key': 'your-private-key-here',
#     'title': 'Encrypted Image Test',
#     'author': 'John Doe',
#     'message': 'This is a test message for the encrypted image.',
#     'is_encrypted': True
# }

# # Send POST request to the API
# response = requests.post(url, json=data)

# # Check the response
# if response.status_code == 200:
#     print("Successfully uploaded:", response.json())
# else:
#     print("Error:", response.status_code, response.text)

def save_keys_to_kv(kv_data):
    kv_api = "http://127.0.0.1:8000/api/apiPost"

    # Headers for the request
    headers = {
        'Content-Type': 'application/json'
    }

    # Sending POST request
    response = requests.post(kv_api, headers=headers, json=kv_data)

    # Print the response
    if response.status_code == 200:
        print("Success:", response.json())
    else:
        print("Failed:", response.status_code, response.text)

def final_api():
    url = 'http://127.0.0.1:8000/api/apiEncrypt'  # Replace with your actual API endpoint

    # Data to be sent in the POST request
    data = {
        'title': 'Encrypted Image Anime',
        'author': 'John Doe',
        'image_url': 'https://64646f9b5ea8571f2ced7edbd8036eb4.r2.cloudflarestorage.com/csp/media/images/0/7cc327da-a0b9-11ef-a973-d843aeb854c8.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ec9cfb9b2a842510c277484e30881b81%2F20241112%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20241112T054641Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Signature=3dbc77115aabeb9f9555264ea37fe1d2c29fa09883aa54bc988415f2f1da40ea',  # Replace with actual image URL
        'is_encrypted': True,  # Encryption status
        'message': 'Hello World',

        'private_key': b'-----BEGIN RSA PRIVATE KEY-----\nMIIEogIBAAKCAQEAlIScHZqZlV88aZBDKA1Tqu8qXFI3r/0V11DucGvppNS6hPvS\nik091x3mrJq5qfh3TPlrwc7zWW/XtA2JX95tATB2YFXpU9sdhlDiz4E/1mWN33AE\nsgf/94xR7dk5NXJFK+SiOJAJoYByxULp3kUnumUq5dfcOWaRua/fsIi63bjLkpAM\nm6kyGsKsATKfu7sIX5K0EGxr6sfCIYSApY0ynERVMM43TvVVxHv7DJbb+NKVrQvV\nnxjWVHBe/7eUs6QWKS/zzBqAHD0YFP5AkAYQKtYdS1ZSCcbdZf1b26me2e5KlXDH\nhsL2n6bNyS5II9SRblrtyvNVHNfKrRkNA8i6NQIDAQABAoIBAD00/aXRrhP6QMp8\nksCx5VZf5IRRufOEiPjIuMuKHas5pHjj01v+A0thXkyqI3QiGwCVFky0PmQQjMP+\nhCwHXcMMtuxy24sclWlicmb0LFvuVG7OGpFIbLwXjzhHuqUFJ+6z9gr7iYyOhD45\nmmpo87uEsA4zTOY3GD1/dt+pKeHwAu5iIFFnHrwBFIbWMx33xNU0kdx4bE390Qs1\nT7CcVaTvhCy6YfjJqq1MxxP4OIOC0jG1Mx0gHbDyAcLL5GwrPOQulvrJNaAzzzql\nRG7YKwWy4twxmqbXd6rARfaBFBzMo/7wPGNaxAecBcP5eVNqFxnff/qZqGbS+Ng0\nTCbeHW0CgYEAv2MCYK0HRkQjrqE70zedj2jM3WrS8gx5j4TvmVL5BTDUFnYwsJtW\nNxkS5GOaXiC/WAoAFu5+WbWY5P5InLN/xWVM4yTZ2I7rum59v2qXMD1eozghEi+j\nSEhy7aYJjW1MEMus58xwUy4zO+tXz+HePkIqVBHvidPh5dZ5f8EFIgsCgYEAxqiU\n4MJiMA17vB4N7SrUlgsvb5HafXASSO7P7ROfomEub52nXhXeJ90l/1OttnEPw9hN\nA6kYLjmFdDdZddpnA40Av+do1rPo0NrnJPzIy/yJwVd+ssqfMaXW7sj3I7pn2cbX\n9wKtya9EwLfKHd0s3iTlM6suDtKtT+KG1DbFfL8CgYA6b1aIggwYjjF+3kfP48k9\nwjfa2wTxVpG/Gk21uLnDtfbrrMaNBcC7LfKwvSCi4MjLbrI8TjFR3rqCIIm3Hq9C\na/2f1N6W2nxq/dVzHm5vEi3VFAw060qlhUlh+jIsdlSlRCrU03zwSMjn4KF9HW+n\n/rfB14AVyxXMAUIzmZGhpQKBgB+Je7kCotvGCDKhAsz306/OLsWjffAT7pMtdkzI\npLr+eoS1nnBNQGtLrFCQVC92W25X1EIUggY0k38TmlwfQ+NIayoL7pTHEtq1JaS1\njJr1iFjtLuvrRsJ29VwLA1Dksr/b1UUdY8F01ZFSm/+JsSnC6a/+KN2pjGH2MDlY\nSJm5AoGAY1QOAtlVXiJT4qKf7et3urT5bG6zZCVfoPjmPW3zs+YArinkb15dzRm/\nxtvu5cAiQHpgcsXweWWMJzSxex3bd8y/iv3N4JuZQoaopkvvfoDFtQtz89DzDb9/\nb1CwQkkXMdvRChZVpQhTRpGsEhTMeg98uoQ2uUs9W+K7w7DOncU=\n-----END RSA PRIVATE KEY-----',

        'public_key': b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAlIScHZqZlV88aZBDKA1T\nqu8qXFI3r/0V11DucGvppNS6hPvSik091x3mrJq5qfh3TPlrwc7zWW/XtA2JX95t\nATB2YFXpU9sdhlDiz4E/1mWN33AEsgf/94xR7dk5NXJFK+SiOJAJoYByxULp3kUn\numUq5dfcOWaRua/fsIi63bjLkpAMm6kyGsKsATKfu7sIX5K0EGxr6sfCIYSApY0y\nnERVMM43TvVVxHv7DJbb+NKVrQvVnxjWVHBe/7eUs6QWKS/zzBqAHD0YFP5AkAYQ\nKtYdS1ZSCcbdZf1b26me2e5KlXDHhsL2n6bNyS5II9SRblrtyvNVHNfKrRkNA8i6\nNQIDAQAB\n-----END PUBLIC KEY-----',
    }

    # Make the POST request to the API
    response = requests.post(url, data=data)
    print(response)

    # Print the status code and response content
    print(f"Status Code: {response.status_code}")
    # print(f"Response Text: {response.text}")

final_api()
