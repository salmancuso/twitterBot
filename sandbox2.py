import feedparser
    
feedURL = str("http://hackerone.com/blog.rss")
feedData = feedparser.parse(feedURL)
if feedData[ "bozo" ] == 0: ## if 0, then it is a good feed.
    print("Feed is good")
else:
    print("bad feed")