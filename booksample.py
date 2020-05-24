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

db = dataset.connect('sqlite:///bookstest.db')

# それぞれの本をスクレイピングする
def scrape_book(html_soup, book_id):
	main = html_soup.find(class_='product_main')
	#print(html_soup)
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
	print(book_product_table)
	for row in book_product_table.find_all('tr'):
		header = row.find('th').get_text(strip=True)
		# ヘッダーをカラムとして使うのでクリーンにして
		# SGLiteが受け付けられるようにする
		header = re.sub('[^a-zA-Z]+', '_', header)
		value = row.find('td').get_text(strip=True)
		book[header] = value
	db['book_info'].upsert(book, ['book_id'])

# 古いものから順に、書籍ごとにスクレイピングする
books = db['books'].find(order_by=['lase_seen'])
book_id = 0
book_url = 'http://books.toscrape.com/catalogue/the-bridge-to-consciousness-im-writing-the-bridge-between-science-and-our-old-and-new-beliefs_840/index.html'
print('Now scraping book: ', book_url)
r = requests.get(book_url)
r.encoding = 'utf-8'
html_soup = BeautifulSoup(r.text, 'html.parser')
scrape_book(html_soup, book_id)
# 最後に見たタイムスタンプを更新する
db['books'].upsert({'book_id' : book_id,
	                'last_seen' : datetime.now()}, 
	                ['book_id'])
