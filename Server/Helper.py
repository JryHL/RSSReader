import random
import time
def getNRandom(n: int, mylist):
    #edge case: requested more than list length
    if n >= len(mylist):
        return mylist
    #use set to prevent duplicates
    obtained = set()
    while len(obtained) < n:
        obtained.add(random.choice(mylist))
    return list(obtained)

def parsedTimeToDate(tup):
    try:
        return time.strftime("%b %d %Y %H:%M:%S", tup)
    except:
        return "Invalid time"