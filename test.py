import requests

r = requests.post('http://127.0.0.1:5000/getItems', json={"username": "bebriki", "password": "1234", "page": 1, "owner": "bebriki", })
print(r.json())