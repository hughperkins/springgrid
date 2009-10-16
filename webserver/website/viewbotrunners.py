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
import datetime

from utils import *
from core import *

import config

dbconnection.connectdb()

sqlalchemysetup.setup()

loginhelper.processCookie()

menu.printPageTop()

botrunners = sqlalchemysetup.session.query(tableclasses.BotRunner)

print "<h3>AILadder - Bot Runner List</h3>" \
"<table border='1' padding='3'>" \
"<tr class='tablehead'><td>Bot Runner Name</td><td>Last ping time</td><td>Last ping status</td><td>Bot Runner Owner Name:</td><td>Shared secret (only visible for your own botrunners)</td><td>Options</td></tr>"

for botrunner in botrunners:
   pingtimeok = False
   lastpingtimeddate = None
   lastpingtime =  botrunner.botrunner_lastpingtime
   if lastpingtime != None:
      lastpingtimedate = dates.dateStringToDateTime( lastpingtime )
      secondssincelastping = dates.timedifftototalseconds( datetime.datetime.now() - lastpingtimedate )
      if secondssincelastping < config.pingtimeoutminutes * 60:
         pingtimeok = True

   if pingtimeok:
      print "<tr class='success'>"
   else:
      print "<tr>"
   print "<td><a href='viewbotrunner.py?botrunnername=" + botrunner.botrunner_name + "'>" + botrunner.botrunner_name + "</a></td>"
   print "<td>" + str( lastpingtimedate ) + "</td>"
   print "<td>" + str( botrunner.botrunner_lastpingstatus ) + "</td>"
   if botrunner.owneraccount != None:
      print "<td>" + botrunner.owneraccount.userfullname + "</td>"
   else:
      print "<td>&nbsp;</td>"
   if botrunner.owneraccount != None:
      if botrunner.owneraccount.username == loginhelper.gusername:
         print "<td>" + botrunner.botrunner_sharedsecret + "</td>"
   else:
      print "<td>&nbsp;</td>"

   print "<td>"
   for option in botrunner.options:
      print option.option.botrunner_option_name + "&npsp;"
   print "&nbsp;</td>"

   print "</tr>"

print "</table>"

if loginhelper.gusername != '' and False:

   print "<p />"
   print "<hr />"
   print "<p />"

   print "<h4>Register new bot runner:</h4>"
   print "You will automatically be marked as 'owner' of this botrunner<p />"
   print "<form action='addbotrunner.py' method='post'>" \
   "<table border='1' padding='3'>" \
   "<tr><td>Bot runner name</td><td><input name='botrunnername'</td></tr>" \
   "<tr><td>Bot runner shared secret</td><td><input name='sharedsecret'</td></tr>" \
   "<tr><td></td><td><input type='submit' value='Add' /></td></tr>" \
   "</table>" \
   "</form>"

sqlalchemysetup.close()

dbconnection.disconnectdb()

menu.printPageBottom()

