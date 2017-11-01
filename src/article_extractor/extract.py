from newspaper import Article
import aylien_news_api
from aylien_news_api.rest import ApiException
import pprint
import geograpy
from geograpy import places
from collections import Counter

import nltk
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
pp = pprint.PrettyPrinter(indent=4)

# Takes in a URL
# returns hte article title, some keywords, and a summary
def extract_article_features(url="http://www.cnn.com/2017/10/25/politics/north-korea-us-hydrogen-bomb-threat/index.html"):
    article = Article(url, language='en')
    article.download()
    article.parse()
    article.nlp()

    return (article.title, article.keywords, article.summary, article.text)


def extract_key_words(article):
    words = article.split(" ")
    words = map(str, words)
    lower_case = map(str.lower, words)
    keywords = Counter(lower_case).most_common()

    good_keywords = []
    for w in keywords:
        word = w[0]
        if word not in stop_words:
            good_keywords.append(word)

    return good_keywords[0:10]

def extract_location_from_text(text):
    #https://stackoverflow.com/questions/40517720/python-geograpy-unable-to-run-demo
    places = geograpy.get_place_context(text=text)
    return places.city_mentions

# Takes in keywords and location
# returns list of related articles
def get_related_stories(headline, text, location):
    # Configure API key authorization: app_id
    aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-ID'] = '05d67d01'
    # Configure API key authorization: app_key
    aylien_news_api.configuration.api_key['X-AYLIEN-NewsAPI-Application-Key'] = 'a2a649ad010cbfd18ec4d17271d5a247'

    # create an instance of the API class
    api_instance = aylien_news_api.DefaultApi()

    opts = {
      'sort_by': 'social_shares_count.facebook',
      'language': ['en'],
      'published_at_start': 'NOW-7DAYS',
      'published_at_end': 'NOW',
      'source_scopes_city': location,
      'story_body': text,
      'story_title': headline
    }

    try:
        # List stories
        api_response = api_instance.list_stories(**opts)
        stories = []
        for story in api_response.stories:
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

title, keywords, summary, text = extract_article_features("http://www.businessinsider.com/rahm-emanuel-on-chicago-and-health-tech-2017-9")
better_keywords = extract_key_words(text)

print(better_keywords)
print(keywords)

cities_output = extract_location_from_text(text)
cities = []
for city in cities_output:
    cities.append(city[0])
#print keywords, cities

print(get_related_stories(title, text, [cities[0]]))
