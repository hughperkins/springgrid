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

import dbconnection
import dates
import config

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
      datetime = dates.dateStringToDateTime( datetimestring )
      
      row = dbconnection.cursor.fetchone()

# this should walk the queue till it finds something that the engine
# can handle
# for now, it just returns the first item in the queue
# we need to only take things that arent in the inprogress queue of course...
def getcompatibleitemfromqueue( calcenginedescription ):
   archiveoldrequests()
   # now we've archived the old requests, we just pick a request
   # in the future, we'll pick a compatible request.  In the future ;-)
   # also, we need to handle options.  In the future ;-)
   dbconnection.cursor.execute("select matchrequestqueue.matchrequest_id, ai0.ai_name, ai0.ai_version, ai1.ai_name, ai1.ai_version, map_name, map_hash, mod_name, mod_hash " \
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
      " where matchrequests_inprogress.matchrequest_id = matchrequestqueue.matchrequest_id ) " )
#      " left join matchrequests_inprogress on       " 
#matchrequests_inprogress.matchrequest_id = matchrequestqueue.matchrequest_id " \
#      " and not exists (select * from matchrequests_inprogress where " \
 #     "                     matchrequests_inprogress.matchrequest_id = matchrequestqueue.matchrequest_id ) " )
   row = dbconnection.cursor.fetchone()
   # just take the first one...
   if row != None:
      # we got a row
      matchrequest = MatchRequest()
      matchrequest.matchrequest_id = row[0]
      matchrequest.ai0name = row[1]
      matchrequest.ai0version = row[2]
      matchrequest.ai1name = row[3]
      matchrequest.ai1version = row[4]
      matchrequest.mapname = row[5]
      matchrequest.maphash = row[6]
      matchrequest.modname = row[7]
      matchrequest.modhash = row[8]
      return matchrequest
   else:
      # no rows left. great!
      return None

def markrequestasinprogress( requestitem, calcenginedescription ):
   dbconnection.cursor.execute("delete from matchrequests_inprogress "\
      "where matchrequest_id = %s", ( requestitem.matchrequest_id, ) )
   dbconnection.cursor.execute("insert into matchrequests_inprogress "\
      "( matchrequest_id, calcengine_id, datetimeassigned ) "\
      " select %s, calcengines.calcengine_id, %s "\
      " from calcengines "\
      " where calcengines.calcengine_name = %s",
      ( requestitem.matchrequest_id, dates.dateTimeToDateString( datetime.datetime.now() ), calcenginedescription ) )

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

