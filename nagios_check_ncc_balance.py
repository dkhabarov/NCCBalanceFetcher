#!/usr/bin/env python
#-*- coding: utf8 -*-
"""
##########################################################################
 nagios_check_etherway_balance.py - Plugin for nagios to check balance privider Etherway.ru

 Copyright © 2013 Denis 'Saymon21' Khabarov
 E-Mail: <saymon@hub21.ru>

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU General Public License version 3
 as published by the Free Software Foundation.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################
"""
"""
Nagios command config:

define command {
        command_name check_ncc_balance
        command_line /usr/lib/nagios/plugins/nagios_check_ncc_balance.py --user='$ARG1$' --password='$ARG2$' --warning='$ARG3$' --critical='$ARG4$'
}

Nagios service config:

define service {
    service_description             NCC Balance
    host_name                       localhost
    check_command                   check_ncc_balance!9080000000!mysuperpassword!15!10
    use                             generic-service
}

"""
##########################################################################
import argparse, sys
try:
	import ncc
except ImportError:
	print 'Unable to import ncc module. See http://opensource.hub21.ru/nccbalancefetcher'
	sys.exit(3)

cliparser = argparse.ArgumentParser(prog=sys.argv[0],description='''Plugin for nagios to get balance from https://iserve.ncc-volga.ru/
Copyright © 2013 by Denis Khabarov aka \'Saymon21\'
E-Mail: saymon at hub21 dot ru (saymon@hub21.ru)
Homepage: http://opensource.hub21.ru/nccbalancefetcher
Licence: GNU General Public License version 3
You can download full text of the license on http://www.gnu.org/licenses/gpl-3.0.txt''',
formatter_class=argparse.RawDescriptionHelpFormatter)
cliparser.add_argument('-w','--warning',dest='warning',metavar='VALUE',help='warning RUB',required=True,type=float)
cliparser.add_argument('-c','--critical',dest='critical',metavar='VALUE',help='critical RUB',required=True,type=float)
cliparser.add_argument('-l','--user',dest='user',metavar='PHONE', help='login for auth in iserve.ncc-volga.ru',required=True,type=str)
cliparser.add_argument('-p','--password',dest='password',metavar='PASSWORD',help='password for auth in iserve.ncc-volga.ru',required=True,type=str)
cliparser.add_argument('-t','--timeout',dest='timeout',metavar='VALUE',help='timeout for http requests (default: 10)',default=10,type=int)
cliargs = cliparser.parse_args()

def main():
	lk=ncc.NCCBalanceFetcher(login=cliargs.user, password=cliargs.password, timeout=cliargs.timeout)
	try:
		mybalance = lk.get_balance()
	except ncc.QueryError as errstr:
		print('UNKNOWN Unable to get balance for ' + cliargs.user + '. Error: ' + str(errstr))
		sys.exit(3)
        
	if mybalance:
		if cliargs.critical >= mybalance:
			print('CRITICAL Balance for ' + cliargs.user + ' = ' + str(mybalance) + ' RUB')
			sys.exit(2)
		elif cliargs.warning >= mybalance:
			print('WARNING Balance for ' + cliargs.user + '= ' + str(mybalance) + ' RUB')
			sys.exit(1)
		else:
			print('OK Balance for ' + cliargs.user + ' = ' + str(mybalance) + ' RUB')
			sys.exit(0)
	else:
		print('UNKNOWN Unable to get balance for ' + cliargs.user)
		sys.exit(3)
                
                 
if __name__ == '__main__':
	main()
