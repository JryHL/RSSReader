import time
class FeedSource:
    def __init__(self, id, name, url):
        self.id = id
        self.name = name
        self.url = url
        self.stories = []
        self.lastUpdate = 0
        
class Story:
    def __init__(self, id, title, summary, url, time, feedSource: FeedSource):
        self.id = id
        self.title = title
        self.summary = summary
        self.url = url
        self.time = time
        self.feedSource = feedSource
        self.simplifiedTitle = "" #title after stemming, stopword removal
        self.ranking = 0
        self.sentiment = 0