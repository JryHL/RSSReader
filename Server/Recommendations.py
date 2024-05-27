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
import math

CATEGORY_STORIES_RATIO = 10 # divide number of stories by this to determine how many categories to generate
MAX_STORIES_PER_CATEGORY = 5 # max number of stories displayed per category
NEGATIVE_SENTIMENT_BOOST = 100
POSITIVE_SENTIMENT_BOOST = 20
POSITIVE_STORY_CAT_BOOST = 100
PENALTY_PER_HOUR = 5

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

    
    
    count = Counter(allWords)
    most_occurrences = count.most_common(math.ceil(len(stories) / CATEGORY_STORIES_RATIO))

    # Generate positive sentiments category

    pos_sent_cat = Category("pos_sent")
    # using neutral terminology: positive sentiment detection is not perfect and may surface negative stories
    # using overly positive terminology could cause offense if it doesn't match the stories
    pos_sent_cat.expandedKeyword = "Stories that stand out 🧐" 
    stories.sort(key=lambda x:x.pos_sentiment, reverse=True)
    for s in stories:
        if len(pos_sent_cat.stories) >= MAX_STORIES_PER_CATEGORY:
            break
        pos_sent_cat.stories.append(s)
        stories.remove(s)


    # Generate semantic categories

    # Ensures biggest categories get to best stories first
    stories.sort(key=lambda x: x.ranking, reverse=True)

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

    if len(pos_sent_cat.stories) > 0:
        categories.insert(1, pos_sent_cat)

    if len(stories) > 0:
        remaining_stories_cat = Category("remaining")
        remaining_stories_cat.expandedKeyword = "Other stories"
        remaining_stories_cat.stories = stories
        categories.append(remaining_stories_cat)

    return categories

def rateCategoryValue(cat, freq: int) -> int:
    ranksum = 0
    for s in cat.stories:
        ranksum += s.ranking
    ranksum = ranksum / len(cat.stories)
    ranksum += freq * 5
    return ranksum

# TODO: Make better story ranking method
def rateStoryValue(s: Story):
    rating = 0
    sentiment = get_sentiments(f"{s.title} {s.summary}")
    s.neg_sentiment = sentiment['neg']
    s.pos_sentiment = sentiment['pos']
    # emphasize negative sentiments as they are likely to be urgent news stories
    # ensure that stories are not penalized for being not negative using max
    rating += max(s.neg_sentiment * NEGATIVE_SENTIMENT_BOOST, 0)
    rating += max(s.pos_sentiment * POSITIVE_SENTIMENT_BOOST, 0)
    try:
        unixtime = time.mktime(s.time)
        age = time.time() - unixtime
        rating -= PENALTY_PER_HOUR * (age / (60 * 60))
    except:
        pass
    return rating

def get_sentiments(text: str) -> float:
    return vaderSentiment.polarity_scores(text)

class Category:
    def __init__(self, keyword):
        self.keyword = keyword
        self.expandedKeyword = "" #keyword as full word rather than stem
        self.stories = []
        self.categoryRank = 0

