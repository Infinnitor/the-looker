import time
import shutil
import atexit
import os

from .lookers import Looker, SyncLooker, LookerState
from .util import *


class DirectoryLooker():
	def __init__(self, path):
		assert os.path.exists(path), f"Path {path} does not exist"
		self._path = path
		self._lookers = [Looker(f) for f in get_all_files(self._path)]
		print("\n".join([repr(w) for w in self._lookers]))

	def __repr__(self):
		return repr(self._lookers)

	def contains_looker(self, p):
		return any([f.path() == p for f in self._lookers])

	def _create_looker(self, p):
		return Looker(p)

	def _check_looker_update(self):
		for i in range(len(self._lookers)-1, -1, -1):
			f = self._lookers[i]

			update_type = f.has_updated()
			if update_type == LookerState.Edit:
				print(f"{f.path()} updated")
				f.update()
			if update_type == LookerState.Delete:
				print(f"{f.path()} deleted")
				self._lookers.pop(i)

	def _check_file_creation(self):
		all_files = get_all_files(self._path)
		for p in all_files:
			if not self.contains_looker(p):
				print(f"{p} created")
				self._lookers.append(self._create_looker(p))

	def poll_forever(self, interval=0.5):
		self.poll_until(lambda: True, interval)

	def poll_until(self, until, interval=0.5):
		while until():
			self._check_looker_update()
			self._check_file_creation()
			time.sleep(interval)


class DirectoryLookerSync(DirectoryLooker):
	def __init__(self, path, sync_folder="/tmp/the_looker/"):
		assert os.path.exists(path), f"Path {path} does not exist"
		self._path = path
		self._sync_folder = sync_folder

		self._lookers = [SyncLooker(f, os.path.join(sync_folder, f)) for f in get_all_files(self._path)]

		os.makedirs(sync_folder, exist_ok=True)
		[w.update() for w in self._lookers]

		print("\n".join([repr(w) for w in self._lookers]))
		atexit.register(shutil.rmtree, self._sync_folder)

	def sync_folder(self):
		return self._sync_folder

	def _create_looker(self, p):
		return SyncLooker(p, os.path.join(self._sync_folder, p))

	def dispose(self):
		atexit.unregister(shutil.rmtree)
		shutil.rmtree(self._sync_folder)

