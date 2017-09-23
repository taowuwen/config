#!/usr/bin/env python3

import time
import os
import stat


'''
cpu  5190 0 1342 234407 2905 0 21 0 0 0
cpu0 1612 0 367 58345 625 0 5 0 0 0
cpu1 1413 0 319 58378 803 0 10 0 0 0
cpu2 1001 0 331 58741 897 0 3 0 0 0
cpu3 1163 0 324 58941 577 0 2 0 0 0



1st column : user = normal processes executing in user mode
2nd column : nice = niced processes executing in user mode
3rd column : system = processes executing in kernel mode
4th column : idle = twiddling thumbs
5th column : iowait = waiting for I/O to complete
6th column : irq = servicing interrupts
7th column : softirq = servicing softirqs



Calculation:

sum up all the columns in the 1st line "cpu" :
	( user + nice + system + idle + iowait + irq + softirq )
this will yield 100% of CPU time

calculate the average percentage of total 'idle' out of 100% of CPU time :
	( user + nice + system + idle + iowait + irq + softirq ) = 100%
	( idle ) = X %
hence
	average idle percentage 
	X % = ( idle * 100 ) / ( user + nice + system + idle + iowait + irq + softirq )

Based on the example above:
	average idle percentage 
	X % = ( 842486413 * 100 ) / ( 79242 + 0 + 74306 + 842486413 + 756859 + 6140 + 67701 + 0 ) = ( 842486413100 ) / ( 843470661 ) = 99.8833 %



Since Linux 2.6.11, there is an 8th column called 'steal' - counts the ticks spent executing other virtual hosts (in virtualised environments like Xen)
Since Linux 2.6.24, there is a 9th column called 'guest' - counts the time spent running a virtual CPU for guest operating systems under the control of the Linux kernel
'''

cpu_name = 0
cpu_user = 1
cpu_nice = 2
cpu_system = 3
cpu_idle   = 4
cpu_iowait = 5
cpu_irq    = 6
cpu_softirq= 7
cpu_usage  = 8

class struct_cpu():
	def __init__(self, args = list()):
		'''
		list[items]
 		cpu, time, user, nice, system, idle, iowait, irq, softirq, usage

		'''

		assert len(args) >= 8, "invalid args,len = {0}, args = {1}".format(len(args), str(args))

		self._cpu = [0 for item in range(cpu_usage + 1)]

		self._cpu[cpu_name] = args[0]
		self._cpu[cpu_usage ] = 0
		self.update_params(args[cpu_user:cpu_usage])

		assert len(self._cpu) == 9

		self.update(self._cpu)


	def update_params(self, args = None):

		assert len(args) == 7, "args should be 7, len = {}, args = {}".format(
				len(args), args)

		self._cpu[cpu_user:cpu_usage] = [ int(item) for item in args ]


	def update(self, st):
		assert len(st) >= 8, "invalid args, len = {0}, args = {1}".format(len(st), str(st))

		cur_st = list(st)
		cur_st[cpu_user:] = [ int(item) for item in cur_st[cpu_user:]]
		
		assert cur_st[cpu_name] == self._cpu[cpu_name], "cpu name not the same"

		total_diff = sum(cur_st[cpu_user:cpu_usage]) - sum(self._cpu[cpu_user: cpu_usage])
		idle_diff = cur_st[cpu_idle] - self._cpu[cpu_idle]
		used_diff = total_diff - idle_diff 

		if total_diff:
			self._cpu[cpu_usage] = (100 * used_diff) / total_diff
			self.update_params(cur_st[cpu_user:cpu_usage])


	@property
	def name(self):
		return self._cpu[cpu_name]

	@property
	def usage(self):
		return "{:^3.1f}".format(self._cpu[cpu_usage])

	def __str__(self):
		s = ""

		for item in self._cpu[:cpu_usage]:
			s += str(item) + " "

		return s
			

	def __repr__(self):
		return repr(self._cpu[cpu_name] + "(" + str(self._cpu[cpu_usage]) + "%)")


class cpuinfo(dict):
	def __init__(self, laststat = "/tmp/cpu_stauts"):
		self._stat = "/proc/stat"
		self._laststat =  laststat

		try:
			mode = os.stat(self._laststat).st_mode;
			if stat.S_ISREG(mode):
				self.last_stat()
			else:
				print("file {} not regular file".format(self._laststat))
				os.exit(-1)
		except FileNotFoundError:
			self.update_stat()


	def write_stat(self):

		with open(self._laststat, "w") as fl:
			for item in self.keys():
				fl.write(str(self[item]) + "\n")

	def load_stat(self, fl=None):
		with open(fl, "r") as fl:
			for line in fl.readlines():
				if line.startswith("cpu"):

					args = line.split()

					if len(args) < 8:
						print("Warning line {} error".format(line))
						pass

					cpu = self.get(args[0], None)
					if cpu:
						cpu.update(args)
					else:
						self[args[0]] = struct_cpu(args) 

		return True

	def update_stat(self):
		self.load_stat(self._stat)
		self.write_stat()

	def last_stat(self):
		return self.load_stat(self._laststat)

	@property
	def usage(self):
		self.update_stat()
		return self["cpu"].usage

	@property
	def info(self):

		str = ""
		for key in self.keys():
			str += "{} = {}%; ".format(key, self[key].usage)

		return str

def main():
	c = cpuinfo()
	print(c.usage)
	print(c.info)


if __name__ == '__main__':
	main()


