from flask import Flask
from flask import request
import FeedController

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/createSource', methods=['POST'])
def createSource():
    if request.method == 'POST':
        request_data = request.get_json()
        feed = FeedController.createSource(request_data['name'], request_data['url'])
        return {
            "status": 200,
            "data": {
                "id": feed.id,
                "name": feed.name,
                "url": feed.url
            }
        }
    else:
        return {
            "status": 405,
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
            "status": 200,
            "feeds": feedDTOs
        }
    else:
        return {
            "status": 405,
            "error": "Needs to be get request"
        }
    
@app.route('/getStoriesFromSource', methods=['GET'])
def getStoriesFromSource():
    if request.method == 'GET':
        request_data = request.get_json()
        stories = FeedController.getStoriesFromSource(request.args.get('id'))
        storyDTOs = []
        for s in stories:
            storyDTOs.append({
                "id": s.id,
                "title": s.title,
                "summary": s.summary,
                "url": s.url,
                "time": s.time,
                "feed_source": s.feedSource.id
            })
        return {
            "status": 200,
            "stories": storyDTOs
        }
    else:
        return {
            "status": 405,
            "error": "Needs to be get request"
        }
    
@app.route('/fetchStoriesFromSource', methods=['GET'])
def fetchStoriesFromSource():
    if request.method == 'GET':
        stories = FeedController.fetchStoriesFromSource(request.args.get('id'))
        storyDTOs = []
        for s in stories:
            storyDTOs.append({
                "id": s.id,
                "title": s.title,
                "summary": s.summary,
                "url": s.url,
                "time": s.time,
                "feed_source": s.feedSource.id
            })
        return {
            "status": 200,
            "stories": storyDTOs
        }
    else:
        return {
            "status": 405,
            "error": "Needs to be get request"
        }