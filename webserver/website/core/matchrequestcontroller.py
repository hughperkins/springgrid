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

from sqlalchemy.orm import join

import config

from utils import *
#from core import *
from tableclasses import *
import sqlalchemysetup
import botrunnerhelper

# go through matchrequests_inprogress table, and remove any rows
# older than a certain time
# placeholder for now
def archiveoldrequests():
   pass
   #dbconnection.cursor.execute("select matchrequest_id, datetimeassigned from matchrequests_inprogress")
   #row = dbconnection.cursor.fetchone()
   #while row != None:
   #   matchrequestid = row[0]
   #   datetimestring = row[1]
   #   # datetime = dates.dateStringToDateTime( datetimestring )
      
  #    row = dbconnection.cursor.fetchone()

# this should walk the queue till it finds something that the engine
# can handle
# for now, it just returns the first item in the queue
# we need to only take things that arent in the inprogress queue of course...
def getcompatibleitemfromqueue( botrunnername ):
   archiveoldrequests()

   botrunner = botrunnerhelper.getbotrunner(botrunnername)

   # Also, remove any requests that this engine was supposedly processing
   # for which there are no results
   matchrequests = sqlalchemysetup.session.query(MatchRequest).filter( MatchRequest.matchresult == None ).filter( MatchRequest.matchrequestinprogress != None )
   for matchrequest in matchrequests:
      if matchrequest.matchrequestinprogress.botrunner is botrunner:
         sqlalchemysetup.session.delete( matchrequest.matchrequestinprogress )
   sqlalchemysetup.session.commit()

   # now we've archived the old requests, we just pick a request
   # in the future, we'll pick a compatible request.  In the future ;-)
   # also, we need to handle options.  In the future ;-)
   #matchrequests = sqlalchemysetup.session.query(MatchRequest.matchrequest_id, Map.map_name,Mod.mod_name).select_from(join(join(MatchRequest,Map),Mod)).filter(MatchRequest.matchrequestinprogress == None ).filter(MatchRequest.matchresult == None ).all()
   matchrequests = sqlalchemysetup.session.query(MatchRequest).filter(MatchRequest.matchrequestinprogress == None ).filter(MatchRequest.matchresult == None ).all()
   #print "matchrequests: " + str( matchrequests )
   for matchrequest in matchrequests:
      #print "matchrequest: " + str( matchrequest )
      #print matchrequest.map.map_name
      mapok = False
      for map in botrunner.supportedmaps:
         if map.map.map_name == matchrequest.map.map_name:
            mapok = True
            #print "mapok"
      modok = False
      for mod in botrunner.supportedmods:
         if mod.mod.mod_name == matchrequest.mod.mod_name:
            modok = True
            #print "modok"
      if mapok and modok:
         # mark request in progress:
         matchrequest.matchrequestinprogress = MatchRequestInProgress( botrunner, dates.dateTimeToDateString( datetime.datetime.now() ) )

         return matchrequest

   # didn't find any compatible match
   return None

def getmatchrequest(matchrequest_id):
   return sqlalchemysetup.session.query(MatchRequest).filter(MatchRequest.matchrequest_id == matchrequest_id ).first()

# validate that an incoming result is for a match assigned to this server
# return true if so, otherwise false
def matchrequestvalidforthisserver( botrunnername, matchrequest_id ):
   #print botrunnername + " " + str(matchrequest_id)
   matchrequest = getmatchrequest( matchrequest_id )
   if matchrequest.matchrequestinprogress == None:
      return False
   return matchrequest.matchrequestinprogress.botrunner.botrunner_name == botrunnername

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
   matchrequest = getmatchrequest( matchrequest_id )
   if matchrequest == None:
      return
   matchrequest.matchresult  = MatchResult( result )
   sqlalchemysetup.session.commit()

#   # remove inprogress marker
 #  dbconnection.cursor.execute("delete from matchrequests_inprogress "\
  #     " where matchrequest_id = %s ", ( matchrequest_id,) )

