#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys


class ctx_parse():
	@staticmethod
	def _load_ctx(fl = None):
		assert fl != None, "file sould no be null"

		_res = [];

		with open(fl, "r") as f:
			for ln in f:
				_res.append(ln.strip())
		return _res

	@staticmethod
	def get_float(fl = None):
		return float(ctx_parse._load_ctx(fl)[0])


	@staticmethod
	def get_int(fl = None):
		return int(ctx_parse._load_ctx(fl)[0])

	@staticmethod
	def get_str(fl = None):
		return ctx_parse._load_ctx(fl)[0]

	@staticmethod
	def get_lns(fl = None):
		return ctx_parse._load_ctx(fl)



class net_info():
	def __init__(self, cfg="/tmp/net_info"):
		self._inf = "eth0"
		self._gateway = 0
		self._addr    = 0
		self._mask    = 0
		self._net     = 0

		self._last_tx = 0
		self._last_rx = 0
		self._last_tm = 0

		self._cur_tx  = 0;
		self._cur_rx  = 0;
		self._cur_tm  = 0;

		self._cfg = cfg

		self._route_refresh()
		self._address_refresh()
		self._load_info()

	def _load_info(self):

		try:
			res = ctx_parse.get_lns(self._cfg)

			item = res[0].split()

			if not (len(item) == 4 and item[0] == self._inf):
				return False

			self._last_tm = float(item[1])
			self._last_rx = int(item[2])
			self._last_tx = int(item[3])

		except FileNotFoundError:
			pass


	@staticmethod
	def hex2int(addr):
		if len(addr) != 8:
			return 0

		return int(addr[-2:] + addr[-4:-2]+ addr[-6:-4] + addr[-8:-6], 16) 


	@staticmethod
	def int2ip(addr):
		return "{0}.{1}.{2}.{3}".format(
				(addr & 0xff000000) >> 24,
				(addr & 0x00ff0000) >> 16,
				(addr & 0x0000ff00) >> 8,
				(addr & 0x000000ff) >> 0)

	def _route_refresh(self):
		res = ctx_parse.get_lns("/proc/net/route");

		for ln in res:
			items = ln.split();

			if items[1] == "00000000":
				self._inf     = items[0]
				self._gateway = self.hex2int(items[2])
				break

		for ln in res:
			items = ln.split();

			if items[2] == "00000000" and self._inf == items[0]:
				self._mask = self.hex2int(items[7])
				self._net  = self.hex2int(items[1])
				if self._net == self._gateway & self._mask:
					break

	def _get_ipaddress(self, res):
		for ln in res:
			ip = self.hex2int(ln.split()[1].split(':')[0])

			if ip & self._mask == self._net:
				self._addr = ip

				return True
		return False


	def _address_refresh(self):
		if self._net == 0:
			return Fasle

		res = ctx_parse.get_lns("/proc/net/tcp");

		if not self._get_ipaddress(res):
			res = ctx_parse.get_lns("/proc/net/udp");

			return self._get_ipaddress(res)

		return True


	@property
	def route_info(self):

		self._route_refresh()
		self._address_refresh()

		return (self._inf, self._addr, self._mask, self._gateway, self._net)


	def _update_speed(self):
		import time
		self._cur_tx = ctx_parse.get_int("/sys/class/net/" + self._inf + "/statistics/tx_bytes")
		self._cur_rx = ctx_parse.get_int("/sys/class/net/" + self._inf + "/statistics/rx_bytes")
		self._cur_tm = time.time()

		with open(self._cfg, "w") as f:
			f.write(self._inf \
				+ " " + str(self._cur_tm)
				+ " " + str(self._cur_rx)
				+ " " + str(self._cur_tx) + "\n")

	@property
	def speed(self, inf = None):

		self._update_speed()

		tx = self._cur_tx - self._last_tx
		rx = self._cur_rx - self._last_rx
		tm = self._cur_tm - self._last_tm

		if tm == 0:
			return (self._inf, 0, 0)

		return (self._inf, rx/tm, tx/tm)

	@staticmethod
	def speed_str(speed):

		# bytes
		if speed <= 1024:
			return "{:0.1f}B".format(speed)

		# kilo
		sp = speed / (1 << 10)
		if sp <= 1024:
			return "{:0.1f}K".format(sp)

		# m
		sp = speed / (1 << 20)
		return "{:0.1f}M".format(sp)




def main():
	net = net_info()

	inf, ip, mask, gateway, network = net.route_info
	print(inf, net.int2ip(ip), net.int2ip(mask), net.int2ip(gateway), net.int2ip(network));
	inf, rx, tx = net.speed

	print(inf, rx, tx, net.speed_str(rx), net.speed_str(tx))


	

if __name__ == '__main__':
	main()
