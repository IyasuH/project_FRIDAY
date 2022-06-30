#!/usr/bin/python3
# for handling news using googlenews
from pygooglenews import GoogleNews

def News(command):
    if 'top' in command:
        print("Top news")
        gn = GoogleNews(lang='en', country='None')
        top = gn.top_news()
        entries = top["entries"]
    elif 'local' in command:
        print("local news")
        gn = GoogleNews(lang='en', country='Et')
        top = gn.top_news()
        entries = top["entries"]
    elif 'tech' in command:
        print("tech news")
        gn = GoogleNews(lang='en', country='None')
        tech = gn.topic_headlines('technology')
        entries = tech["entries"]
    elif 'science' in command:
        print("science news")
        gn = GoogleNews(lang='en', country='None')
        science = gn.topic_headlines('science')
        entries = science["entries"]
    elif 'business' in command:
        print("business news")
        gn = GoogleNews(lang='en', country='None')
        business = gn.topic_headlines('business')
        entries = business["entries"]
    elif 'entertainment' in command:
        print("entertainment news")
        gn = GoogleNews(lang='en', country='None')
        entertainment = gn.topic_headlines('entertainment')
        entries = entertainment["entries"]
    elif 'sport' in command:
        print("sport news")
        gn = GoogleNews(lang='en', country='None')
        sport = gn.topic_headlines('sports')
        entries = sport["entries"]
    elif 'health' in command:
        print("health news")
        gn = GoogleNews(lang='en', country='None')
        health = gn.topic_headlines('health')
        entries = health["entries"]
    else:
        print("world news")
        gn = GoogleNews(lang='en', country='None')
        world = gn.topic_headlines('world')
        entries = world["entries"]
    newss = []
    for entry in entries:
        newss.append(entry['title'])
        
    return newss
  