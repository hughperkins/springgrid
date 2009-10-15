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
import base64
import xmlrpclib

from unitsync import unitsync as unitsyncpkg

config = None
unitsync = None
writabledatadirectory = None

scriptdir = os.path.dirname( os.path.realpath( __file__ ) )

def StringToBoolean( booleanstring ):
   if booleanstring.lower() == "yes":
      return True
   if booleanstring.lower() == "true":
      return True
   return False

def StringToInteger( integerstring ):
   return int( integerstring )

def requestgamefromwebserver():
   [result, serverrequest ] = getxmlrpcproxy().getrequest(config.botrunnername, config.sharedsecret )
   if not result:
      print "Something went wrong: " + serverrequest
      return None

   print serverrequest

   return serverrequest

def readFile( filepath ):
   filehandle = open( filepath, "r" )
   filecontents = ""
   line = filehandle.readline()
   while( line != "" ):
      filecontents = filecontents + line
      line = filehandle.readline()
   filehandle.close()
   return filecontents

def writeFile( filepath, contents ):
   filehandle = open( filepath, "w" )
   filehandle.write( contents )
   filehandle.close()

# return xmlrpcproxy to communicate with web server
def getxmlrpcproxy():
   return xmlrpclib.ServerProxy( uri = config.websiteurl + "/botrunner_webservice.py", allow_none = True )

def doping( status ):
   return getxmlrpcproxy().ping( config.botrunnername, config.sharedsecret, status )

def rungame( serverrequest ):
   global config, writabledatadirectory
   scripttemplatecontents = readFile( scriptdir + "/" + config.scripttemplatefilename )

   scriptcontents = scripttemplatecontents
   scriptcontents = scriptcontents.replace("%MAP%", serverrequest['mapname'] )
   scriptcontents = scriptcontents.replace("%MOD%", serverrequest['modname'] )
   scriptcontents = scriptcontents.replace("%AI0%", serverrequest['ai0name'] )
   scriptcontents = scriptcontents.replace("%AI0VERSION%", serverrequest['ai0version'] )
   scriptcontents = scriptcontents.replace("%AI1%", serverrequest['ai1name'] )
   scriptcontents = scriptcontents.replace("%AI1VERSION%", serverrequest['ai1version'] )

   map_info = unitsyncpkg.MapInfo()
   unitsync.GetMapInfoEx(str(serverrequest['mapname']), map_info, 1)
   team0startpos = map_info.StartPos[0]
   team1startpos = map_info.StartPos[1]
   # we always play team 0 on startpos0 ,and team1 on startpos1, for repeatability
   # it is for hte website to decide which team should go on which side, not the
   # botrunner
   print team0startpos
   scriptcontents = scriptcontents.replace("%TEAM0STARTPOSX%", str( team0startpos.x ) )   
   scriptcontents = scriptcontents.replace("%TEAM0STARTPOSZ%", str( team0startpos.y ) )   
   scriptcontents = scriptcontents.replace("%TEAM1STARTPOSX%", str( team1startpos.x ) )   
   scriptcontents = scriptcontents.replace("%TEAM1STARTPOSZ%", str( team1startpos.y ) )   

   scriptpath = writabledatadirectory + "/script.txt"
   writeFile( scriptpath, scriptcontents )

   if os.path.exists( writabledatadirectory + "/infolog.txt" ):
      os.remove( writabledatadirectory + "/infolog.txt" )

   os.chdir( writabledatadirectory )
   popen = subprocess.Popen( [ config.springPath, writabledatadirectory + "/script.txt"])
   finished = False
   starttimeseconds = time.time()
   doping("playing game " + serverrequest['ai0name'] + " vs " + serverrequest['ai1name'] + " on " + serverrequest['mapname'] + " " + serverrequest['modname'] )
   lastpingtimeseconds = time.time()
   gameresult = {}
   while not finished:
      print "waiting for game to terminate..."
      if time.time() - lastpingtimeseconds > config.pingintervalminutes * 60:
         doping ("playing game " + serverrequest['ai0name'] + " vs " + serverrequest['ai1name'] + " on " + serverrequest['mapname'] + " " + serverrequest['modname'] )
      if os.path.exists( writabledatadirectory + "/infolog.txt" ):
         infologcontents = readFile( writabledatadirectory + "/infolog.txt" )
         # print infologcontents
         ai0endstring = serverrequest['gameendstring'].replace("%TEAMNUMBER%", "0")
         ai1endstring = serverrequest['gameendstring'].replace("%TEAMNUMBER%", "1")
         if ( infologcontents.find( ai0endstring ) != -1 ) and ( infologcontents.find(ai1endstring ) == - 1 ):
            # ai0 died
            print "team 1 won!"
            gameresult['winningai'] = 1
            gameresult['resultstring'] = "ai1won"
            popen.kill()
            return gameresult
         if infologcontents.find( ai0endstring ) == -1 and infologcontents.find(ai1endstring ) != - 1:
            # ai1 died
            print "team 0 won!"
            gameresult['winningai'] = 0
            gameresult['resultstring'] = "ai0won"
            popen.kill()
            return gameresult
         if infologcontents.find( ai0endstring ) != -1 and infologcontents.find(ai1endstring ) != - 1:
            # both died...
            print "A draw..." 
            gameresult['winningai'] = -1
            gameresult['resultstring'] = "draw"
            popen.kill()
            return gameresult

      # check timeout (== draw)
      if ( time.time() - starttimeseconds ) > serverrequest['gametimeoutminutes'] * 60:
         # timeout
         print "Game timed out"
         gameresult['winningai'] = -1
         gameresult['resultstring'] = "gametimeout"
         popen.kill()
         return gameresult

      if popen.poll() != None:
         # spring finished / died / crashed
         # presumably if we got here, it crashed, otherwise infolog would have been written   
         print "Crashed" 
         gameresult['winningai'] = -1
         gameresult['resultstring'] = "crashed"
         return gameresult

      time.sleep (1)

   return gameresult

