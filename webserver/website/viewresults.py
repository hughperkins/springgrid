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
import os

from utils import *
from core import *

import core.replaycontroller as replaycontroller

sqlalchemysetup.setup()

loginhelper.processCookie()

menu.printPageTop()

requests = sqlalchemysetup.session.query(tableclasses.MatchRequest)

print "<h3>AILadder - Match results</h3>" \
"<table>" \
"<tr class='tablehead'>"
print "<td>matchrequestid</td>"
print "<td>ai0name</td>"
print "<td>ai0version</td>"
print "<td>ai1name</td>"
print "<td>ai1version</td>"
print "<td>mapname</td>"
print "<td>modname</td>"
print "<td>options</td>"
print "<td>botrunnername</td>"
print "<td>result</td>"
print "<td>replay</td>"
print "</tr>"

for request in requests:
   if request.matchresult == None:
      continue
   print "<tr>"
   print "<td>" + str(request.matchrequest_id) + "</td>"
   print "<td>" + request.ai0.ai_name + "</td>"
   print "<td>" + request.ai0.ai_version + "</td>"
   print "<td>" + request.ai1.ai_name + "</td>"
   print "<td>" + request.ai1.ai_version + "</td>"
   print "<td>" + request.map.map_name + "</td>"
   print "<td>" + request.mod.mod_name + "</td>"
   print "<td>"
   for option in request.options:
      print option.option.option_name + "&nbsp;" 
   print "&nbsp;</td>"
   print "<td>" + request.matchrequestinprogress.botrunner.botrunner_name + "</td>"
   print "<td>" + request.matchresult.matchresult + "</td>"
   print "<td>"
   if os.path.isfile( replaycontroller.getReplayPath(request.matchrequest_id) ):
      print "<a href='" + replaycontroller.getReplayWebRelativePath(request.matchrequest_id) + "'>replay</a>"
   print "</td>"
   print "</tr>"

print "</table>"

sqlalchemysetup.close()

menu.printPageBottom()

