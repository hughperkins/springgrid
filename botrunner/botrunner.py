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
import traceback
import imp

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
   parser.add_option( "--target-web-site", help = 'website we should subscribe to', dest = 'targetwebsite' )
   parser.add_option( "--botrunner-name", help = 'botrunner-name', dest = 'botrunnername' )
   parser.add_option( "--botrunner-shared-secret", help = 'botrunner shared secret', dest = 'botrunnersharedsecret' )
   parser.add_option( "--spring-path", help = 'path to spring executable', dest = 'springpath' )
   parser.add_option( "--unitsync-path", help = 'path to unitsync library', dest = 'unitsyncpath' )
   parser.add_option( "--downloading-ok", help = 'ok to download AIs', dest = 'downloadingok', action='store_true' )
   parser.add_option( "--yes", help = 'automatically confirm', dest = 'yes', action='store_true' )
   parser.add_option( "--configpath", help = 'path to configfile (default: config.py).  Note: must already exist.', dest = 'configpath' )
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
      print "got request, matchrequestid = " + str(serverrequest[0]['matchrequest_id'])
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

def getreplaypath( infologcontents ):
   splitlines = infologcontents.split("\n")
   for line in splitlines:
      if line.find("] Recording demo ") != -1:
         demopath = line.split("] Recording demo ")[1]
         print "demo path: [" + demopath + "]"
         return demopath
   return None

