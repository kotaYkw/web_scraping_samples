import requests

url = 'http://www.webscrapingfordatascience.com/postform3/'

formdata = {
	'name': 'yukawa',
	'gender': 'M',
	'pizza': 'like',
	'haircolor': 'brown',
	'comments': '',
	'protection': '6c841236602cb1d4b0040fb5aee56b41'
}

r = requests.post(url, data=formdata)
print(r.text)
# 毎回変更されるprotectionの隠しフォームの値を正しく入れないとタイムアウトになる