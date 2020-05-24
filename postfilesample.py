import requests

url = 'http://www.webscrapingfordatascience.com/postform2/'

formdata = {'name': 'yukawa'}
filedata = {'profile_picture': open('me.jpg', 'rb')}
r = requests.post(url, data=formdata, files=filedata)
print(r.text)