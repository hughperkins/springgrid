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

mods = dbconnection.querytomaplist( "select mod_name, mod_hash from mods", ('mod_name','mod_hash' ) )

print "<html>" \
"<head>" \
"<title>AILadder - Mod List</title>" \
"</head>" \
"<body>" \
"<h3>AILadder - Mod List</h3>" \
"<table border='1' padding='3'>" \
"<tr><td>Mod name</td><td>Mod hash</td></tr>"

for mod in mods:
   print "<tr><td>" + mod['mod_name'] + "</td><td>" + mod['mod_hash'] + "</td></tr>"

print "</table>"

if loginhelper.gusername != '':

   print "<p />"
   print "<hr />"
   print "<p />"

   print "<h4>Register new mod:</h4>"
   print "Note: the modname and the modhash should be set to whatever is used "
   print "in the startscript, so an easy way to get them is to start a game "
   print "from the lobby, then look at the file 'script.txt' in the spring "
   print "game directory<p />"
   print "<form action='addmod.py' method='post'>" \
   "<table border='1' padding='3'>" \
   "<tr><td>Mod name</td><td><input name='modname'</td></tr>" \
   "<tr><td>Mod hash</td><td><input name='modhash'</td></tr>" \
   "<tr><td></td><td><input type='submit' value='Add' /></td></tr>" \
   "</table>" \
   "</form>" \


print "</body>" \
"</html>"

dbconnection.disconnectdb()


