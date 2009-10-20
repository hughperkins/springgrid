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
ai0nameversion = formhelper.getValue("ai0nameversion")
ai0name = ai0nameversion.split("|")[0]
ai0version = ai0nameversion.split("|")[1]
ai1nameversion = formhelper.getValue("ai1nameversion")
ai1name = ai1nameversion.split("|")[0]
ai1version = ai1nameversion.split("|")[1]
mapname = formhelper.getValue("mapname")
modname = formhelper.getValue("modname")

sqlalchemysetup.setup()

loginhelper.processCookie()

if loginhelper.isLoggedOn():
   #if matchrequestcontroller.submitrequest( matchrequest ):
    #  jinjahelper.message( "Submitted"
      # could be nice to print out queue here, or make another page for that

   map = sqlalchemysetup.session.query(tableclasses.Map).filter(tableclasses.Map.map_name == mapname ).first()
   mod = sqlalchemysetup.session.query(tableclasses.Mod).filter(tableclasses.Mod.mod_name == modname ).first()
   ai0 = sqlalchemysetup.session.query(tableclasses.AI).filter(tableclasses.AI.ai_name == ai0name ).filter(tableclasses.AI.ai_version == ai0version ).first()
   ai1 = sqlalchemysetup.session.query(tableclasses.AI).filter(tableclasses.AI.ai_name == ai1name ).filter(tableclasses.AI.ai_version == ai1version ).first()

   matchrequest = tableclasses.MatchRequest( ai0, ai1, map, mod )
   sqlalchemysetup.session.add( matchrequest )

   # add options:
   availableoptions = sqlalchemysetup.session.query(tableclasses.AIOption)
   # get selected options from form submission:
   for option in availableoptions:
      if formhelper.getValue( "option_" + option.option_name ) != None:
         matchrequest.options.append( tableclasses.MatchRequestOption( option ) )

   sqlalchemysetup.session.commit()

   jinjahelper.message( "Submitted ok." )
else:
   jinjahelper.message( "Please login first." )

sqlalchemysetup.close()

