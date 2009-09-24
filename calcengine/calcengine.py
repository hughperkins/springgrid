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

import time
import urllib
import urllib2
import subprocess
import os
import sys
import io
from xml.dom import minidom
import tarfile

import config
import urllib2_file

scriptdir = os.path.dirname( os.path.realpath( __file__ ) )

class ServerRequest():
   def __init__( self ):
     pass     

class GameResult():
   def __init__( self ):
      pass

def StringToBoolean( booleanstring ):
   if booleanstring.lower() == "yes":
      return True
   if booleanstring.lower() == "true":
      return True
   return False

def StringToInteger( integerstring ):
   return int( integerstring )

def requestgamefromwebserver():
   requestparams = urllib.urlencode({'calcenginename': config.calcenginename, 'sharedsecret': config.sharedsecret })
   serverrequesthandle = urllib.urlopen( config.websiterequestpage, requestparams )
   serverrequestarray = serverrequesthandle.readlines()
   # print serverrequestarray
   serverrequeststring = ''.join( serverrequestarray )
   print serverrequeststring
   serverrequestdom = minidom.parseString( serverrequeststring )
   # print serverrequestdom
   if serverrequestdom.documentElement.hasAttribute("summary"):
      print serverrequestdom.documentElement.getAttribute("summary")
      return None
   serverrequest = ServerRequest()
   serverrequest.matchrequestid = serverrequestdom.documentElement.getAttribute("matchrequestid")
   serverrequest.ai0 = serverrequestdom.documentElement.getAttribute("ai0")
   serverrequest.ai0version = serverrequestdom.documentElement.getAttribute("ai0version")
   serverrequest.ai1 = serverrequestdom.documentElement.getAttribute("ai1")
   serverrequest.ai1version = serverrequestdom.documentElement.getAttribute("ai1version")
   serverrequest.map = serverrequestdom.documentElement.getAttribute("map")
   serverrequest.mod = serverrequestdom.documentElement.getAttribute("mod")
   serverrequest.maphash = serverrequestdom.documentElement.getAttribute("maphash")
   serverrequest.modhash = serverrequestdom.documentElement.getAttribute("modhash")
   serverrequest.cheatingallowed = StringToBoolean( serverrequestdom.documentElement.getAttribute("cheatingallowed") )
   serverrequest.gametimeoutminutes = StringToInteger( serverrequestdom.documentElement.getAttribute("gametimeoutminutes") )
   serverrequest.gameendstring = serverrequestdom.documentElement.getAttribute("gameendstring")
   return serverrequest

def readFile( filepath ):
   filehandle = io.open( filepath, "r" )
   filecontents = ""
   line = filehandle.readline()
   while( line != "" ):
      filecontents = filecontents + line
      line = filehandle.readline()
   filehandle.close()
   return filecontents

def writeFile( filepath, contents ):
   filehandle = io.open( filepath, "w" )
   filehandle.write( contents )
   filehandle.close()

