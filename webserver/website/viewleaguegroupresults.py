#!/usr/bin/python

import cgitb; cgitb.enable()

from core import *
from utils import *
from core.tableclasses import *

sqlalchemysetup.setup()

loginhelper.processCookie()

menu.printPageTop()

print "Page not implemented yet."

menu.printPageBottom()

sqlalchemysetup.close()

