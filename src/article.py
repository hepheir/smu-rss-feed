import dataclasses
import datetime

from feedgen.feed import FeedEntry


@dataclasses.dataclass
class Article:
    id: str
    title: str
    author: str
    date: datetime.datetime
    content: str
    url: str


class ArticleFeedEntryAdaptor(FeedEntry):
    def __init__(self, article: Article):
        super().__init__()
        self.id(article.id)
        self.title(article.title)
        self.link(href=article.url, rel='alternate')
        self.author(name=article.author)
        self.published(article.date)
        self.content(src=article.url)
