'''
https://news.ycombinator.com/news
のトップページをスクレイピングし、辞書オブジェクトとして保存し、シンプルな構造で把握できるようにする。
'''

import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = 'https://news.ycombinator.com/news'

r = requests.get(url)
html_soup = BeautifulSoup(r.text, 'html.parser')
articles = []
comments_links = []

# 各ニュースは<tr>タグのclass="athing"で並んでいるので、全部取得して順番に処理
for item in html_soup.find_all('tr', class_='athing'):
	# <a>タグのリンクを取得
	item_a = item.find('a', class_='storylink')
	item_link = item_a.get('href') if item_a else None
	# <a>タグの文字（タイトル）を取得
	item_text = item_a.get_text(strip=True) if item_a else None
	# 次の<tr>タグの中の<span>タグにあるスコアを取得
	next_row = item.find_next_sibling('tr')
	item_score = next_row.find('span', class_='score')
	item_score = item_score.get_text(strip=True) if item_score else '0 points'
	# ここではregexを使って正しい要素を見つける
	# 十進数の数字+"&nbsp;"という文字列、または何かしらの文字列+"comment"という文字列+(s)で正規表現をマッチングする
	item_comments = next_row.find('a', text=re.compile('\d+(&nbsp;|\s)comment(s?)'))
	comments_link = item_comments.get('href') if item_comments else None
	comments_link = urljoin(url, comments_link)
	comments_links.append(comments_link)
	item_comments = item_comments.get_text(strip=True).replace('\xa0', ' ') if item_comments else '0 comments'
	articles.append({
		'link' : item_link,
		'title' : item_text,
		'score' : item_score,
		'comments' : item_comments
		})

for article in articles:
	print(article)
print()

all_comments = []
for link in comments_links:
	r = requests.get(link)
	html_soup = BeautifulSoup(r.text, 'html.parser')
	comment_tree = html_soup.find('table', class_='comment-tree')
	comment_list = []
	if comment_tree is None:
		all_comments.append(comment_list)
		continue
	comments = comment_tree.find_all('tr', class_='athing comtr')
	for comment in comments:
		comment = comment.find('span', class_='commtext c00')
		comment_text = comment.get_text(strip=True) if comment else None
		comment_list.append(comment_text)
	all_comments.append(comment_list)

print(all_comments)