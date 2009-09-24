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

import dbconnection
import htmlformshelper
import loginhelper

dbconnection.connectdb()

loginhelper.processCookie()

print "Content-type: text/html"
print ""
print ""

rows = dbconnection.querytomaplist( "select "\
   "     leaguegroup_name "\
   " from leaguegroups ",
   ('leaguegroupname', ) )

print "<html>" \
"<head>" \
"<title>AILadder - View league groups</title>" \
"</head>" \
"<body>" \
"<h3>AILadder - View leagues</h3>" \
"<p>A league is a specific game configuration used for testing AIs "\
" against each other</p>"\
"<p>For example, a league could be a specific map, mod, and certain options,"\
" like say cheating on, or cheating off</p>"\
"<p>You can group leagues together in leaguegroups.</p>"\
"<table border='1' padding='3'>" \
"<tr><td>League group name:</td></tr>"

for row in rows:
   print "<tr>"
   print "<td><a href='viewleaguegroup.py?leaguegroupname=" + row['leaguegroupname'] + "'>" + row['leaguegroupname'] + "</a></td>"
   print "</tr>"

print "</table>"

if loginhelper.gusername != '':

   print "<p />"
   print "<hr />"
   print "<p />"

   print "<h4>Create new league group:</h4>"
   print "<form action='addleaguegroup.py' method='post'>" \
   "<table border='1' padding='3'>" \
   "<tr><td>League group name</td><td><input name='leaguegroupname'</td></tr>"

   print "<tr><td></td><td><input type='submit' value='Add' /></td></tr>" \
   "</table>" \
   "</form>" \


print "</body>" \
"</html>"

dbconnection.disconnectdb()


