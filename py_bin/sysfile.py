#!/usr/bin/env python3

import os, stat, re

flg_ignorecase = 0x00000001

class CFind:
	def __init__(self, path = "."):
		self._path = path
		self._key  = None
		self._patt = None
		self._flg  = 0

	def walk_path(self, path=None):
		subitems = os.listdir(path)
		for elem in subitems:
			cur = path + "/" + elem

			self.handle_file(cur, path, elem)
			if os.path.isdir(cur):
				try:
					self.walk_path(cur)
				except PermissionError:
					import sys
					sys.stderr.write("(Skip) Permission Denied: %s\n"%(cur))
					pass

		return 0

	def walk(self):
		if self._path == None:
			self._path = "."

		try:
			self.walk_path(self._path)
		except:
			return -1
	
		return 0


	def handle_file(self, path, parent=None, elem=None):

		if os.path.isdir(path):
			print("dir >>>", path)

		elif os.path.isfile(path):
			print("file >>>", path)
		else:
			print("unknown file >> ", path)
			pass

	def paint(self, line, color="\033[01;31m"):

		ret   = ""
		pos   = 0
		beg   = 0
		l     = len(self._key)

		while True:
			inx = line.find(self._key, beg)
			if inx < 0:
				break
			beg = inx + l

			ret += line[pos:inx] \
			       		+ color \
					+ line[inx:beg] \
					+ "\033[00;00m"
			pos = beg

		ret = ret + line[beg:]
		return ret

	def paint_ex(self, line, color="\033[01;31m"):
		ret = ""
		pos = 0

		results = self._patt.finditer(line)
		for item in results:
			ret += line[pos:item.start()]
			ret += color
			ret += item.group()
			ret += "\033[00;00m"
			pos  = item.end()

		ret += line[pos:]
		return ret

	@property
	def root(self):
		return self._path

	@root.setter
	def root(self, val):
		self._path = val

	@root.deleter
	def root(self):
		self._path = "."

	@property
	def target(self):
		return self._key

	@target.setter
	def target(self, val):
		self._key  = val
		if self._flg & flg_ignorecase:
			self._patt = re.compile(val, re.I)
		else:
			self._patt = re.compile(val)

	@target.deleter
	def target(self):
		del self._key

	@property
	def flag(self):
		return self._flg

	@flag.setter
	def flag(self, val):
		self._flg |= val

	@flag.deleter
	def flag(self):
		self._flg = 0

class CChmodFile(CFind):
	def __init__(self, path=None):
		CFind.__init__(self, path)

	def handle_file(self, path, parent=None, elem=None):
		if os.path.isfile(path):
			os.chmod(path, stat.S_IRUSR| stat.S_IWUSR|stat.S_IRGRP|stat.S_IROTH)

class CChmodDir(CFind):
	def __init__(self, path=None):
		CFind.__init__(self, path)

	def handle_file(self, path, parent=None, elem=None):
		if os.path.isdir(path):
			os.chmod(path, stat.S_IRWXU|stat.S_IRGRP|stat.S_IXGRP)


class CFindDir(CFind):
	def __init__(self):
		CFind.__init__(self)

	def handle_file(self, path, parent=None, elem=None):
		if os.path.isdir(path) and elem:
			if self._patt.search(elem): print(parent + "/" + self.paint_ex(elem))


class CFindFile(CFind):
	def __init__(self):
		CFind.__init__(self)

	def handle_file(self, path, parent=None, elem=None):
		if os.path.isfile(path) and elem:
			if self._patt.search(elem): print(parent + "/" + self.paint_ex(elem))

class CFindString(CFind):
	def __init__(self):
		CFind.__init__(self)


	def parse_content(self, fl):
		try:
			fobj = open(fl, "r")
			n_ln = 0

			for ln in fobj:
				n_ln = n_ln + 1

				ln = ln.strip()
				if self._patt.search(ln):
					print("%s:\033[00;32m%d\033[00;00m:%s"\
						%(fl, n_ln, self.paint_ex(ln, "\033[00;33m").strip('\n')))
		except FileNotFoundError:
			print("file", fl, "not exist")
			return -1

		except:
# import sys
#			print("Can't open file", fl)
#, str(sys.exc_info()))
			return -1
		else:
			fobj.close()
		return 0

	def handle_file(self, path, parent=None, elem=None):
		if os.path.isfile(path):
			self.parse_content(path)


def main():
	find = CFind()

	find.walk()
	

if __name__ == '__main__':
	main()
