#!/usr/bin/env python3

import os
import sys
import re

from collections import defaultdict

#MemTotal:        7865848 kB
#MemFree:           59476 kB
#Buffers:         3039508 kB
#Cached:          3061696 kB
#SwapCached:            0 kB
#SwapTotal:             0 kB
#SwapFree:              0 kB

#sys.stdout.write(ln);
#os.write(sys.stdout.fileno(), ln.encode());


frees = ( "MemFree", "Buffers", "Cached", "SwapCached", "SwapFree" )
total = ( "MemTotal", "SwapTotal" )

class meminfo(defaultdict):
	'''
	print memory usage and memory info
	'''
	def __init__(self, *args):
		super().__init__(*args)
		self._pattn = re.compile(meminfo.gen_re())
		self.update_meminfo()


	def parse_line(self, ln):
		ct = list(ln.split());
#		sys.stdout.write(ln);

		if len(ct) < 2:
			return

		if ct[0].endswith(':'):
			ct[0] = ct[0][:-1]

		if ct[1].endswith('kB'):
			ct[1] = ct[1][:-2]

		self[ct[0]] = int(ct[1])


	def update_meminfo(self):
		with open("/proc/meminfo", "r") as fp:
			for ln in fp:
				# use both match and search would be ok here
				if self._pattn.match(ln):
					self.parse_line(ln)


	@property
	def total(self):
		t = 0

		for f in total:
			t += self[f]

		return t

	@property
	def free(self):
		t = 0

		for f in frees:
			t += self[f]

		return t

	@property
	def used(self):
		return self.total - self.free

	@staticmethod
	def gen_re():

		s = ""
		for key in set(total + frees):
			s += "\\b" + key + "\\b|"

		s = s[:-1]

		return s

	@property
	def usage(self):
		return 100 * self.used / self.total


	@property
	def info(self):
		return "total: {total}M free: {free}M used: {used}M usage: {usage:>3.2f}%".\
		format( total= self.total // 1024, 
			free = self.free  // 1024, 
			used = self.used  // 1024, 
			usage= self.usage)



def main():
	mem = meminfo(lambda:0)

	print("memory usage: {:>3.2f}%".format(mem.usage))
	print(mem.info)


if __name__ == '__main__':
	main()

