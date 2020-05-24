'''
https://github.com/内の指定したusernameの
プログラミング言語とそのリポジトリ、スター数のリストを取得する。
'''

import requests
import re
from bs4 import BeautifulSoup

session = requests.Session()

url = 'https://github.com/{}'
# 企業
#username = 'google'
# 一般ユーザー
username = 'Macuyiko'

r = session.get(url.format(username), params={'page' : 1, 'tab' : 'repositories'})
html_soup = BeautifulSoup(r.text, 'html.parser')

is_normal_user = False
repos_element = html_soup.find(class_='repo-list')
if not repos_element:
	is_normal_user = True
	repos_element = html_soup.find(id='user-repositories-list')

repos = repos_element.find_all('li')
for repo in repos:
	name = repo.find('h3').find('a').get_text(strip=True)
	language = repo.find(attrs={'itemprop' : 'programmingLanguage'})
	language = language.get_text(strip=True) if language else 'unknown'
	stars = repo.find('a', attrs={'href' : re.compile('\/stargazers')})
	stars = int(stars.get_text(strip=True).replace(',', '')) if stars else 0
	print(name, language, stars)
