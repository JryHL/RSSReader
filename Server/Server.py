from flask import Flask
from flask import request
import FeedController

app = Flask(__name__)

@app.route('/createSource', methods=['POST'])
def createSource():
    if request.method == 'POST':
        feed = FeedController.createSource(request.form['name'], request.form['url'])
        return {
            "id": feed.id,
            "name": feed.name,
            "url": feed.url
        }
    else:
        return {
            "error": "Needs to be post request"
        }
    
@app.route('/getSources', methods=['GET'])
def getSources():
    if request.method == 'GET':
        feeds = FeedController.getSources()
        feedDTOs = []
        for f in feeds:
            feedDTOs.append({
                "id": f.id,
                "name": f.name,
                "url": f.url
            })
        return {
            "feeds": feedDTOs
        }
    else:
        return {
            "error": "Needs to be get request"
        }
    
@app.route('/getStoriesFromSource', methods=['GET'])
def getStoriesFromSource():
    if request.method == 'GET':
        stories = FeedController.getStoriesFromSource(request.form['source_id'])
        storyDTOs = []
        for s in stories:
            storyDTOs.append({
                "id": s.id,
                "title": s.title,
                "summary": s.summary,
                "contents": s.contents,
                "url": s.url,
                "time": s.time,
                "feed_source": s.feedSource.id
            })
        return {
            "stories": storyDTOs
        }
    else:
        return {
            "error": "Needs to be get request"
        }
    
@app.route('/fetchStoriesFromSource', methods=['GET'])
def fetchStoriesFromSource():
    if request.method == 'GET':
        stories = FeedController.fetchStoriesFromSource(request.form['source_id'])
        storyDTOs = []
        for s in stories:
            storyDTOs.append({
                "id": s.id,
                "title": s.title,
                "summary": s.summary,
                "contents": s.contents,
                "url": s.url,
                "time": s.time,
                "feed_source": s.feedSource.id
            })
        return {
            "stories": storyDTOs
        }
    else:
        return {
            "error": "Needs to be get request"
        }