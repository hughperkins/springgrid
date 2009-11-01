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

# So, this will be included in an installation packge, with a hierarchy as follows:
# /
#    setup_vm_botrunner.py
#    /utils
# ... and that's it: it will download everything else it needs (?)

# The target hierarchy, after download, will be:
# /
#    setup_vm_botrunner.py
#    /utils
#       ...
#    # I suppose the vm will end up wherever import puts it
#    /springgrid
#       /botrunner
#          config_vbox.py
#          ...
#    /springheadless
#       spring-headlessstubs
#       libunitsync.so
#       /AI
#           /Interfaces
#               /Java
#                  ...
#               /C
#                  ...
#    /writabledatadir
#       /AI
#    plus, somewhere the user has a springdata directory with maps and mods, which we need to
#    get from him
#
#    we can also have:
#    /tmp
#        ... download the vm image to here, download other things to here
# 

import sys
import os
import subprocess
import urllib
import imp
import tarfile
import md5

from utils import *

scriptdir = os.path.dirname( os.path.realpath( __file__ ) )

import cmdlineoptions

urllisturl = 'http://manageddreams.com/ailadder/download/botrunner_urllist.txt'

urllist = None  # do we want this downloaded, or we just include it in the package?

# returns md5sum of file at filepath
def md5sumfile( filepath ):
   checksum = md5.md5()
   file = open( filepath, "rb" )
   data = file.read(100000)
   while( len(data) > 0 ):
      checksum.update(data)
      data = file.read(100000)
   return checksum.hexdigest()

def downloaddataurl( url, filepath, md5sum ):
   print "Downloading " + url + " ..."

   if md5sum != None:
      if os.path.exists( filepath ):
         print "... file already exists, checking checksum... "
         checksum = md5sumfile( filepath )
         if checksum == md5sum:
            print " ... already downloaded (md5sum " + md5sum + ")"
            return

   serverrequesthandle = urllib.urlopen( url, None )
   data = serverrequesthandle.read(10000)
   # print data
   #  we download a bit, then check its not an  error message, then download in chunks so that
   # each chunk doesnt timeout
   if len(data) < 1000:
      print data
      if data.find("404 Not Found") != -1:
         raise Exception("URL not valid: " + url )
      if data.find("<title>") != -1:
         raise Exception( data.split("<title>")[1].split("</title>")[0] + " " + url )
   file = open(filepath, "wb")
   while len(data) > 0:
      file.write(data)
      sys.stdout.write( "." )
      data = serverrequestarray = serverrequesthandle.read(1000000)
   file.close()

def downloadurllist():
   global urllist

   if cmdlineoptions.options.urllisturl != None:
      urllisturl = cmdlineoptions.options.urllisturl

   downloaddataurl( urllisturl, gettempdir() + "/urllist.py", None )
   urllist = imp.load_source('urllist', gettempdir() + "/urllist.py" )
   # import urllist

def downloadvm():
   downloaddataurl( urllist.vmhdurl, gettempdir() + "/" + os.path.basename( urllist.vmhdurl ), urllist.vmhdmd5 )
   downloaddataurl( urllist.vmmachineurl, gettempdir() + "/" + os.path.basename( urllist.vmmachineurl ), urllist.vmmachinemd5 )   

def downloadspringheadless():
   downloaddataurl( urllist.springheadlessurl, gettempdir() + "/springheadless.tar.bz2", urllist.springheadlessmd5 )
   tar = tarfile.open( gettempdir() + "/springheadless.tar.bz2" )
   tar.extractall(scriptdir + "/spring-headlessstubs")
   tar.close()

def downloadbotrunner():
   git.gitClone( urllist.springgridgiturl, scriptdir + "/springgrid" )

def installvm():
   virtualbox.importAppliance( gettempdir() + "/botrunner.ovf" )

def configuresharedfolders():
   vminfo = virtualbox.getvminfo('botrunner')
   print vminfo
   #   virtualbox.
   pass

# configures botrunner/config_vbox.py
def configurebotrunnerconfig():
   pass

def gettempdir():
   return scriptdir + "/tmp"

springdatadir = None
def go():
   global springdatadir
   virtualbox.vboxmanagepath = userinput.getPath("VBoxManage full path", ['/usr/bin/VBoxManage', 'C:\\Program File\\VirtualBox\\VBoxManage.exe'])
   springdatadir = userinput.getPath("Spring directory containing 'maps' and 'mods'.  It will be mounted read-only by the vm.", ['/usr/share/games/spring', 'C:\\Program File\\SpringRTS'])

   if not os.path.exists( gettempdir() ):
      os.makedirs( gettempdir() )

   downloadurllist()
   downloadvm()
   downloadspringheadless()
   downloadbotrunner()

   #installvm()
   #configurebotrunnerconfig()
   configuresharedfolders()

go()


