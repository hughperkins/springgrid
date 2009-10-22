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

   # returns a list of [ainame,aiversion] lists
   def getais(self):
      ailist = []
      for ai in sqlalchemysetup.session.query(AI):
         ailist.append([ai.ai_name, ai.ai_version])
      return ailist

   # schedule a single match
   # - 'ais' should contain a list of [ainame,aiversion] lists
   # containing all ais that should play on the map
   # - 'options' should contain a list of option name strings
   #
   # note: later versions of this function should be added with a new version number
   # ie v2, v3 etc... to avoid breaking the api for old clients
   def schedulematchv1(self,mapname,modname,ais,options):
      pass

   def getmatchrequestqueue(self):
      pass

   def getmatchresults(self):
      pass

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

