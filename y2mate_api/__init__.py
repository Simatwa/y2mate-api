__version__ = "0.0.1"
__info__ = "Download youtube videos and audios by title or link"
__author__ = "Smartwa"
__repo__ = "https://github.com/Simatwa/y2mate-api"
__disclaimer__ = "This script has no official relation with y2mate.com"

from .main import first_query
from .main import second_query
from .main import third_query
from .downloader import Handler

__all__ = [
    "first_query",
    "second_query",
    "third_query",
    "Handler",
]
