import requests

url = 'http://www.webscrapingfordatascience.com/cookielogin/secret.php'

r = requests.get(url)
print(r.text)
print()

# ユーザー名はyukawa、パスワードはpassでブラウザからログインし閉じないで実行
my_cookies = {'PHPSESSID': 'ersi0tehmpbbe4tepapgktsns5'}
r = requests.get(url, cookies=my_cookies)
print(r.text)