def uploadresulttoserver( serverrequest, gameresult ):
   global writabledatadirectory

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
      tarhandle = tarfile.open(writabledatadirectory + "/thisreplay.tar.bz2", "w:bz2" )
      os.chdir( writabledatadirectory + "/demos" )  # cd in, so that we don't embed the paths
                   # in the tar file...
      tarhandle.add( thisreplayfilename )
      tarhandle.close()

   # ok, let's do the upload... if we don't have a replay, we won't send the replay
   if thisreplayfilename != '':
      replayfilehandle = open( writabledatadirectory + "/thisreplay.tar.bz2", 'rb' )
      replaycontents = replayfilehandle.read()
      replayfilehandle.close()

      print "binary length: " + str(len(replaycontents))
      replaybinarywrapper = xmlrpclib.Binary(replaycontents)

      requestuploadedok = False    
      while not requestuploadedok:
         try:
            (result,errormessage ) = getxmlrpcproxy().submitresult( config.botrunnername, config.sharedsecret, serverrequest['matchrequestid'], gameresult['resultstring'], replaybinarywrapper )
            print "upload result: " + str( result) + " " + errormessage
            requestuploadedok = True
         except:
            print "Something went wrong uploading to the server: " + str( sys.exc_value ) + ".\nRetrying ... "
            time.sleep(5)
   else:
      print "we haven't programmed in the case of no replay found yet..."
      pass

demosdirectorylistingbeforegame = None

# we'll find the names of all files in the demos directory (the 
# replays), and then any new one will be assumed to be the one from the
# game we just played
def snapshotdemosdirectory():
   global writabledatadirectory

   listing = []
   for filename in os.listdir( writabledatadirectory + "/demos" ):
      listing.append(filename)
   return listing

def getValueFromUser(questiontouser):
   while True:
      print questiontouser
      inputline = sys.stdin.readline()
      uservalue = inputline.strip()
      if uservalue != '':
         return uservalue

