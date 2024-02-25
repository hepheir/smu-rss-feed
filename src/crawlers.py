import abc
from datetime import datetime
from typing import Iterable
from urllib.parse import urljoin
from urllib.parse import parse_qs

from bs4 import BeautifulSoup
from bs4 import Tag

from .article import Article
from .utils import fix_img_urls
from .utils import safe_https_get
from .utils import TIMEZONE


class ArticleCrawler(abc.ABC):
    @abc.abstractmethod
    def get_articles(self) -> Iterable[Article]:
        """여러 아티클들을 불러옵니다."""
        raise NotImplementedError


class HtmlArticleCrawler(ArticleCrawler):
    def get_articles(self) -> Iterable[Article]:
        for url in self._list_article_urls():
            yield self._get_article(url)

    @abc.abstractmethod
    def _list_article_urls(self, *args, **kwargs) -> Iterable[str]:
        """아티클들의 URL을 yield 하는 함수입니다."""
        raise NotImplementedError

    @abc.abstractmethod
    def _get_article(self, url: str) -> Article:
        """하나의 아티클 URL을 입력받아 `Article`객체를 생성합니다."""
        raise NotImplementedError


class CommunityHtmlArticleCrawler(HtmlArticleCrawler):
    def __init__(self, url: str) -> None:
        self.url = url

    def _list_article_urls(self):
        html = safe_https_get(self.url).text
        soup = BeautifulSoup(html, 'html.parser')
        selector_path = 'ul.board-thumb-wrap dl'
        for dl in soup.select(selector_path):
            dl: Tag
            rel_href = dl.find('a').attrs['href']
            abs_href = urljoin(self.url, rel_href)
            yield abs_href

    def _get_article(self, url: str) -> Article:
        html = safe_https_get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        return Article(
            id=self.__get_id(url),
            title=self.__get_title(soup),
            author=self.__get_author(soup),
            date=self.__get_date(soup),
            content=self.__get_content(soup, url),
            url=url,
        )

    def __get_id(self, url: str) -> str:
        return parse_qs(url)['articleNo'][0]

    def __get_title(self, soup: BeautifulSoup) -> str:
        selector_path = '#jwxe_main_content div.board-view-title-wrap > h4'
        return soup.select_one(selector_path).get_text(strip=True)

    def __get_author(self, soup: BeautifulSoup) -> str:
        selector_path = '#jwxe_main_content li.board-thumb-content-writer'
        return soup.select_one(selector_path).get_text(strip=True)

    def __get_date(self, soup: BeautifulSoup) -> datetime.date:
        selector_path = '#jwxe_main_content li.board-thumb-content-date'
        element = soup.select_one(selector_path).__copy__()
        element.select_one('span').extract()
        timestr_format = '%Y-%m-%d'
        date = datetime.strptime(element.get_text(strip=True), timestr_format)
        return date.replace(tzinfo=TIMEZONE)

    def __get_content(self, soup: BeautifulSoup, url: str) -> str:
        selector_path = '#jwxe_main_content div.board-view-content-wrap'
        element = soup.select_one(selector_path).__copy__()
        return fix_img_urls(element, url).__str__()


class BbsHtmlArticleCrawler(HtmlArticleCrawler):
    def __init__(self, url: str) -> None:
        self.url = url

    def _list_article_urls(self):
        html = safe_https_get(self.url).text
        soup = BeautifulSoup(html, 'html.parser')
        selector_path = 'form#fboardlist tbody tr'
        for tr in soup.select(selector_path):
            tr: Tag
            rel_href = tr.find('a').attrs['href']
            abs_href = urljoin(self.url, rel_href)
            yield abs_href

    def _get_article(self, url: str) -> Article:
        html = safe_https_get(url).text
        soup = BeautifulSoup(html, 'html.parser')
        return Article(
            id=self.__get_id(url),
            title=self.__get_title(soup),
            author=self.__get_author(soup),
            date=self.__get_date(soup),
            content=self.__get_content(soup, url),
            url=url,
        )

    def __get_id(self, url: str) -> str:
        return parse_qs(url)['wr_id'][0]

    def __get_title(self, soup: BeautifulSoup) -> str:
        selector_path = 'article#bo_v h2#bo_v_title'
        return soup.select_one(selector_path).get_text(strip=True)

    def __get_author(self, soup: BeautifulSoup) -> str:
        selector_path = 'article#bo_v section#bo_v_info span.sv_member'
        return soup.select_one(selector_path).get_text(strip=True)

    def __get_date(self, soup: BeautifulSoup) -> datetime.date:
        selector_path = 'article#bo_v section#bo_v_info strong.if_date'
        element = soup.select_one(selector_path).__copy__()
        element.select_one('span').extract()
        timestr_format = '%Y-%m-%d %H:%M'
        date = datetime.strptime(element.get_text(strip=True), timestr_format)
        return date.replace(tzinfo=TIMEZONE)

    def __get_content(self, soup: BeautifulSoup, url: str) -> str:
        selector_path = 'article#bo_v section#bo_v_atc'
        element = soup.select_one(selector_path).__copy__()
        return fix_img_urls(element, url).__str__()
