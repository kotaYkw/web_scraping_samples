import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

url = 'https://www.imdb.com/title/tt0944947/episodes'

episodes = []
ratings = []

# シーズン1~8までループ
for season in range(1, 9):
	r = requests.get(url, params={'season' : season})
	soup = BeautifulSoup(r.text, 'html.parser')
	listing = soup.find('div', class_='eplist')
	for epnr, div in enumerate(listing.find_all('div', recursive=False)):
		episode = "{}.{}".format(season, epnr+1)
		rating_el = div.find(class_='ipl-rating-star__rating')
		rating = float(rating_el.get_text(strip=True))
		print('Episode: ', episode, '-- rating: ', rating)
		episodes.append(episode)
		ratings.append(rating)

episodes = ['S' + e.split('.')[0] if int(e.split('.')[1]) == 1 else '' for e in episodes]

plt.figure()
positions = [a*2 for a in range(len(ratings))]
plt.bar(positions, ratings, align='center')
plt.xticks(positions, episodes)
plt.show()
