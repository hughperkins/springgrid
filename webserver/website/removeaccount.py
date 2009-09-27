#!/usr/bin/python

# Copyright Hugh Perkins 2009
# hughperkins@gmail.com http://manageddreams.com
#
# This program is free software; you can redistribute it and/or aiify it
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

# lets a user add a single account to the database
#
# This is mostly for bootstrapping, to make the website immediately useful

import cgitb; cgitb.enable()
import cgi

from utils import *
from core import *

dbconnection.connectdb()

loginhelper.processCookie()

menu.printPageTop()

if not roles.isInRole(roles.accountadmin):
   print "You must be logged in as an accountadmin"
else:
   username = formhelper.getValue('username')

   if username != None and username != '':
      if roles.isInRole2( username, roles.accountadmin ):
         print "Please drop the accountadmin role from " + username + " and try again"
      else:
         rows = dbconnection.cursor.execute( "delete accounts.* "\
            " from accounts "\
            " where username = %s",
            ( username, ) )
         if rows == 1:
            print "Removed ok"
         else:
            print "Something went wrong.  Please check your values and try again."
   else:
      print "Please fill in the fields and try again"

dbconnection.disconnectdb()

menu.printPageBottom()

