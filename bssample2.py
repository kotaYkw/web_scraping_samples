import requests
from bs4 import BeautifulSoup

url = 'https://en.wikipedia.org/w/index.php?title=List_of_Game_og_Thrones_episodes&oldid=802553687'
r = requests.get(url)
html_contents = r.text
html_soup = BeautifulSoup(html_contents, 'html.parser')

# 最初の<h1>タグを検索する
first_h1 = html_soup.find('h1')
print(first_h1.name)
print(first_h1.contents)
print(str(first_h1))
print(first_h1.text)
print(first_h1.get_text())
print(first_h1.attrs)
print(first_h1.attrs['id'])
print(first_h1['id'])
print(first_h1.get('id'))

print('----------CITATION----------')
cites = html_soup.find_all('cite', class_='citation', limit=5)
for citation in cites:
	print(citation.get_text())
	link = citation.find('a')
	print(link.get('href'))
	print()

	
