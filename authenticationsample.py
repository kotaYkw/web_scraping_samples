import requests

url = 'http://www.webscrapingfordatascience.com/authentication/'
r = requests.get(url)
print(r.text)
print(r.headers)
print(r.request.headers)
print()

r = requests.get(url, auth=('yukawa', 'my_pass'))
print(r.text)
print(r.headers)
print(r.request.headers)
print()