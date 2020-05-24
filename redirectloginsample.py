import requests

url = 'http://www.webscrapingfordatascience.com/redirlogin/'

# まずPOSTリクエストを実行する
r = requests.post(url, data={'username': 'yukawa', 'password': 'pass'}, 
	allow_redirects=False)

# r.headersまたはr.cookiesでCookieの値を取得
print(r.cookies)
my_cookies = r.cookies
# 秘密のページへのGETリクエスト
r = requests.get(url + 'secret.php', cookies=my_cookies)
print(r.text)
