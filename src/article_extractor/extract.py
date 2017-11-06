from newspaper import Article
import aylien_news_api
from aylien_news_api.rest import ApiException
import pprint
import geograpy
from geograpy import places
from collections import Counter

import nltk
from nltk.corpus import stopwords
from nltk.tag import pos_tag

stop_words = set(stopwords.words('english'))
additional_stop_words = ["The", "Read", "More", "(CNN)", "CNN", "Among", "Story", "said", "review", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "must", "proposed"]

pp = pprint.PrettyPrinter(indent=4)

# Takes in a URL
# returns hte article title, some keywords, and a summary
def extract_article_features(url="http://www.cnn.com/2017/10/25/politics/north-korea-us-hydrogen-bomb-threat/index.html"):
    article = Article(url, language='en')
    article.download()
    article.parse()
    article.nlp()

    return (article.title, article.keywords, article.summary, article.text)

def cleanAritlce(article):
    a = article.replace("\u", "")
    return a

def extract_key_words(article):

    words = article.split()
    new_words = []
    for w in words:
        new_words.append(w.encode('utf-8'))

    words = new_words
    words = map(str, words)
    #words = map(stripx, words)

    #tagged = pos_tag(words)
    #propernouns = [word for word,pos in tagged if pos == 'NNP']

    keywords = Counter(words).most_common()

    good_keywords = []
    for w in keywords:
        word = w[0]
        if (word.lower() not in stop_words) and (word not in additional_stop_words):
            good_keywords.append(word)

    return good_keywords[0:10]

def extract_location_from_text(text):
    #https://stackoverflow.com/questions/40517720/python-geograpy-unable-to-run-demo
    places = geograpy.get_place_context(text=text)
    return places.country_mentions

# Takes in keywords and location
# returns list of related articles
def get_related_stories(keywords, text, location, url, headline):
    # Configure API key authorization: app_id
    aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = '05d67d01'
    # Configure API key authorization: app_key
    aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = 'a2a649ad010cbfd18ec4d17271d5a247'

    # create an instance of the API class
    api_instance = aylien_news_api.DefaultApi()

    keyword_string = ""
    length = len(keywords)
    for i in range(length):
        k = keywords[i]
        keyword_string += k
        if i < 1:
            keyword_string += " || "
        else:
            keyword_string += " || "


    keyword_string = keyword_string[:-4]
    print(keyword_string)

    opts = {
      'language': ['en'],
      'published_at_start': 'NOW-7DAYS',
      'published_at_end': 'NOW',
      'source_scopes_country': ['US'],
      'story_url': url
    }

    try:
        # List stories
        api_response = api_instance.list_related_stories(**opts)
        stories = []
        for story in api_response.related_stories:
          the_story = {
            "title": story.title,
            "url": story.links.permalink,
            "source": story.source.name,
            "locations": story.source.locations
          }
          stories.append(the_story)
        return stories
    except ApiException as e:
        print("Exception when calling DefaultApi->list_stories: %s\n" % e)

url = "https://www.japantimes.co.jp/news/2017/11/01/world/politics-diplomacy-world/trump-faults-schumer-diversity-immigration-new-york-city-attack/#.Wfp5H7b-2u4"
title, keywords, summary, text = extract_article_features(url)
better_keywords = extract_key_words(text)

countries_output = extract_location_from_text(text)
countries = []
for country in countries_output:
    countries.append(country[0])

print better_keywords, keywords, countries

print(get_related_stories(better_keywords, text, [countries[0]], url, title))