def getPath( pathname, potentialpaths ):
   # just include paths that exist
   paths = []
   for potentialpath in potentialpaths:
      if os.path.exists( potentialpath ):
         paths.append( potentialpath )

   print paths
   while True:
      print "Please enter the number of the path to " + pathname + ":"
      for i in xrange( len( paths ) ):
         print str(i + 1 ) + ". " + paths[i]
      print str( len( paths ) + 1 ) + ". custom path (eg " + potentialpaths[0] + ")"

      inputline = sys.stdin.readline().strip()
      if inputline == '':
         continue
      try:
         index = int( inputline )
      except:
         # user didn't enter a number
         # could be a path?
         try:
            if not os.path.exists( inputline ):
               print "Not a valid path for " + pathname
               continue
            return inputline
         except:
            # probably not a spring executable
            print "Not a valid path for " + pathname
            continue
         
      if index < 1 or index > len( paths ) + 1:
         print "Please enter a number from 1 to " + str( len( paths ) + 1 ) + "."
         continue
      if index <= len( paths ):
         return paths[index - 1]
      # user wants to enter a custom path:
      print "Please type in the path to " + pathname + " (eg " + potentialpaths[0] + ") :"
      inputline = sys.stdin.readline().strip()
      if inputline == '':
         continue
      if not os.path.exists( inputline ):
         print "Not a valid path for " + pathname
         continue
      return inputline

def getSpringPath():
   potentialpaths = []
   if os.name == 'posix':
      potentialpaths = ( '/usr/games/spring', '/usr/games/spring-headlessstubs' )
   elif os.name == 'nt':
      potentialpaths = ( 'C:\Program Files\Spring\spring.exe', 'C:\Program Files\Spring\spring-headlessstubs.exe' )

   return getPath( "the Spring executable", potentialpaths )

def getUnitSyncPath():
   potentialpaths = []
   if os.name == 'posix':
      potentialpaths = ( '/usr/lib/spring/unitsync.so', )
   elif os.name == 'nt':
      potentialpaths = ( "C:\\Program Files\\Spring\\unitsync.dll", )

   return getPath( "unitsync", potentialpaths )

# returns True for confirmed, otherwise False
def getConfirmation( confirmationquestion ):
   print confirmationquestion + " (y to confirm)"
   confirmation = sys.stdin.readline().strip().lower()
   if confirmation == 'y':
      return True
   return False

# returns the entered file path or ""
def askForPathToFile( pathName ):
   while True:
      print "Please enter the full path to " + pathName + ":"
      thePath = sys.stdin.readline().strip()
      if os.path.exists(thePath):
         return thePath
      else:
         print "The specified file \"" + thePath + "\" does not exist, please try again."
         continue
   return ''

def  setupConfig():
   global config

   print ""
   print "Welcome to botrunner."
   print ""
   print "Let's get you set up..."
   gotdata = False
   while not gotdata:
      print ""
      weburl = getValueFromUser("Which webserver to you want to subscribe to?  Examples:\n   - manageddreams.com/ailadder\n   - manageddreams.com/ailadderstaging\n   - localhost/ailadder")
      print ""
      if weburl.lower().find("http://") == -1:
         weburl = "http://" + weburl
      botrunnername = getValueFromUser("What name do you want to give to your botrunner?  This name will be shown on the website.")
      print ""
      botrunnersharedsecret = getValueFromUser("What sharedsecret do you want to use with this botrunner?  This will be used to authenticate your botrunner to the website.  Just pick something, and remember it.")
      print ""
      springPath = getSpringPath()
      if springPath == '':
         print "Spring executable not found. Please check that it is installed"
         return False
      print "Spring executable found: " + springPath
      print ""
      unitsyncPath = getUnitSyncPath()
      if unitsyncPath == '':
         print "UnitSync not found. Please check that it is installed"
         return False
      print "UnitSync found: " + unitsyncPath
      print ""
      print "You have input:"
      print "   target web server: " + weburl
      print "   botrunner name: " + botrunnername
      print "   botrunner shared secret: " + botrunnersharedsecret
      print "   spring executable path: " + springPath
      print "   UnitSync path: " + unitsyncPath
      print ""
      if getConfirmation( "Is this correct?" ):
         gotdata = True

   # that's all we need, let's create the config file...
   templatecontents = readFile(scriptdir + "/config.py.template")
   newconfig = templatecontents
   newconfig = newconfig.replace( "WEBSITEURL", weburl )
   newconfig = newconfig.replace( "BOTRUNNERNAME", botrunnername )
   newconfig = newconfig.replace( "SHAREDSECRET", botrunnersharedsecret )
   newconfig = newconfig.replace( "SPRINGPATH", springPath )
   newconfig = newconfig.replace( "UNITSYNCPATH", unitsyncPath )
   writeFile( scriptdir + "/config.py", newconfig )

   # and import it...
   import config
   return True

