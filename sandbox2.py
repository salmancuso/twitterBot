import feedparser
    
feedURL = str("https://gizmodo.com/rss")
feedData = feedparser.parse(feedURL)
if feedData[ "bozo" ] == 0: ## if 0, then it is a good feed.
    print("Feed is good")
else:
    print("bad feed")