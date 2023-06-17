# y2mate-api

<p align="center">
<a href="https://github.com/Simatwa/y2mate-api"><img alt="Github" src="https://img.shields.io/static/v1?logo=github&color=blueviolet&label=Test&message=Passing"/></a>
<a href="LICENSE"><img alt="License" src="https://img.shields.io/static/v1?logo=GPL&color=Blue&message=MIT&label=License"/></a>
<a href="https://pypi.org/project/y2mate-api"><img alt="PyPi" src="https://img.shields.io/static/v1?logo=pypi&label=Pypi&message=v0.0.3&color=green"/></a>
<a href="https://github.com/psf/black"><img alt="Black" src="https://img.shields.io/static/v1?logo=Black&label=Code-style&message=Black"/></a>
<a href="#"><img alt="Passing" src="https://img.shields.io/static/v1?logo=Docs&label=Docs&message=Passing&color=green"/></a>
<a href="#"><img alt="coverage" src="https://img.shields.io/static/v1?logo=Coverage&label=Coverage&message=90%&color=yellowgreen"/></a>
<a href="#" alt="progress"><img alt="Progress" src="https://img.shields.io/static/v1?logo=Progress&label=Progress&message=95%&color=green"/></a>
<a href="https://pepy.tech/project/livescore-api"><img src="https://static.pepy.tech/personalized-badge/y2mate-api?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads" alt="Downloads"></a>
</p>

> Download youtube videos and audios by **title/id/url**

# Installation

- Either of the following ways will get you ready.

1. Pip

  a. From source

```sh
pip install git+https://github.com/Simatwa/y2mate-api.git
```
  b. From pypi

```sh
pip install y2mate-api
```

2. Locally

```sh
git clone https://github.com/Simatwa/y2mate-api.git
cd y2mate-api
python setup.py build
python setup.py install
```

# Usage 

`$ y2mate <youtube-link or video id or keyword>`

<details>
<summary>
Developer docs
</summary>
1.Generate download links and other metadata

- Video

```py
from y2mate_api import Handler
api = Handler("Quantum computing in detail")
for video_metadata in api.run():
	print(video_metadata)
"""Output
{
    "size": "13.9 MB",
    "f": "mp4",
    "q": "720p",
    "q_text": "720p (.mp4) <span class=\"label label-primary\"><small>m-HD</small></span>",
    "k": "joQdX4S3z8ShOJWn6qaA9sL4Al7j4vBwhNgqkwx0U/tQ99R4mbX1dYceffBBnNn7",
    "status": "ok",
    "mess": "",
    "c_status": "CONVERTED",
    "vid": "X8MZWCGgIb8",
    "title": "Quantum Computing In 5 Minutes | Quantum Computing Explained | Quantum Computer |Simplilearn",
    "ftype": "mp4",
    "fquality": "720",
    "dlink": "https://rr2---sn-gjo-w43s.googlevideo.com/videoplayback?expire=1686946638&ei=7m6MZK-2NdKQgAepgJGIBg&ip=212.119.40.85&id=o-ADe3hAAtGl6fkEeUD9HKkFNoeQBSwEuttoN5vFPyzLdQ&itag=22&source=youtube&requiressl=yes&mh=Zy&mm=31%2C29&mn=sn-gjo-w43s%2Csn-ab5l6nr6&ms=au%2Crdu&mv=m&mvi=2&pl=23&initcwndbps=1013750&spc=qEK7B_bA4LnIWnJEJPO8Lp__Gz-ysFYRbF7IYj1J5g&vprv=1&svpuc=1&mime=video%2Fmp4&ns=L1NG4wpa6rJJmunA_QDUTswN&cnr=14&ratebypass=yes&dur=298.608&lmt=1682850029743273&mt=1686924560&fvip=1&fexp=24007246&c=WEB&txp=5311224&n=XD35AJLYPy2nng&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cspc%2Cvprv%2Csvpuc%2Cmime%2Cns%2Ccnr%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRQIhAJdMdpsMBBByQZCOIglT_EvluXBK2wQ7mH32Ob95WAWJAiAP9PfGRwJKeJcZJXc5ZuVaZMImCAXCnbPcHyoSmRhH4A%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRQIgAMVlWxHYtKeZEzbpKQ9Huqrk-5CQ0kTpSFgAmTIGaE4CIQDR0NJHxHO_TtRbn-HmDOgVD6H3ZUntvgcD1V5yfkngAA%3D%3D&title=Quantum+Computing+In+5+Minutes+%7C+Quantum+Computing+Explained+%7C+Quantum+Computer+%7C+Simplilearn"
}
"""
```

- Audio

