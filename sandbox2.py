import feedparser
    
feedURL = str("https://rss.bizjournals.com/feed/4d3b75f3af9d6c56af49b9e8a79ff847173c75c4/3033?market=sanfrancisco,sanjose&selectortype=channel&selectorvalue=15")
feedData = feedparser.parse(feedURL)
if feedData[ "bozo" ] == 0: ## if 0, then it is a good feed.
    print("Feed is good")
else:
    print("bad feed")