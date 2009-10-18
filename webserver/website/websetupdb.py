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

import cgitb; cgitb.enable()

from utils import filehelper

scriptdir = os.path.dirname( os.path.realpath( __file__ ) )

setupdb = None

# carry out some verification checks on the installation
def runchecks():
   # check replays directory is writable
   if not os.path.exists(scriptdir + "/replays"):
      try:
         os.makedirs( scriptdir + "/replays" )
      except:
         print "Cannot create 'replays' directory in website directory.  Please create the 'replays' directory in the website directory, and ensure it is writable"
         return False
   # if we got here, replays directory exists, check writable...
   testfilepath = scriptdir + "/replays/~test"
   if os.path.exists( testfilepath ):
      try:
         os.remove( testfilepath )
      except:
         print str(sys.exc_value) + "<br />"
      if os.path.exists( testfilepath ):  
         print "Cannot delete old testfile from 'replays' directory on website.  Please check that the 'replays' directory in the website directory is writable, and then try again."
         return False

   try:
      filehelper.writeFile( testfilepath, "foo" )
   except:
      print str(sys.exc_value) + "<br /><br />"

   if not os.path.exists( testfilepath ):  
      print "Please check that the 'replays' directory in the website directory is writable, and then try again."
      return False

   os.remove( testfilepath )

   return True

def go():
   try:
      # If we can import config, then we are already configured
      import config
      print "Content-type: text/html\n\n"
      print "Unauthorized"
      return
   except:
      pass
      # ok

   print "Content-type: text/html\n\n"

   # try to set up the database, then write to the config file
   # let's hope the web site has write access to the website directory...

   from utils import formhelper

   dbuser = formhelper.getValue('dbuser')
   dbpassword = formhelper.getValue('dbpassword')
   dbname = formhelper.getValue('dbname')
   dbhost = formhelper.getValue('dbhost')

   if not runchecks():
      return

   if dbuser == None or dbpassword == None or dbname == None or dbhost == None or dbuser == '' or dbpassword == '' or dbname == '' or dbhost == '':
      print "Please fill in all the values and try again."
      return

   from core import sqlalchemysetup

   try:
      sqlalchemysetup.setupwithcredentials( 'mysql', dbuser, dbpassword, dbhost, dbname )
   except:
      # if can't connect, then abort
      print "Exception: " + str(sys.exc_value)
      return

   try:
      sqlalchemysetup.reloadalltables()
      sqlalchemysetup.close()
   except:
      # if can't connect, then abort
      print "Exception: " + str(sys.exc_value)
      return

   # Thats done.. now create the config file, first read the template:
   from utils import filehelper
   templatecontents = filehelper.readFile("config.py.template")
   # substitute in connection details
   templatecontents = templatecontents.replace("DBENGINE", 'mysql' ) #hardcode for now, can make a better form in the future...
   templatecontents = templatecontents.replace("DBNAME", dbname )
   templatecontents = templatecontents.replace("DBPASS", dbpassword )
   templatecontents = templatecontents.replace("DBHOST", dbhost )
   templatecontents = templatecontents.replace("DBUSER", dbuser )
   filehelper.writeFile("config.py", templatecontents)

   # signal that ok
   print "<br /><br />Everything should hopefully be configured now.  Please go to <a href='index.cgi'>home page</a> to continue."

def usage():
   print "Usage: " + sys.argv[0] + " username password dbname dbhostname [create|drop]"

go()

