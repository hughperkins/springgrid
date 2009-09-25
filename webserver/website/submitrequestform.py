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

# creates a form to submit a single game request
# this won't be used later on, but it's good for getting the site started
# with something that works

# we'll load the available ai names, versions, maps, and mods
# from the database, to make it easy to use

import cgitb; cgitb.enable()

import utils.loginhelper as loginhelper
import utils.dbconnection as dbconnection
import utils.formhelper as formhelper
import utils.htmlformshelper as htmlformshelper

dbconnection.connectdb()

print "Content-type: text/html"
print ""
print ""

ainames = dbconnection.querytolist("select distinct ai_name from ais")
# just get all aiversions for now, otherwise we need ajax and stuff...
aiversions = dbconnection.querytolist("select distinct ai_version from ais")
maps = dbconnection.querytolist("select distinct map_name from maps")
mods = dbconnection.querytolist("select distinct mod_name from mods")

print "<html>" \
"<head>" \
"<title>AILadder - submit game request</title>" \
"</head>" \
"<body>" \
"<h3>AILadder - submit game request</h3>" \
"<form action='submitrequest.py' method='post'>" \
"<table border='1' padding='3'>" \
"<tr><td>AI0 name</td><td>" + htmlformshelper.listToDropdown("ai0name", ainames) + "</td></tr>" \
"<tr><td>AI0 version</td><td>" + htmlformshelper.listToDropdown("ai0version", aiversions) + "</td></tr>" \
"<tr><td>AI1 name</td><td>" + htmlformshelper.listToDropdown("ai1name", ainames) + "</td></tr>" \
"<tr><td>AI1 version</td><td>" + htmlformshelper.listToDropdown("ai1version", aiversions) + "</td></tr>" \
"<tr><td>Map</td><td>" + htmlformshelper.listToDropdown("mapname", maps) + "</td></tr>" \
"<tr><td>Mod</td><td>" + htmlformshelper.listToDropdown("modname", mods) + "</td></tr>" \
"<tr><td></td><td><input type='submit' value='Submit Request' /></td></tr>" \
"</table>" \
"</form>" \
"</body>" \
"</html>"

dbconnection.disconnectdb()

