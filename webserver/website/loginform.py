#!/usr/bin/python

# Copyright Hugh Perkins 2009
# hughperkins@gmail.com http://manageddreams.com
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
#  more details.
#
# You should have received a copy of the GNU General Public License along
# with this program in the file licence.txt; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-
# 1307 USA
# You can find the licence also on the web at:
# http://www.opensource.org/licenses/gpl-license.php
#

# handles user login

import cgitb; cgitb.enable()
import cgi

from utils import *
from core import *

dbconnection.connectdb()

print "Content-type: text/html"
print ""
print ""
menu.printPageTop()

print "<h3>AI Ladder - login</h3>"
print "<form action='login.py' method='post'>"
print "<table border='1' cellpadding='3'>"
print "<tr><td>Username:</td><td><input type='text' name='username'></td></tr>"
print "<tr><td>Password:</td><td><input type='password' name='password'></td></tr>"
print "<tr><td></td><td><input type='submit' value='Login'></td></tr>"
print "</table>"
print "</form>"

dbconnection.disconnectdb()

menu.printPageBottom()


