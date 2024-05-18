
class FeedSource:
    def __init__(self, id, name, url):
        self.id = id
        self.name = name
        self.url = url
        self.stories = []
        self.lastUpdate = 0
class Story:
    def __init__(self, id, title, summary, contents, url, time, feedSource: FeedSource):
        self.id = id
        self.title = title
        self.summary = summary
        self.contents = contents
        self.url = url
        self.time = time
        self.feedSource = feedSource