def trydownloadingai(host):
   global sessionid, config, writabledatadirectory
   try:
      [success, downloadrequestlist ] = getxmlrpcproxy(host).getdownloadrequest(config.botrunnername, config.sharedsecret, sessionid )
      if not success:
         print downloadrequestlist
         return
  
      if len(downloadrequestlist) == 0:
         print "Nothing to download from " + host
         return

      downloadrequest = downloadrequestlist[0]

      print "Got download request: " + str( downloadrequest )
      ai_name = downloadrequest['ai_name']
      ai_version = downloadrequest['ai_version']

      # ok, so we'll download it  to .... writabledatadirectory?
      # then use tar to extract it to .... the writabledatadirectory/AI ?
      # start by retrieving it:
      serverrequesthandle = urllib.urlopen( downloadrequest['ai_downloadurl'], None )
      data = serverrequestarray = serverrequesthandle.read()
      file = open(writabledatadirectory + "aidownload.tar.bz2", "wb")
      file.write(data)
      file.close()

      extractdir = writabledatadirectory + "/extractdir"
      # should think about purgging the old directory...

      if not os.path.exists(extractdir):
         os.makedirs(extractdir)

      tar = tarfile.open(writabledatadirectory + "aidownload.tar.bz2")
      tar.extractall(extractdir)
      tar.close()

      sourcepath = None
      for root, dirs, files in os.walk( extractdir ):
         if root.find( ai_name + "/" + ai_version ) != -1:
            sourcepath = root.split( ai_name + "/" + ai_version )[0] + ai_name + "/" + ai_version
         if root.find( ai_name + "\\" + ai_version ) != -1:
            sourcepath = root.split( ai_name + "\\" + ai_version )[0] + ai_name + "\\" + ai_version

      if sourcepath == None:
         print "Failed to find ai in download"
         return

      print "ai sourcepath: " + sourcepath

      aiinfopath = sourcepath + "/AIInfo.lua"
      if not os.path.exists( aiinfopath ):
         print "No AIAinfo.lua found, so aborting"
         return

      try:
         aiinfodict = aiinfoparser.parse( aiinfopath )
      except:
         print "Failed to parse AIInfo.lua, aborting " + str(sys.exc_info()) + "\n" + str( traceback.extract_tb( sys.exc_traceback ) )
         return
        
      if not aiinfodict.has_key('shortName') or not aiinfodict.has_key('version'):
         print "AIInfo.lua does not appear to contain shortName or version -> aborting"
         return

      if ai_name != aiinfodict['shortName'] or ai_version != aiinfodict['version']:
         print "shortName (" + aiinfodict['shortName'] + ") or version (" + aiinfodict['version'] + ") contained in AIInfo.lua do not match requested download AI (" + ai_name + ", " + ai_version + ") -> aborting"
         return

      targetpath = config.aiinstallationdirectory + "/Skirmish/" + ai_name + "/" + ai_version
      if not os.path.exists(targetpath):
         os.makedirs(targetpath)

      # copy the files across...
      filehelper.rsyncav( sourcepath, targetpath )
         
      # so it is installed....
      # rerun unitsync I guess?

      initUnitSync()
      registeraisallhosts()
      
      # tell base we're finished...
      getxmlrpcproxy(host).finisheddownloadingai( config.botrunnername, config.sharedsecret, sessionid, ai_name, ai_version )

   except:
      print "something went wrong: " + str(sys.exc_info()) + "\n" + str( traceback.extract_tb( sys.exc_traceback ) )

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
   if config.JAVA_HOME != None:
      existingenv = {}
      for varname in os.environ.keys():
         if os.getenv(varname) != None:
            existingenv[varname ] = os.getenv(varname)
      existingenv[ "JAVA_HOME" ] = os.path.dirname( config.JAVA_HOME )
      popen = subprocess.Popen( [ config.springPath, writabledatadirectory + "/script.txt"], 
         env = existingenv )
   else:
      popen = subprocess.Popen( [ config.springPath, writabledatadirectory + "/script.txt"])
   finished = False
   starttimeseconds = time.time()
   doping( "playing game " + serverrequest['ai0_name'] + " vs " + serverrequest['ai1_name'] + " on " + serverrequest['map_name'] + " " + serverrequest['mod_name'] )
   lastpingtimeseconds = time.time()
   gameresult = {}
   waitingcount = 0
   while not finished:
      if waitingcount % 30 == 0:
         print "botrunner: waiting for game to terminate..."
      waitingcount = waitingcount + 1
      if time.time() - lastpingtimeseconds > config.pingintervalminutes * 60:
         doping ( "playing game " + serverrequest['ai0_name'] + " vs " + serverrequest['ai1_name'] + " on " + serverrequest['map_name'] + " " + serverrequest['mod_name'] )
         lastpingtimeseconds = time.time()
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
            gameresult['replaypath'] = getreplaypath( infologcontents )
            return gameresult
         if infologcontents.find( ai0endstring ) == -1 and infologcontents.find(ai1endstring ) != - 1:
            # ai1 died
            print "team 0 won!"
            gameresult['winningai'] = 0
            gameresult['resultstring'] = "ai0won"
            popen.kill()
            gameresult['replaypath'] = getreplaypath( infologcontents )
            return gameresult
         if infologcontents.find( ai0endstring ) != -1 and infologcontents.find(ai1endstring ) != - 1:
            # both died...
            print "A draw..." 
            gameresult['winningai'] = -1
            gameresult['resultstring'] = "draw"
            popen.kill()
            gameresult['replaypath'] = getreplaypath( infologcontents )
            return gameresult

      # check timeout (== draw)
      if ( time.time() - starttimeseconds ) > serverrequest['gametimeoutminutes'] * 60:
         # timeout
         print "Game timed out"
         gameresult['winningai'] = -1
         gameresult['resultstring'] = "gametimeout"
         popen.kill()
         gameresult['replaypath'] = getreplaypath( infologcontents )
         return gameresult

      # check timeout in game time:
      infologlines = infologcontents.split("\n")
      lastguaranteedinfologline = infologlines[len(infologlines) - 1]
      if lastguaranteedinfologline.find("[") != -1:
         numstring = lastguaranteedinfologline.split("[")[1].split("]")[0].strip()
         print "frame number string: " + numstring
         try:
            frames = int(numstring)
            print "frames: " + str( frames )
            if frames / 30 > serverrequest['gametimeoutminutes'] * 60:
               # timeout
               print "Game timed out"
               gameresult['winningai'] = -1
               gameresult['resultstring'] = "gametimeout"
               popen.kill()
               gameresult['replaypath'] = getreplaypath( infologcontents )
               return gameresult
         except:
            pass

      if popen.poll() != None:
         # spring finished / died / crashed
         # presumably if we got here, it crashed, otherwise infolog would have been written   
         print "Crashed" 
         gameresult['winningai'] = -1
         gameresult['resultstring'] = "crashed"
         gameresult['replaypath'] = getreplaypath( infologcontents )
         return gameresult

      time.sleep (1)

   return gameresult

# when spring crashes, the replay is called 'unnamed', so we'll grab that file instead
def getreplayfullpath( writabledatadirectory, relativereplaypathfrominfolog ):
   if relativereplaypathfrominfolog == None:
      print "No replay found"
      return None

   replayfullpath = writabledatadirectory + relativereplaypathfrominfolog
   if os.path.isfile(replayfullpath):
      return replayfullpath

   demo_folderpath = os.path.dirname( replayfullpath )
   demo_filename = os.path.basename( replayfullpath )

   demo_splitunder = demo_filename.split('_')
   demo_newname = '_'.join(demo_splitunder[:3] + ['unnamed',] + demo_splitunder[4:])
   demo_newpath = os.path.join(demo_folderpath, demo_newname)

   if not os.path.isfile( demo_newpath ):
      print "No replay found"
      return None

   print 'Spring bug: replay is actually named:', demo_newname
   return demo_newpath

