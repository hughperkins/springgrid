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

import cgitb; cgitb.enable()

from utils import *
from core import *

dbconnection.connectdb()

loginhelper.processCookie()

menu.printPageTop()

rows = dbconnection.querytomaplist( "select "\
   "    calcengine_name, "\
   "    username, "\
   "    userfullname, "\
   "    calcengine_sharedsecret "\
   " from calcengines, " \
   "    accounts "\
   " where calcengines.calcengine_owneraccountid = accounts.account_id ",
   ('calcenginename','username','userfullname', 'sharedsecret' ) )

print "<h3>AILadder - Calc Engine List</h3>" \
"<table border='1' padding='3'>" \
"<tr class='tablehead'><td>Calc Engine Name</td><td>Calc Engine Owner Name:</td><td>Shared secret (only visible for your own calcengines)</td><td>Options</td></tr>"

for row in rows:
   print "<tr>"
   print "<td>" + row['calcenginename'] + "</td>"
   print "<td>" + row['userfullname'] + "</td>"
   if row['username'] == loginhelper.gusername:
      print "<td>" + row['sharedsecret'] + "</td>"
   else:
      print "<td></td>"

   options = dbconnection.querytolistwithparams( "select calcengine_option_name "\
      " from calcengine_options, calcengine_assignedoptions, calcengines "\
      " where calcengines.calcengine_name = %s "\
      " and calcengine_assignedoptions.calcengine_id = calcengines.calcengine_id "\
      " and calcengine_options.calcengine_option_id = calcengine_assignedoptions.calcengine_option_id ",
      ( row['calcenginename'], ) )
   print "<td>" + ''.join( options ) + "</td>"

   print "</tr>"

print "</table>"

if loginhelper.gusername != '':

   print "<p />"
   print "<hr />"
   print "<p />"

   print "<h4>Register new calc engine:</h4>"
   print "You will automatically be marked as 'owner' of this calcengine<p />"
   print "<form action='addcalcengine.py' method='post'>" \
   "<table border='1' padding='3'>" \
   "<tr><td>Calc engine name</td><td><input name='calcenginename'</td></tr>" \
   "<tr><td>Calc engine shared secret</td><td><input name='sharedsecret'</td></tr>" \
   "<tr><td></td><td><input type='submit' value='Add' /></td></tr>" \
   "</table>" \
   "</form>"

dbconnection.disconnectdb()

menu.printPageBottom()

