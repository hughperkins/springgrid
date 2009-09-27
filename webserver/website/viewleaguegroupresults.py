#!/usr/bin/python

from core import *
from utils import *

dbconnection.connectdb()

loginhelper.processCookie()

menu.printPageTop()

print "Page under construction."

menu.printPageBottom()

dbconnection.disconnectdb()