def uploadresulttoserver( host, serverrequest, gameresult ):
   global writabledatadirectory

   # upload gameresult and serverrequest to server...
   # ...

   # first we should take care of the replay
   replaypath = getreplayfullpath( writabledatadirectory, gameresult['replaypath'] )

   uploaddatadict = {} # dict of 'replay': replaydata, etc ...

   if replaypath != '' and replaypath != None and os.path.exists( replaypath ):
      # first tar.bz2 it
      tarhandle = tarfile.open(writabledatadirectory + "/thisreplay.tar.bz2", "w:bz2" )
      os.chdir( os.path.dirname(replaypath) )  # cd in, so that we don't embed the paths
                   # in the tar file...
      tarhandle.add( os.path.basename(replaypath) )
      tarhandle.close()

      replayfilehandle = open( writabledatadirectory + "/thisreplay.tar.bz2", 'rb' )
      replaycontents = replayfilehandle.read()
      replayfilehandle.close()

      print "replay binary length: " + str(len(replaycontents))
      replaybinarywrapper = xmlrpclib.Binary(replaycontents)
      uploaddatadict['replay'] = replaybinarywrapper

   # should move this stuff to a function, but just hacking it in for now to get it working
   if os.path.exists( writabledatadirectory + 'infolog.txt' ):
      # first tar.bz2 it
      tarhandle = tarfile.open(writabledatadirectory + "/thisinfolog.tar.bz2", "w:bz2" )
      os.chdir( writabledatadirectory )  # cd in, so that we don't embed the paths
                   # in the tar file...
      tarhandle.add( os.path.basename('infolog.txt') )
      tarhandle.close()

      replayfilehandle = open( writabledatadirectory + "/thisinfolog.tar.bz2", 'rb' )
      replaycontents = replayfilehandle.read()
      replayfilehandle.close()

      print "infolog binary length: " + str(len(replaycontents))
      replaybinarywrapper = xmlrpclib.Binary(replaycontents)
      uploaddatadict['infolog'] = replaybinarywrapper

   requestuploadedok = False    
   while not requestuploadedok:
      try:
         (result,errormessage ) = getxmlrpcproxy(host).submitresult( config.botrunnername, config.sharedsecret, serverrequest['matchrequest_id'], gameresult['resultstring'], uploaddatadict )
         print "upload result: " + str( result) + " " + errormessage
         requestuploadedok = True
      except:
         print "Something went wrong uploading to the server: " + str( sys.exc_value ) + ".\nRetrying ... "
         time.sleep(5)

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
   global config, options

   print ""
   print "Welcome to botrunner."
   print ""
   print "Let's get you set up..."
   gotdata = False

   while not gotdata:
      print ""
      if options.targetwebsite != None:
         weburl = options.targetwebsite
      else:
         weburl = userinput.getChoice("Which webserver to you want to subscribe to?", ['manageddreams.com/springgrid','manageddreams.com/springgridstaging', 'localhost/springgrid' ], None, None )
         print ""
      if weburl.lower().find("http://") == -1:
         weburl = "http://" + weburl
      if options.botrunnername != None:
         botrunnername = options.botrunnername
      else:
         botrunnername = userinput.getValueFromUser("What name do you want to give to your botrunner?  This name will be shown on the website.")
         print ""
      if options.botrunnersharedsecret != None:
         botrunnersharedsecret = options.botrunnersharedsecret
      else:
         botrunnersharedsecret = userinput.getValueFromUser("What sharedsecret do you want to use with this botrunner?  This will be used to authenticate your botrunner to the website.  Just pick something, and remember it.")
         print ""

      if options.springpath != None:
         springPath = options.springpath
      else:
         springPath = getSpringPath()
         if springPath == '':
            print "Spring executable not found. Please check that it is installed"
            return False
         print "Spring executable found: " + springPath
         print ""
      if options.unitsyncpath != None:
         unitsyncPath = options.unitsyncpath
      else:
         unitsyncPath = getUnitSyncPath()
         if unitsyncPath == '':
            print "UnitSync not found. Please check that it is installed"
            return False
         print "UnitSync found: " + unitsyncPath
         print ""
      if os.getenv('JAVA_HOME') != None:
         JAVA_HOME=os.getenv('JAVA_HOME')
         usejava = True
      else:
         usejava = userinput.getbooleanfromuser( "Do you have Java installed?  This will increase the number of AIs this botrunner can run." )
         if usejava:
            print ""
            JAVA_HOME = userinput.getPath( "Appropriate value for JAVA_HOME (eg /usr/lib/jvm/java-6-sun/jre or c:\\program files\\sun jdk\\bin\\java)", [ 'c:\\program files\\sun jdk', '/usr/lib/jvm/java-6-sun/jre'] )
         else:
            JAVA_HOME = None
         print ""
      if options.downloadingok:
         downloadingok = True
      else:
         downloadingok = userinput.getbooleanfromuser( "Are you ok with downloading new AIs?  You can answer no, but your botrunner will be far more useful if you answer yes.  You should be aware that the code you download is not necessarily trusted or safe.  By answering yes, you confirm that you are running the botrunner on a machine that does not contain sensitive data, and whose compromise will not cause any issues to you or others.  You agree that you will not hold the SpringGrid website host, or admin, or author responsible for any damages that may occur whatsover." )
         print ""
      print "You have input:"
      print "   target web server: " + weburl
      print "   botrunner name: " + botrunnername
      print "   botrunner shared secret: " + botrunnersharedsecret
      print "   spring executable path: " + springPath
      print "   UnitSync path: " + unitsyncPath
      print "   Enable Java AIs: " + str(usejava)
      if usejava:
         print "   JAVA_HOME: " + JAVA_HOME
      print "   Downloading ok: " + str( downloadingok )
      print ""
      if options.yes or userinput.getConfirmation( "Is this correct?" ):
         gotdata = True

   # that's all we need, let's create the config file...
   # wait, need writable datadirectory from unitsync:

   initUnitSyncWithUnitSyncPath( unitsyncPath )

   templatecontents = filehelper.readFile(scriptdir + "/config.py.template")
   newconfig = templatecontents
   newconfig = newconfig.replace( "WEBSITEURL", weburl )
   newconfig = newconfig.replace( "BOTRUNNERNAME", botrunnername )
   newconfig = newconfig.replace( "SHAREDSECRET", botrunnersharedsecret )
   newconfig = newconfig.replace( "SPRINGPATH", springPath )
   newconfig = newconfig.replace( "UNITSYNCPATH", unitsyncPath )
   newconfig = newconfig.replace( "ALLOWDOWNLOADING", str(downloadingok) )
   newconfig = newconfig.replace( "AIINSTALLATIONDIRECTORY", writabledatadirectory + 'AI' )
   newconfig = newconfig.replace( "CANCOMPILE", 'False' )
   if usejava:
      newconfig = newconfig.replace( "$JAVA_HOME", JAVA_HOME )
   else:
      newconfig = newconfig.replace( "$JAVA_HOME", "None" )
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
   registeredaiswehave = []  # we'll go through this and figure out which ones we don't have,
                             # then unregister them
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
         else:
            registeredaiswehave.append( [shortname,version] )

   for shortname, version in registeredais:
      if registeredaiswehave.count( [shortname, version] ) == 0:
         print "un-registering ai " + shortname + " version " + version + " ..."
         multicall.registerunsupportedai( config.botrunnername, config.sharedsecret, shortname, version )

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

