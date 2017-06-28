import requests

url = "http://127.0.0.1:8000/api/talent/record/"

payload = "{}"
headers = {
    'content-type': "application/json",
    'authorization': "jwt eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3Q0IiwidXNlcl9pZCI6NSwiZW1haWwiOiJzNHNhaWYuMTIxQGdtYWlsLmNvbSIsImV4cCI6MTUyNDQzNzc0NH0.xav8m6foOrogCg8irIWsoyNZ6qSH-BbUcjUM-Lt3-WA",
    'cache-control': "no-cache",
    'postman-token': "73ccc0d5-b4d8-c890-94d2-d63cbd4c1397"
    }

response = requests.request("GET", url, data=payload, headers=headers)

print(response.text)
