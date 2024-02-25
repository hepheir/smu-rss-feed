from dataclasses import dataclass
from typing import Iterable

from article import ArticleFeedEntryAdaptor
from crawlers import ArticleCrawler
from feed import Feed


@dataclass
class FeedCreateJob:
    crawler: ArticleCrawler
    id: str
    url: str
    title: str
    description: str
    rss_filename: str


def create_one(job: FeedCreateJob):
    feed = Feed(
        id=job.id,
        url=job.url,
        title=job.title,
        description=job.description,
    )
    for article in job.crawler.get_articles():
        entry = ArticleFeedEntryAdaptor(article)
        feed.add_entry(entry)
    feed.rss_file(job.rss_filename)


def create_all(jobs: Iterable[FeedCreateJob]):
    for job in jobs:
        create_one(job)
