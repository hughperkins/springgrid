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
class APIService:
   # returns a list of mapnames
   def getmaps(self):
      return listhelper.tuplelisttolist( sqlalchemysetup.session.query(Map.map_name) )

   # returns a list of modnames
   def getmods(self):
      return listhelper.tuplelisttolist( sqlalchemysetup.session.query(Mod.mod_name) )

   # returns a list of {'ai_name': ainame, 'ai_version': aiversion } ] dictionaries
   def getais(self):
      ailist = []
      for ai in sqlalchemysetup.session.query(AI):
         ailist.append({'ai_name': ai.ai_name, 'ai_version': ai.ai_version})
      return ailist

   # schedule a single match
   # - 'ais' should contain a list of {'ai_name': ainame, 'ai_version': aiversion} dicts
   # containing all ais that should play on the map
   # - 'options' should contain a list of option name strings
   #
   # note: later versions of this function should be added with a new version number
   # ie v2, v3 etc... to avoid breaking the api for old clients
   # returns [True,''] or [False, errormessage ]
   def schedulematchv1(self,map_name,mod_name,ais,options):
      try:
         map = sqlalchemysetup.session.query(Map).filter(Map.map_name == map_name ).first()
         mod = sqlalchemysetup.session.query(Mod).filter(Mod.mod_name == mod_name ).first()
         ai0 = sqlalchemysetup.session.query(AI).filter(AI.ai_name == ais[0]['ai_name'] ).filter(AI.ai_version == ais[0]['ai_version'] ).first()
         ai1 = sqlalchemysetup.session.query(AI).filter(AI.ai_name == ais[1]['ai_name'] ).filter(AI.ai_version == ais[1]['ai_version'] ).first()

         matchrequest = MatchRequest( ai0 = ai0, ai1 = ai1, map = map, mod = mod )
         sqlalchemysetup.session.add( matchrequest )

         # add options:
         availableoptions = sqlalchemysetup.session.query(AIOption)
         for option in availableoptions:
            if option.option_name in options:
               matchrequest.options.append( MatchRequestOption( option ) )

         sqlalchemysetup.session.commit()

         return [True, '' ]
      except:
         return (False,"An unexpected exception occurred: " + str( sys.exc_info() ) + "\n" + str( traceback.extract_tb( sys.exc_traceback ) ) )
      
   # returns list of dictionaries
   # note: later versions of this function, with incompatiable changes, should be added with a new version number
   # ie v2, v3 etc... to avoid breaking the api for old clients
   # returns [True,list] if successful or [False,errormessage] if something went wrnog
   def getmatchrequestqueuev1(self):
      try:
         requests = sqlalchemysetup.session.query(MatchRequest).filter(MatchRequest.matchresult == None )
         requeststoreturn = []
         for request in requests:
            options = []
            for option in request.options:
               options.append(option.option.option_name)
            requeststoreturn.append( {
               'matchrequest_id': request.matchrequest_id,
               'map_name': request.map.map_name,
               'mod_name': request.mod.mod_name,
               'ais': [ { 'ai_name': request.ai0.ai_name, 'ai_version': request.ai0.ai_version },
                  { 'ai_name': request.ai1.ai_name, 'ai_version': request.ai1.ai_version } ],
               'options': options } )
         return [True, requeststoreturn ]
      except:
         return (False,"An unexpected exception occurred: " + str( sys.exc_info() ) + "\n" + str( traceback.extract_tb( sys.exc_traceback ) ) )

   # returns list of dictionaries
   # note: later versions of this function, with incompatiable changes, should be added with a new version number
   # ie v2, v3 etc... to avoid breaking the api for old clients
   # returns [True,list] if successful or [False,errormessage] if something went wrnog
   def getmatchresultsv1(self):
      try:
         requests = sqlalchemysetup.session.query(MatchRequest).filter(MatchRequest.matchresult != None )
         resultstoreturn = []
         for request in requests:
            options = []
            for option in request.options:
               options.append(option.option.option_name)
            newresulttoreturn = {
               'matchrequest_id': request.matchrequest_id,
               'map_name': request.map.map_name,
               'mod_name': request.mod.mod_name,
               'ais': [ { 'ai_name': request.ai0.ai_name, 'ai_version': request.ai0.ai_version },
                  { 'ai_name': request.ai1.ai_name, 'ai_version': request.ai1.ai_version } ],
               'options': options,
               'botrunner_name': request.matchrequestinprogress.botrunner.botrunner_name,
               'matchresult': request.matchresult.matchresult
            }
            if os.path.isfile( replaycontroller.getReplayPath(request.matchrequest_id) ):
               newresulttoreturn['replayrelativeurl'] = replaycontroller.getReplayWebRelativePath(request.matchrequest_id) 
            resultstoreturn.append( newresulttoreturn )
         return [True, resultstoreturn ]
      except:
         return (False,"An unexpected exception occurred: " + str( sys.exc_info() ) + "\n" + str( traceback.extract_tb( sys.exc_traceback ) ) )

handler = SimpleXMLRPCServer.CGIXMLRPCRequestHandler()
handler.register_instance( APIService() )
handler.register_introspection_functions()
handler.register_multicall_functions()

if __name__ == '__main__':
   sqlalchemysetup.setup()
   try:
      handler.handle_request()
   except:
      print str( sys.exc_value )
   sqlalchemysetup.close()

