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

leaguegroupname = formhelper.getValue('leaguegroupname')

dbconnection.cursor.execute( "select "\
   "     league_name "\
   " from leaguegroup_leaguemembers, leaguegroups, leagues "\
   " where leaguegroup_leaguemembers.leaguegroup_id = leaguegroups.leaguegroup_id " \
   " and leaguegroups.leaguegroup_name = %s "\
   " and leagues.league_id = leaguegroup_leaguemembers.league_id ",
   (leaguegroupname, ) )
leagues = []
row = dbconnection.cursor.fetchone()
while row != None:
   leagues.append( row[0])
   row = dbconnection.cursor.fetchone()

print "<h3>AILadder - View league group " + leaguegroupname + "</h3>" \
"<p>A league is a specific game configuration used for testing AIs "\
" against each other</p>"\
"<p>For example, a league could be a specific map, mod, and certain options,"\
" like say cheating on, or cheating off</p>"\
"<p>You can group leagues together in leaguegroups.</p>"\
"<table border='1' padding='3'>" \
"<tr class='tablehead'><td>Member league:</td></tr>"

for league in leagues:
   print "<tr>"
   print "<td>" + league + "</td>"
   print "</tr>"

print "</table>"

if loginhelper.gusername != '':

   print "<p />"
   print "<hr />"
   print "<p />"

   dbconnection.cursor.execute( "select "\
      "  league_name "\
      " from leagues "\
      " where not exists ( "\
      "    select * from leaguegroup_leaguemembers, leaguegroups " \
      "    where leaguegroup_leaguemembers.leaguegroup_id = leaguegroups.leaguegroup_id " \
      "    and leaguegroups.leaguegroup_name = %s "\
      "    and leagues.league_id = leaguegroup_leaguemembers.league_id )",
      (leaguegroupname, ) )
   potentialleagues = []
   row = dbconnection.cursor.fetchone()
   while row != None:
      potentialleagues.append( row[0])
      row = dbconnection.cursor.fetchone()

   print "<h4>Add league to league group:</h4>"
   print "<form action='addleaguetoleaguegroup.py' method='post'>" \
   "<table border='1' padding='3'>" \
   "<tr><td>League name</td><td>"
   print htmlformshelper.listToDropdown( 'leaguename', potentialleagues )
   print "</td></tr>"

   print "<tr><td></td><td><input type='submit' value='Add' /></td></tr>" \
   "</table>" \
   "<input type='hidden' name='leaguegroupname' value='" + leaguegroupname + "' />"\
   "</form>"

dbconnection.disconnectdb()

menu.printPageBottom()

