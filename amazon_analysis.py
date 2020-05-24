from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from nltk import tokenize
import dataset
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')

db = dataset.connect('sqlite:///reviews.db')
reviews = db['reviews'].all()

analyzer = SentimentIntensityAnalyzer()

sentiment_by_stars = [[] for r in range(1,6)]

for review in reviews:
    full_review = review['title'] + '. ' + review['review']
    sentence_list = tokenize.sent_tokenize(full_review)
    # 各文の累積の感情スコア
    cumulative_sentiment = 0.0
    # 一文ずつスコアを計算する
    for sentence in sentence_list:
        # 'neg'(否定的)、'neu'（中立的）、'pos'（肯定的）、'compound'（全体）のスコアが計算される
        vs = analyzer.polarity_scores(sentence)
        cumulative_sentiment += vs["compound"]
    average_score = cumulative_sentiment / len(sentence_list)
    # レビューの星の数（１～５）ごとに感情スコアを登録する
    sentiment_by_stars[int(review['rating'])-1].append(average_score)

plt.violinplot(sentiment_by_stars,
               range(1,6),
               vert=False, widths=0.9,
               showmeans=False, showextrema=True, showmedians=True,
               bw_method='silverman')
plt.axvline(x=0, linewidth=1, color='black')
#plt.show()
plt.savefig('amazon_sentiment_analysis.png')