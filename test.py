import requests
url = 'http://127.0.0.1:5000/'
page = 'editItem'
data = {
    "username": "eblanus",
    "password": "hues0s",
    "name": "bebra",
    "description": None,
    "quantity": 100 
}
request = requests.post(url+page, json=data)
print(request.text)

#  curl -X POST -H "Content-Type: application/json" -d '{"username": "bok", "password": "1"}' http://127.0.0.1:5000/authUser
