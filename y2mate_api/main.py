# import requests
from curl_cffi import requests
import logging
from time import sleep
import json
from os import path, makedirs
from datetime import datetime
from appdirs import AppDirs
from sys import exit

__prog__ = "y2mate"
session = requests.Session()

headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9",
    "referer": "https://y2mate.com",
}

session.headers.update(headers)

get_excep = lambda e: e.args[1] if len(e.args) > 1 else e

appdir = AppDirs(__prog__)

if not path.isdir(appdir.user_cache_dir):
    try:
        makedirs(appdir.user_cache_dir)
    except Exception as e:
        print(
            f"Error : {get_excep(e)}  while creating site directory - "
            + appdir.user_cache_dir
        )

history_path = path.join(appdir.user_cache_dir, "history.json")


class utils:
    @staticmethod
    def error_handler(resp=None, exit_on_error=False, log=True):
        r"""Exception handler decorator"""

        def decorator(func):
            def main(*args, **kwargs):
                try:
                    try:
                        return func(*args, **kwargs)
                    except KeyboardInterrupt as e:
                        print()
                        logging.info(f"^KeyboardInterrupt quitting. Goodbye!")
                        exit(1)
                except Exception as e:
                    if log:
                        # logging.exception(e)
                        logging.debug(f"Function ({func.__name__}) : {get_excep(e)}")
                        logging.error(get_excep(e))
                    if exit_on_error:
                        exit(1)

                    return resp

            return main

        return decorator

    @staticmethod
    def get(*args, **kwargs):
        r"""Sends http get request"""
        kwargs["impersonate"] = "chrome"
        resp = session.get(*args, **kwargs)
        return all([resp.ok, "application/json" in resp.headers["content-type"]]), resp

    @staticmethod
    def post(*args, **kwargs):
        r"""Sends http post request"""
        kwargs["impersonate"] = "chrome"
        resp = session.post(*args, **kwargs)
        return all([resp.ok, "application/json" in resp.headers["content-type"]]), resp

    @staticmethod
    def add_history(data: dict) -> None:
        f"""Adds entry to history
        :param data: Response of `third query`
        :type data: dict
        :rtype: None
        """
        try:
            if not path.isfile(history_path):
                data1 = {__prog__: []}
                with open(history_path, "w") as fh:
                    json.dump(data1, fh)
            with open(history_path) as fh:
                saved_data = json.load(fh).get(__prog__)
            data["datetime"] = datetime.now().strftime("%c")
            saved_data.append(data)
            with open(history_path, "w") as fh:
                json.dump({__prog__: saved_data}, fh, indent=4)
        except Exception as e:
            logging.error(f"Failed to add to history - {get_excep(e)}")

    @staticmethod
    def get_history(dump: bool = False) -> list:
        r"""Loads download history
        :param dump: (Optional) Return whole history as str
        :type dump: bool
        :rtype: list|str
        """
        try:
            resp = []
            if not path.isfile(history_path):
                data1 = {__prog__: []}
                with open(history_path, "w") as fh:
                    json.dump(data1, fh)
            with open(history_path) as fh:
                if dump:
                    return json.dumps(json.load(fh), indent=4)
                entries = json.load(fh).get(__prog__)
            for entry in entries:
                resp.append(entry.get("vid"))
            return resp
        except Exception as e:
            logging.error(f"Failed to load history - {get_excep(e)}")
            return []


class first_query:
    def __init__(self, query: str):
        r"""Initializes first query class
        :param query: Video name or youtube link
        :type query: str
        """
        self.query_string = query
        self.url = "https://www.y2mate.com/mates/analyzeV2/ajax"
        self.payload = self.__get_payload()
        self.processed = False
        self.is_link = False

    def __get_payload(self):
        return {
            "hl": "en",
            "k_page": "home",
            "k_query": self.query_string,
            "q_auto": "0",
        }

    def __str__(self):
        return """
{    
    "page": "search",
    "status": "ok",
    "keyword": "happy birthday",
    "vitems": [
        {
            "v": "_z-1fTlSDF0",
            "t": "Happy Birthday song"
        },
     ]
}"""

    def __enter__(self, *args, **kwargs):
        return self.__call__(*args, **kwargs)

    def __exit__(self, *args, **kwargs):
        self.processed = False

    def __call__(self, timeout: int = 30):
        return self.main(timeout)

    def main(self, timeout=30):
        r"""Sets class attributes
        :param timeout: (Optional) Http requests timeout
        :type timeout: int
        """
        logging.debug(f"Making first query  : {self.payload.get('k_query')}")
        okay_status, resp = utils.post(self.url, data=self.payload, timeout=timeout)
        # print(resp.headers["content-type"])
        # print(resp.content)
        if okay_status:
            dict_data = resp.json()
            self.__setattr__("raw", dict_data)
            for key in dict_data.keys():
                self.__setattr__(key, dict_data.get(key))
            self.is_link = not hasattr(self, "vitems")
            self.processed = True
        else:
            logging.debug(f"{resp.headers.get('content-type')} - {resp.content}")
            logging.error(f"First query failed - [{resp.status_code} : {resp.reason}]")
            if session.cookies.get("cf_clearance"):
                logging.info("Seems like CF-CLEARANCE cookie has expired!")
            else:
                logging.info("Try passing CF-CLEARANCE cookie.")
        return self


