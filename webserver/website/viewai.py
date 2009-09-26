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

ainame = formhelper.getValue('ainame')
aiversion = formhelper.getValue('aiversion')

compatibleoptions = dbconnection.querytolistwithparams( "select option_name "\
   " from ai_allowedoptions, aioptions, ais "\
   " where ai_allowedoptions.option_id = aioptions.option_id "\
   " and ai_allowedoptions.ai_id = ais.ai_id "\
   " and ais.ai_name = %s "\
   " and ais.ai_version= %s ",
   ( ainame, aiversion, ) )

print "<h3>AILadder - View AI '" + ainame + " " + aiversion + "'</h3>"

print "<p>This page can configure the options compatible with one ai</p>"
print "<p>For example, if it can run when cheating is allowed, then add the option 'cheatingallowed', or, if it can run when cheating is banned, then add the option 'cheatingequalslose'</p>"

print "<table border='1' padding='3'>" \
"<tr><td>Compatible options</td><td></td></tr>"

for option in compatibleoptions:
   print "<tr>"
   print "<td>" + option + "</td>"
   print "<td><a href='deleteoptionfromai.py?ainame=" + ainame + "&aiversion=" + aiversion + "&aioption=" + option + "'>Remove option</a></td>"
   print "</tr>"

print "</table>"

if roles.isInRole(roles.aiadmin):

   print "<p />"
   print "<hr />"
   print "<p />"

   print "<h4>Add new compatible options:</h4>"

   potentialoptions = dbconnection.querytolistwithparams( "select option_name from aioptions where not exists ( "\
   "    select * from ai_allowedoptions, ais "\
   "    where ai_allowedoptions.option_id = aioptions.option_id "\
   "    and ai_allowedoptions.ai_id = ais.ai_id "\
   "    and ais.ai_name = %s "\
   "    and ais.ai_version= %s ) ",
   ( ainame, aiversion, ) )
  
   print "<form action='addoptiontoai.py' method='post'>" \
   "<table border='1' padding='3'>" \
   "<tr><td>Option to add:</td><td>" + htmlformshelper.listToDropdown( 'aioption', potentialoptions ) + "</td></tr>" \
   "<tr><td></td><td><input type='submit' value='Add' /></td></tr>" \
   "</table>" \
   "<input type='hidden' name='ainame' value='" + ainame + "' />" \
   "<input type='hidden' name='aiversion' value='" + aiversion + "' />" \
   "</form>"

menu.printPageBottom()

dbconnection.disconnectdb()


