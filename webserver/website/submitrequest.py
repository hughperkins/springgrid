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

import utils.loginhelper as loginhelper
import utils.dbconnection as dbconnection
import utils.formhelper as formhelper
import utils.htmlformshelper as htmlformshelper

import core.matchrequestcontroller as matchrequestcontroller

# get request from form
matchrequest = matchrequestcontroller.MatchRequest()
matchrequest.ai0name = formhelper.getValue("ai0name")
matchrequest.ai0version = formhelper.getValue("ai0version")
matchrequest.ai1name = formhelper.getValue("ai1name")
matchrequest.ai1version = formhelper.getValue("ai1version")
matchrequest.mapname = formhelper.getValue("mapname")
# matchrequest.maphash = formhelper.getValue("maphash")
matchrequest.modname = formhelper.getValue("modname")
# matchrequest.modhash = formhelper.getValue("modhash")

print "Content-type: text/plain"
print ""
print ""

dbconnection.connectdb()

loginhelper.processCookie()

if loginhelper.gusername != '':
   if matchrequestcontroller.submitrequest( matchrequest ):
      print "Submitted"
      # could be nice to print out queue here, or make another page for that
   else:
      print "Not submitted, please check your values and try again."
else:
   print "Please login first."

dbconnection.disconnectdb()


