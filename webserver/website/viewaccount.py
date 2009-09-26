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

print "Content-type: text/html"
print ""
print ""

menu.printPageTop()

username = formhelper.getValue('username')

rows = dbconnection.querytolistwithparams( "select role_name "\
   " from roles, accounts, role_members "\
   " where role_members.role_id = roles.role_id "\
   " and accounts.account_id = role_members.account_id "\
   " and accounts.username = %s",
   (username,) )

print "<h3>AILadder - View account " + username + "</h3>" \
"<table border='1' padding='3'>" \
"<tr class='tablehead'><td>Role:</td><td></td></tr>"

for row in rows:
   print "<tr>"
   print "<td>" + row + "</td>"
   print "<td><a href='removerolefromaccount.py?"\
      "username=" + username + "&rolename=" + row + "'>"\
      "Remove from role</a></td>"
   print "</tr>"

print "</table>"

if roles.isInRole(roles.accountadmin):

   print "<p />"
   print "<hr />"
   print "<p />"

   potentialroles = dbconnection.querytolistwithparams("select "\
      " role_name "\
      " from roles "\
      " where not exists ( select * from role_members, accounts "\
      " where role_members.role_id = roles.role_id and "\
      " accounts.account_id = role_members.account_id and "\
      " accounts.username = %s ) ",
      ( username, ) )

   print "<h4>Add roles to account:</h4>"
   print "<form action='addroletoaccount.py' method='post'>" \
   "<table border='1' padding='3'>" \
   "<tr><td>Role name</td><td>"
   print htmlformshelper.listToDropdown( 'rolename', potentialroles )
   print "</td></tr>"

   print "<tr><td></td><td><input type='submit' value='Add' /></td></tr>" \
   "</table>" \
   "<input type='hidden' name='username' value='" + username + "' />"\
   "</form>"

dbconnection.disconnectdb()

menu.printPageBottom()

