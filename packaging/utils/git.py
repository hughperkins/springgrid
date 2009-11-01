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

import sys
import os
import subprocess
import shutil
import bz2
from optparse import OptionParser

scriptdir = os.path.dirname( os.path.realpath( __file__ ) )

# creates bz2 archive at current directory, for relative filepath, called bz2tarfilename
def gitArchiveToBz2( relativefilepath, bz2tarfilename ):
   popen = subprocess.Popen( ["git", "archive", "HEAD@{0}", relativefilepath, "--format", "tar"], stdout = subprocess.PIPE)
   print "Creating git archive " + bz2tarfilename + " ..."
   (stdoutdata, stderrdata ) = popen.communicate(None)
   print " ... git archive finished ... waiting for bz2 ..."
   tarcontents = stdoutdata
   # tarcontents = popen.stdout.read()
   tarbz2contents = bz2.compress( tarcontents )
   fh = open( bz2tarfilename, "wb" )
   fh.write( tarbz2contents )
   fh.close()
   print " ... bz2 finished."

def gitAdd( filepath ):
      popen = subprocess.Popen( ["git", "add", filepath ] )
      popen.wait()   

def gitCommit(message):
   popen = subprocess.Popen( ["git", "commit", "-m", message ] )
   popen.wait()

def gitPush( destination ):
   popen = subprocess.Popen( ["git", "push", destination ] )
   popen.wait()

def gitClone( url, targetpath ):
   print 'git cloning ' + url + ' to ' + targetpath + ' ...'
   popen = subprocess.Popen(['git','clone',url,targetpath] )
   popen.wait()
   print ' ... done'

def gitFetch( targetpath, remotename ):
   oldcurdir = os.path.abspath( os.curdir )
   os.chdir( targetpath )
   popen = subprocess.Popen(['git','fetch', remotename] )
   popen.wait()
   os.chdir( oldcurdir )

def gitPull( targetpath ):
   oldcurdir = os.path.abspath( os.curdir )
   os.chdir( targetpath )
   popen = subprocess.Popen(['git','pull'] )
   popen.wait()
   os.chdir( oldcurdir )

