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

scriptdir = os.path.dirname( os.path.realpath( __file__ ) )

setupdb = None

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

   if dbuser == None or dbpassword == None or dbname == None or dbhost == None or dbuser == '' or dbpassword == '' or dbname == '' or dbhost == '':
      print "Please fill in all the values and try again."
      return

   from utils import dbconnection

   try:
      dbconnection.connectdbwiththesecredentials(dbuser, dbpassword, dbname, dbhost )
   except:
      # if can't connect, then abort
      print "Exception: " + str(sys.exc_value)
      return

   sys.path.append("db")
   import setupdb
   setupdb.createall(dbuser,dbpassword,dbname,dbhost)

   # Thats done.. now create the config file, first read the template:
   from utils import filehelper
   templatecontents = filehelper.readFile("config.py.template")
   # substitute in connection details
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

