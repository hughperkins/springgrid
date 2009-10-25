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
from optparse import OptionParser

from unitsync import unitsync as unitsyncpkg

from utils import *
version = None
try:
   import version
except:
   pass

config = None
unitsync = None
writabledatadirectory = None

scriptdir = os.path.dirname( os.path.realpath( __file__ ) )

options = {}
args = {}

def parseopts():
   global sessionid, options, args

   parser = OptionParser()
   parser.add_option( "--sessionid", help = 'force sessionid to specific string', dest = 'sessionid' )
   parser.add_option( "--no-register-capabilities", help = 'do not register maps, mods or ais with web service', dest = 'noregistercapabilities', action='store_true' )
   parser.add_option( "--version", '-V', help = 'show version', dest = 'version', action='store_true' )

   (options, args ) = parser.parse_args()

   sessionid = options.sessionid

def requestgamefromwebserver(host):
   global sessionid
   try:
      [result, serverrequest ] = getxmlrpcproxy(host).getrequest(config.botrunnername, config.sharedsecret, sessionid )
      if not result:
         print "Something went wrong: " + serverrequest
         return None

      if len(serverrequest) == 0:
         return None
      return serverrequest[0]  # can't handle passing None in python 2.4
   except:
      print "Something went wrong: " + str( sys.exc_info() )
      return None

# return xmlrpcproxy to communicate with web server
def getxmlrpcproxy(host):
   return xmlrpclib.ServerProxy( uri = host + "/botrunner_webservice.py" )

# returns true if there is at least one host pinging ok
def doping( status ):
   global sessionid
   atleastonehostsucceeded = False
   for host in config.websiteurls:
      try:
         print "pinging " + host + " ..."
         getxmlrpcproxy(host).ping( config.botrunnername, config.sharedsecret, sessionid, status )
         atleastonehostsucceeded = True
      except:
         print "Failed to ping " + host
   return atleastonehostsucceeded

def rungame( serverrequest ):
   global config, writabledatadirectory
   scripttemplatecontents = filehelper.readFile( scriptdir + "/" + config.scripttemplatefilename )

   scriptcontents = scripttemplatecontents
   scriptcontents = scriptcontents.replace("%MAP%", serverrequest['map_name'] )
   scriptcontents = scriptcontents.replace("%MOD%", serverrequest['mod_name'] )
   scriptcontents = scriptcontents.replace("%AI0%", serverrequest['ai0_name'] )
   scriptcontents = scriptcontents.replace("%AI0VERSION%", serverrequest['ai0_version'] )
   scriptcontents = scriptcontents.replace("%AI1%", serverrequest['ai1_name'] )
   scriptcontents = scriptcontents.replace("%AI1VERSION%", serverrequest['ai1_version'] )

   map_info = unitsyncpkg.MapInfo()
   unitsync.GetMapInfoEx(str(serverrequest['map_name']), map_info, 1)
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
   filehelper.writeFile( scriptpath, scriptcontents )

   if os.path.exists( writabledatadirectory + "/infolog.txt" ):
      os.remove( writabledatadirectory + "/infolog.txt" )

   os.chdir( writabledatadirectory )
   popen = subprocess.Popen( [ config.springPath, writabledatadirectory + "/script.txt"])
   finished = False
   starttimeseconds = time.time()
   doping( "playing game " + serverrequest['ai0_name'] + " vs " + serverrequest['ai1_name'] + " on " + serverrequest['map_name'] + " " + serverrequest['mod_name'] )
   lastpingtimeseconds = time.time()
   gameresult = {}
   while not finished:
      print "waiting for game to terminate..."
      if time.time() - lastpingtimeseconds > config.pingintervalminutes * 60:
         doping ( "playing game " + serverrequest['ai0_name'] + " vs " + serverrequest['ai1_name'] + " on " + serverrequest['map_name'] + " " + serverrequest['mod_name'] )
      if os.path.exists( writabledatadirectory + "/infolog.txt" ):
         infologcontents = filehelper.readFile( writabledatadirectory + "/infolog.txt" )
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

