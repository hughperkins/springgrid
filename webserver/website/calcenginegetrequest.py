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

import matchrequestcontroller
import calcenginecontroller

class InputParameters:
   def __init__(self):
      pass

# retrieve calcengine name and calcengine sharedsecret
def getinputparameters():
   form = cgi.FieldStorage()
   inputparameters = InputParameters()
   inputparameters.calcenginename = form["calcenginename"].value
   inputparameters.sharedsecret = form["sharedsecret"].value
   return inputparameters

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
# should call something in calcenginecontroller, or similar
def getcalcenginedescription(inputparameters):
   return None

def sendrequesttoengine( requestitem ):
   print "Content-type: text/xml"
   print ""
   print ""
   print "<request "
   print "mod='" + requestitem.modname + "' "
   print "modhash='" + requestitem.modhash + "' "
   print "map='" + requestitem.mapname + "' "
   print "maphash='" + requestitem.maphash + "' "
   print "ai0='" + requestitem.ai0name + "' "
   print "ai0version='" + requestitem.ai0version + "' "
   print "ai1='" + requestitem.ai1name + "' "
   print "ai1version='" + requestitem.ai1version + "' "
   print "gametimeoutminutes='" + str(config.gametimeoutminutes) + "' "
   print "gameendstring='" + config.gameendstring + "' "
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
dbconnection.connectdb()
if not validatesharedsecret( inputparameters ):
   fail()
   dbconnection.disconnectdb()
   sys.exit(0)

calcenginedescription = getcalcenginedescription(inputparameters)
requestitem = matchrequestcontroller.getcompatibleitemfromqueue(calcenginedescription)
if requestitem == None:
   sendnothing()
   dbconnection.disconnectdb()
   sys.exit(0)

matchrequestcontroller.markrequestasinprogress( requestitem, calcenginedescription )
sendrequesttoengine( requestitem )
dbconnection.disconnectdb()

