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
from core.tableclasses import *

sqlalchemysetup.setup()

loginhelper.processCookie()

menu.printPageTop()

botrunnername = formhelper.getValue("botrunnername")

botrunner = sqlalchemysetup.session.query(BotRunner).filter(BotRunner.botrunner_name == botrunnername ).first()

isbotrunnerowner = ( loginhelper.isLoggedOn() and botrunner.owneraccount != None and botrunner.owneraccount.username == loginhelper.getUsername() )

print "<h3>AILadder - Bot Runner '" + botrunnername + "'</h3>" \
"<table border='1' padding='3'>"

if botrunner.owneraccount != None:
   print "<tr><td>Bot runner owner: </td><td>" + botrunner.owneraccount.userfullname + "</td></tr>"
else:
   print "<tr><td>Bot runner owner: </td><td>None assigned</td></tr>"
if isbotrunnerowner:
   print "<tr><td>Shared secret: </td><td>" + botrunner.botrunner_sharedsecret + "</td></tr>"
else:
   print "<tr><td>Shared secret: </td><td>&lt;only visible to owner&gt;</td></tr>"

print "</table>"

print "<h3>Assigned options</h3>"

print "<table>"


if isbotrunnerowner:
   print "<tr class='tablehead'><td>Option name</td><td></td></tr>"
else:
   print "<tr class='tablehead'><td>Option name</td></tr>"

for option in botrunner.options:
   print "<tr><td>" + option.option.option_name + "</td>"
   if isbotrunnerowner:
      print "<td><a href='deleteoptionfrombotrunner.py?botrunnername=" + botrunnername + "&optionname=" + option.option.option_name + "'>Delete option</a></td>"
   print "</tr>"

print "</table>"

print "<h3>Supported Maps</h3>"

print "<table>"
print "<tr class='tablehead'><td>Map</td>"
for map in botrunner.supportedmaps:
   print "<tr class='success'><td>" + map.map.map_name + "</td>"
print "</table>"

print "<h3>Supported Mods</h3>"

print "<table>"
print "<tr class='tablehead'><td>Mod</td>"
for mod in botrunner.supportedmods:
   print "<tr class='success'><td>" + mod.mod.mod_name + "</td>"
print "</table>"

if isbotrunnerowner or roles.isInRole(roles.botrunneradmin):
   print "<p />"
   print "<hr />"
   print "<p />"

   potentialoptions = listhelper.tuplelisttolist( sqlalchemysetup.session.query(AIOption.option_name) )
   for option in botrunner.options:
      potentialoptions.remove(option.option.option_name )

   print "<h4>Add new options to engine:</h4>"
   print "<form action='addoptiontobotrunner.py' method='post'>" \
   "<table border='1' padding='3'>" \
   "<tr><td>Option to add:</td><td>" + htmlformshelper.listToDropdown( 'optionname', potentialoptions ) + "</td></tr>" \
   "<tr><td></td><td><input type='submit' value='Add' /></td></tr>" \
   "</table>" \
   "<input type='hidden' name='botrunnername' value='" + botrunnername + "' />"\
   "</form>"

sqlalchemysetup.close()

menu.printPageBottom()

