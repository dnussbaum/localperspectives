from newspaper import Article

url = 'http://www.cnn.com/2017/10/25/politics/north-korea-us-hydrogen-bomb-threat/index.html'
article = Article(url, language='en')
article.download()
article.parse()
print(article.authors)
print(article.publish_date)
print(article.text)
