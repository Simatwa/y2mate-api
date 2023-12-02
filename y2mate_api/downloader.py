from .main import (
    requests,
    logging,
    utils,
    first_query,
    second_query,
    third_query,
    session,
    headers,
)
from tqdm import tqdm
from colorama import Fore
from os import path, getcwd
from threading import Thread
from sys import stdout
from click import launch as launch_media, confirm as confirm_from_user
import warnings

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
    def __init__(
        self,
        query: str,
        author: str = None,
        timeout: int = 30,
        confirm: bool = False,
        unique: bool = False,
        thread: int = 0,
    ):
        r"""Initializes this `class`
        :param query: Video name or youtube link
        :type query: str
        :param author: (Optional) Author (Channel) of the videos
        :type author: str
        :param timeout: (Optional) Http request timeout
        :type timeout: int
        :param confirm: (Optional) Confirm before downloading media
        :type confirm: bool
        :param unique: (Optional) Ignore previously downloaded media
        :type confirm: bool
        :param thread: (Optional) Thread the download process through `auto-save` method
        :type thread int
        """
        self.query = query
        self.author = author
        self.timeout = timeout
        self.keyword = None
        self.confirm = confirm
        self.unique = unique
        self.thread = thread
        self.vitems = []
        self.related = []
        self.dropped = []
        self.total = 1
        self.saved_videos = utils.get_history()

    def __str__(self):
        return self.query

    def __enter__(self, *args, **kwargs):
        return self

    def __exit__(self, *args, **kwargs):
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

    @utils.error_handler(exit_on_error=True)
    def __verify_item(self, second_query_obj) -> bool:
        video_id = second_query_obj.vid
        video_author = second_query_obj.a
        video_title = second_query_obj.title
        if video_id in self.saved_videos:
            if self.unique:
                return False, "Duplicate"
            if self.confirm:
                choice = confirm_from_user(
                    f">> Re-download : {Fore.GREEN+video_title+Fore.RESET} by {Fore.YELLOW+video_author+Fore.RESET}"
                )
                print("\n[*] Ok processing...", end="\r")
                return choice, "User's choice"
        if self.confirm:
            choice = confirm_from_user(
                f">> Download : {Fore.GREEN+video_title+Fore.RESET} by {Fore.YELLOW+video_author+Fore.RESET}"
            )
            print("\n[*] Ok processing...", end="\r")
            return choice, "User's choice"
        return True, "Auto"

    def __make_second_query(self):
        r"""Links first query with 3rd query"""
        init_query_two = second_query(self.query_one)
        x = 0
        if not self.query_one.is_link:
            for video_dict in self.vitems:
                init_query_two.video_dict = video_dict
                query_2 = init_query_two.main(timeout=self.timeout)
                if query_2.processed:
                    if query_2.vid in self.dropped:
                        continue
                    if self.author and not self.author.lower() in query_2.a.lower():
                        logging.warning(
                            f"Dropping {Fore.YELLOW+query_2.title+Fore.RESET} by  {Fore.RED+query_2.a+Fore.RESET}"
                        )
                        continue
                    else:
                        yes_download, reason = self.__verify_item(query_2)
                        if not yes_download:
                            logging.warning(
                                f"Skipping {Fore.YELLOW+query_2.title+Fore.RESET} by {Fore.MAGENTA+query_2.a+Fore.RESET} -  Reason : {Fore.BLUE+reason+Fore.RESET}"
                            )
                            self.dropped.append(query_2.vid)
                            continue
                        self.related.append(query_2.related)
                        yield query_2
                        x += 1
                        if x >= self.total:
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
                    for video_dict in self.vitems:
                        init_query_two.video_dict = video_dict
                        query_2 = init_query_two.main(timeout=self.timeout)
                        if query_2.processed:
                            if (
                                self.author
                                and not self.author.lower() in query_2.a.lower()
                            ):
                                logging.warning(
                                    f"Dropping {Fore.YELLOW+query_2.title+Fore.RESET} by  {Fore.RED+query_2.a+Fore.RESET}"
                                )
                                continue
                            else:
                                yes_download, reason = self.__verify_item(query_2)
                                if not yes_download:
                                    logging.warning(
                                        f"Skipping {Fore.YELLOW+query_2.title+Fore.RESET} by {Fore.MAGENTA+query_2.a+Fore.RESET} -  Reason : {Fore.BLUE+reason+Fore.RESET}"
                                    )
                                    self.dropped.append(query_2.vid)
                                    continue

                                self.related.append(query_2.related)
                                yield query_2
                                x += 1
                                if x >= self.total:
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
        quality: str = "auto",
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

    def generate_filename(self, third_dict: dict, naming_format: str = None) -> str:
        r"""Generate filename based on the response of `third_query`
        :param third_dict: response of `third_query.main()` object
        :param naming_format: (Optional) Format for generating filename based on `third_dict` keys
        :type third_dict: dict
        :type naming_format: str
        :rtype: str
        """
        fnm = (
            f"{naming_format}" % third_dict
            if naming_format
            else f"{third_dict['title']} {third_dict['vid']}_{third_dict['fquality']}.{third_dict['ftype']}"
        )

        def sanitize(nm):
            trash = [
                "\\",
                "/",
                ":",
                "*",
                "?",
                '"',
                "<",
                "|",
                ">",
                "y2mate.com",
                "y2mate com",
            ]
            for val in trash:
                nm = nm.replace(val, "")
            return nm.strip()

        return sanitize(fnm)

    def auto_save(
        self,
        dir: str = "",
        iterator: object = None,
        progress_bar=True,
        quiet: bool = False,
        naming_format: str = None,
        chunk_size: int = 512,
        play: bool = False,
        *args,
        **kwargs,
    ):
        r"""Query and save all the media
        :param dir: (Optional) Path to Directory for saving the media files
        :param iterator: (Optional) Function that yields third_query object - `Handler.run`
        :param progress_bar: (Optional) Display progress bar
        :param quiet: (Optional) Not to stdout anything
        :param naming_format: (Optional) Format for generating filename
        :param chunk_size: (Optional) Chunk_size for downloading files in KB
        :param play: (Optional) Auto-play the media after download
        :type dir: str
        :type iterator: object
        :type progress_bar: bool
        :type quiet: bool
        :type naming_format: str
        :type chunk_size: int
        :type play: bool
        args & kwargs for the iterator
        :rtype: None
        """
        iterator_object = iterator or self.run(*args, **kwargs)

        for x, entry in enumerate(iterator_object):
            if self.thread:
                t1 = Thread(
                    target=self.save,
                    args=(
                        entry,
                        dir,
                        False,
                        quiet,
                        naming_format,
                        chunk_size,
                        play,
                    ),
                )
                t1.start()
                thread_count = x + 1
                if thread_count % self.thread == 0 or thread_count == self.total:
                    logging.debug(
                        f"Waiting for current running threads to finish - thread_count : {thread_count}"
                    )
                    t1.join()
            else:
                self.save(
                    entry, dir, progress_bar, quiet, naming_format, chunk_size, play
                )

    def save(
        self,
        third_dict: dict,
        dir: str = "",
        progress_bar=True,
        quiet: bool = False,
        naming_format: str = None,
        chunk_size: int = 512,
        play: bool = False,
    ):
        r"""Download media based on response of `third_query` dict-data-type
        :param third_dict: Response of `third_query.run()`
        :param dir: (Optional) Directory for saving the contents
        :param progress_bar: (Optional) Display download progress bar
        :param quiet: (Optional) Not to stdout anything
        :param naming_format: (Optional) Format for generating filename
        :param chunk_size: (Optional) Chunk_size for downloading files in KB
        :param play: (Optional) Auto-play the media after download
        :type third_dict: dict
        :type dir: str
        :type progress_bar: bool
        :type quiet: bool
        :type naming_format: str
        :type chunk_size: int
        :type play: bool
        :rtype: None
        """
        if third_dict:
            assert third_dict.get(
                "dlink"
            ), "The video selected does not support that quality, try lower qualities."
            if third_dict.get("mess"):
                logging.warning(third_dict.get("mess"))
            resp = requests.get(third_dict["dlink"], stream=True, headers=headers)
            default_content_length = 1000000000
            size_in_bytes = int(
                resp.headers.get("content-length", default_content_length)
            )
            if size_in_bytes == default_content_length:
                warnings.warn(
                    f"Seems the media doesn't support that quality try {'.m4a quality' if 'mp3' in third_dict.get('f','str').lower() else 'other qualities'} or resolvers if this warning persist!"
                )
            size_in_mb = round(size_in_bytes / 1000000, 2)
            chunk_size_in_bytes = chunk_size * 1024
            filename = self.generate_filename(third_dict, naming_format)
            save_to = path.join(dir, filename)

            third_dict["saved_to"] = (
                save_to
                if any([save_to.startswith("/"), ":" in save_to])
                else path.join(getcwd(), dir, filename)
            )
            try_play_media = (
                lambda: launch_media(third_dict["saved_to"]) if play else None
            )
            if progress_bar:
                if not quiet:
                    print(f"{filename}")
                with tqdm(
                    total=size_in_bytes,
                    bar_format="%s%d MB %s{bar} %s{l_bar}%s"
                    % (Fore.GREEN, size_in_mb, Fore.CYAN, Fore.YELLOW, Fore.RESET),
                ) as p_bar:
                    with open(save_to, "wb") as fh:
                        for chunks in resp.iter_content(chunk_size=chunk_size_in_bytes):
                            fh.write(chunks)
                            p_bar.update(chunk_size_in_bytes)
                    utils.add_history(third_dict)
                    try_play_media()
                    return save_to
            else:
                with open(save_to, "wb") as fh:
                    for chunks in resp.iter_content(chunk_size=chunk_size_in_bytes):
                        fh.write(chunks)
                utils.add_history(third_dict)
                try_play_media()
                logging.info(f"{filename} - {size_in_mb}MB ✅")
                return save_to
        else:
            logging.error(f"Empty `third_dict` parameter parsed : {third_dict}")
