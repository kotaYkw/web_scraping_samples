import requests

url = 'http://www.webscrapingfordatascience.com/cookielogin/'

# まずPOSTリクエストを実行する
r = requests.post(url, data={'username': 'yukawa', 'password': 'pass'})

# r.headersまたはr.cookiesでCookieの値を取得
my_cookies = r.cookies
print(r.cookies)
print()
# r.cookiesはRequestCookieJarオブジェクト
my_cookies['PHPSESSID'] = r.cookies.get('PHPSESSID')
print(my_cookies)
print()

# 秘密のページへのGETリクエスト
r = requests.get(url + 'secret.php', cookies=my_cookies)
print(r.text)
print()