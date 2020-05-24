import requests

url = 'http://www.webscrapingfordatascience.com/trickylogin/'

# 通常のGETリクエストをして、フォームを取得
r = requests.get(url)

# Cookiesを設定
my_cookies = r.cookies
print(my_cookies)

# リダイレクトされないようにしてPOSTする
r = requests.post(url, params={'p': 'login'}, 
	data={'username': 'yukawa', 'password': 'pass'}, 
	allow_redirects=False, 
	cookies=my_cookies)

# Cookiesを再度更新する必要がある
# PHPSESSIDの値が変更されていることに注意
my_cookies = r.cookies
print(my_cookies)

# Cookiesを使って秘密のページへのGETを実行
# Cookiesは更新されたものを使う
r = requests.get(url, params={'p': 'protected'}, cookies=my_cookies)

print(r.text)	
