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

# This page is called by the calcengines, and returns xml

# used to upload the result of a game to the webserver from the calcengine

import cgitb; cgitb.enable()
import sys
import os
import Cookie
# import cookiefile
import cgi

import config

from utils import *
from core import *

testing = False

scriptdir = os.path.dirname( os.path.realpath( __file__ ) )

print "Content-type: text/xml"
print ""
print ""

dbconnection.connectdb()

def run():
   if testing:
      calcenginehelper.calcenginename = 'test'

   if testing or calcenginehelper.calcengineauthorized():
      matchrequest_id = int(formhelper.getValue('matchrequestid'))
      result = formhelper.getValue('result') # 'ai0won', 'draw', 'crashed', 'hung', ...

      # check if this matchrequest_id was actually assigned to this engine
      # otherwise ditch the result
      if not matchrequestcontroller.matchrequestvalidforthisserver( calcenginehelper.calcenginename, matchrequest_id ):
         print "<response response='invalid matchrequest_id' />"
         return

      # store the result, and remove from queue
      # if the replay upload fails, well, that's a shame, but it's not the end 
      # of the world...
      # or we could get the calcengine to retry several times, to be decided.
      matchrequestcontroller.storeresult( calcenginehelper.calcenginename, matchrequest_id, result )

      # now to handle uploading the replay...
      formhelper.writeIncomingFileToDisk('replay', replaycontroller.getReplayPath(matchrequest_id)) # really, we should validate that this match was assigned to this server first...
                   # also, ideally, if there is no upload, we should store that info in the database somewheree
   else:
      print "<response response='unauthorized' />"

run()

dbconnection.disconnectdb()

