#!/usr/bin/env python3

import os, sys, stat, re

from sysfile import CChmodDir , CChmodFile \
	     ,CFindDir, CFindFile, CFindString

from sysfile import flg_ignorecase

from dup import CFindDUP

class Nothing:
	pass


def main():
	cmd = {
		"chdmod": [main_chmod, CChmodDir ],
		"chfmod": [main_chmod, CChmodFile],
		"fdir":   [main_find,  CFindDir  ], 
		"ffile":  [main_find,  CFindFile ], 
		"fstring":[main_find,  CFindString], 
		"fword":  [main_find,  CFindString, True],
		"fdup":   [main_finddup, Nothing]
	}.get(os.path.basename(sys.argv[0]), None)

	if not cmd:
		print("unknown cmd: ", sys.argv[0])
		sys.exit(-1)

	entry_ = cmd[0]
	class_ = cmd[1]

	return entry_(class_(), *set(cmd[2:]))

def main_finddup(*argvs, **kw):
	if len(sys.argv) >= 2 and sys.argv[1] == "-d":
		return CFindDUP(rm=True).run()
	else:
		return CFindDUP().run()


def main_chmod(ch):
	assert(isinstance(ch, CChmodDir) or isinstance(ch, CChmodFile))

	argv = sys.argv[1:]
	if len(argv) <= 0:
		return ch.walk()

	for argc in argv:
		ch.root = argc
		ch.walk()


def main_find(find, word=False):
	argv = sys.argv[1:]

	if len(argv) <= 0:
		print(sys.argv[0], "missing targets")
		sys.exit(-1)

	if re.match(r"-i", argv[0], re.I):
		find.flag = flg_ignorecase
		argv = argv[1:]

		if len(argv) <= 0:
			print(sys.argv[0], "missing targets")
			sys.exit(-1)
	if word:
		target = "\\b" + argv[0] + "\\b"
	else:
		target = argv[0]

	for argc in argv[1:]:
		if word:
			target += "|" + "\\b" + argc + "\\b"
		else:
			target += "|" + argc

	try:
		find.target = target
	except:
		sys.exit(-2)

	find.walk()


if __name__ =="__main__":
	main()
