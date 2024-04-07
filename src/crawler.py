from __future__ import annotations

from typing import Iterable
import abc
import datetime
import logging
import urllib.parse

import bs4

from article import Article
from utils import safe_https_get, TIMEZONE


class ArticleCrawler(abc.ABC):
    def __init__(self, url: str) -> None:
        self.url = url
        self.logger = logging.getLogger(self.__class__.__name__)

    def __repr__(self) -> str:
        return f'<ArticleCrawler for {self.url}>'

    @abc.abstractmethod
    def get_articles(self) -> Iterable[Article]:
        """여러 아티클들을 불러옵니다."""
        raise NotImplementedError


class SmuArticleCrawler(ArticleCrawler):
    def get_articles(self) -> Iterable[Article]:
        parser = self._get_parser()
        return parser.parse_articles()

    def _get_parser(self) -> ArticleParser:
        html = safe_https_get(self.url).text
        soup = bs4.BeautifulSoup(html, 'html.parser')
        if '/community/' in self.url:
            return SmuCommunityArticleParser(self.url, soup)
        if '/bbs/' in self.url:
            return SmuBbsArticleParser(self.url, soup)
        raise Exception('지원되는 공지사항 주소가 아닙니다.')


class ArticleParser(abc.ABC):
    def __init__(self, url: str, soup: bs4.BeautifulSoup) -> None:
        self.url = url
        self.soup = soup
        self.logger = logging.getLogger(self.__class__.__name__)

    @abc.abstractmethod
    def parse_articles(self) -> Iterable[Article]:
        raise NotImplementedError


class SmuCommunityArticleParser(ArticleParser):
    def parse_articles(self) -> Iterable[Article]:
        selector_path = 'ul.board-thumb-wrap dl'
        for tag in self.soup.select(selector_path):
            tag: bs4.Tag
            yield Article(
                id=self._get_id(tag),
                url=self._get_url(tag),
                title=self._get_title(tag),
                author=self._get_author(tag),
                date=self._get_date(tag),
                content=None,
            )

    def _get_url(self, tag: bs4.Tag) -> str:
        rel_href = tag.find('a').attrs['href']
        return urllib.parse.urljoin(self.url, rel_href)

    def _get_id(self, tag: bs4.Tag) -> str:
        url = self._get_url(tag)
        return urllib.parse.parse_qs(url)['articleNo'][0]

    def _get_title(self, tag: bs4.Tag) -> str:
        return tag.find('a').attrs['title']

    def _get_author(self, tag: bs4.Tag) -> str:
        return tag.select_one('li.board-thumb-content-writer') \
            .get_text(separator=':', strip=True) \
            .lstrip('작성자:')

    def _get_date(self, tag: bs4.Tag) -> datetime.date:
        date_string = tag.select_one('li.board-thumb-content-date') \
            .get_text(separator=':', strip=True) \
            .lstrip('작성일:')
        return datetime.datetime(*map(int, date_string.split('-')), tzinfo=TIMEZONE)


class SmuBbsArticleParser(ArticleParser):
    def parse_articles(self) -> Iterable[Article]:
        selector_path = 'form#fboardlist tbody tr'
        for tag in self.soup.select(selector_path):
            tag: bs4.Tag
            yield Article(
                id=self._get_id(tag),
                url=self._get_url(tag),
                title=self._get_title(tag),
                author=self._get_author(tag),
                date=self._get_date(tag),
                content=None,
            )

    def _get_url(self, tag: bs4.Tag) -> str:
        rel_href = tag.find('a').attrs['href']
        return urllib.parse.urljoin(self.url, rel_href)

    def _get_id(self, tag: bs4.Tag) -> str:
        url = self._get_url(tag)
        return urllib.parse.parse_qs(url)['wr_id'][0]

    def _get_title(self, tag: bs4.Tag) -> str:
        return tag.find('a').text.strip()

    def _get_author(self, tag: bs4.Tag) -> str:
        return tag.select_one('span.sv_member').text.strip()

    def _get_date(self, tag: bs4.Tag) -> datetime.date:
        date_string = tag.select_one('td.td_datetime').text.strip()
        return datetime.datetime(*map(int, date_string.split('-')), tzinfo=TIMEZONE)