# registers ais to all hosts
# used after downloading a new AI
def registeraisallhosts():
   for host in config.websiteurls:
      registeredais = getxmlrpcproxy(host).getsupportedais( config.botrunnername, config.sharedsecret )
      registerais(host, registeredais )

def initUnitSync():
   global config
   initUnitSyncWithUnitSyncPath(config.unitsyncPath)

def initUnitSyncWithUnitSyncPath(unitsyncpath):
   global unitsync, writabledatadirectory
   unitsync = unitsyncpkg.Unitsync(unitsyncpath)
   unitsync.Init(True,1)
   writabledatadirectory = unitsync.GetWritableDataDirectory()

def go():
   global config, unitsync, writabledatadirectory
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
      if options.configpath != None:
         config = imp.load_source('config', options.configpath )
      else:
         import config
      print "Configuration found, using"
   except:
      ok = setupConfig()
      if not ok:
         return

   initUnitSync()

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
            result = rungame( serverrequest )
            uploadresulttoserver( host, serverrequest, result )
            gotrequest = True

      if not gotrequest and config.allowdownloading:  # see if we can download a new ai
         print "checking for download request ... "
         for host in config.websiteurls:
            if trydownloadingai(host) != None:
               gotrequest = True
               break
      
      if not gotrequest:
         # else, sleep...
         print "Nothing to do.  Sleeping..."
         doping("sleeping")
         time.sleep(config.sleepthislongwhennothingtodoseconds)

if __name__ == '__main__':
   go()

