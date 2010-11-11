#!/usr/bin/env python

import datetime
import os
import socket
socket.setdefaulttimeout(10)
import urllib2

try:
    f = urllib2.urlopen('http://flightlogg.in/is_alive').read()
    
except:
    print("{0}: error detected, restarting apache".format(start))
    os.system("/etc/init.d/apache restart")
