import requests

url = 'http://www.webscrapingfordatascience.com/redirect/'
r = requests.get(url)
print(r.text)
print(r.headers)
print()

r = requests.get(url, allow_redirects=False)
print(r.text)
print(r.headers)
print(r.headers.get('SECRET-CODE'))