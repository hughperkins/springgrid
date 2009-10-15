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
from db import *

dbconnection.connectdb()

sqlalchemysetup.setup()

username = formhelper.getValue('username')
password = formhelper.getValue('password')
if username == None or password == None or username == '' or password == '':
   menu.printPageTop()
   print "<h4>Logon error: Please fill in the username and password fields.</h4>"
else:
   loginhelper.logonUser( username, password )

   headers = "Content-type: text/html\n"
   # adding the cookie into the headers keeps hte cookie there magically
   # for the rest of the session
   headers = headers + loginhelper.cookie.output() + "\n"
   menu.printPageTop( headers )

   print loginhelper.loginhtml

sqlalchemysetup.close()

dbconnection.disconnectdb()

menu.printPageBottom()


