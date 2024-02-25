from datetime import timedelta
from datetime import timezone
from urllib.parse import urljoin
from urllib3.util.retry import Retry

from bs4 import Tag
from requests import Session
from requests import Response
from requests.adapters import HTTPAdapter

TIMEZONE = timezone(timedelta(hours=9))


def fix_img_urls(root: Tag, url: str) -> Tag:
    """홈페이지 외부에서도 이미지가 보이도록 URL을 절대경로로 변경하는 함수.

    Parameters:
        `root`: 해당 태그의 자식들에서 `<img/>`를 찾아 주소를 변경합니다.
        `url`: 절대 경로로 변경하기 위해 기준으로 사용할 URL.

    이 함수는 `root`의 원소를 직접 수정하므로, 원본 데이터에 영향을 줄 수 있습니다.
    """
    for img in root.select('img'):
        img.attrs['src'] = urljoin(url, img.attrs['src'])
    return root


def safe_https_get(url: str) -> Response:
    session = Session()
    retry = Retry(connect=3, backoff_factor=0.5)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session.get(url)
