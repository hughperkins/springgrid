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

# This is basically used for debug
# It pumps a single request into the queue
# Once there are other systems in place, this file will either be purged, moved
# elsewhere, or protected by some admin authentication system
# for now, no authentication...

# also, no form for now, we just put the request into the querystring ;-)

import cgitb; cgitb.enable()
import sys
import os
import Cookie
# import cookiefile
import cgi

import config

from utils import *
from core import *

# get request from form
#matchrequest = matchrequestcontroller.MatchRequest()
ai0name = formhelper.getValue("ai0name")
ai0version = formhelper.getValue("ai0version")
ai1name = formhelper.getValue("ai1name")
ai1version = formhelper.getValue("ai1version")
mapname = formhelper.getValue("mapname")
# matchrequest.maphash = formhelper.getValue("maphash")
modname = formhelper.getValue("modname")
# matchrequest.modhash = formhelper.getValue("modhash")

print "Content-type: text/html"
print ""
print ""

dbconnection.connectdb()

loginhelper.processCookie()

menu.printPageTop()

if loginhelper.isLoggedOn():
   #if matchrequestcontroller.submitrequest( matchrequest ):
    #  print "Submitted"
      # could be nice to print out queue here, or make another page for that

   # we need to get the matchrequestid first, otherwise we 
   # can't retrieve it reliably
   # if someone beats us to it on that id, we'll get a unique
   # row violation, which is ok
   dbconnection.cursor.execute("select max(matchrequest_id) "\
      " from matchrequestqueue " )
   matchrequestid = dbconnection.cursor.fetchone()[0] + 1
   rows = dbconnection.cursor.execute("insert into matchrequestqueue (matchrequest_id, ai0_id, ai1_id, map_id, mod_id) " \
      " select %s, ai0.ai_id, ai1.ai_id, map_id, mod_id " \
      " from ais ai0, ais ai1, maps, mods " \
      " where ai0.ai_name = %s " \
      " and ai0.ai_version = %s " \
      " and ai1.ai_name = %s " \
      " and ai1.ai_version =%s " \
      " and maps.map_name = %s " \
      " and mods.mod_name =%s ",
      (matchrequestid, ai0name, ai0version, ai1name, ai1version,
      mapname, modname, ) )
   if rows == 1:
      #print dbconnection.cursor.fetchone()[0]

      # add options:
      options = dbconnection.querytolist("select option_name from aioptions")
      selectedoptions = []
      # get selected options from form submission:
      for option in options:
         if formhelper.getValue( "option_" + option ) != None:
            selectedoptions.append( option )
      # add to db
      for option in selectedoptions:
         dbconnection.cursor.execute("insert into matchrequest_options "\
            " ( matchrequest_id, option_id ) " \
            " select %s, option_id "\
            " from aioptions "\
            " where aioptions.option_name = %s ",
            (matchrequestid,option) )
      print "Submitted ok"
   else:
      print "Not submitted, please check your values and try again."
else:
   print "Please login first."

dbconnection.disconnectdb()

menu.printPageBottom()

