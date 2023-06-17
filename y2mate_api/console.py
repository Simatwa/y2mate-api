import argparse
import logging
from . import __version__, __info__, __disclaimer__
from .main import utils
from os import getcwd, remove
from sys import exit
from .main import history_path, utils

mp4_qualities = [
    "4k",
    "1080p",
    "720p",
    "480p",
    "360p",
    "240p",
    "144p",
    "auto",
]
mp3_qualities = ["mp3", "m4a", ".m4a", "128kbps", "192kbps", "328kbps"]
resolvers = ["m4a", "3gp", "mp4", "mp3"]
media_qualities = mp4_qualities + mp3_qualities
logging.basicConfig(
    format="%(asctime)s - %(levelname)s : %(message)s",
    datefmt="%H:%M:%S",
    level=logging.INFO,
)


def get_args():
    parser = argparse.ArgumentParser(
        description=__info__, epilog=__disclaimer__, add_help=True, exit_on_error=True
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s v{__version__}"
    )
    parser.add_argument(
        "query", nargs="*", help="Youtube video title, link or id - %(default)s"
    )
    parser.add_argument(
        "-f",
        "--format",
        help="Specify media type - audio/video",
        choices=["mp4", "mp3"],
        metavar="mp4|mp3",
    )
    parser.add_argument(
        "-q",
        "--quality",
        help="Media quality -%(default)s",
        choices=media_qualities,
        metavar="|".join(media_qualities),
        default="720p",
    )
    parser.add_argument(
        "-r",
        "--resolver",
        help="Other media formats incase of multiple options - mp4/mp3",
        choices=resolvers,
        metavar="|".join(resolvers),
    )
    parser.add_argument(
        "-k",
        "--keyword",
        nargs="*",
        help="Media should contain this keywords - %(default)s",
    )
    parser.add_argument(
        "-a",
        "--author",
        nargs="*",
        help="Media author i.e YouTube channel name - %(default)s",
    )
    parser.add_argument(
        "-l",
        "--limit",
        help="Total videos to be downloaded - %(default)s",
        type=int,
        default=1,
    )
    parser.add_argument(
        "-d",
        "--dir",
        help="Directory for saving the contents - %(default)s",
        default=getcwd(),
        metavar="PATH",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        help="Http request timeout - %(default)ss",
        type=int,
        default=30,
    )
    parser.add_argument(
        "-i",
        "--input",
        help="Path to text file containing query per line - %(default)s",
        metavar="PATH",
    )
    parser.add_argument(
        "-thr",
        "--thread",
        help="Download [x] amount of videos/audios at once - 1",
        type=int,
        default=0,
    )
    parser.add_argument(
        "--disable-bar",
        help="Disables download progress bar - %(default)s",
        action="store_true",
    )
    parser.add_argument(
        "--ask",
        help="Confirm before downloading file - %(default)s",
        action="store_true",
    )
    parser.add_argument(
        "--unique",
        help="Auto-skip any media that you once dowloaded - %(default)s",
        action="store_true",
    )
    parser.add_argument(
        "--quiet",
        help="Not to stdout anything other than logs - %(default)s",
        action="store_true",
    )
    parser.add_argument(
        "--history",
        help="Stdout all media metadata ever downloaded - %(default)s",
        action="store_true",
    )
    parser.add_argument(
        "--clear",
        help="Clear all download histories - %(default)s",
        action="store_true",
    )
    return parser.parse_args()


@utils.error_handler(exit_on_error=True)
def main():
    args = get_args()
    from . import Handler

    if args.history:
        print(utils.get_history(dump=True))
        exit(0)
    if args.clear:
        remove(history_path)
        logging.info("Histories cleared successfully!")
        exit(0)
    if not args.format:
        raise Exception("You must specify media format [ -f mp3/4]")
    h_mult_args = lambda v: v if not v else " ".join(v)
    handler_init_args = dict(
        query=h_mult_args(args.query),
        author=args.author,
        timeout=args.timeout,
        ask=args.ask,
        unique=args.unique,
        thread=args.thread,
    )
    auto_save_args = dict(
        dir=args.dir,
        progress_bar=args.disable_bar == False,
        quiet=args.quiet,
        format=args.format,
        quality=args.quality,
        resolver=args.resolver,
        limit=args.limit,
        keyword=h_mult_args(args.keyword),
        author=h_mult_args(args.author),
    )
    logging.info(f"y2mate launched - v{__version__}")
    if args.input:
        for query in open(args.input).read().strip().split("\n"):
            handler_init_args["query"] = query
            auto_save_args["limit"] = 1
            Handler(**handler_init_args).auto_save(**auto_save_args)
    else:
        Handler(**handler_init_args).auto_save(**auto_save_args)
    logging.info(
        f"Done downloading [{args.limit}] {'audio' if args.format=='mp3' else 'video'}(s)"
    )
