from __future__ import annotations

import datetime
import os
import typing
import urllib.parse

import bs4
import feedgen.feed
import requests


_TIMEZONE = datetime.timezone(datetime.timedelta(hours=9))


class FeedGenerator(feedgen.feed.FeedGenerator):
    @classmethod
    def from_community(cls, url: str) -> typing.Self[FeedGenerator]:
        feed = FeedGenerator()

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

            feed.add_entry(entry)

        return feed

    @classmethod
    def from_bbs(cls, url: str) -> typing.Self[FeedGenerator]:
        feed = FeedGenerator()

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

            feed.add_entry(entry)

        return feed

    def __add__(self, other: FeedGenerator) -> typing.Self[FeedGenerator]:
        self.__feed_entries.extend(other.__feed_entries)
        return self

    def rss_file(self, filename: str) -> None:
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))

        # Sort before serialize
        self.__feed_entries.sort(key=lambda e: e.published())

        return super().rss_file(filename, pretty=True, xml_declaration=True)


if __name__ == '__main__':
    FILENAME = 'docs/feed_%s.xml'
    TITLE = '상명대학교 %s 공지사항'
    DESCRIPTION = '상명대학교 %s 공지사항 게시판의 내용을 (Atom 기반) RSS Feed로 가공한 내용입니다. [제작자: 김동주 <hepheir@gmail.com>]'

    cs_feed = FeedGenerator.from_community('https://cs.smu.ac.kr/cs/community/notice.do')
    cs_feed.id('https://cs.smu.ac.kr')
    cs_feed.link(href='https://github.com/hepheir/smu-rss-feed', rel='alternate')
    cs_feed.title(TITLE % '컴퓨터과학과')
    cs_feed.description(DESCRIPTION % '컴퓨터과학과')
    cs_feed.rss_file(FILENAME % 'cs')

    aiot_feed = FeedGenerator.from_community('https://aiot.smu.ac.kr/aiot/community/notice.do')
    aiot_feed.id('https://aiot.smu.ac.kr')
    aiot_feed.link(href='https://github.com/hepheir/smu-rss-feed', rel='alternate')
    aiot_feed.title(TITLE % '지능IOT융합전공')
    aiot_feed.description(DESCRIPTION % '지능IOT융합전공')
    aiot_feed.rss_file(FILENAME % 'aiot')

    swai_feed = FeedGenerator.from_bbs('https://swai.smu.ac.kr/bbs/board.php?bo_table=07_01')
    swai_feed.id('https://swai.smu.ac.kr')
    swai_feed.link(href='https://github.com/hepheir/smu-rss-feed', rel='alternate')
    swai_feed.title(TITLE % 'SW중심사업단')
    swai_feed.description(DESCRIPTION % 'SW중심사업단')
    swai_feed.rss_file(FILENAME % 'swai')
