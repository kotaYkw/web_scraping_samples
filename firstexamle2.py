import requests

url = 'http://www.webscrapingfordatascience.com/paramhttp/'
r = requests.get(url)
print(r.text)

print('=======================')

url = 'http://www.webscrapingfordatascience.com/paramhttp/?query=this is test'
r = requests.get(url)
print(r.request.url)
print(r.text)

print('=======================')

url = 'http://www.webscrapingfordatascience.com/paramhttp/'
parameters = {
	'query': 'a query with /, space and ?&'
}
r = requests.get(url, params=parameters)
print(r.url)
print(r.text)