def uploadresulttoserver( host, serverrequest, gameresult ):
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
   replaybinarywrapper = xmlrpclib.Binary('')
   if thisreplayfilename != '':
      replayfilehandle = open( writabledatadirectory + "/thisreplay.tar.bz2", 'rb' )
      replaycontents = replayfilehandle.read()
      replayfilehandle.close()

      print "binary length: " + str(len(replaycontents))
      replaybinarywrapper = xmlrpclib.Binary(replaycontents)

   requestuploadedok = False    
   while not requestuploadedok:
      try:
         (result,errormessage ) = getxmlrpcproxy(host).submitresult( config.botrunnername, config.sharedsecret, serverrequest['matchrequest_id'], gameresult['resultstring'], replaybinarywrapper )
         print "upload result: " + str( result) + " " + errormessage
         requestuploadedok = True
      except:
         print "Something went wrong uploading to the server: " + str( sys.exc_value ) + ".\nRetrying ... "
         time.sleep(5)

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

def getSpringPath():
   potentialpaths = []
   if os.name == 'posix':
      potentialpaths = ( '/usr/games/spring', '/usr/games/spring-headlessstubs' )
   elif os.name == 'nt':
      potentialpaths = ( 'C:\Program Files\Spring\spring.exe', 'C:\Program Files\Spring\spring-headlessstubs.exe' )

   return userinput.getPath( "the Spring executable", potentialpaths )

def getUnitSyncPath():
   potentialpaths = []
   if os.name == 'posix':
      potentialpaths = ( '/usr/lib/spring/unitsync.so', )
   elif os.name == 'nt':
      potentialpaths = ( "C:\\Program Files\\Spring\\unitsync.dll", )

   return userinput.getPath( "unitsync", potentialpaths )

def  setupConfig():
   global config

   print ""
   print "Welcome to botrunner."
   print ""
   print "Let's get you set up..."
   gotdata = False
   while not gotdata:
      print ""
      weburl = userinput.getValueFromUser("Which webserver to you want to subscribe to?  Examples:\n   - manageddreams.com/ailadder\n   - manageddreams.com/ailadderstaging\n   - localhost/ailadder")
      print ""
      if weburl.lower().find("http://") == -1:
         weburl = "http://" + weburl
      botrunnername = userinput.getValueFromUser("What name do you want to give to your botrunner?  This name will be shown on the website.")
      print ""
      botrunnersharedsecret = userinput.getValueFromUser("What sharedsecret do you want to use with this botrunner?  This will be used to authenticate your botrunner to the website.  Just pick something, and remember it.")
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
      if userinput.getConfirmation( "Is this correct?" ):
         gotdata = True

   # that's all we need, let's create the config file...
   templatecontents = filehelper.readFile(scriptdir + "/config.py.template")
   newconfig = templatecontents
   newconfig = newconfig.replace( "WEBSITEURL", weburl )
   newconfig = newconfig.replace( "BOTRUNNERNAME", botrunnername )
   newconfig = newconfig.replace( "SHAREDSECRET", botrunnersharedsecret )
   newconfig = newconfig.replace( "SPRINGPATH", springPath )
   newconfig = newconfig.replace( "UNITSYNCPATH", unitsyncPath )
   filehelper.writeFile( scriptdir + "/config.py", newconfig )

   # and import it...
   import config
   return True

def registermaps(host,registeredmaps):
   print registeredmaps

   multicall = xmlrpclib.MultiCall(getxmlrpcproxy(host))
   for i in xrange( unitsync.GetMapCount() ):
      mapname = unitsync.GetMapName(i)
      if registeredmaps.count( mapname ) == 0:
         print "registering map " + mapname + " ..."
         unitsync.GetMapArchiveCount(mapname)
         archivename = unitsync.GetMapArchiveName(0)
         #print unitsync.GetMapArchiveName(1)
         archivechecksum = unitsync.GetArchiveChecksum( archivename )
         multicall.registersupportedmap( config.botrunnername, config.sharedsecret, mapname, str(archivechecksum) )
   results = multicall()
   successcount = 0
   total = 0
   for result in results:
      total = total + 1
      if result[0]:
         successcount = successcount + 1
   if total > 0:
      print str(successcount) + " successes out of " + str(total)

