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

# webservice for use through xmlrpclib

import SimpleXMLRPCServer
import sys
import os
import datetime
import base64
import traceback

from utils import *
from core import *
from core.tableclasses import *

import config

# entry point for method calls from botrunner to the server
# botrunner simply calls getxmlrpcproxy().<methodname>( params, ... )
class SpringGridService:
   # return (True,'') if goes ok, otherwise (False,message)
   def ping(self, botrunnername, sharedsecret, sessionid, status):
      if not botrunnerhelper.validatesharedsecret(botrunnername, sharedsecret):
         return (False, "Not authenticated")

      botrunner = botrunnerhelper.getBotRunner( botrunnername )
      if botrunner == None:
         return (False,'')

      targetsession = None
      for session in botrunner.sessions:
         if session.botrunner_session_id == sessionid:
            targetsession = session

      if targetsession == None:
         targetsession = BotRunnerSession( sessionid )
         botrunner.sessions.append(targetsession)
      targetsession.lastpingtime = dates.dateTimeToDateString( datetime.datetime.now() )
      targetsession.lastpingstatus = status
      sqlalchemysetup.session.commit()
      return (True,'')

   # return (True,'') if goes ok, otherwise (False,message)
   # needs to pass as string, since xmlrpc doesn't support long :-/
   def registersupportedmap( self, botrunnername, sharedsecret, mapname, maparchivechecksum_string ):
      if not botrunnerhelper.validatesharedsecret(botrunnername, sharedsecret):
         return (False, "Not authenticated")

      if not maphelper.addmapifdoesntexist(mapname, long(maparchivechecksum_string)):
         return (False, "Couldn't register map")

      if not maphelper.setbotrunnersupportsthismap( botrunnername, mapname ):
         return (False, "couldn't mark map as supported for botrunner")

      return (True,'')

   # return (True,'') if goes ok, otherwise (False,message)
   # needs to pass as string, since xmlrpc doesn't support long :-/
   def registersupportedmod( self, botrunnername, sharedsecret, modname, modarchivechecksum_string ):
      if not botrunnerhelper.validatesharedsecret(botrunnername, sharedsecret):
         return (False, "Not authenticated")

      if not modhelper.addmodifdoesntexist(modname, long(modarchivechecksum_string)):
         return (False, "Couldn't register mod")

      if not modhelper.setbotrunnersupportsthismod( botrunnername, modname ):
         return (False, "couldn't mark mod as supported for botrunner")

      return (True,'')

   def registersupportedai( self, botrunnername, sharedsecret, ainame, aiversion ):
      if not botrunnerhelper.validatesharedsecret(botrunnername, sharedsecret):
         return (False, "Not authenticated")

      if not aihelper.addaiifdoesntexist(ainame, aiversion):
         return (False, "Couldn't register ai")

      if not aihelper.setbotrunnersupportsthisai( botrunnername, ainame, aiversion ):
         return (False, "couldn't mark ai as supported for botrunner")

      return (True,'')

   def getsupportedmods( self, botrunnername, sharedsecret ):
      return modhelper.getsupportedmods(botrunnername)

   def getsupportedmaps( self, botrunnername, sharedsecret ):
      return maphelper.getsupportedmaps(botrunnername)

   def getsupportedais( self, botrunnername, sharedsecret ):
      return aihelper.getsupportedais(botrunnername)

   #  resultstring is: 'ai0won', 'draw', 'crashed', 'hung', ...
   # returns (True,message) or (False,message)
   def submitresult( self, botrunnername, sharedsecret, matchrequestid, resultstring, uploaddatadict ):
      try:
         if not botrunnerhelper.validatesharedsecret(botrunnername, sharedsecret):
            return (False, "Not authenticated")

         # check if this matchrequest_id was actually assigned to this engine
         # otherwise ditch the result
         if not matchrequestcontroller.matchrequestvalidforthisserver( botrunnername, matchrequestid ):
            return (False, "invalid matchrequestid" )

         # store the result, and remove from queue
         # if the replay upload fails, well, that's a shame, but it's not the end 
         # of the world...
         # or we could get the botrunner to retry several times, to be decided.
         matchrequestcontroller.storeresult( botrunnername, matchrequestid, resultstring )

         if uploaddatadict.has_key('replay'):
            # now to handle uploading the replay...
            replaycontentsraw = uploaddatadict['replay'].data
            if replaycontentsraw != None and replaycontentsraw != '':
               replayfilehandle = open( replaycontroller.getReplayPath(matchrequestid), "wb" )
               replayfilehandle.write( replaycontentsraw )
               replayfilehandle.close()
            # really, we should validate that this match was assigned to this server first...
            # also, ideally, if there is no upload, we should store that info in the database somewheree

         if uploaddatadict.has_key('infolog'):
            contentsraw = uploaddatadict['infolog'].data
            if contentsraw != None and contentsraw != '':
               filehandle = open( replaycontroller.getInfologPath(matchrequestid), "wb" )
               filehandle.write( contentsraw )
               filehandle.close()

         return (True,'' )
      except:
         return (False,"An unexpected exception occurred: " + str( sys.exc_info() ) + "\n" + str( traceback.extract_tb( sys.exc_traceback ) ) )

   # request info on an ai that can be downloaded that matches a match currently available in the queue
   # the idea is that the botrunner will:
   # - cycle through all hosts looking for a match
   # - if it finds one -> great
   # - otherwise it checks with each host if there is an ai that it would be useful to download
   # - note that where there are multiple sessions for a botrunner, only one session will be 
   #   assigned a specific ai to download, ie they can download different ones in paralle
   #   but not the same one.  That's for configurations like aegis' where all AIs are in the same
   #   physical directory across all instances
   # Note that after downloading, the botrunner is expected to reregister capabilities before
   # doing anything else, eg before making new requests for download
   # Also, we'll just assume that any botrunner that calls this is ok with downloadnig stuff
   # otherwise it wouldnt have called htis ;-)
   def getdownloadrequest( self, botrunnername, sharedsecret, sessionid ):
      try:
         if not botrunnerhelper.validatesharedsecret(botrunnername, sharedsecret):
            return (False, "Not authenticated")
  
         botrunner = botrunnerhelper.getBotRunner( botrunnername )

         requests = sqlalchemysetup.session.query(MatchRequest).\
            filter(MatchRequest.matchresult == None ).\
            filter(MatchRequest.matchrequestinprogress == None ).\
            all()
         aitodownload = None
         for request in requests:
            mapok = False
            modok = False
            ai0ok = False
            ai1ok = False
            # probably can add this stuff to the query abovee, but not sure how compliated that
            # would look.  fairly readable in this format at least
            for map in botrunner.supportedmaps:
               if map.map_name == request.map.map_name:
                  mapok = True
            for mod in botrunner.supportedmods:
               if mod.mod_name == request.mod.mod_name:
                  modok = True
            for ai in botrunner.supportedais:
               if ai.ai_name == request.ai0.ai_name and ai.ai_version == request.ai0.ai_version:
                  ai0ok = True 
               if ai.ai_name == request.ai1.ai_name and ai.ai_version == request.ai1.ai_version:
                  ai1ok = True 
            if mapok and modok:
               if not ai0ok and not request.ai0.ai_needscompiling:  # this should be added to some flags somewhere, but for now....
                  aitodownload = request.ai0
               if not ai1ok and not request.ai1.ai_needscompiling:
                  aitodownload = request.ai1
         if aitodownload == None:
            return [True,[]]  #cannot return None in python xmlrpclib 2.4
         return [True,[{'ai_name': aitodownload.ai_name, 
                        'ai_version': aitodownload.ai_version,
                        'ai_downloadurl': aitodownload.ai_downloadurl,
                        'ai_needscompiling': aitodownload.ai_needscompiling } ] ]
      except:
         return (False,"An unexpected exception occurred: " + str( sys.exc_info() ) + "\n" + str( traceback.extract_tb( sys.exc_traceback ) ) )

   # returns (True, request) (True, None) or (False, errormessage)
   def getrequest( self, botrunnername, sharedsecret, sessionid ):
      try:
         if not botrunnerhelper.validatesharedsecret(botrunnername, sharedsecret):
            return (False, "Not authenticated")

         requestitem = matchrequestcontroller.getcompatibleitemfromqueue(botrunnername, sessionid)
         if requestitem == None:
            return ( True, [] ) # can't return None in python 2.4

         # convert to dict, otherwise can't marshall :-/
         # is there a better way to do this?
         requestitemdict = {}

         requestitemdict['matchrequest_id'] = requestitem.matchrequest_id
         requestitemdict['ai0_name'] = requestitem.ai0.ai_name
         requestitemdict['ai0_version'] = requestitem.ai0.ai_version
         requestitemdict['ai1_name'] = requestitem.ai1.ai_name
         requestitemdict['ai1_version'] = requestitem.ai1.ai_version
         requestitemdict['map_name'] = requestitem.map.map_name
         requestitemdict['mod_name'] = requestitem.mod.mod_name
         requestitemdict['gametimeoutminutes'] = confighelper.getValue('gametimeoutminutes')
         requestitemdict['gameendstring'] = confighelper.getValue('gameendstring')

         return (True, [ requestitemdict ] )  
      except:
         return (False,"An unexpected exception occurred: " + str( sys.exc_info() ) + "\n" + str( traceback.extract_tb( sys.exc_traceback ) ) )

handler = SimpleXMLRPCServer.CGIXMLRPCRequestHandler()
handler.register_instance( SpringGridService() )
handler.register_introspection_functions()
handler.register_multicall_functions()

if __name__ == '__main__':
   sqlalchemysetup.setup()
   try:
      handler.handle_request()
   except:
      print str( sys.exc_value )
   sqlalchemysetup.close()

