import requests

url = 'http://www.webscrapingfordatascience.com/basichttp/'
r = requests.get(url)

# サーバーから返されたステータスコード
print(r.status_code)
# テキストのステータスメッセージ
print(r.reason)
# HTTPレスポンスヘッダー
print(r.headers)
# リクエスト情報はr.requestにPythonオブジェクトとして保存される
print(r.request)
# HTTPリクエストヘッダー
print(r.request.headers)
# HTTPレスポンスのコンテンツ
print(r.text)