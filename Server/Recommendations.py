from unicodedata import category
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from FeedModel import Story
from typing import List
from collections import Counter
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import time
import string 
import random
import copy
from MyConstants import *

NUM_CATEGORIES = 30
MAX_STORIES_PER_CATEGORY = 5


categories = []
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
stop_words = set(stopwords.words('english'))

stop_words.update(ADDITIONAL_STOPWORDS)
last_update = 0
ps = PorterStemmer()
vaderSentiment = SentimentIntensityAnalyzer()

punctuation = set(string.punctuation)
other_puncts = ['’', '–', '‘']
punctuation.update(other_puncts)

# strips string of punctuation, turns into lowercase, removes stopwords, stems
def tokenizeAndClean(s: str) -> List[str]:
    for p in (punctuation):
        s = s.replace(p, '')
    s = s.lower()
    tokens = word_tokenize(s)
    
    resTokens = []
    for word in tokens:
        stem = ps.stem(word)
        if not word in stop_words and not stem in stop_words:
            resTokens.append(stem)
    return resTokens
    
def expandStemToFullWord(keyword: str, s: Story) -> str:
    titlecpy = s.title
    for p in (punctuation):
        titlecpy = titlecpy.replace(p, '')
    titlecpy = titlecpy.lower()
    tokens = word_tokenize(titlecpy)
    for t in tokens:
        if keyword in t:
            return t
    return ""

def categorizeStories(feedStories: List[Story]):

    # reset categories and dictionary
    global categories
    global last_update
    # shallow copy to preserve story instances while not changing story list
    stories = copy.copy(feedStories)
    if not len(stories):
        return []
    if (time.time() - last_update) < (15 * 60):
        return categories
    categories = []
    # build up dictionary
    allWords = []
    for s in stories:
        s.ranking = rateStoryValue(s)
        cleaned = tokenizeAndClean(s.title)
        s.simplifiedTitle = cleaned
        allWords.extend(cleaned)
    stories.sort(key=lambda x: x.ranking, reverse=True)
    count = Counter(allWords)
    most_occurrences = count.most_common(NUM_CATEGORIES)
    # build up categories
    print(most_occurrences)
    for k in most_occurrences:
        keywd = k[0]
        cat = Category(keywd)
        for s in stories:
            if len(cat.stories) >= MAX_STORIES_PER_CATEGORY:
                break
            if keywd in s.simplifiedTitle:
                # restore full word
                if cat.expandedKeyword == "":
                    cat.expandedKeyword = expandStemToFullWord(keywd, s)
                cat.stories.append(s)
                stories.remove(s) #remove duplicates
        # if still failed to find full keyword in story, use stem as graceful fallback
        if cat.expandedKeyword == "":
            cat.expandedKeyword = cat.keyword
        #duplicate avoidance may cause empty categories
        if len(cat.stories) > 0:  
            # set rank of category to mean of story rank, plus consider number of occurrences and add some randomness
            cat.categoryRank = rateCategoryValue(cat, k[1])
            categories.append(cat)
    last_update = time.time()
    categories.sort(key=lambda x: x.categoryRank, reverse=True)
    return categories

def rateCategoryValue(cat, freq: int) -> int:
    ranksum = 0
    for s in cat.stories:
        ranksum += s.ranking
    ranksum = ranksum / len(cat.stories)
    ranksum += freq * 10
    ranksum *= (random.randrange(75, 125) * 0.01)
    return ranksum

# TODO: Make better story ranking method
def rateStoryValue(s: Story):
    rating = 0
    sentiment = get_sentiments(f"{s.title} {s.summary}")
    s.neg_sentiment = sentiment['neg']
    s.pos_sentiment = sentiment['pos']
    rating += s.neg_sentiment * 20 #emphasize negative sentiments as they are likely to be urgent news stories
    rating += s.pos_sentiment * 5
    try:
        unixtime = time.mktime(s.time)
        age = time.time() - unixtime
        rating -= 0.0002 * age
    except:
        pass
    rating += random.randint(-7, 7)
    return rating

def get_sentiments(text: str) -> float:
    return vaderSentiment.polarity_scores(text)

class Category:
    def __init__(self, keyword):
        self.keyword = keyword
        self.expandedKeyword = "" #keyword as full word rather than stem
        self.stories = []
        self.categoryRank = 0

