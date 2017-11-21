from newspaper import Article
import aylien_news_api
from aylien_news_api.rest import ApiException
import pprint
import geograpy
import pycountry
from geograpy import places
from collections import Counter
import json

import nltk
from nltk.corpus import stopwords
from nltk.tag import pos_tag

stop_words = set(stopwords.words('english'))
additional_stop_words = ["The", "Read", "More", "(CNN)", "CNN", "Among", "Story", "said", "review", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday", "must", "proposed", "according", "know", "new"]

# Configure API key authorization: app_id
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = '50b90058'
# Configure API key authorization: app_key
aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = '8403356a759375e9093e204457f77b94'

# create an instance of the API class
api_instance = aylien_news_api.DefaultApi()

# Takes in a URL
# returns hte article title, some keywords, and a summary
def extract_article_features(url):
    article = Article(url, language='en')
    article.download()
    article.parse()
    article.nlp()

    return (article.text, article.publish_date, article.title)

def cleanWord(word):
    w = word.replace(".", "")
    w = w.replace("\"", "")
    w = w.replace("'s", "")
    w = w.replace(":", "")
    w = w.replace(";", "")

    return w

def extract_keywords(article):
    words = article.split()
    new_words = []
    for w in words:
        new_word = w.encode('utf-8')
        new_word = cleanWord(new_word)
        new_words.append(new_word)

    words = new_words
    words = map(str, words)

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

def searchForCountries(text):
    one_word_countries = {
      "Saudi" : "Saudi Arabia",
      "Korea": "South Korea",
      "Emirates" : "United Arab Emirates",
      "Britian" : "Great Britain"
    }

    countries = dict()
    words = text.split()
    for word in words:
        if word in one_word_countries.keys():
            if countries.get(word) is None:
                countries[word] = 0
            else:
                countries[word] += 1

    c = countries.keys()
    toreturn = []

    for country in c:
        toreturn.append((one_word_countries.get(country), 1))

    return toreturn

# Takes in keywords and location
# returns list of related articles
def get_related_stories(location, url, t, d, title):

    opts = {
      'language': ['en'],
      'published_at_start': 'NOW-7DAYS',
      'published_at_end': 'NOW',
      'source_scopes_country': [location],
      'story_url': url
    }

    try:
        # List stories
        api_response = api_instance.list_related_stories(**opts)
        stories = []

        for story in api_response.related_stories:

          locations = story.source.locations

          np = {
            "name": story.source.name,
            "location": "" if len(locations) == 0 else pycountry.countries.get(alpha_2=locations[0].country).name
          }

          article = {
            "headline": story.title,
            "location": "" if len(locations) == 0 else pycountry.countries.get(alpha_2=locations[0].country).name,
            "link": story.links.permalink,
            "date": "" if d is None else str(d)

          }

          obj = {
            "article": article,
            "newspaper": np
          }

          stories.append(obj)
        return stories
    except ApiException as e:
        print("Exception when calling DefaultApi->list_stories: %s\n" % e)

def get_locations(url):
    org_text, org_date, title = extract_article_features(url)
    text = title + " " + org_text

    better_keywords = extract_keywords(text)

    countries_output = extract_location_from_text(text)

    countries = []

    oneword = searchForCountries(text)

    if len(oneword) > 0:
        countries_output += oneword

    for country in countries_output:
        isocode = pycountry.countries.get(name=country[0]).alpha_2
        countries.append(isocode)

    unique_countries = []
    for i in countries:
      if i not in unique_countries:
          unique_countries.append(i)

    length = len(better_keywords)
    news_keyword_string = ""
    google_keyword_string = ""

    for i in range(length):
        k = better_keywords[i]
        news_keyword_string += k
        news_keyword_string += "%20"
        google_keyword_string += k
        google_keyword_string += "+"

    news_keyword_string = news_keyword_string[:-3]
    google_keyword_string = google_keyword_string[:-1]

    json_obj = {
        "google_news_url":"https://news.google.com/news/search/section/q/" + news_keyword_string,
        "google_url":"https://google.com/search?q=" + google_keyword_string,
        "keywords": better_keywords,
        "locations": unique_countries,
        "related_articles": []
    }

    return json_obj

def get_articles(url, country):
    org_text, org_date, title = extract_article_features(url)
    related_article_arr = get_related_stories(country, url, org_text, org_date, title)

    json_obj = {
        "related_articles": related_article_arr,
    }

    return json_obj
