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

calcenginename = formhelper.getValue("calcenginename")

dbconnection.dictcursor.execute( "select "\
   "    username, "\
   "    userfullname, "\
   "    calcengine_sharedsecret "\
   " from calcengines, " \
   "    accounts "\
   " where calcengines.calcengine_owneraccountid = accounts.account_id "\
   " and calcengines.calcengine_name = %s ",
   (calcenginename ) )
row = dbconnection.dictcursor.fetchone()

iscalcengineowner = ( loginhelper.isLoggedOn() and row['username'] == loginhelper.getUsername() )

options = dbconnection.querytolistwithparams( "select calcengine_option_name "\
      " from calcengine_options, calcengine_assignedoptions, calcengines "\
      " where calcengines.calcengine_name = %s "\
      " and calcengine_assignedoptions.calcengine_id = calcengines.calcengine_id "\
      " and calcengine_options.calcengine_option_id = calcengine_assignedoptions.calcengine_option_id ",
      ( calcenginename, ) )

print "<h3>AILadder - Calc Engine '" + calcenginename + "'</h3>" \
"<table border='1' padding='3'>"

print "<tr><td>Calc engine owner: </td><td>" + row['userfullname'] + "</td></tr>"
if iscalcengineowner:
   print "<tr><td>Shared secret: </td><td>" + row['calcengine_sharedsecret'] + "</td></tr>"
else:
   print "<tr><td>Shared secret: </td><td>&lt;only visible to owner&gt;</td></tr>"

print "</table>"

print "<h3>Assigned options</h3>"

print "<table>"


if iscalcengineowner:
   print "<tr class='tablehead'><td>Option name</td><td></td></tr>"
else:
   print "<tr class='tablehead'><td>Option name</td></tr>"

for option in options:
   print "<tr><td>" + option + "</td>"
   if iscalcengineowner:
      print "<td><a href='deleteoptionfromcalcengine.py?calcenginename=" + calcenginename + "&optionname=" + option + "'>Delete option</a></td>"
   print "</tr>"

print "</table>"

if row['username'] == loginhelper.getUsername():

   print "<p />"
   print "<hr />"
   print "<p />"

   potentialoptions = dbconnection.querytolistwithparams( "select calcengine_option_name "\
         " from calcengine_options where not exists( "\
         " select * from calcengine_assignedoptions, calcengines "\
         " where calcengines.calcengine_name = %s "\
         " and calcengine_assignedoptions.calcengine_id = calcengines.calcengine_id "\
         " and calcengine_options.calcengine_option_id = calcengine_assignedoptions.calcengine_option_id "
         " ) ",
         ( calcenginename, ) )

   print "<h4>Add new options to engine:</h4>"
   print "<form action='addoptiontocalcengine.py' method='post'>" \
   "<table border='1' padding='3'>" \
   "<tr><td>Option to add:</td><td>" + htmlformshelper.listToDropdown( 'optionname', potentialoptions ) + "</td></tr>" \
   "<tr><td></td><td><input type='submit' value='Add' /></td></tr>" \
   "</table>" \
   "<input type='hidden' name='calcenginename' value='" + calcenginename + "' />"\
   "</form>"

dbconnection.disconnectdb()

menu.printPageBottom()

