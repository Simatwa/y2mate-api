from y2mate_api import Handler

import logging

logging.basicConfig(format="%(asctime)s - %(levelname)s - %(message)s",level=logging.INFO,datefmt="%H:%M:%S")

run = Handler(query="Etana weekness in me")
resp = run.run(format="mp3",limit=1)
for v in resp:
	run.save(v)