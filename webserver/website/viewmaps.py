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

# lets a user add a single map to the database
#
# This is mostly for bootstrapping, to make the website immediately useful

import cgitb; cgitb.enable()

import dbconnection
import htmlformshelper

dbconnection.connectdb()

print "Content-type: text/html"
print ""
print ""

maps = dbconnection.querytomaplist( "select map_name, map_hash from maps", ('map_name','map_hash' ) )

print "<html>" \
"<head>" \
"<title>AILadder - Map List</title>" \
"</head>" \
"<body>" \
"<h3>AILadder - Map List</h3>" \
"<table border='1' padding='3'>" \
"<tr><td>Map name</td><td>Map hash</td></tr>"

for map in maps:
   print "<tr><td>" + map['map_name'] + "</td><td>" + map['map_hash'] + "</td></tr>"

print "</table>"

print "<p />"
print "<hr />"
print "<p />"

print "<h4>Register new map:</h4>"
print "<form action='addmap.py' method='post'>" \
"<table border='1' padding='3'>" \
"<tr><td>Map name</td><td><input name='mapname'</td></tr>" \
"<tr><td>Map hash</td><td><input name='maphash'</td></tr>" \
"<tr><td></td><td><input type='submit' value='Add' /></td></tr>" \
"</table>" \
"</form>" \


print "</body>" \
"</html>"

dbconnection.disconnectdb()


