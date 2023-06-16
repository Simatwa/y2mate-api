from .main import requests, logging, utils, first_query, second_query, third_query
from tqdm import tqdm
from colorama import Fore
from os import path

"""
- query string
- format mp4/3
- quality 720p/128kbps
- keywords
- Specify video author
- download related
- max-video limit
- min-video quality
- max-video quality
- path to file containing links
"""


class Handler:
    def __init__(self, query: str, author: str = None, timeout: int = 30):
        r"""Initializes this `class`
        :param query: Video name or youtube link
        :type query: str
        :param author: (Optional) Author (Channel) of the videos
        :type author: str
        :param timeout: (Optional) Http request timeout
        :type timeout: int
        """
        self.query = query
        self.author = author
        self.timeout = timeout
        self.keyword = None
        self.vitems = []
        self.related = []
        self.total = 1

    def __str__(self):
        return self.query

    def __enter__(self):
        pass

    def __exit__(self):
        self.vitems.clear()
        self.total = 1

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def __filter_videos(self, entries: list) -> list:
        f"""Filter videos based on keyword
        :param entries: List containing dict of video id and their titles
        :type entries: list
        :rtype: list
        """
        if self.keyword:
            keyword = self.keyword.lower()
            resp = []
            for entry in entries:
                if keyword in entry.get("t").lower():
                    resp.append(entry)
            return resp

        else:
            return entries

    def __make_first_query(self):
        r"""Sets query_one attribute to `self`"""
        query_one = first_query(self.query)
        self.__setattr__("query_one", query_one.main(self.timeout))
        if self.query_one.is_link == False:
            self.vitems.extend(self.__filter_videos(self.query_one.vitems))

    def __make_second_query(self):
        r"""Links first query with 3rd query"""
        init_query_two = second_query(self.query_one)
        if not self.query_one.is_link:
            for x, video_dict in enumerate(self.vitems):
                init_query_two.video_dict = video_dict
                query_2 = init_query_two.main(timeout=self.timeout)
                if query_2.processed:
                    if self.author and not self.author.lower() in query_2.a.lower():
                        logging.warning(f"Dropping '{query_2.title}' by  '{query_2.a}'")
                        continue
                    else:
                        self.related.append(query_2.related)
                        yield query_2
                        if x + 1 >= self.total:
                            break
                else:
                    logging.warning(
                        f"Dropping unprocessed query_two object of index {x}"
                    )

        else:
            query_2 = init_query_two.main(timeout=self.timeout)
            if query_2.processed:
                # self.related.extend(query_2.related)
                self.vitems.extend(query_2.related)
                self.query_one.is_link = False
                if self.total == 1:
                    yield query_2
                else:
                    for x, video_dict in enumerate(self.vitems):
                        init_query_two.video_dict = video_dict
                        query_2 = init_query_two.main(timeout=self.timeout)
                        if query_2.processed:
                            if (
                                self.author
                                and not self.author.lower() in query_2.a.lower()
                            ):
                                logging.warning(
                                    f"Dropping '{query_2.title}' by  '{query_2.a}'"
                                )
                                continue
                            else:
                                self.related.append(query_2.related)
                                yield query_2
                                if x + 1 >= self.total:
                                    break
                        else:
                            logging.warning(
                                f"Dropping unprocessed query_two object of index {x}"
                            )
                            yield
            else:
                logging.warning("Dropping unprocessed query_two object")
                yield

    def run(
        self,
        format: str = "mp4",
        quality: str = "720p",
        resolver: str = None,
        limit: int = 1,
        keyword: str = None,
        author: str = None,
    ):
        r"""Generate and yield video dictionary
        :param format: (Optional) Media format mp4/mp3
        :param quality: (Optional) Media qualiy such as 720p/128kbps
        :param resolver: (Optional) Additional format info : [m4a,3gp,mp4,mp3]
        :param limit: (Optional) Total videos to be generated
        :param keyword: (Optional) Video keyword
        :param author: (Optional) Author of the videos
        :type quality: str
        :type total: int
        :type keyword: str
        :type author: str
        :rtype: object
        """
        self.author = author
        self.keyword = keyword
        self.total = limit
        self.__make_first_query()
        for query_two_obj in self.__make_second_query():
            if query_two_obj:
                self.vitems.extend(query_two_obj.related)
                yield third_query(query_two_obj).main(
                    **dict(
                        format=format,
                        quality=quality,
                        resolver=resolver,
                        timeout=self.timeout,
                    )
                )
            else:
                logging.error(f"Empty object - {query_two_obj}")

    def generate_filename(self, third_dict: dict, format: str = None) -> str:
        r"""Generate filename based on the response of `third_query`
        :param third_dict: response of `third_query.main()` object
        :param format: Format for formatting fnm based on `third_dict` keys
        :type third_dict: dict
        :type format: str
        :rtype: str
        """
        fnm = (
            f"{format}" % third_dict
            if format
            else f"{third_dict['title']} {third_dict['vid']}_{third_dict['fquality']}.{third_dict['ftype']}"
        )
        return fnm

    def auto_save(
        self, dir: str = "", iterator: object = None, progress_bar=True, *args, **kwargs
    ):
        r"""Query and save all the media
        :param dir: Path to Directory for saving the media files
        :param iterator: Function that yields third_query object - `Handler.run`
        :param progress_bar: Display progress bar
        :type dir: str
        :type iterator: object
        :type progress_bar: bool
        args & kwargs for the iterator
        :rtype: None
        """
        iterator_object = iterator or self.run(*args, **kwargs)

        for entry in iterator_object:

            self.save(entry, dir, progress_bar)

    def save(self, third_dict: dict, dir: str = "", progress_bar=True):
        r"""Download media based on response of `third_query` dict-data-type
        :param third_dict: Response of `third_query.main()`
        :param dir: Directory for saving the contents
        :param progress_bar: Display download progress bar
        :type third_dict: dict
        :type dir: str
        :type progress_bar: bool
        :rtype: None
        """
        if third_dict:
            resp = requests.get(third_dict["dlink"], stream=True)
            size_in_bits = int(resp.headers["content-length"])
            size_in_mb = round(size_in_bits / 1000000, 2)
            chunk_size = 1024
            filename = self.generate_filename(third_dict)

            if progress_bar:
                print(f"{filename}")
                with tqdm(
                    total=size_in_bits,
                    bar_format="%s%d MB %s{bar} %s{l_bar}%s"
                    % (Fore.GREEN, size_in_mb, Fore.CYAN, Fore.YELLOW, Fore.RESET),
                ) as p_bar:
                    with open(path.join(dir, filename), "wb") as fh:
                        for chunks in resp.iter_content(chunk_size=chunk_size):
                            fh.write(chunks)
                            p_bar.update(chunk_size)
            else:
                with open(path.join(dir, filename), "wb") as fh:
                    for chunks in resp.iter_content(chunk_size=chunk_size):
                        fh.write(chunks)
                        p_bar.update(chunk_size)
        else:
            logging.error(f"Empty `third_dict` parameter parsed : {third_dict}")
