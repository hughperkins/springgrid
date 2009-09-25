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

import utils.dbconnection as dbconnection
import utils.htmlformshelper as htmlformshelper
import utils.loginhelper as loginhelper

import core.replaycontroller as replaycontroller

dbconnection.connectdb()

loginhelper.processCookie()

print "Content-type: text/html"
print ""
print ""

requests = dbconnection.querytomaplist( "select matchrequestqueue.matchrequest_id, " \
      "ai0.ai_name, "\
      "ai0.ai_version, "\
      "ai1.ai_name, "\
      "ai1.ai_version, "\
      "map_name, "\
      "mod_name, " \
      "calcengine_name, "\
      "matchresult "\
      "from ais as ai0, "\
      "   ais as ai1, "\
      "   maps, "\
      "   mods, "\
      "   matchrequestqueue, "\
      "   matchrequests_inprogress, "\
      "   matchresults, "\
      "   calcengines "\
      " where "\
      "   matchresults.matchrequest_id = matchrequestqueue.matchrequest_id " \
      "   and matchrequests_inprogress.matchrequest_id = matchrequestqueue.matchrequest_id " \
      "   and calcengines.calcengine_id = matchrequests_inprogress.calcengine_id"\
      "   and ai0.ai_id = matchrequestqueue.ai0_id "\
      "   and ai1.ai_id = matchrequestqueue.ai1_id "\
      "   and maps.map_id = matchrequestqueue.map_id "\
      "   and mods.mod_id = matchrequestqueue.mod_id ",
   ( 'matchrequestid','ai0name', 'ai0version', 'ai1name', 'ai1version', 'mapname', 'modname', 'calcenginename', 'matchresult', ) )

print "<html>" \
"<head>" \
"<title>AILadder - Match results</title>" \
"</head>" \
"<body>" \
"<h3>AILadder - Match results</h3>" \
"<table border='1' padding='3'>" \
"<tr>"
print "<td>matchrequestid</td>"
print "<td>ai0name</td>"
print "<td>ai0version</td>"
print "<td>ai1name</td>"
print "<td>ai1version</td>"
print "<td>mapname</td>"
print "<td>modname</td>"
print "<td>calcenginename</td>"
print "<td>result</td>"
print "<td>replay</td>"
print "</tr>"

for request in requests:
   print "<tr>"
   matchrequest_id = request['matchrequestid']
   print "<td>" + str(request['matchrequestid']) + "</td>"
   print "<td>" + request['ai0name'] + "</td>"
   print "<td>" + request['ai0version'] + "</td>"
   print "<td>" + request['ai1name'] + "</td>"
   print "<td>" + request['ai1version'] + "</td>"
   print "<td>" + request['mapname'] + "</td>"
   print "<td>" + request['modname'] + "</td>"
   print "<td>" + str(request['calcenginename']) + "</td>"
   print "<td>" + str(request['matchresult']) + "</td>"
   print "<td>"
   if os.path.isfile( replaycontroller.getReplayPath(matchrequest_id) ):
      print "<a href='" + replaycontroller.getReplayWebRelativePath(matchrequest_id) + "'>replay</a>"
   print "</td>"
   print "</tr>"

print "</table>"

print "</body>" \
"</html>"

dbconnection.disconnectdb()


