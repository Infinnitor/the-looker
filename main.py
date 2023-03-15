import sys
import os
import the_looker
import traceback

from the_looker import DirectoryLooker, DirectoryLookerSync

def main(args):
	assert len(args) > 1, "No args"
	if len(args) < 3:
		args.append(".")

	BASE_PATH = args[2]
	SYNC_PATH = args[1]

	if os.path.exists(SYNC_PATH):
		if len(os.listdir(SYNC_PATH)) != 0:
			assert False, "Sync path must be empty"

	dir_watch = DirectoryLookerSync(BASE_PATH, SYNC_PATH)

	try:
		dir_watch.poll_forever()
	except Exception as e:
		traceback.print_exc()

		print(f"Remove tree {dir_watch.sync_folder()}")
		dir_watch.dispose()


if __name__ == "__main__":
	try:
		main(sys.argv)
	except AssertionError as e:
		print(f"E: {e}")

