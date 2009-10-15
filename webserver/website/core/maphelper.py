# Copyright Hugh Perkins 2009
# hughperkins@gmail.com http://manageddreams.com
#
# This program is free software; you can redistribute it and/or mapify it
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

from utils import *

# returns True if exists, or added ok, otherwise False
def addmapifdoesntexist(mapname, maparchivechecksum):
   rows = dbconnection.dictcursor.execute("select map_archivechecksum from maps where map_name = %s", (mapname) )
   if rows == 0:
      try:
         rows = dbconnection.dictcursor.execute( "insert into maps ( map_name, map_archivechecksum ) "\
            " values ( %s, %s )", ( mapname, maparchivechecksum) )
      except:
         return(False, "error adding to db: " + str( sys.exc_value ) )

      if rows != 1:
         return(False,"error adding to db")
      
      return (True,'')

   row = dbconnection.dictcursor.fetchone()
   if row["map_archivechecksum"] != maparchivechecksum:
      return (False,"map archive checksum doesn't match the one already on the website.")

   return (True,'')

def setbotrunnersupportsthismap( botrunnername, mapname ):
   # Now, register the map as supported map
   rows = dbconnection.dictcursor.execute("select * from botrunners, botrunner_supportedmaps, maps " \
      " where botrunners.botrunner_id = botrunner_supportedmaps.botrunner_id "\
      " and botrunners.botrunner_name = %s "\
      " and botrunner_supportedmaps.map_id = maps.map_id "\
      " and maps.map_name = %s ",
      ( botrunnername, mapname ) )
   #print rows
   if rows == 0:
      dbconnection.dictcursor.execute("insert into botrunner_supportedmaps "\
         " ( botrunner_id, map_id ) "\
         " select botrunner_id, map_id "\
         " from botrunners, maps "\
         " where botrunners. botrunner_name = %s "\
         " and maps.map_name = %s ",
         ( botrunnername, mapname ) )
   return (True,'')

