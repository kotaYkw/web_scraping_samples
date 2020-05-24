'''
http://books.toscrape.com/から書籍ごとに
タイトル、表紙画像、価格、在庫の有無、評価、商品の説明、商品その他の情報
を取得する
'''

import requests
import dataset
import re
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

db = dataset.connect('sqlite:///books.db')
base_url = 'http://books.toscrape.com/'

# すべての本をスクレイピングし、URL、タイムスタンプを保存する
def scrape_books(html_soup, url):
	for book in html_soup.select('article.product_pod'):
		# とりあえず書籍のURLのみ保存する
		book_url = book.find('h3').find('a').get('href')
		book_url = urljoin(url, book_url)
		path = urlparse(book_url).path
		book_id = path.split('/')[2]
		# upsertはまず更新を試行してから挿入を実行する
		db['books'].upsert({'book_id' : book_id,
			                'last_seen' : datetime.now()
			                }, ['book_id'])

# それぞれの本をスクレイピングする
def scrape_book(html_soup, book_id):
	main = html_soup.find(class_='product_main')
	book = {}
	book['book_id'] = book_id
	book['title'] = main.find('h1').get_text(strip=True)
	book['price'] = main.find(class_='price_color').get_text(strip=True)
	book['stock'] = main.find(class_='availability').get_text(strip=True)
	book['rating'] = ' '.join(main.find(class_='star-rating').get('class')).replace('star-rating', '').strip()
	book['img'] = html_soup.find(class_='thumbnail').find('img').get('src')
	desc = html_soup.find(id='product_description')
	book['description'] = ''
	if desc:
		book['description'] = desc.find_next_sibling('p').get_text(strip=True)
	book_product_table = html_soup.find(text='Product Information').find_next('table')
	for row in book_product_table.find_all('tr'):
		header = row.find('th').get_text(strip=True)
		# ヘッダーをカラムとして使うのでクリーンにして
		# SGLiteが受け付けられるようにする
		header = re.sub('[^a-zA-Z]+', '_', header)
		value = row.find('td').get_text(strip=True)
		book[header.lower()] = value
	db['book_info'].upsert(book, ['book_id'])

# カタログ内のページをスクレイピングする
url = base_url
inp = input('Do you wish to re-scrape the catalogue (y/n)? ')
while True and inp == 'y':
	print('Now scraping page: ', url)
	r = requests.get(url)
	html_soup = BeautifulSoup(r.text, 'html.parser')
	scrape_books(html_soup, url)
	# 次のページはある？
	next_a = html_soup.select('li.next > a')
	if not next_a or not next_a[0].get('href'):
		break
	url = urljoin(url, next_a[0].get('href'))

# 古いものから順に、書籍ごとにスクレイピングする
books = db['books'].find(order_by=['last_seen'])
for book in books:
	book_id = book['book_id']
	book_url = base_url + 'catalogue/{}'.format(book_id)
	print('Now scraping book: ', book_url)
	r = requests.get(book_url)
	r.encoding = 'utf-8'
	html_soup = BeautifulSoup(r.text, 'html.parser')
	scrape_book(html_soup, book_id)
	# 最後に見たタイムスタンプを更新する
	db['books'].upsert({'book_id' : book_id,
		                'last_seen' : datetime.now()}, 
		                ['book_id'])
