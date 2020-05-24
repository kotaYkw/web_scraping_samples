import requests
import dataset
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag
from joblib import Parallel, delayed

db = dataset.connect('sqlite:///wikipedia_graph.db')
base_url = 'https://en.wikipedia.org/wiki/'

# pagesテーブルにwebページのURLとタイトルを保存する
def store_page(url, title):
    print('Visited page:', url)
    print('       title:', title)
    db['pages'].upsert({'url': url, 'title': title}, ['url'])

# linksテーブルにリンク元ページとリンク先ページのURLを保存する
# リンク先をまとめてupsertして高速化している
def store_links(from_url, links):
    db.begin()
    for to_url in links:
        db['links'].upsert({'from_url': from_url, 'to_url': to_url}, ['from_url', 'to_url'])
    db.commit()

# pagesテーブルに存在しない（まだ訪問していない）ページのリストをランダムに並べて返す（最大１０件）
def get_random_unvisited_pages(amount=10):
    result = db.query('''SELECT * FROM links
        WHERE to_url NOT IN (SELECT url FROM pages)
        ORDER BY RANDOM() LIMIT {}'''.format(amount))
    return [r['to_url'] for r in result]

# リンクがクローリング対象（https://en.wikipedia.org/wiki/のページか、トップページなどの情報がなくよくリンクが貼ってあるページどうか）かを判定する
def should_visit(base_url, url):
    if url is None:
        return None
    full_url = urljoin(base_url, url)
    full_url = urldefrag(full_url)[0]
    if not full_url.startswith(base_url):
        # This is an external URL
        return None
    ignore = ['Wikipedia:', 'Template:', 'File:', 'Talk:', 'Special:',
              'Template talk:', 'Portal:', 'Help:', 'Category:', 'index.php']
    if any([i in full_url for i in ignore]):
        # This is a page to be ignored
        return None
    return full_url

# スクレイピングしてURL、タイトル、リンク先URLのリストを取得する
def get_title_and_links(base_url, url):
    html = requests.get(url).text
    html_soup = BeautifulSoup(html, 'html.parser')
    page_title = html_soup.find(id='firstHeading')
    page_title = page_title.text if page_title else ''
    links = []
    for link in html_soup.find_all("a"):
        link_url = should_visit(base_url, link.get('href'))
        if link_url:
            links.append(link_url)
    return url, page_title, links

if __name__ == '__main__':
    urls_to_visit = [base_url]
    while urls_to_visit:
        # joblibライブラリで並列処理（マルチスレッド）する
        # 負荷がかかりすぎないように、job数を5にする
        # マルチスレッドはマルチプロセスよりGILの影響で遅い
        scraped_results = Parallel(n_jobs=5, backend="threading")(
            delayed(get_title_and_links)(base_url, url) for url in urls_to_visit
        )
        # 保存処理は並列書き込みに適していないので別でやる
        for url, page_title, links in scraped_results:
            store_page(url, page_title)
            store_links(url, links)
        urls_to_visit = get_random_unvisited_pages()