class second_query:
    def __init__(self, query_one: object, item_no: int = 0):
        r"""Initializes second_query class
        :param query_one: Query_one class
        :type query_one: object
        :param item_no: (Optional) Query_one.vitems index
        :type item_no: int
        """
        assert query_one.processed, "First query failed"

        self.query_one = query_one
        self.item_no = item_no
        self.processed = False
        self.video_dict = None
        self.url = "https://www.y2mate.com/mates/analyzeV2/ajax"
        # self.payload  = self.__get_payload()

    def __str__(self):
        return """
{
    "status": "ok",
    "mess": "",
    "page": "detail",
    "vid": "_z-1fTlSDF0",
    "extractor": "youtube",
    "title": "Happy Birthday song",
    "t": 62,
    "a": "infobells",
    "links": {
        "mp4": {
            "136": {
                "size": "5.5 MB",
                "f": "mp4",
                "q": "720p",
                "q_text": "720p (.mp4) <span class=\"label label-primary\"><small>m-HD</small></span>",
                "k": "joVBVdm2xZWhaZWhu6vZ8cXxAl7j4qpyhNgqkwx0U/tcutx/harxdZ8BfPNcg9n1"
            },
         },
        "mp3": {
            "140": {
                "size": "975.1 KB",
                "f": "m4a",
                "q": ".m4a",
                "q_text": ".m4a (128kbps)",
                "k": "joVBVdm2xZWhaZWhu6vZ8cXxAl7j4qpyhNhuxgxyU/NQ9919mbX2dYcdevRBnt0="
            }, 
         },
    "related": [
        {
            "title": "Related Videos",
            "contents": [
                {
                    "v": "KK24ZvxLXGU",
                    "t": "Birthday Songs - Happy Birthday To You | 15 minutes plus"
                },
   ]
        }
    ]
}                 
            		"""

    def __call__(self, *args, **kwargs):
        return self.main(*args, **kwargs)

    def get_item(self, item_no=0):
        r"""Return specific items on `self.query_one.vitems`"""
        if self.video_dict:
            return self.video_dict
        if self.query_one.is_link:
            return {"v": self.query_one.vid, "t": self.query_one.title}
        all_items = self.query_one.vitems
        assert (
            self.item_no < len(all_items) - 1
        ), "The item_no  is greater than largest item's index -  try lower value"

        return self.query_one.vitems[item_no or self.item_no]

    def get_payload(self):
        return {
            "hl": "en",
            "k_page": "home",
            "k_query": f"https://www.youtube.com/watch?v={self.get_item().get('v')}",
            "q_auto": "1",
        }

    def __main__(self, *args, **kwargs):
        return self.main(*args, **kwargs)

    def __enter__(self, *args, **kwargs):
        return self.__main__(*args, **kwargs)

    def __exit__(self, *args, **kwargs):
        self.processed = False

    def main(self, item_no: int = 0, timeout: int = 30):
        r"""Requests for video formats and related videos
        :param item_no: (Optional) Index of query_one.vitems
        :type item_no: int
        :param timeout:  (Optional)Http request timeout
        :type timeout: int
        """
        self.processed = False
        if item_no:
            self.item_no = item_no
        okay_status, resp = utils.post(
            self.url, data=self.get_payload(), timeout=timeout
        )

        if okay_status:
            dict_data = resp.json()
            for key in dict_data.keys():
                self.__setattr__(key, dict_data.get(key))
            links = dict_data.get("links")
            self.__setattr__("video", links.get("mp4"))
            self.__setattr__("audio", links.get("mp3"))
            self.__setattr__("related", dict_data.get("related")[0].get("contents"))
            self.__setattr__("raw", dict_data)
            self.processed = True

        else:
            logging.debug(f"{resp.headers.get('content-type')} - {resp.content}")
            logging.error(f"Second query failed - [{resp.status_code} : {resp.reason}]")
        return self


