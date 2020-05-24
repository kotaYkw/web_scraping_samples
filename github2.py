import requests
from bs4 import BeautifulSoup

session = requests.Session()

url = 'https://github.com/{}'
username = 'Macuyiko'

# ログインページに移動
r = session.get(url.format('login'))
html_soup = BeautifulSoup(r.text, 'html.parser')
data = {}
for form in html_soup.find_all('form'):
	# 非表示のフォームフィールドを取り出す
	for inp in form.select('input[type=hidden]'):
		data[inp.get('name')] = inp.get('value')

# ログイン情報を設定する
data.update({'login':'ykwkota', 'password':'1997PyPro'})

print('Going to login with the following POST data:')
print(data)

if input('Do you want to login (y/n): ') == 'y':
	r = session.get(url.format(username))
	html_soup = BeautifulSoup(r.text, 'html.parser')
	user_info = html_soup.find(class_='vcard-details')
	print(user_info.text)
