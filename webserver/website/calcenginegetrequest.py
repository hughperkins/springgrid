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
# ======================================================================================
#

# job of this is to deliver a request from the queue to a calcengine
# and somehow mark that that request is undergoing processing

# inputs:
# - name of calcengine
# - calcengine sharedsecret

# these will come in in 'post' values

# as far as maps and mods that the calcengine can use:
# - this info will be obtained from the database
# - either the calcengine can signal that it will download things as it goes
# - or the database will contain a list of maps and mods that each engine currently has
# - for now, we'll just store a list of maps and mods supported by each engine in the database, and deal with the issue of downloading later
#

#
# so... we're going to have to:
# - connect to the database
# - validate the engine's shared secret
# - get an item from the queue
# - check it's compatible with the engine
# - mark the request as undergoing processing, with a date/time stamp
# - create the appropriate xml to return the request to the calcengine

import cgitb; cgitb.enable()
import sys
import os
import Cookie
# import cookiefile
import cgi

import config
import dbconnection
import dates

class InputParameters:
   def __init__(self):
      pass

class MatchRequest:
   def __init__(self):
      pass

# retrieve calcengine name and calcengine sharedsecret
def getinputparameters():
   form = cgi.FieldStorage()
   inputparameters = InputParameters()
   inputparameters.calcenginename = form["calcenginename"].value
   inputparameters.sharedsecret = form["sharedsecret"].value
   return inputparameters

# can probably be in some shared file, rather than in each python file...
def connectdb():
   dbconnection.connectdb()

def validatesharedsecret(inputparameters):
   sharedsecret = dbconnection.cursor.execute("select calcengine_sharedsecret from calcengines where calcengine_name=%s", (inputparameters.calcenginename,) )
   row = dbconnection.cursor.fetchone()
   if row == None:
      return False
   actualsharedsecret = row[0]
   if actualsharedsecret == inputparameters.sharedsecret:
      return True
   return False

# basically, we want to know what maps and stuff it supports
# for now this is a placeholder...
def getcalcenginedescription(inputparameters):
   return None

# go through matchrequests_inprogress table, and remove any rows
# older than a certain time
# placeholder for now
def archiveoldrequests():
   dbconnection.cursor.execute("select datetimeassigned from matchrequests_inprogress")
   row = dbconnection.cursor.fetchone()
   while row != None:
      datetimestring = row[0]
      datetime = dates.dateStringToDateTime( datetimestring )
      # do stuff

# this should walk the queue till it finds something that the engine
# can handle
# for now, it just returns the first item in the queue
# we need to only take things that arent in the inprogress queue of course...
def getcompatibleitemfromqueue( calcenginedescription ):
   archiveoldrequests()
   # now we've archived the old requests, we just pick a request
   # in the future, we'll pick a compatible request.  In the future ;-)
   # also, we need to handle options.  In the future ;-)
   dbconnection.cursor.execute("select matchrequest_id, ai0.ai_name, ai0.ai_version, ai1.ai_name, ai1.ai_version, mapname, maphash, modname, modhash " \
      "from matchrequestqueue," \
      " ais as ai0," \
      " ais as ai1, " \
      " maps, " \
      " mods " \
      " where ai0.ai_id = ai0_id " \
      " and ai1.ai_id = ai1_id " \
      " and maps.mapid = matchrequestqueue.map_id " \
      " and mods.mod_id = matchrequestqueue.mod_id" )
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
   pass

def sendrequesttoengine( requestitem ):
   print "Content-type: text/xml"
   print ""
   print ""
   print "<request "
   print "mod='" + requestitem.modname + " "
   print "modhash='" + requestitem.modhash + " "
   print "map='" + requestitem.mapname + " "
   print "maphash='" + requestitem.maphash + " "
   print "ai0='" + requestitem.ai0name + " "
   print "ai0version='" + requestitem.ai0version + " "
   print "ai1='" + requestitem.ai1name + " "
   print "ai1version='" + requestitem.ai1version + " "
   print "gametimeoutminutes='" + config.gametimeoutminutes + " "
   print "gameendstring='" + config.gameendstring + " "
   print ">"
   print "</request>"

def fail():
   print "Content-type: text/xml"
   print ""
   print ""
   print "<request summary='unauthorized' />"
   print ""

def sendnothing():
   print "Content-type: text/xml"
   print ""
   print ""
   print "<request summary='nothingtodo' />"
   print ""



inputparameters = getinputparameters()
connectdb()
if not validatesharedsecret( inputparameters ):
   fail()
   sys.exit(0)

calcenginedescription = getcalcenginedescription(inputparameters)
requestitem = getcompatibleitemfromqueue(calcenginedescription)
if requestitem == None:
   sendnothing()
   sys.exit(0)

markrequestasinprogress( requestitem, calcenginedescription )
sendrequesttoengine( requestitem )