class third_query:
    def __init__(self, query_two: object):
        assert query_two.processed, "Unprocessed second_query object parsed"
        self.query_two = query_two
        self.url = "https://www.y2mate.com/mates/convertV2/index"
        self.formats = ["mp4", "mp3"]
        self.qualities_plus = ["best", "worst"]
        self.qualities = {
            self.formats[0]: [
                "4k",
                "1440p",
                "1080p",
                "720p",
                "480p",
                "360p",
                "240p",
                "144p",
                "auto",
            ]
            + self.qualities_plus,
            self.formats[1]: ["mp3", "m4a", ".m4a", "128kbps", "192kbps", "328kbps"],
        }

    def __call__(self, *args, **kwargs):
        return self.main(*args, **kwargs)

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
        pass

    def __str__(self):
        return """
{
    "status": "ok",
    "mess": "",
    "c_status": "CONVERTED",
    "vid": "_z-1fTlSDF0",
    "title": "Happy Birthday song",
    "ftype": "mp4",
    "fquality": "144p",
    "dlink": "https://dl165.dlmate13.online/?file=M3R4SUNiN3JsOHJ6WWQ2a3NQS1Y5ZGlxVlZIOCtyZ01tY1VxM2xzQkNMbFlyb2t1enErekxNZElFYkZlbWQ2U1g5TkVvWGplZU55T0R4K0lvcEI3QnlHbjd0a29yU3JOOXN0eWY4UmhBbE9xdmI3bXhCZEprMHFrZU96QkpweHdQVWh0OGhRMzQyaWUzS1dTdmhEMzdsYUk0VWliZkMwWXR5OENNUENOb01rUWd6NmJQS2UxaGRZWHFDQ2c0WkpNMmZ2QTVVZmx5cWc3NVlva0Nod3NJdFpPejhmeDNhTT0%3D"
}
"""

    def get_payload(self, keys):
        return {"k": keys.get("k"), "vid": self.query_two.vid}

    def main(
        self,
        format: str = "mp4",
        quality="auto",
        resolver: str = None,
        timeout: int = 30,
    ):
        r"""
        :param format: (Optional) Media format mp4/mp3
        :param quality: (Optional) Media qualiy such as 720p
        :param resolver: (Optional) Additional format info : [m4a,3gp,mp4,mp3]
        :param timeout: (Optional) Http requests timeout
        :type type: str
        :type quality: str
        :type timeout: int
        """
        if not resolver:
            resolver = "mp4" if format == "mp4" else "mp3"
        if format == "mp3" and quality == "auto":
            quality = "128kbps"
        assert (
            format in self.formats
        ), f"'{format}' is not in supported formats - {self.formats}"

        assert (
            quality in self.qualities[format]
        ), f"'{quality}' is not in supported qualities - {self.qualities[format]}"

        items = self.query_two.video if format == "mp4" else self.query_two.audio
        hunted = []
        if quality in self.qualities_plus:
            keys = list(items.keys())
            if quality == self.qualities_plus[0]:
                hunted.append(items[keys[0]])
            else:
                hunted.append(items[keys[len(keys) - 2]])
        else:
            for key in items.keys():
                if items[key].get("q") == quality:
                    hunted.append(items[key])
        if len(hunted) > 1:
            for entry in hunted:
                if entry.get("f") == resolver:
                    hunted.insert(0, entry)
        if hunted:

            def hunter_manager(souped_entry: dict = hunted[0], repeat_count=0):
                payload = self.get_payload(souped_entry)
                okay_status, resp = utils.post(self.url, data=payload)
                if okay_status:
                    sanitized_feedback = resp.json()
                    if sanitized_feedback.get("c_status") == "CONVERTING":
                        if repeat_count >= 4:
                            return (False, {})
                        else:
                            logging.debug(
                                f"Converting video  : sleeping for 5s - round {repeat_count+1}"
                            )
                            sleep(5)
                            repeat_count += 1
                            return hunter_manager(souped_entry)
                    return okay_status, resp
                return okay_status, resp

            okay_status, resp = hunter_manager()

            if okay_status:
                resp_data = hunted[0]
                resp_data.update(resp.json())
                return resp_data

            else:
                logging.debug(f"{resp.headers.get('content-type')} - {resp.content}")
                logging.error(
                    f"Third query failed - [{resp.status_code} : {resp.reason}]"
                )
                return {}
        else:
            logging.error(
                f"Zero media hunted with params : {{quality : {quality}, format : {format}  }}"
            )
            return {}
