#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, stat, re, sys


class CList(list):
	def __init__(self, path = ".", maxdepth = -1):
		super().__init__()

		self._path     = path if path != None else "."
		self._maxdepth = maxdepth if maxdepth > 0 else -1

		self.walking()


	def walk_path(self, path, deep):
		if self._maxdepth > 0 and deep > self._maxdepth:
			return 0

		deep += 1

		subitems = os.listdir(path)
		for elem in subitems:
			cur = path + "/" + elem

			self.append(cur)

			if os.path.isdir(cur):
				try:
					self.walk_path(cur, deep)
				except PermissionError:
					import sys
					sys.stderr.write("(Skip) directory: %s\n"%(cur))
					pass

		return 0

	def walking(self):
		try:
			deep = 1
			self.walk_path(self._path, deep)

		except KeyboardInterrupt:
			pass

		except:
			import traceback, sys
			traceback.print_exc(file=sys.stderr)
			return -1
	
		return 0

	def __str__(self):
		s = "\n===> {}\n[\n".format(self._path)
		for item in self:
			s += "\t {}\n".format(item)
		s += "]"

		return s

class Cdybg:

	def __init__(self, path):
		self._ls = CList(path, 1)
		self._random = 0
		self._internal  = 300

		while True:

			for ind, fl in enumerate(self._ls):
				if fl.lower().endswith(".jpg") or \
					fl.lower().endswith(".png") or \
					fl.lower().endswith(".jpeg"):
					continue

				del self._ls[ind]
				break
			else:
				break

		self._ls.sort()
		print(self._ls)

	@property
	def rand(self):
		return self._random

	@rand.setter
	def rand(self, val):
		import random
		self._random = val

		if self._random:
			random.shuffle(self._ls)
		else:
			self._ls.sort()

	@property
	def internal(self):
		return self._internal

	@internal.setter
	def internal(self, val):
		if val > 10:
			self._internal = val

	def run(self):
		import time
		import random

		while True and len(self._ls) > 0:

			if self._random:
				random.shuffle(self._ls)

			for ind, fl in enumerate(self._ls):
				if 0 != os.system("feh --bg-fill '{}'".format(fl)):
					del self._ls[ind]
					break

				time.sleep(self._internal)


def main():
	if len(sys.argv) < 2:
		print("Usage {} directorys".format(sys.argv[0]))
		return 1

	pattn = re.compile("python.*." + sys.argv[0].split("/")[-1])

	import subprocess

	with subprocess.Popen(["ps", "au"], stdout = subprocess.PIPE) as proc:
		outputs=proc.stdout.read().decode().split("\n")

		for ln in outputs:
			if pattn.search(ln):
				pid = int(ln.split()[1])
				if pid == os.getpid():
					continue

				print("stop process {} -> {}".format(pid, ln))
				os.kill(pid, 9)


# for line in out.splitlines():
# ...   if 'iChat' in line:
# ...     pid = int(line.split(None, 1)[0])
# ...     os.kill(pid, signal.SIGKILL)
# ... 

	dybg = Cdybg(sys.argv[1])
	dybg.rand = 1
	dybg.run()

	return 0

if __name__ == '__main__':
	exit (main())

