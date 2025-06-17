import requests

message = {
    "content": "Hello from the other Python script!"
}

response = requests.post("http://127.0.0.1:5000/notify", json=message)

print(response.json())