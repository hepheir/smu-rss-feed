import datetime
import os
import typing
import urllib.parse

import bs4
import feedgen.feed
import requests


_TIMEZONE = datetime.timezone(datetime.timedelta(hours=9))


class FeedGenerator(feedgen.feed.FeedGenerator):
    def __init__(self):
        super().__init__()

        self.id('https://github.com/hepheir/smu-rss-feed')
        self.title('상명대학교 공지사항 모음')
        self.link(href='https://github.com/hepheir/smu-rss-feed', rel='alternate')
        self.description('상명대학교 공지사항 모음 (서울캠퍼스, 컴퓨터과학과, 지능IOT융합전공, SW중심사업단)')

    def sort(self):
        self.__feed_entries.sort(key=lambda e: e.published())


feed = FeedGenerator()


def serialize(filename: os.PathLike) -> None:
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    feed.sort()
    feed.rss_file(filename, pretty=True, xml_declaration=True)

def sync() -> None:
    try:
        entries: typing.List[feedgen.feed.FeedEntry] = []
        entries.extend(_pull_from_community('https://cs.smu.ac.kr/cs/community/notice.do'))
        entries.extend(_pull_from_community('https://aiot.smu.ac.kr/aiot/community/notice.do'))
        entries.extend(_pull_from_bbs('https://swai.smu.ac.kr/bbs/board.php?bo_table=07_01'))
        for entry in entries:
            feed.add_entry(entry)
    except Exception as e:
        print(e)

def _pull_from_community(url: str) -> typing.Iterable[feedgen.feed.FeedEntry]:
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text)

    # 각 공지 별로 내용을 파싱해오기.
    for dl in soup.find('ul', attrs={'class': 'board-thumb-wrap'}).find_all('dl'):
        dl: bs4.Tag

        href = urllib.parse.urljoin(url, dl.find('a').attrs['href'])
        title = dl.find('a').attrs['title']
        author = dl.find('li', attrs={'class', 'board-thumb-content-writer'}) \
                .get_text(separator=':', strip=True) \
                .lstrip('작성자:')
        date_string = dl.find('li', attrs={'class', 'board-thumb-content-date'}) \
                .get_text(separator=':', strip=True) \
                .lstrip('작성일:')
        date = datetime.datetime(*map(int, date_string.split('-')), tzinfo=_TIMEZONE)

        entry = feedgen.feed.FeedEntry()
        entry.id(href)
        entry.title(title)
        entry.link(href=href, rel='alternate')
        entry.author(name=author)
        entry.published(date)
        yield entry


def _pull_from_bbs(url: str) -> typing.Iterable[feedgen.feed.FeedEntry]:
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text)

    for tr in soup.find('form', attrs={'id': 'fboardlist'}).find('tbody').find_all('tr'):
        tr: bs4.Tag

        href = tr.find('a').attrs['href']
        title = tr.find('a').text.strip()
        author = tr.find('span', attrs={'class', 'sv_member'}).text.strip()
        date_string = tr.find('td', attrs={'class', 'td_datetime'}).text.strip()
        date = datetime.datetime(*map(int, date_string.split('-')), tzinfo=_TIMEZONE)

        entry = feedgen.feed.FeedEntry()
        entry.id(href)
        entry.title(title)
        entry.link(href=href, rel='alternate')
        entry.author(name=author)
        entry.published(date)
        yield entry

if __name__ == '__main__':
    FILENAME = 'docs/feed.xml'

    sync()
    serialize(FILENAME)
