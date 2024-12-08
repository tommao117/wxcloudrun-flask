import requests

url = "http://127.0.0.1:80/api/service"

data = {
    "FromUserName": "from",
    "ToUserName": "to",
    "Content": "笑话亚亚",
}

r = requests.post(url=url, json=data)
print(r.json())
