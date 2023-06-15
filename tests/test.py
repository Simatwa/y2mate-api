from y2mate_api import first_query
from y2mate_api.main import utils

@utils.error_handler()
def main():
	run = first_query("https://youtu.be/POPoAjWFkGg")
	obj=run()
	import json 
	with open("test.json","w") as fh:
		json.dump(obj.raw,fh,indent=4)
main()