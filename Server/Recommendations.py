import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from FeedModel import Story
from typing import List
from collections import Counter
import time
import string 
import random
import copy

NUM_CATEGORIES = 15

categories = []
nltk.download('punkt')
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
other_stopwords = ["say", "time", "could", "new"]
stop_words.update(other_stopwords)
last_update = 0
ps = PorterStemmer()

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
    

def categorizeStories(feedStories: List[Story]):

    # reset categories and dictionary
    global categories
    global last_update
    # shallow copy to preserve story instances while not changing story list
    stories = copy.copy(feedStories)
    if (time.time() - last_update) < (15 * 60):
        return categories
    categories = []
    # build up dictionary
    allWords = []
    for s in stories:
        cleaned = tokenizeAndClean(s.title)
        s.simplifiedTitle = cleaned
        allWords.extend(cleaned)
    count = Counter(allWords)
    most_occurrences = count.most_common(NUM_CATEGORIES)
    random.shuffle(most_occurrences)
    # build up categories
    for k in most_occurrences:
        keywd = k[0]
        cat = Category(keywd)
        for s in stories:
            if keywd in s.simplifiedTitle:
                cat.stories.append(s)
                stories.remove(s) #remove duplicates
        #duplicate avoidance may cause empty categories
        if len(cat.stories) > 0:
            categories.append(cat)
    last_update = time.time()
    return categories


class Category:
    def __init__(self, keyword):
        self.keyword = keyword
        self.stories = []

