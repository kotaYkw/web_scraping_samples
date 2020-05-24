import requests
from bs4 import BeautifulSoup

url ='http://www.webscrapingfordatascience.com/simplejavascript/'

r = requests.get(url)
html_soup = BeautifulSoup(r.text, 'html.parser')

# ここにタグは含まれていない
ul_tag = html_soup.find('ul')
print(ul_tag)

# JavaScriptのこーどを表示する
script_tag = html_soup.find('script', attrs={'src': None})
print(script_tag)

url = 'http://www.webscrapingfordatascience.com/simplejavascript/quotes.php'

# Cookieの値は文字列で指定する必要がある
# Cookieを設定しないと、ブラウザから見ていないとバレてアクセスを拒否される
r = requests.get(url, cookies={'jsenabled': '1'})
print(r.json())
