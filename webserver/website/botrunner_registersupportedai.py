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

# lets a botrunner add a single mod to the database

# import cgitb; cgitb.enable()
import cgi
import sys

from utils import *
from core import *

def printfailresponse(reason ):
   print '<response success="false" reason="' + reason.replace('"', "'") + '" />'

def printsuccessresponse():
   print "<response success='true' />"

def addaiifdoesntexist(ainame, aiversion):
   rows = dbconnection.dictcursor.execute("select * from ais where ai_name = %s and ai_version = %s", (ainame, aiversion) )
   if rows == 0:
      try:
         rows = dbconnection.dictcursor.execute( "insert into ais ( ai_name, ai_version ) "\
            " values ( %s, %s )", ( ainame, aiversion ) )
      except:
         printfailresponse("error adding to db: " + str( sys.exc_value ) )
         return False

      if rows != 1:
         printfailresponse("error adding to db")
         return False

   return True

def go():
   if not botrunnerhelper.botrunnerauthorized():
      printfailresponse("Not authenticated")
      return 

   ainame = formhelper.getValue("ainame")
   aiversion = formhelper.getValue("aiversion")
   if ainame == None  or ainame == '' or aiversion == None or aiversion == '':
      printfailresponse("not all fields supplied")
      return

   if not addaiifdoesntexist(ainame, aiversion):
      return

   # Now, register the mod as supported mod

   printsuccessresponse()

print "Content-type: text/xml\n\n"
try:
   dbconnection.connectdb()
   go()
   dbconnection.disconnectdb()
except:
   printfailresponse("Unexpected exception: " + str( sys.exc_value ) )

