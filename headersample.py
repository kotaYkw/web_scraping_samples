import requests

url = 'http://www.webscrapingfordatascience.com/usercheck/'

my_headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}
r = requests.get(url, headers=my_headers)

print(r.text)
print(r.request.headers)
