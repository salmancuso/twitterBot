tweetDict = {"http://feeds.feedburner.com/TechCrunchIT": "#tech",
             "http://feeds.feedburner.com/TechCrunch/startups": "#startup",
             "http://rss.nytimes.com/services/xml/rss/nyt/Technology.xml": "#tech",
             "https://www.wired.com/feed/category/security/latest/rss": "#security",
             "https://www.wired.com/feed/rss": "#tech #news",
             "https://www.wired.com/feed/category/science/latest/rss": "#science",
             "https://www.wired.com/feed/category/business/latest/rss": "#tech #business",
             "http://feeds.arstechnica.com/arstechnica/technology-lab": "#tech",
             "http://feeds.arstechnica.com/arstechnica/business": "#tech #business",
             "http://feeds.arstechnica.com/arstechnica/security": "#security #hacktivism",
             "http://feeds.arstechnica.com/arstechnica/tech-policy": "#tech #law",
             "https://krebsonsecurity.com/feed/": "#security #data",
             "https://www.hackread.com/sec/": "#security #data #hacking",
             "https://www.hackread.com/sec/malware/": "#security #malware",
             "https://www.hackread.com/latest-cyber-crime/": "#security #hacking #cybercrime",
             "https://www.hackread.com/latest-cyber-crime/phishing-scam/": "#security #phishing #cybercrime",
             "https://www.hackread.com/how-to/": "#lifehack #tech #howto",
             "https://www.hackerone.com/blog/category/Data%20and%20Analysis": "#data #analysis",
             "https://www.hackread.com/cyber-events/cyber-attacks-cyber-events/": "#security #cyberattack #data",
             "https://www.hackread.com/cyber-events/censorship/": "#censorship",
             "https://www.hackread.com/surveillance/": "#surveillance",
             "http://starbridgepartners.com/data-science-report/": "#data #DataScience #DataEngineering",
             "https://www.smartdatacollective.com/feed/": "#data #DataScience #DataEngineering",
             "https://insidebigdata.com/feed/": "#bigdata #data #DataScience #DataEngineering",
             "https://simplystatistics.org/": "#data #statistics #DataScience #DataEngineering",
             "https://101.datascience.community/": "#data #DataScience #DataEngineering",
             "https://dataconomy.com/": "#data #DataScience #DataEngineering",
             "https://www.hackread.com/surveillance/drones/": "#drone #security #surveillance",
             "https://www.hackread.com/surveillance/nsa/": "#nsa #security #surveillance",
             "https://www.hackread.com/surveillance/privacy/": "#privacy #security #surveillance",
             "https://www.darkreading.com/rss_simple.asp?f_n=644&f_ln=Attacks/Breaches": "#security #data #breach",
             "https://www.darkreading.com/rss_simple.asp?f_n=645&f_ln=Application%20Security": "#security #data #Application",
             "https://www.darkreading.com/rss_simple.asp?f_n=647&f_ln=Cloud": "#cloud #data",
             "https://www.darkreading.com/rss_simple.asp?f_n=649&f_ln=Authentication": "#authentication #security",
             "https://www.darkreading.com/rss_simple.asp?f_n=650&f_ln=Privacy": "#privacy #data",
             "https://www.darkreading.com/rss_simple.asp?f_n=661&f_ln=Vulnerabilities%20/%20Threats": "#Vulnerability #security",
             "https://www.darkreading.com/rss_simple.asp?f_n=659&f_ln=Threat%20Intelligence": "#ThreatIntelligence #security #data"
             }


for url,hash in tweetDict.items():
    print(url)
    print(hash)
    print("\n\n")