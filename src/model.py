import dataclasses
import datetime


@dataclasses.dataclass
class Article:
    url: str
    title: str
    author: str
    date: datetime.date
    content: str
