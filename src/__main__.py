import logging

from .automation import FeedCreateJob
from .automation import create_all
from .crawlers import *


logging.basicConfig(level=logging.DEBUG)


jobs = [
    FeedCreateJob(
        crawler=CommunityHtmlArticleCrawler('https://cs.smu.ac.kr/cs/community/notice.do'),
        id='https://cs.smu.ac.kr',
        url='https://cs.smu.ac.kr',
        title='컴퓨터과학과',
        description='상명대학교 컴퓨터과학과 공지사항 게시판의 내용을 (Atom 기반) RSS Feed로 가공한 내용입니다.\n\n[제작자: 김동주 <hepheir@gmail.com>]',
        rss_filename='docs/cs/feed.xml',
    ),
    FeedCreateJob(
        crawler=CommunityHtmlArticleCrawler('https://aiot.smu.ac.kr/cs/community/notice.do'),
        id='https://aiot.smu.ac.kr',
        url='https://aiot.smu.ac.kr',
        title='지능IOT융합전공',
        description='상명대학교 지능IOT융합전공 공지사항 게시판의 내용을 (Atom 기반) RSS Feed로 가공한 내용입니다.\n\n[제작자: 김동주 <hepheir@gmail.com>]',
        rss_filename='docs/aiot/feed.xml',
    ),
    FeedCreateJob(
        crawler=BbsHtmlArticleCrawler('https://swai.smu.ac.kr/bbs/board.php?bo_table=07_01'),
        id='https://swai.smu.ac.kr',
        url='https://swai.smu.ac.kr',
        title='SW중심사업단',
        description='상명대학교 SW중심사업단 공지사항 게시판의 내용을 (Atom 기반) RSS Feed로 가공한 내용입니다.\n\n[제작자: 김동주 <hepheir@gmail.com>]',
        rss_filename='docs/swai/feed.xml',
    ),
]

create_all(jobs)
