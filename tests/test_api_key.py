import requests 

url = "http://127.0.0.1:5000/books/"
api_key = "1PtgnPmS.5D5gigDEYQVpkwinZEhZSefb9mywpANm"
api_key2 = "OsoBPzgT.0GvStzbSV2YJaHzLsHBIuPqmDREhvZtd"

print('From api 1')
# Add the API key to the Authorization header
headers = {
    "Authorization": f"Api-Key {api_key}"
}
# Make the request
response = requests.get(url, headers=headers)

# Print the response
print(response.json())

print('From api 2')
# Add the API key to the Authorization header
headers = {
    "Authorization": f"Api-Key {api_key2}"
}
# Make the request
response = requests.get(url, headers=headers)

# Print the response
print(response.json())

# payload = {
#     "title": "Test book",
#     "author": "Gabriel ludel",
#     "published_date": "1998-07-14",
#     "isbn": "1234567890",
# }
# response = requests.post(url, headers=headers, json=payload)
# print(response.json())
