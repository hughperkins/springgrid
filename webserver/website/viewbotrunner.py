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
sqlalchemysetup.setup()

loginhelper.processCookie()

menu.printPageTop()

botrunnername = formhelper.getValue("botrunnername")

dbconnection.dictcursor.execute( "select "\
   "    username, "\
   "    userfullname, "\
   "    botrunner_sharedsecret "\
   " from botrunners " \
   "  left join accounts "\
   " on botrunners.botrunner_owneraccountid = accounts.account_id "\
   " where botrunners.botrunner_name = %s "\
,
   (botrunnername ) )
row = dbconnection.dictcursor.fetchone()

isbotrunnerowner = ( loginhelper.isLoggedOn() and row['username'] != None and row['username'] == loginhelper.getUsername() )

options = dbconnection.querytolistwithparams( "select botrunner_option_name "\
      " from botrunner_options, botrunner_assignedoptions, botrunners "\
      " where botrunners.botrunner_name = %s "\
      " and botrunner_assignedoptions.botrunner_id = botrunners.botrunner_id "\
      " and botrunner_options.botrunner_option_id = botrunner_assignedoptions.botrunner_option_id ",
      ( botrunnername, ) )

print "<h3>AILadder - Bot Runner '" + botrunnername + "'</h3>" \
"<table border='1' padding='3'>"

if row['userfullname'] != None:
   print "<tr><td>Bot runner owner: </td><td>" + row['userfullname'] + "</td></tr>"
else:
   print "<tr><td>Bot runner owner: </td></tr>"
if isbotrunnerowner:
   print "<tr><td>Shared secret: </td><td>" + row['botrunner_sharedsecret'] + "</td></tr>"
else:
   print "<tr><td>Shared secret: </td><td>&lt;only visible to owner&gt;</td></tr>"

print "</table>"

print "<h3>Assigned options</h3>"

print "<table>"


if isbotrunnerowner:
   print "<tr class='tablehead'><td>Option name</td><td></td></tr>"
else:
   print "<tr class='tablehead'><td>Option name</td></tr>"

for option in options:
   print "<tr><td>" + option + "</td>"
   if isbotrunnerowner:
      print "<td><a href='deleteoptionfrombotrunner.py?botrunnername=" + botrunnername + "&optionname=" + option + "'>Delete option</a></td>"
   print "</tr>"

print "</table>"

print "<h3>Supported Maps</h3>"

maps = dbconnection.querytolistwithparams( "select map_name "\
   " from maps, botrunner_supportedmaps, botrunners "\
   " where botrunners   .botrunner_id = botrunner_supportedmaps.botrunner_id "\
   " and maps.map_id = botrunner_supportedmaps.map_id "\
   " and botrunners.botrunner_name = %s ",
   ( botrunnername ) )
print "<table>"
print "<tr class='tablehead'><td>Map</td>"
for map in maps:
   print "<tr class='success'><td>" + map + "</td>"
print "</table>"

print "<h3>Supported Mods</h3>"

mods = dbconnection.querytolistwithparams( "select mod_name "\
   " from mods, botrunner_supportedmods, botrunners "\
   " where botrunners   .botrunner_id = botrunner_supportedmods.botrunner_id "\
   " and mods.mod_id = botrunner_supportedmods.mod_id "\
   " and botrunners.botrunner_name = %s ",
   ( botrunnername ) )
print "<table>"
print "<tr class='tablehead'><td>Mod</td>"
for mod in mods:
   print "<tr class='success'><td>" + mod + "</td>"
print "</table>"

if row['username'] == loginhelper.getUsername():

   print "<p />"
   print "<hr />"
   print "<p />"

   potentialoptions = dbconnection.querytolistwithparams( "select botrunner_option_name "\
         " from botrunner_options where not exists( "\
         " select * from botrunner_assignedoptions, botrunners "\
         " where botrunners.botrunner_name = %s "\
         " and botrunner_assignedoptions.botrunner_id = botrunners.botrunner_id "\
         " and botrunner_options.botrunner_option_id = botrunner_assignedoptions.botrunner_option_id "
         " ) ",
         ( botrunnername, ) )

   print "<h4>Add new options to engine:</h4>"
   print "<form action='addoptiontobotrunner.py' method='post'>" \
   "<table border='1' padding='3'>" \
   "<tr><td>Option to add:</td><td>" + htmlformshelper.listToDropdown( 'optionname', potentialoptions ) + "</td></tr>" \
   "<tr><td></td><td><input type='submit' value='Add' /></td></tr>" \
   "</table>" \
   "<input type='hidden' name='botrunnername' value='" + botrunnername + "' />"\
   "</form>"

dbconnection.disconnectdb()
sqlalchemysetup.close()

menu.printPageBottom()

