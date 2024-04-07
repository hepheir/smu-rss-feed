import urllib3
import logging
import json
import pathlib

from article import ArticleFeedEntryAdaptor
from crawler import SmuArticleCrawler
from feed import Feed

logging.basicConfig(level=logging.DEBUG)
logging.getLogger(urllib3.__name__).setLevel(level=logging.WARNING)


REPOSITORY = pathlib.Path(__file__).parent.parent


with open(REPOSITORY / 'settings.json', 'r') as rfp:
    for data in json.load(rfp)['feeds']:
        feed = Feed(
            id=data['id'],
            url=data['href'],
            title=data['title'],
            description=data['description']
        )
        crawler = SmuArticleCrawler(data['src'])
        for article in crawler.get_articles():
            feed.add_entry(ArticleFeedEntryAdaptor(article))
        feed.rss_file(REPOSITORY / data['output'])
