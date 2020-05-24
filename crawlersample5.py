import requests
import records
import re
import os, os.path
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag
from sqlalchemy.exc import IntegrityError

db = records.Database('sqlite:///wikipediaAll.db')

# クロースしたページとこれからクロールするページをテーブルに記録する
db.query('''CREATE TABLE IF NOT EXISTS pages (
	        url text PRIMARY KEY,
	        created_at datetime,
	        html_file text NULL,
	        visited_at datetime NULL)''')
# このテーブルに<a>タグに記録する
db.query('''CREATE TABLE IF NOT EXISTS links (
	        url text, link_url text,
	        PRIMARY KEY (url, link_url))''')
# このテーブルに<img>タグに記録する
db.query('''CREATE TABLE IF NOT EXISTS images (
	        url text, img_url text, img_file text,
	        PRIMARY KEY (url, img_url))''')

base_url = 'https://en.wikipedia.org/wiki/'
file_store = 'downloads'
if not os.path.exists(file_store):
	os.makedirs(file_store)

def url_to_file_name(url):
	url = str(url).strip().replace(' ', '_')
	return re.sub(r'(?u)[^-\w.]', '', url)

def download(url, filename):
	r = requests.get(url, stream=True)
	with open(os.path.join(file_store, filename), 'wb') as the_image:
		for byte_chunk in r.iter_content(chunk_size=4096*4):
			the_image.write(byte_chunk)

def store_page(url):
	try:
		db.query('''INSERT INTO pages (url, created_at)
			        VALUES (:url, CURRENT_TIMESTAMP)''', url=url)
	except IntegrityError as ie:
		# このページはすでに存在する
		pass

def store_link(url, link_url):
	try:
		db.query('''INSERT INTO links (url, link_url)
			        VALUES (:url, :link_url)''', url=url, link_url=link_url)
	except IntegrityError as ie:
		# このリンクはすでに存在する
		pass

def store_image(url, img_url, img_file):
	try:
		db.query('''INSERT INTO images (url, img_url, img_file)
			        VALUES (:url, :img_url, :img_file)''', 
			        url=url, img_url=img_url, img_file=img_file)
	except IntegrityError as ie:
		pass

def set_visited(url, html_file):
	db.query('''UPDATE pages 
		        SET visited_at=CURRENT_TIMESTAMP,
		            html_file=:html_file
		        WHERE url=:url''', 
		        url=url, html_file=html_file)

def get_random_unvisited_page():
	link = db.query('''SELECT * FROM pages
		               WHERE visited_at IS NULL
		               ORDER BY RANDOM() LIMIT 1''').first()
	return NOne if link is None else link.url

def should_visit(link_url):
	link_url = urldefrag(link_url)[0]
	if not link_url.startswith(base_url):
		return None
	return link_url

def visit(url):
	print('Now visiting:', url)
	html = requests.get(url).text
	html_soup = BeautifulSoup(html, 'html.parser')
	# <a>タグのリンクを保存
	for link in html_soup.find_all("a"):
		link_url = link.get('href')
		if link_url is None:
			# hrefがないのでスキップする
			continue
		link_url = urljoin(base_url, link_url)
		store_link(url, link_url)
		full_url = should_visit(link_url)
		if full_url:
			# クローリングのキュー
			store_page(full_url)
	# imgのsrcに指定されたファイルを保存する
	for img in html_soup.find_all("img"):
		img_url = img.get('src')
		if img_url is None:
			continue
		img_url = urljoin(base_url, img_url)
		filename = url_to_file_name(img_url)
		filename = filename.split('.')[-3:]
		filename = '.'.join(filename)
		if '.png' in filename:
			print(' image:',filename)
			download(img_url, filename)
			store_image(url, img_url, filename)
	# HTMLコンテンツを保存
	filename = url_to_file_name(url) + '.html'
	filename = os.path.join(file_store, filename)
	print(' html:', filename)
	with open(filename, 'w', encoding='utf-8') as the_html:
		the_html.write(html)
	set_visited(url, filename)

store_page(base_url)
url_to_visit = get_random_unvisited_page()
while url_to_visit is not None:
	visit(url_to_visit)
	url_to_visit = get_random_unvisited_page()
