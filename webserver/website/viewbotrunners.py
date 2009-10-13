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
   "    botrunner_name as botrunnername, "\
   "    username, "\
   "    userfullname, "\
   "    botrunner_sharedsecret as sharedsecret "\
   " from botrunners " \
   " left join accounts on  "\
   "    botrunners.botrunner_owneraccountid = accounts.account_id " )

print "<h3>AILadder - Bot Runner List</h3>" \
"<table border='1' padding='3'>" \
"<tr class='tablehead'><td>Bot Runner Name</td><td>Bot Runner Owner Name:</td><td>Shared secret (only visible for your own botrunners)</td><td>Options</td></tr>"

for row in rows:
   print "<tr>"
   print "<td><a href='viewbotrunner.py?botrunnername=" + row['botrunnername'] + "'>" + row['botrunnername'] + "</a></td>"
   if row['userfullname'] != None:
      print "<td>" + row['userfullname'] + "</td>"
   else:
      print "<td></td>"
   if row['username'] != None and row['username'] == loginhelper.gusername:
      print "<td>" + row['sharedsecret'] + "</td>"
   else:
      print "<td></td>"

   options = dbconnection.querytolistwithparams( "select botrunner_option_name "\
      " from botrunner_options, botrunner_assignedoptions, botrunners "\
      " where botrunners.botrunner_name = %s "\
      " and botrunner_assignedoptions.botrunner_id = botrunners.botrunner_id "\
      " and botrunner_options.botrunner_option_id = botrunner_assignedoptions.botrunner_option_id ",
      ( row['botrunnername'], ) )
   print "<td>" + ' '.join( options ) + "</td>"

   print "</tr>"

print "</table>"

if loginhelper.gusername != '' and False:

   print "<p />"
   print "<hr />"
   print "<p />"

   print "<h4>Register new bot runner:</h4>"
   print "You will automatically be marked as 'owner' of this botrunner<p />"
   print "<form action='addbotrunner.py' method='post'>" \
   "<table border='1' padding='3'>" \
   "<tr><td>Bot runner name</td><td><input name='botrunnername'</td></tr>" \
   "<tr><td>Bot runner shared secret</td><td><input name='sharedsecret'</td></tr>" \
   "<tr><td></td><td><input type='submit' value='Add' /></td></tr>" \
   "</table>" \
   "</form>"

dbconnection.disconnectdb()

menu.printPageBottom()

