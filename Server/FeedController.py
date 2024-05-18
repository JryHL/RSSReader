from FeedModel import *
from FeedPersistence import *
import feedparser
import time

db = Persistence()

def createSource(name, url):
    feed = FeedSource(-1, name, url)
    db.addSource(feed)
    return feed

def getSources():
    return db.getSources()

def fetchStoriesFromSource(source_id):
    source = db.feedSources[int(source_id)]
    if (time.time() - source.lastUpdate) > (15 * 60):
        db.deleteStoriesFromSource(source)
        rssResults = feedparser.parse(source.url)
        for e in rssResults.entries:
            contents = ""
            if hasattr(e, 'content'):
                for c in e.content:
                    contents += c.value
            storyObj = Story(-1, getattr(e, "title", ""), getattr(e, "summary_detail.value", ""), contents, getattr(e, "link", ""), getattr(e, "published", ""), source)
            db.addStory(storyObj)
        source.lastUpdate = time.time()
    return getStoriesFromSource(source_id)
        

def getStoriesFromSource(source_id):
    return db.getStoriesFromSource(int(source_id))