def registermods(host,registeredmods):
   print registeredmods

   multicall = xmlrpclib.MultiCall(getxmlrpcproxy(host))
   for i in xrange( unitsync.GetPrimaryModCount() ):
      modname = unitsync.GetPrimaryModName(i)
      if registeredmods.count( modname ) == 0:
         print "registering mod " + modname + " ..."
         unitsync.GetPrimaryModArchiveCount(i)
         modarchive = unitsync.GetPrimaryModArchive(0)
         modarchivechecksum = unitsync.GetArchiveChecksum( modarchive )
         multicall.registersupportedmod( config.botrunnername, config.sharedsecret, modname, str(modarchivechecksum) )
   results = multicall()
   successcount = 0
   total = 0
   for result in results:
      total = total + 1
      if result[0]:
         successcount = successcount + 1
   if total > 0:
      print str(successcount) + " successes out of " + str(total)

def registerais(host,registeredais):
   print registeredais

   multicall = xmlrpclib.MultiCall(getxmlrpcproxy(host))
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
            multicall.registersupportedai( config.botrunnername, config.sharedsecret, shortname, version )
   results = multicall()
   successcount = 0
   total = 0
   for result in results:
      total = total + 1
      if result[0]:
         successcount = successcount + 1
   if total > 0:
      print str(successcount) + " successes out of " + str(total)

# we do a single multicall to retrieve all registerdd mods, maps and ais
# first, which should speed up launch after initial launch
def registercapabilities(host):
   multicall = xmlrpclib.MultiCall(getxmlrpcproxy(host))
   multicall.getsupportedmaps( config.botrunnername, config.sharedsecret )
   multicall.getsupportedmods( config.botrunnername, config.sharedsecret )
   multicall.getsupportedais( config.botrunnername, config.sharedsecret )
   resultsets = multicall()
   registeredmaps = resultsets[0]
   registeredmods = resultsets[1]
   registeredais = resultsets[2]
   registermaps(host,registeredmaps)
   registermods(host,registeredmods)
   registerais(host,registeredais)

def go():
   global config, unitsync, writabledatadirectory, demosdirectorylistingbeforegame
   global sessionid, options

   parseopts()

   if options.version:
      print ""
      if version != None:
         print "AILadder, version: " + version.version
      else:
         print "AILadder, version: dev code, not a versioned release."
      print ""
      return

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

   if sessionid == None:
      sessionid = stringhelper.getRandomAlphaNumericString(60)
   print "Sessionid: " + sessionid
   
   if not doping( "Connection Test!"):
      print "Failed to ping all configured websites.  Please check your configuration and internet connection and try again."
      return

   for host in config.websiteurls:
      if not options.noregistercapabilities:
         try:
            print "registering capabilities with " + host + " ..."
            registercapabilities(host)
         except:
            print "Couldn't register capabilities to host " + host + " " + str( sys.exc_info() )

   while True:
      print "Checking for new request..."
      # go through each host getting a request
      # Process each request, then go back to start of loop,
      # otherwise wait a bit
      gotrequest = False
      for host in config.websiteurls:
         print "checking " + host + " ..."
         serverrequest = requestgamefromwebserver(host)
         if serverrequest != None:
            # we have a request to process
            demosdirectorylistingbeforegame = snapshotdemosdirectory()
            result = rungame( serverrequest )
            uploadresulttoserver( host, serverrequest, result )
            gotrequest = True
      
      if not gotrequest:
         # else, sleep...
         print "Nothing to do.  Sleeping..."
         doping("sleeping")
         time.sleep(config.sleepthislongwhennothingtodoseconds)

go()