def rungame( serverrequest ):
   gameresult = GameResult()
   scripttemplatecontents = readFile( scriptdir + "/" + config.scripttemplatefilename )

   scriptcontents = scripttemplatecontents
   scriptcontents = scriptcontents.replace("%MAP%", serverrequest.map )
   scriptcontents = scriptcontents.replace("%MAPHASH%", serverrequest.maphash )
   scriptcontents = scriptcontents.replace("%MOD%", serverrequest.mod )
   scriptcontents = scriptcontents.replace("%MODHASH%", serverrequest.modhash )
   scriptcontents = scriptcontents.replace("%AI0%", serverrequest.ai0 )
   scriptcontents = scriptcontents.replace("%AI0VERSION%", serverrequest.ai0version )
   scriptcontents = scriptcontents.replace("%AI1%", serverrequest.ai1 )
   scriptcontents = scriptcontents.replace("%AI1VERSION%", serverrequest.ai1version )

   writeFile( config.springgamedir + "/script.txt", scriptcontents )

   if os.path.exists( config.springgamedir + "/infolog.txt" ):
      os.remove( config.springgamedir + "/infolog.txt" )

   os.chdir( config.springgamedir )
   # os.exec( "./spring script.txt" )
   # subprocess.call(["./spring", "script.txt"])
   # popen = subprocess.Popen(["./spring", "script.txt"])
   popen = subprocess.Popen([config.springgamedir + "/spring", "script.txt"])
   finished = False
   while not finished:
      print "waiting for game to terminate..."
      if os.path.exists( config.springgamedir + "/infolog.txt" ):
         infologcontents = readFile( config.springgamedir + "/infolog.txt" )
         # print infologcontents
         ai0endstring = serverrequest.gameendstring.replace("%TEAMNUMBER%", "0")
         ai1endstring = serverrequest.gameendstring.replace("%TEAMNUMBER%", "1")
         if ( infologcontents.find( ai0endstring ) != -1 ) and ( infologcontents.find(ai1endstring ) == - 1 ):
            # ai0 died
            print "team 1 won!"
            gameresult.winningai = 1
            gameresult.resultstring = "ai1won"
            popen.kill()
            return gameresult
         if infologcontents.find( ai0endstring ) == -1 and infologcontents.find(ai1endstring ) != - 1:
            # ai1 died
            print "team 0 won!"
            gameresult.winningai = 0
            gameresult.resultstring = "ai0won"
            popen.kill()
            return gameresult
         if infologcontents.find( ai0endstring ) != -1 and infologcontents.find(ai1endstring ) != - 1:
            # both died...
            print "A draw..." 
            gameresult.winningai = -1
            gameresult.resultstring = "draw"
            popen.kill()
            return gameresult

      # could also check for spring exiting here (== draw)
      # and timeout (== draw)

      if popen.poll() != None:
         # spring finished / died / crashed
         # presumably if we got here, it crashed, otherwise infolog would have been written   
         print "Crashed" 
         gameresult.winningai = -1
         gameresult.resultstring = "crashed"
         return gameresult

      time.sleep (1)

   return gameresult

def uploadresulttoserver( serverrequest, gameresult ):
   # upload gameresult and serverrequest to server...
   # ...

   # first we should take care of the replay
   # what was its filename? :-O
   # right, going to take a snapshot of the replay directory before starting
   # and then we'll take anything new as the correct replay
   global demosdirectorylistingbeforegame
   demosdirectorynow = snapshotdemosdirectory()
   thisreplayfilename = ''
   for filename in demosdirectorynow:
      if not filename in demosdirectorylistingbeforegame:
         print thisreplayfilename
         thisreplayfilename = filename
   if thisreplayfilename == '':
      # then we didn't create a replay for some reason..
      pass
   else:
      # first tar.bz2 it
      tarhandle = tarfile.open(config.springgamedir + "/thisreplay.tar.bz2", "w:bz2" )
      os.chdir( config.springgamedir + "/demos" )  # cd in, so that we don't embed the paths
                   # in the tar file...
      tarhandle.add( thisreplayfilename )
      tarhandle.close()

   # ok, let's do the upload... if we don't have a replay, we won't send the replay
   if thisreplayfilename != '':
      replayfilehandle = open( config.springgamedir + "/thisreplay.tar.bz2", 'r' )

#      requestparams = urllib.urlencode({
      requestparams = {
          'calcenginename': config.calcenginename,
          'sharedsecret': config.sharedsecret,
          'matchrequestid': serverrequest.matchrequestid,
          'result': gameresult.resultstring,
          'replay': replayfilehandle }
      # serverrequesthandle = urllib.urlopen( config.websitepostpage, requestparams )      
      serverrequest = urllib2.Request( config.websitepostpage, requestparams, {} )      
      stream = urllib2.urlopen( serverrequest )
      pageresult = stream.read()
      print pageresult
      replayfilehandle.close()
   else:
      print "we haven't programmed in the case of no replay found yet..."
      pass

demosdirectorylistingbeforegame = None

# we'll find the names of all files in the demos directory (the 
# replays), and then any new one will be assumed to be the one from the
# game we just played
def snapshotdemosdirectory():
   listing = []
   for filename in os.listdir( config.springgamedir + "/demos" ):
      listing.append(filename)
   return listing

while True:
   print "Checking for new request..."
   serverrequest = requestgamefromwebserver()
   if serverrequest != None:
      # we have a request to process
      demosdirectorylistingbeforegame = snapshotdemosdirectory()
      result = rungame( serverrequest )
      uploadresulttoserver( serverrequest, result )
   else:
      # else, sleep...
      print "Nothing to do.  Sleeping..."
      time.sleep(config.sleepthislongwhennothingtodoseconds)
   
