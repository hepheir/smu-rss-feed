# 상명대학교 공지사항 RSS Feed

매번 학과 사무실 홈페이지 찾아보기가 번거로워서 만들었는데, 만들고보니 다른 사람들에게도 좀 쓸만하지 않나 싶어서 공유합니다.

필요에 의해 만든거라 아래 3개 부서의 공지사항 밖에 없습니다. RSS 피드이니 구독할 줄 아는 사람은 알아서 잘 쓰시리라 믿습니다.

---

🔗 SW중심사업단 RSS Feed
```
https://hepheir.github.io/smu-rss-feed/swai/feed.xml
```

🔗 컴퓨터과학과 RSS Feed
```
https://hepheir.github.io/smu-rss-feed/cs/feed.xml
```

🔗 지능IOT융합전공 RSS Feed
```
https://hepheir.github.io/smu-rss-feed/aiot/feed.xml
```

---

자동 업데이트 주기는 하루 2회, 매일 자정과 정오에 업데이트 됩니다.

## Tips

저는 Feedly 라는 앱을 사용해 아래 화면과 같이 배경 위젯에 등록해두고 보는 편입니다.

iOS
- <https://apps.apple.com/kr/app/feedly-smart-news-reader/id396069556>

Android (저는 iPhone 사용자라 안드로이드에서 잘 되는지는 모르겠습니다.)
- <https://play.google.com/store/apps/details?id=com.devhd.feedly>

## RSS 피드란?

RSS 피드라는건, 간단하게 말하면 게시판 내용을 XML 이라는 파일 형식으로 인터넷 사이트가 제공하는 거에요.

RSS 형태로 제공되는 XML을 읽기 위해 사용하는 프로그램을 'RSS 리더'라고 하는데,
이는 PC나 모바일기기에서 내가 구독하고자 하는 사이트가 제공하는 RSS 피드(XML 파일)을 주기적으로 읽어와
추가된 내용이 있는지 정리해서 사용자한테 보여주는 것이구요.

제가 주로 쓰는 RSS 리더 중 하나가 Feedly인 셈입니다.

![모바일 배경화면 위젯](https://github.com/hepheir/smu-rss-feed/assets/19310326/3a63bd0e-8f15-40fb-869b-5e498a702fa8)

Feedly 앱에서 피드를 등록하는 방법은 아래 설명을 참고하시기 바랍니다.

![Feedly 위젯 등록 방법](https://github.com/hepheir/smu-rss-feed/assets/19310326/52c8e772-dc3d-4bad-9455-ca3e25877125)

위 과정을 통해 위젯을 생성하면 첫 번째 사진과 같은 모습이 됩니다.

![iPad에서 응용](https://github.com/hepheir/smu-rss-feed/assets/19310326/d4fe0da9-cbd1-4dda-860a-7c399e5c4854)

응용하면 이렇게 패드에서 모아놓고 볼 수도 있습니다.

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
