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

rows = dbconnection.querytomaplist( "select "\
   "    league_name, "\
   "    mod_name, "\
   "    map_name "\
   " from leagues, maps, mods " \
   " where leagues.map_id = maps.map_id "\
   " and leagues.mod_id = mods.mod_id ",
   ('leaguename', 'modname', 'mapname' ) )

print "<h3>AILadder - View leagues</h3>" \
"<p>A league is a specific game configuration used for testing AIs "\
" against each other</p>"\
"<p>For example, a league could be a specific map, mod, and certain options,"\
" like say cheating on, or cheating off</p>"\
"<p>You can group leagues together in leaguegroups.</p>"\
"<table border='1' padding='3'>" \
"<tr class='tablehead'><td>League Name:</td><td>Mod Name</td><td>Map Name</td><td>Assigned options</td></tr>"

for row in rows:
   print "<tr>"
   print "<td><a href='viewleague.py?leaguename=" + row['leaguename'] + "'>" + row['leaguename'] + "</a></td>"
   print "<td>" + row['modname'] + "</td>"
   print "<td>" + row['mapname'] + "</td>"

   print "<td>"
   options = dbconnection.querytolistwithparams("select option_name "\
      " from aioptions, leagueoptions, leagues " \
      " where leagueoptions.option_id = aioptions.option_id "\
      " and leagueoptions.league_id = leagues.league_id "\
      " and league_name = %s ",
      ( row['leaguename'], ) )
   print ' '.join( options )
   print "</td>"

   print "</tr>"

print "</table>"

if loginhelper.gusername != '':

   print "<p />"
   print "<hr />"
   print "<p />"

   maps = dbconnection.querytolist("select map_name from maps")
   mods = dbconnection.querytolist("select mod_name from mods")

   print "<h4>Create new league:</h4>"
   print "<form action='addleague.py' method='post'>" \
   "<table border='1' padding='3'>" \
   "<tr><td>League name</td><td><input name='leaguename'</td></tr>"
   print "<tr><td>Mod name</td><td>" + htmlformshelper.listToDropdown( 'modname', mods ) + "</td></tr>"
   print "<tr><td>Map name</td><td>" + htmlformshelper.listToDropdown( 'mapname', maps ) + "</td></tr>"   

   print "<tr><td></td><td><input type='submit' value='Add' /></td></tr>" \
   "</table>" \
   "</form>"

dbconnection.disconnectdb()

menu.printPageBottom()

