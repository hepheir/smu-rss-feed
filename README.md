# 상명대학교 공지사항 RSS Feed

> 매번 학과 사무실 홈페이지 찾아보기가 번거로워서 만들었습니다.

## RSS 링크

* [SW중심사업단 RSS Feed 🔗](https://hepheir.github.io/smu-rss-feed/feed_cs.xml)

* [컴퓨터과학과 RSS Feed 🔗](https://hepheir.github.io/smu-rss-feed/feed_cs.xml)

* [지능IOT융합전공 RSS Feed 🔗](https://hepheir.github.io/smu-rss-feed/feed_cs.xml)

## Tips

저는 Feedly 라는 앱을 사용해 아래 화면과 같이 배경 위젯에 등록해두고 보는 편입니다.

* [Android](https://play.google.com/store/apps/details?id=com.devhd.feedly) <sub>(저는 iPhone 사용자라 안드로이드에서 잘 되는지는 모르겠습니다.)</sub>
* [iOS](https://apps.apple.com/kr/app/feedly-smart-news-reader/id396069556)

![image](https://github.com/hepheir/smu-rss-feed/assets/19310326/3a63bd0e-8f15-40fb-869b-5e498a702fa8)

## 변경 사항

2024-02-12

- 최초 배포 시작, 에브리타임에 관련 글 게시.
- UTC 기준 매일 자정에 피드 목록을 자동적으로 갱신되도록 함.
    - GitHub Actions의 `cron` 스케쥴러 이용

2024-02-16
- UTC 기준 매일 정오에도 피드 목록을 추가로 갱신하도록 함.
    - 매일 12:00, 24:00에 두 차례 갱신

2024-02-25

- xml 주소 패턴을 `/smu-rss-feed/feed_<학과>.xml` 에서 `/smu-rss-feed/<학과>/feed.xml`로 변경.
    - 기존 url로 구독 중이던 사람들을 위해 기존 경로는 symlink로 대체하여 기존 url의 호환성을 유지함.

## 참고 문서

- <https://datatracker.ietf.org/doc/html/rfc3987>
