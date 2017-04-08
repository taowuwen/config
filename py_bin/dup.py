#!/usr/bin/env python3

import os

from sysfile import CFind

class CFindDUP(CFind):
	def __init__(self, rm=False, path=None):
		CFind.__init__(self, path)
		self._files = {}
		self._del   = rm


	def push(self, path):
		import stat
		st = os.stat(path)

		if st.st_size <= 0:
			return

		fls = self._files.get(st.st_size)
		if not fls:
			fls = []
			self._files[st.st_size] = fls
		fls.append(path)

	def pop(self, key):
		del self._files[key]

	def handle_file(self, path):
		if os.path.isfile(path):
			self.push(path)

	def fl_checksum(self, fl):
		import hashlib
		chk = hashlib.md5()
		f = open(fl, 'rb')
		while True:
			b = f.read(4096)
			if not b:
				break
			chk.update(b)
		f.close()
		return chk.hexdigest().upper()

	def fl_filter_the_same(self, fls):
		md5dict = {}

		for elem in fls:
			chk = self.fl_checksum(elem)
			lists = md5dict.get(chk)
			if not lists:
				lists = []
				md5dict[chk] = lists
			lists.append(elem)

		while True:
			for key in md5dict.keys():
				if len(md5dict[key]) <= 1:
					del md5dict[key]
					break
			else: break

		for key in md5dict.keys():
			fls = md5dict[key]
			print("<START> ---", key, ">>>", fls[0])

			l = len(md5dict[key])

			for ind in range(1, l):
				if self._del: 
					print(key, "=", fls[ind], "deleted")
					os.remove(fls[ind])
				else:
					print(key, "=", fls[ind])

			print("<END> ---", key)

		md5dict.clear()

	def run(self):
		self.walk()

		keys = self._files.keys()

		while True:
			for key in self._files.keys():
				if len(self._files[key]) <= 1:
					self.pop(key)
					break
			else:
				break

		keys = self._files.keys()
		for key in keys:
			self.fl_filter_the_same(self._files[key])

			
def main():
	find = CFindDUP()
	find.run()


if __name__ =="__main__":
	main()
