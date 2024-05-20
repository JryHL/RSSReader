from FeedModel import *
from FeedPersistence import *
import feedparser
import time
import Recommendations
from bs4 import BeautifulSoup
import random
from threading import Thread



db = Persistence()

MAX_STORIES_PER_SOURCE = 15

def createSource(name, url):
    waitForFeedUpdate()
    feed = FeedSource(-1, name, url)
    db.addSource(feed)
    fetchStoriesFromSource(feed.id)
    return feed

def deleteSource(id) -> bool:
    waitForFeedUpdate()
    forceRecommendationReset()
    return db.deleteSource(db.feedSources[int(id)])

def getSources():
    waitForFeedUpdate()
    sourcesList = db.getSources()
    return sourcesList

# fetches stories from feed if more than 15 minutes since last fetch
def fetchStoriesFromSourceReal(source_id):
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
    return getStoriesFromSourceReal(source_id)
        
def fetchStoriesFromSource(source_id):
    # when called externally, wait until background update thread has finished
    waitForFeedUpdate()
    return fetchStoriesFromSourceReal(source_id)

def getStoriesFromSource(source_id):
    waitForFeedUpdate()
    return getStoriesFromSourceReal(source_id)

def getStoriesFromSourceReal(source_id):
    return db.getStoriesFromSource(int(source_id))

def updateAllFeeds():
    print("Background feed update started")
    for id in db.feedSources.keys():
        fetchStoriesFromSourceReal(id)
    print("Background feed update finished")

def returnCategories():
    waitForFeedUpdate()
    start_time = time.time()
    fullyUpdated = True
    for id in db.feedSources.keys():
        fetchStoriesFromSource(id)
        if time.time() - start_time > 2:
            # leave remaining update for next run
            feedUpdateThread.start()
            fullyUpdated = False
            break
       
    categoryList = Recommendations.categorizeStories(db.stories)
    return (categoryList, fullyUpdated)

def forceRecommendationReset():
    Recommendations.last_update = 0

def waitForFeedUpdate():
    if feedUpdateThread.is_alive():
        feedUpdateThread.join()

feedUpdateThread = Thread(target = updateAllFeeds)