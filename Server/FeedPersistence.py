import sqlite3
from FeedModel import *
import Helper
class Persistence:
    def __init__(self):
        self.con = sqlite3.connect("feedData.db", check_same_thread=False)
        
        self.feedSources = {}
        self.stories = []
        cur = self.con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS feed_sources(feed_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, url TEXT);")
        cur.execute("CREATE TABLE IF NOT EXISTS stories(story_id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, summary TEXT, url TEXT, time TEXT, feed_id INTEGER, FOREIGN KEY(feed_id) REFERENCES feed_sources(feed_id));")
        self.deserializeData()

    def deserializeData(self):
        cur = self.con.cursor()
        feedsResult = cur.execute("SELECT * FROM feed_sources;")
        while True:
            fetched = feedsResult.fetchone()
            if fetched is None:
                break
            feed = FeedSource(int(fetched[0]), fetched[1], fetched[2])
            self.feedSources[int(fetched[0])] = feed

        storiesResult = cur.execute("SELECT * FROM stories;")
        while True:
            fetched = storiesResult.fetchone()
            if fetched is None:
                break
            assocSource = self.feedSources[int(fetched[5])]
            story = Story(fetched[0], fetched[1], fetched[2], fetched[3], Helper.textDateToTimeTup(fetched[4]), assocSource)
            assocSource.stories.append(story)
            self.stories.append(story)
    
    def getSources(self):
        return self.feedSources.values()
    
    def getStoriesFromSource(self, source_id):
        return self.feedSources[int(source_id)].stories

    def addSource(self, feed: FeedSource):
        cur = self.con.cursor()
        sql = "INSERT INTO feed_sources(name, url) VALUES(?, ?);"
        args = (feed.name, feed.url)
        cur.execute(sql, args)
        self.con.commit()
        feed.id = cur.lastrowid
        self.feedSources[int(feed.id)] = feed


    def addStory(self, story: Story):
        cur = self.con.cursor()
        sql = f"INSERT INTO stories(title, summary, url, time, feed_id) VALUES(?, ?, ?, ?, ?);"
        args = (str(story.title), str(story.summary), str(story.url), Helper.parsedTimeToDate(story.time), int(story.feedSource.id))
        cur.execute(sql, args)
        self.con.commit()
        story.id = cur.lastrowid
        self.stories.append(story)
        story.feedSource.stories.append(story)
    
    def deleteStoriesFromSource(self, feed: FeedSource):
        cur = self.con.cursor()
        sql = f"DELETE FROM stories WHERE feed_id={int(feed.id)};"
        cur.execute(sql)
        self.con.commit()
        for story in feed.stories:
            self.stories.remove(story)
        feed.stories = []
    
    def deleteSource(self, feed: FeedSource) -> bool:
        cur = self.con.cursor()
        self.deleteStoriesFromSource(feed)

        sql = f"DELETE FROM feed_sources WHERE feed_id={int(feed.id)};"
        cur.execute(sql) 
        self.con.commit()
        self.feedSources.pop(feed.id)
        return True



    def close(self):
        self.con.close()


