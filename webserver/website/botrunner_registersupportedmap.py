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

# lets a botrunner add a single map to the database

# import cgitb; cgitb.enable()
import cgi
import sys

from utils import *
from core import *

def printfailresponse(reason ):
   print '<response success="false" reason="' + reason.replace('"', "'") + '" />'

def printsuccessresponse():
   print "<response success='true' />"

def addmapifdoesntexist(mapname, maparchivechecksum):
   rows = dbconnection.cursor.execute("select map_archivechecksum from maps where map_name = %s", (mapname) )
   if rows == 0:
      try:
         rows = dbconnection.cursor.execute( "insert into maps ( map_name, map_archivechecksum ) "\
            " values ( %s, %s )", ( mapname, maparchivechecksum) )
      except:
         printfailresponse("error adding to db: " + str( sys.exc_value ) )
         return False

      if rows != 1:
         printfailresponse("error adding to db")
         return False

   if rows.fetchone()["map_archivechecksum"] != maparchivechecksum:
      printfailresponse("map archive checksum doesn't match the one already on the website.")
      return False

   return True

def go():
   if not botrunnerhelper.botrunnerauthorized():
      printfailresponse("Not authenticated")
      return 

   mapname = formhelper.getValue("mapname")
   maparchivechecksum = formhelper.getValue("maparchivechecksum")
   if mapname == None  or mapname == '' or maparchivechecksum == None or maparchivechecksum == '':
      printfailresponse("not all fields supplied")
      return

   if not addmapifdoesntexist(mapname, maparchivechecksum):
      return

   # Now, register the map as supported map

   printsuccessresponse()

print "Content-type: text/xml\n\n"
try:
   dbconnection.connectdb()
   go()
   dbconnection.disconnectdb()
except:
   printfailresponse("Unexpected exception: " + str( sys.exc_value ) )

