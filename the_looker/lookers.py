#!/usr/bin/python3
import os
from threading import Thread

class LookerState:
	Nothing = 0
	Edit = 1
	Delete = 2
	Create = 3


class Looker():
	def __init__(self, path):
		assert os.path.exists(path), f"Path {path} does not exist"
		self._path = path
		self._cached_timestamp = self._get_timestamp()

	def path(self):
		return self._path

	def _get_timestamp(self):
		return os.stat(self._path).st_mtime

	def has_updated(self):
		result = LookerState.Nothing
		if not os.path.exists(self._path):
			return LookerState.Delete

		tm = self._get_timestamp()
		if tm != self._cached_timestamp:
			self._cached_timestamp = tm
			result = LookerState.Edit

		return result

	def update(self):
		pass

	def __repr__(self):
		return f"look * {self._path}"


class SyncLooker(Looker):
	def __init__(self, path, sync_path):
		super().__init__(path)
		self._sync_path = sync_path

	def update(self):
		FILE = open(self._path, "rb")
		contents = FILE.read()
		FILE.close()

		b = os.path.dirname(self._sync_path)
		if not os.path.exists(b):
			os.makedirs(b, exist_ok=True)

		sync_FILE = open(self._sync_path, "wb+")
		sync_FILE.write(contents)
		sync_FILE.close()

	def __repr__(self):
		return f"sync * {self._path} -> {self._sync_path}"

