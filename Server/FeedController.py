from FeedModel import *
from FeedPersistence import *
import feedparser
import time
import Recommendations
from bs4 import BeautifulSoup
import random
db = Persistence()

MAX_STORIES_PER_SOURCE = 15

def createSource(name, url):
    feed = FeedSource(-1, name, url)
    db.addSource(feed)
    fetchStoriesFromSource(feed.id)
    return feed

def deleteSource(id) -> bool:
    forceRecommendationReset()
    return db.deleteSource(db.feedSources[int(id)])

def getSources():
    sourcesList = db.getSources()
    return sourcesList

# fetches stories from feed if more than 15 minutes since last fetch
def fetchStoriesFromSource(source_id):
    source = db.feedSources[int(source_id)]
    if (time.time() - source.lastUpdate) > (15 * 60):
        
        rssResults = feedparser.parse(source.url)
        if len(rssResults.entries) > 0:
            db.deleteStoriesFromSource(source)
            for e in rssResults.entries[:MAX_STORIES_PER_SOURCE]:
                soup = BeautifulSoup(str(getattr(getattr(e, "summary_detail", ""), "value", "")),features="html.parser")
                summary = soup.get_text()
                storyObj = Story(-1, getattr(e, "title", ""), summary, getattr(e, "link", ""), getattr(e, "published_parsed", ""), source)
                db.addStory(storyObj)
            source.lastUpdate = time.time()
            Recommendations.last_update = 0 #force recommendations re-recommend
    return getStoriesFromSource(source_id)
        

def getStoriesFromSource(source_id):
    return db.getStoriesFromSource(int(source_id))

def returnCategories():
    for index, id in enumerate(db.feedSources.keys()):
        fetchStoriesFromSource(id)
       
    return Recommendations.categorizeStories(db.stories)


def forceRecommendationReset():
    Recommendations.last_update = 0
