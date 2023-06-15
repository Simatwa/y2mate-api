from y2mate_api import Handler

import logging

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",level=logging.INFO,datefmt="%H:%M:%S")

run = Handler(query="Zuchu Nani",)
run.auto_save(format="mp3",keyword="official music",author="zuchu")