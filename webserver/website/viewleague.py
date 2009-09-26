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

leaguename = formhelper.getValue('leaguename')

compatibleoptions = dbconnection.querytolistwithparams( "select option_name "\
   " from leagueoptions, aioptions, leagues "\
   " where leagueoptions.league_id = leagues.league_id "\
   " and leagues.league_name = %s "\
   " and leagueoptions.option_id = aioptions.option_id ",
   ( leaguename, ) )

print "<h3>AILadder - View League '" + leaguename + "'</h3>"

print "<p>This page can configure the options that will be used for this league.</p>"
print "<p>Try to make sure not to add two incompatible options ;-)</p>"

print "<table border='1' padding='3'>" \
"<tr><td>Assigned options</td><td></td></tr>"

for option in compatibleoptions:
   print "<tr>"
   print "<td>" + option + "</td>"
   print "<td><a href='deleteoptionfromleague.py?leaguename=" + leaguename + "&aioption=" + option + "'>Remove option</a></td>"
   print "</tr>"

print "</table>"

if roles.isInRole(roles.leagueadmin):

   print "<p />"
   print "<hr />"
   print "<p />"

   print "<h4>Assign new options:</h4>"

   potentialoptions = dbconnection.querytolistwithparams( "select option_name "\
      " from aioptions "\
      " where not exists ( select * from leagues, leagueoptions "\
      " where leagueoptions.league_id = leagues.league_id "\
      " and leagues.league_name = %s "\
      " and leagueoptions.option_id = aioptions.option_id ) ",
      ( leaguename, ) )
  
   print "<form action='addoptiontoleague.py' method='post'>" \
   "<table border='1' padding='3'>" \
   "<tr><td>Option to add:</td><td>" + htmlformshelper.listToDropdown( 'aioption', potentialoptions ) + "</td></tr>" \
   "<tr><td></td><td><input type='submit' value='Add' /></td></tr>" \
   "</table>" \
   "<input type='hidden' name='leaguename' value='" + leaguename + "' />" \
   "</form>"


dbconnection.disconnectdb()

menu.printPageBottom()

