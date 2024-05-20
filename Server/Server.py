from flask import Flask
from flask import request
import FeedController
import Helper
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

@app.route('/deleteSource', methods=['DELETE'])
def deleteSource():
    if request.method == 'DELETE':
        if FeedController.deleteSource(request.args.get('id')):
            return {
                "status": 200,
            }
        else:
            return {
                "status": 500,
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
                "feed_source": s.feedSource.id,
                "sentiment": s.sentiment
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
                "time": Helper.parsedTimeToDate(s.time),
                "feed_source": s.feedSource.id,
                "feed_source_name": s.feedSource.name,
                "story_ranking": s.ranking,
                "neg_sentiment": s.neg_sentiment,
                "pos_sentiment": s.pos_sentiment
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

@app.route('/getStoryCategories', methods=['GET'])
def getStoryCategories():
    if request.method == 'GET':
        catResults = FeedController.returnCategories()
        categories = catResults[0]
        fullyUpdated = catResults[1]
        categoryDTOs = []
        for c in categories:
            categoryDTO = {
                "keyword": c.expandedKeyword,
                "stories": []
            }
            for s in c.stories:
                categoryDTO["stories"].append({
                    "id": s.id,
                    "title": s.title,
                    "summary": s.summary,
                    "url": s.url,
                    "time": Helper.parsedTimeToDate(s.time),
                    "feed_source": s.feedSource.id,
                    "feed_source_name": s.feedSource.name,
                    "story_ranking": s.ranking,
                    "neg_sentiment": s.neg_sentiment,
                    "pos_sentiment": s.pos_sentiment
                })
            categoryDTOs.append(categoryDTO)
        return {
            "status": 200,
            "categories": categoryDTOs,
            "fullyUpdated": fullyUpdated
        }
    else:
        return {
            "status": 405,
            "error": "Needs to be get request"
        }

@app.route('/getRefreshedStoryCategories', methods=['GET'])
def getRefreshedStoryCategories():
    if request.method == 'GET':
        FeedController.forceRecommendationReset()
        catResults = FeedController.returnCategories()
        categories = catResults[0]
        fullyUpdated = catResults[1]
        categoryDTOs = []
        for c in categories:
            categoryDTO = {
                "keyword": c.expandedKeyword,
                "stories": []
            }
            for s in c.stories:
                categoryDTO["stories"].append({
                    "id": s.id,
                    "title": s.title,
                    "summary": s.summary,
                    "url": s.url,
                    "time": Helper.parsedTimeToDate(s.time),
                    "feed_source": s.feedSource.id,
                    "feed_source_name": s.feedSource.name,
                    "story_ranking": s.ranking,
                    "neg_sentiment": s.neg_sentiment,
                    "pos_sentiment": s.pos_sentiment
                })
            categoryDTOs.append(categoryDTO)
        return {
            "status": 200,
            "categories": categoryDTOs,
            "fullyUpdated": fullyUpdated
        }
    else:
        return {
            "status": 405,
            "error": "Needs to be get request"
        }