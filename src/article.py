import dataclasses
import datetime
import typing

from feedgen.feed import FeedEntry


@dataclasses.dataclass
class Article:
    id: str
    url: str
    title: str
    author: str
    date: datetime.datetime
    content: typing.Optional[str] = dataclasses.field(default=None)


class ArticleFeedEntryAdaptor(FeedEntry):
    def __init__(self, article: Article):
        super().__init__()
        self.id(article.id)
        self.title(article.title)
        self.link(href=article.url, rel='alternate')
        self.author(name=article.author)
        self.published(article.date)
        self.content(content=article.content)
