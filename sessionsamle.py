import requests

url = 'http://www.webscrapingfordatascience.com/trickylogin/'

my_session = requests.Session()
# このセッション中はこのUser-Agentヘッダーを使う
my_session.headers.update({'User-Agent': 'Chrome!'})

r = my_session.get(url)
r = my_session.post(url, params={'p': 'login'}, data={'usename': 'yukawa', 'password': 'pass'})
r = my_session.get(url, params={'p': 'protected'})

print(r.request.headers)
print(r.text)
