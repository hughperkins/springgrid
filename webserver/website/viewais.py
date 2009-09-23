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

dbconnection.connectdb()

print "Content-type: text/html"
print ""
print ""

ais = dbconnection.querytomaplist( "select ai_name, ai_version from ais", ('ai_name','ai_version' ) )

print "<html>" \
"<head>" \
"<title>AILadder - AI List</title>" \
"</head>" \
"<body>" \
"<h3>AILadder - AI List</h3>" \
"<table border='1' padding='3'>" \
"<tr><td>AI Name</td><td>AI Version</td></tr>"

for ai in ais:
   print "<tr><td>" + ai['ai_name'] + "</td><td>" + ai['ai_version'] + "</td></tr>"

print "</table>"

print "<p />"
print "<hr />"
print "<p />"

print "<h4>Register new AI:</h4>"
print "<form action='addai.py' method='post'>" \
"<table border='1' padding='3'>" \
"<tr><td>AI name</td><td><input name='ainame'</td></tr>" \
"<tr><td>AI version</td><td><input name='aiversion'</td></tr>" \
"<tr><td></td><td><input type='submit' value='Add' /></td></tr>" \
"</table>" \
"</form>" \


print "</body>" \
"</html>"

dbconnection.disconnectdb()


