from os import makedirs
from os.path import exists
from os.path import dirname
from typing import Dict

from feedgen.feed import FeedGenerator
from feedgen.feed import FeedEntry


class Feed(FeedGenerator):
    def __init__(self, id: str, url: str, title: str, description: str):
        super().__init__()
        self.id(id)
        self.link(href=url, rel='alternate')
        self.title(title)
        self.description(description)
        self.__feed_entries: Dict[str, FeedEntry] = {}

    def add_entry(self, entry: FeedEntry):
        self.__feed_entries[entry.id()] = entry

    def add_item(self, item):
        return self.add_entry(item)

    def rss_file(self, filename, extensions=True, pretty=False, encoding='UTF-8', xml_declaration=True):
        if not exists(dirname(filename)):
            makedirs(dirname(filename))
        # Sort before serialize
        entries = self.__feed_entries.values()
        for entry in sorted(entries, key=lambda e: e.published()):
            super().add_entry(entry)
        return super().rss_file(filename, extensions, pretty, encoding, xml_declaration)