def registermaps():
   registeredmaps = getxmlrpcproxy().getsupportedmaps( config.botrunnername, config.sharedsecret )
   print registeredmaps

   for i in xrange( unitsync.GetMapCount() ):
      mapname = unitsync.GetMapName(i)
      if registeredmaps.count( mapname ) == 0:
         print "registering map " + mapname + " ..."
         unitsync.GetMapArchiveCount(mapname)
         archivename = unitsync.GetMapArchiveName(0)
         #print unitsync.GetMapArchiveName(1)
         archivechecksum = unitsync.GetArchiveChecksum( archivename )
         print getxmlrpcproxy().registersupportedmap( config.botrunnername, config.sharedsecret, mapname, str(archivechecksum) )

def registermods():
   registeredmods = getxmlrpcproxy().getsupportedmods( config.botrunnername, config.sharedsecret )
   print registeredmods

   for i in xrange( unitsync.GetPrimaryModCount() ):
      modname = unitsync.GetPrimaryModName(i)
      if registeredmods.count( modname ) == 0:
         print "registering mod " + modname + " ..."
         unitsync.GetPrimaryModArchiveCount(i)
         modarchive = unitsync.GetPrimaryModArchive(0)
         modarchivechecksum = unitsync.GetArchiveChecksum( modarchive )
         print getxmlrpcproxy().registersupportedmod( config.botrunnername, config.sharedsecret, modname, str(modarchivechecksum) )

def registerais():
   registeredais = getxmlrpcproxy().getsupportedais( config.botrunnername, config.sharedsecret )
   print registeredais

   for i in xrange( unitsync.GetSkirmishAICount() ):
      shortname = ''
      version = ''
      for j in xrange( unitsync.GetSkirmishAIInfoCount(i) ):
         if unitsync.GetInfoKey(j) == "shortName":
            shortname = unitsync.GetInfoValue(j)
         if unitsync.GetInfoKey(j) == "version":
            version = unitsync.GetInfoValue(j)
         
      if shortname != '' and version != '':
         if registeredais.count( [ shortname, version ] ) == 0:
            print "registering ai " + shortname + " version " + version + " ..."
            print getxmlrpcproxy().registersupportedai( config.botrunnername, config.sharedsecret, shortname, version )

def go():
   global config, unitsync, writabledatadirectory, demosdirectorylistingbeforegame
   # check for config, question user if doesn't exist
   try:
      import config
      print "Configuration found, using"
   except:
      ok = setupConfig()
      if not ok:
         return

   unitsync = unitsyncpkg.Unitsync(config.unitsyncPath)

   unitsync.Init(True,1)

   writabledatadirectory = unitsync.GetWritableDataDirectory()

   try:
      doping("Connection Test!")
      print "Connection test to server " + config.websiteurl + " was successfull."
   except:
      print "Connection test to server " + config.websiteurl + " failed!"
      print "Please make sure it is a valid AI Ladder URL, and you can connect to it."
      return

   registermaps()
   registermods()
   registerais()

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
         doping("sleeping")
         time.sleep(config.sleepthislongwhennothingtodoseconds)

go()