```py
from y2mate_api import Handler
api = Handler("Quantum computing in detail")
for audio_metadata in api.run(format="mp3"):
	print(audio_metadata)

"""Output

{
    "size": "4.6 MB",
    "f": "mp3",
    "q": "128kbps",
    "q_text": "MP3 - 128kbps",
    "k": "joQdX4S3z8ShOJWn6qaA9sL4Al7j4vBwhNgqlAxyU/NQ99R4mbX1dYceffBBnNn7",
    "status": "ok",
    "mess": "",
    "c_status": "CONVERTED",
    "vid": "X8MZWCGgIb8",
    "title": "Quantum Computing In 5 Minutes | Quantum Computing Explained | Quantum Computer |Simplilearn",
    "ftype": "mp3",
    "fquality": "128",
    "dlink": "https://dl201.dlmate53.xyz/?file=M3R4SUNiN3JsOHJ6WWQ2a3NQS1Y5ZGlxVlZIOCtyZ1ZqZFEwMHdVdVNvaERxNTA2dysydUpJSm1JT3hhaHFlckg4dEE4QzJUT3VHZU1RR2RvNVZ0WVh5TTU4TXBzREhJdUtzNFNjVndYeGo5bjYzb3B5UjNoeFBnYzVQdUdyVkdlR04rc1F0UTJpdUR3UGpZdkJUcXZUT2d0eDdGYWkwR3R3UWJQT0hZck5vYTgzREVldVB4MFpWQS93Q1M4c2tNaU5hWThWUFErK29UZ3V0V2VVTmRjY2dUMUlxbW1mZkpxaG95cGQ4WndsMnR1K2V5RDVNd1FmVElJV0VwYkhwUXVieXBUaDRZOENZVy9XKzFxLzVqL1drVGRQMGhzREhucXFDNElDeU9JOGIwSHNBPQ%3D%3D"
}
"""
```
- **Note** : To download the media returned, pass the response to `api.save()`

2. Auto-download media

```py
from y2mate_api import Handler
api = Handler("Quantum computing in detail")
api.auto_save()
```
This will proceed to download the first video found and save it in the `current directory`

You can as well specify total videos to be downloaded by using `limit` argument.
For instance:

```py
from y2mate_api import Handler
api = Handler("https://youtu.be/POPoAjWFkGg")
api.auto_save(limit=10)
# This will download the video in path and 9 other videos related to the query specified
```
**Note** : You can still use  **video id** such as `POPoAjWFkGg` as query parameter.

## Other parameters

- `Handler`
  * author : Video author i.e Youtube Channel
  * timeout : http requests timeout
  * ask : Confirm before downloading media
  * unique : Auto-ignore previously downloaded media

- `Handler.run`
  * format : Media format mp4/mp3
  * quality : Media qualiy such as 720p/128kbps
  * resolver : Additional format info : [m4a,3gp,mp4,mp3]
  * limit : Total videos to be retrieved
  * keyword : Phrase(s) that must be in media title
  * author : Video author i.e Youtube Channel

- `Handler.auto_save`
  * dir : Path to Directory for saving the media files
  * iterator : Function that yields third_query object - `Handler.run`
  * progress_bar : Stdout media-name & Display progress bar
 
- `Handler.save`
  * third_dict : Response of `third_query.run()`
  * dir : Directory for saving the contents
  * progress_bar : Stdout media-name & Display download progress bar
 
</details>
 
<details>
<summary>
	
For more info run `$ y2mate -h`

</summary>

```
usage: y2mate [-h] [-v] [-f mp4|mp3]
              [-q 4k|1080p|720p|480p|360p|240p|144p|auto|mp3|m4a|.m4a|128kbps|192kbps|328kbps]
              [-r m4a|3gp|mp4|mp3] [-k [KEYWORD ...]]
              [-a [AUTHOR ...]] [-l LIMIT] [-d PATH]
              [-t TIMEOUT] [-i PATH] [-thr THREAD]
              [--disable-bar] [--ask] [--unique] [--quiet]
              [--history] [--clear]
              [query ...]

Download youtube videos and audios by title or link

positional arguments:
  query                 Youtube video title, link or id - None

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -f mp4|mp3, --format mp4|mp3
                        Specify media type - audio/video
  -q 4k|1080p|720p|480p|360p|240p|144p|auto|mp3|m4a|.m4a|128kbps|192kbps|328kbps, --quality 4k|1080p|720p|480p|360p|240p|144p|auto|mp3|m4a|.m4a|128kbps|192kbps|328kbps
                        Media quality -720p
  -r m4a|3gp|mp4|mp3, --resolver m4a|3gp|mp4|mp3
                        Other media formats incase of multiple
                        options - mp4/mp3
  -k [KEYWORD ...], --keyword [KEYWORD ...]
                        Media should contain this keywords -
                        None
  -a [AUTHOR ...], --author [AUTHOR ...]
                        Media author i.e YouTube channel name -
                        None
  -l LIMIT, --limit LIMIT
                        Total videos to be downloaded - 1
  -d PATH, --dir PATH   Directory for saving the contents -
                        /storage/emulated/0/git/Smartwa
  -t TIMEOUT, --timeout TIMEOUT
                        Http request timeout - 30s
  -i PATH, --input PATH
                        Path to text file containing query per
                        line - None
  -thr THREAD, --thread THREAD
                        Download [x] amount of videos/audios at
                        once - 1
  --disable-bar         Disables download progress bar - False
  --ask                 Confirm before downloading file - False
  --unique              Auto-skip any media that you once
                        dowloaded - False
  --quiet               Not to stdout anything other than logs -
                        False
  --history             Stdout all media metadata ever
                        downloaded - False
  --clear               Clear all download histories - False

This script has no official relation with y2mate.com
```
</details>

- Review [CHANGELOG](https://github.com/Simatwa/y2mate-api/blob/main/Docs/CHANGELOG.md) for latest updates.

## Disclaimer

This repository is intended for educational and personal use only. The use of this repository for any commercial or illegal purposes is strictly prohibited. The repository owner does not endorse or encourage the downloading or sharing of copyrighted material without permission. The repository owner is not responsible for any misuse of the software or any legal consequences that may arise from such misuse.
