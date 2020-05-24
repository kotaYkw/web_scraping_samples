import requests
import records
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag
from sqlalchemy.exc import IntegrityError

db = records.Database('sqlite:///wikipedia.db')

db.query('''CREATE TABLE IF NOT EXISTS pages (
	        url text PRIMARY KEY,
	        page_title text NULL,
	        created_at datetime,
	        visited_at datetime NULL)''')
db.query('''CREATE TABLE IF NOT EXISTS links (
	        url text, url_to text,
	        PRIMARY KEY (url, url_to))''')

base_url = 'https://en.wikipedia.org/wiki/'

def store_page(url):
	try:
		db.query('''INSERT INTO pages (url, created_at)
			        VALUES (:url, CURRENT_TIMESTAMP)''', url=url)
	except IntegrityError as ie:
		# このページはすでに存在する
		pass


def store_link(url, url_to):
	try:
		db.query('''INSERT INTO links (url, url_to)
			        VALUES (:url, :url_to)''', url=url, url_to=url_to)
	except IntegrityError as ie:
		# このリンクはすでに存在する
		pass

def set_visited(url):
	db.query('''UPDATE pages SET visited_at=CURRENT_TIMESTAMP
		        WHERE url=:url''', url=url)

def set_title(URL, page_title):
	db.query('''UPDATE pages SET page_title=:page_title WHERE url=:url''', 
		url=url, page_title=page_title)

def get_random_unvisited_page():
	link = db.query('''SELECT * FROM pages
		               WHERE visited_at IS NULL
		               ORDER BY RANDOM() LIMIT 1''').first()
	return NOne if link is None else link.url

def visit(url):
	print('Now visiting:', url)
	html = requests.get(url).text
	html_soup = BeautifulSoup(html, 'html.parser')
	page_title = html_soup.find(id='firstHeading')
	page_title = page_title.text if page_title else ''
	print(' page title:', page_title)
	for link in html_soup.find_all("a"):
		link_url = link.get('href')
		if link_url is None:
			# hrefがないのでスキップする
			continue
		full_url = urljoin(url, link_url)
		# フラグメント識別子の部分を削除する
		full_url = urldefrag(full_url)[0]
		if not full_url.startswith(base_url):
			# これは外部リンクなのでスキップする
			continue
		store_link(url, full_url)
		store_page(full_url)
	set_visited(url)

store_page(base_url)
url_to_visit = get_random_unvisited_page()
while url_to_visit is not None:
	visit(url_to_visit)
	url_to_visit = get_random_unvisited_page()
