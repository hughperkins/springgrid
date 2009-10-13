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

# This contains code for manipulating the matchrequest tables

import datetime

import config

from utils import *
#from core import *

class MatchRequest:
   def __init__(self):
      pass


# go through matchrequests_inprogress table, and remove any rows
# older than a certain time
# placeholder for now
def archiveoldrequests():
   dbconnection.cursor.execute("select matchrequest_id, datetimeassigned from matchrequests_inprogress")
   row = dbconnection.cursor.fetchone()
   while row != None:
      matchrequestid = row[0]
      datetimestring = row[1]
      # datetime = dates.dateStringToDateTime( datetimestring )
      
      row = dbconnection.cursor.fetchone()

# this should walk the queue till it finds something that the engine
# can handle
# for now, it just returns the first item in the queue
# we need to only take things that arent in the inprogress queue of course...
def getcompatibleitemfromqueue( botrunnerdescription ):
   archiveoldrequests()
   # now we've archived the old requests, we just pick a request
   # in the future, we'll pick a compatible request.  In the future ;-)
   # also, we need to handle options.  In the future ;-)
   dbconnection.dictcursor.execute("select matchrequestqueue.matchrequest_id, ai0.ai_name as ai0name, ai0.ai_version as ai0version, ai1.ai_name as ai1name, ai1.ai_version as ai1version, map_name, map_archivechecksum, mod_name, mod_archivechecksum " \
      "from ais as ai0," \
      " ais as ai1, " \
      " maps, " \
      " mods, " \
      " matchrequestqueue " \
      " where ai0.ai_id = ai0_id " \
      " and ai1.ai_id = ai1_id " \
      " and maps.map_id = matchrequestqueue.map_id " \
      " and mods.mod_id = matchrequestqueue.mod_id " \
      " and not exists (select * from matchrequests_inprogress "\
      " where matchrequests_inprogress.matchrequest_id = matchrequestqueue.matchrequest_id ) " \
      " and not exists (select * from matchresults "\
      " where matchresults.matchrequest_id = matchrequestqueue.matchrequest_id ) " )
#      " left join matchrequests_inprogress on       " 
#matchrequests_inprogress.matchrequest_id = matchrequestqueue.matchrequest_id " \
#      " and not exists (select * from matchrequests_inprogress where " \
 #     "                     matchrequests_inprogress.matchrequest_id = matchrequestqueue.matchrequest_id ) " )
   row = dbconnection.dictcursor.fetchone()
   # just take the first one...
   if row != None:
      # we got a row
      matchrequest = MatchRequest()
      matchrequest.matchrequest_id = row['matchrequest_id']
      matchrequest.ai0name = row['ai0name']
      matchrequest.ai0version = row['ai0version']
      matchrequest.ai1name = row['ai1name']
      matchrequest.ai1version = row['ai1version']
      matchrequest.mapname = row['map_name']
      matchrequest.maparchivechecksum = row['map_archivechecksum']
      matchrequest.modname = row['mod_name']
      matchrequest.modarchivechecksum = row['mod_archivechecksum']
      return matchrequest
   else:
      # no rows left. great!
      return None

def markrequestasinprogress( requestitem, botrunnerdescription ):
   dbconnection.cursor.execute("delete from matchrequests_inprogress "\
      "where matchrequest_id = %s", ( requestitem.matchrequest_id, ) )
   dbconnection.cursor.execute("insert into matchrequests_inprogress "\
      "( matchrequest_id, botrunner_id, datetimeassigned ) "\
      " select %s, botrunners.botrunner_id, %s "\
      " from botrunners "\
      " where botrunners.botrunner_name = %s",
      ( requestitem.matchrequest_id, dates.dateTimeToDateString( datetime.datetime.now() ), botrunnerdescription ) )

# validate that an incoming result is for a match assigned to this server
# return true if so, otherwise false
def matchrequestvalidforthisserver( botrunnername, matchrequest_id ):
   print botrunnername + " " + str(matchrequest_id)
   rows = dbconnection.cursor.execute("select * from matchrequests_inprogress, "\
      " botrunners "\
      " where matchrequest_id = %s " \
      " and botrunners.botrunner_id = matchrequests_inprogress.botrunner_id "\
      " and botrunner_name = %s ",
      ( matchrequest_id, botrunnername, ) )
   return ( rows == 1 )

def submitrequest( requestitem ):
   # ignoring hashes for now...
   rows = dbconnection.cursor.execute("insert into matchrequestqueue (ai0_id, ai1_id, map_id, mod_id) " \
      " select ai0.ai_id, ai1.ai_id, map_id, mod_id " \
      " from ais ai0, ais ai1, maps, mods " \
      " where ai0.ai_name = %s " \
      " and ai0.ai_version = %s " \
      " and ai1.ai_name = %s " \
      " and ai1.ai_version =%s " \
      " and maps.map_name = %s " \
      " and mods.mod_name =%s ",
      (requestitem.ai0name, requestitem.ai0version, requestitem.ai1name, requestitem.ai1version,
          requestitem.mapname, requestitem.modname, ) )
   return ( rows == 1 )

def storeresult( botrunnername, matchrequest_id, result ):
   # delete any existing result, saves doing check first...
   dbconnection.cursor.execute("delete from matchresults where "\
      " matchrequest_id = %s ", ( matchrequest_id, ) )
   dbconnection.cursor.execute("insert into matchresults "\
      " (matchrequest_id, matchresult ) "\
      " values ( %s, %s ) ",
      ( matchrequest_id, result, ) )
#   # remove inprogress marker
 #  dbconnection.cursor.execute("delete from matchrequests_inprogress "\
  #     " where matchrequest_id = %s ", ( matchrequest_id,) )
1
