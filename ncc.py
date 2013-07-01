#!/usr/bin/env python
#-*- coding: utf8 -*-
# NCCBalanceFetcher - Simple Python script to get balance from https://iserve.ncc-volga.ru/

# Copyright © 2013 Denis 'Saymon21' Khabarov
# E-Mail: saymon at hub21 dot ru (saymon@hub21.ru)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3
# as published by the Free Software Foundation.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


__author__ = "Denis 'Saymon21' Khabarov"
__copyright__ = "Copyright © 2013 Denis 'Saymon21' Khabarov"
__credits__ = []
__license__ = "GPLv3"
__version__ = "0.1"
__maintainer__ = "Denis 'Saymon21' Khabarov"
__email__ = "saymon@hub21.ru"
__status__ = "Development"
try:
	import urllib, urllib2
except ImportError as errstr:
	print errstr
	exit(1)

class QueryError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

class NCCBalanceFetcher:
	def __init__(self, login, password, timeout=10):
		self.login = login
		self.password = password
		self.timeout = timeout
		if self.login is None:
			raise QueryError("Please enter login!")
		if self.password is None:
			raise QueryError("Please enter password!")
		
	def auth(self):
		urllib2.install_opener(urllib2.build_opener(urllib2.HTTPCookieProcessor))
		params = urllib.urlencode({'userv': self.login, 'passv': self.password})
		request = urllib2.Request('https://iserve.ncc-volga.ru/?path=iserv', params)
		try:
			result = urllib2.urlopen(request, timeout = self.timeout)
		except (urllib2.URLError,urllib2.HTTPError) as err_msg:
			raise QueryError(err_msg)
		return result.read()

	def get_balance(self):
		from re import search
		source = self.auth()
		if source:
			data= search('<input type="hidden" name="balance" id="balance" value="(.+)">',source)
			if data is not None:
				return float(data.group(1))
			else:
				raise QueryError('Balance not found.')
		else:
			raise QueryError('Unable to auth.')

# Example usage:
# ./ncc.py mylogin mypassword				
if __name__ == "__main__":
	import sys
	if not len(sys.argv) < 3:
		fetcher = NCCBalanceFetcher(login = sys.argv[1],password = sys.argv[2])
		try:
			data = fetcher.get_balance()
		except QueryError as err_msg:
			print('Error: ' + str(err_msg))
			sys.exit(1)	
		print('Your balance: ' + str(data))
		sys.exit(0)
	else:
		print('Usage ' + sys.argv[0] + ' login password')
		sys.exit(1)
