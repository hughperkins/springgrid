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

from utils import *
#from core import *
from tableclasses import *
import sqlalchemysetup
import botrunnerhelper
import confighelper

# go through matchrequests_inprogress table, and remove any rows
# where the session is older than a certain time
def archiveoldrequests():
   botrunnerhelper.purgeExpiredSessions()

# this should walk the queue till it finds something that the engine
# can handle
# for now, it just returns the first item in the queue
# we need to only take things that arent in the inprogress queue of course...
def getcompatibleitemfromqueue( botrunnername, sessionid ):
   archiveoldrequests()

   botrunner = botrunnerhelper.getBotRunner( botrunnername )
   botrunnersession = botrunnerhelper.getBotRunnerSession( botrunnername, sessionid )

   # Also, remove any requests that this engine was supposedly processing
   # for which there are no results
   matchrequests = sqlalchemysetup.session.query(MatchRequest).filter( MatchRequest.matchresult == None ).filter( MatchRequest.matchrequestinprogress != None )
   for matchrequest in matchrequests:
      if matchrequest.matchrequestinprogress.botrunner is botrunner:
         if matchrequest.matchrequestinprogress.botrunnersession is botrunnersession:
            sqlalchemysetup.session.delete( matchrequest.matchrequestinprogress )
   sqlalchemysetup.session.commit()

   # now we've archived the old requests, we just pick a request
   # in the future, we'll pick a compatible request.  In the future ;-)
   # also, we need to handle options.  In the future ;-)
   matchrequests = sqlalchemysetup.session.query(MatchRequest).filter(MatchRequest.matchrequestinprogress == None ).filter(MatchRequest.matchresult == None ).all()
   for matchrequest in matchrequests:
      mapok = False
      modok = False
      ai0ok = False
      ai1ok = False
      for map in botrunner.supportedmaps:
         if map.map_name == matchrequest.map.map_name:
            mapok = True
      for mod in botrunner.supportedmods:
         if mod.mod_name == matchrequest.mod.mod_name:
            modok = True
      for ai in botrunner.supportedais:
         if ai.ai_name == matchrequest.ai0.ai_name and ai.ai_version == matchrequest.ai0.ai_version:
            ai0ok = True 
         if ai.ai_name == matchrequest.ai1.ai_name and ai.ai_version == matchrequest.ai1.ai_version:
            ai1ok = True 
      if mapok and modok and ai0ok and ai1ok:
         # mark request in progress:
         matchrequest.matchrequestinprogress = MatchRequestInProgress( botrunner, botrunnersession, dates.dateTimeToDateString( datetime.datetime.now() ) )

         return matchrequest

   # didn't find any compatible match
   return None

def getmatchrequest(matchrequest_id):
   return sqlalchemysetup.session.query(MatchRequest).filter(MatchRequest.matchrequest_id == matchrequest_id ).first()

# validate that an incoming result is for a match assigned to this server
# return true if so, otherwise false
def matchrequestvalidforthisserver( botrunnername, matchrequest_id ):
   matchrequest = getmatchrequest( matchrequest_id )
   if matchrequest.matchrequestinprogress == None:
      return False
   return matchrequest.matchrequestinprogress.botrunner.botrunner_name == botrunnername

def storeresult( botrunnername, matchrequest_id, result ):
   # delete any existing result, saves doing check first...
   matchrequest = getmatchrequest( matchrequest_id )
   if matchrequest == None:
      return
   matchrequest.matchresult  = MatchResult( result )
   sqlalchemysetup.session.commit()

# returns the new match request, so can add options and so on
# doesn't commit
def addmatchrequest( ai0, ai1, mod, map, league = None ):
   newmatchrequest = MatchRequest( ai0 = ai0, ai1 = ai1, mod = mod, map = map, league = league )
   sqlalchemysetup.session.add(newmatchrequest)

