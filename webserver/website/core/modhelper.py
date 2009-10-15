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

from utils import *

# returns True if exists, or added ok, otherwise False
def addmodifdoesntexist(modname, modarchivechecksum):
   rows = dbconnection.dictcursor.execute("select mod_archivechecksum from mods where mod_name = %s", (modname) )
   if rows == 0:
      try:
         rows = dbconnection.dictcursor.execute( "insert into mods ( mod_name, mod_archivechecksum ) "\
            " values ( %s, %s )", ( modname, modarchivechecksum) )
      except:
         return(False, "error adding to db: " + str( sys.exc_value ) )

      if rows != 1:
         return(False,"error adding to db")
      
      return (True,'')

   row = dbconnection.dictcursor.fetchone()
   if row["mod_archivechecksum"] != modarchivechecksum:
      return (False,"mod archive checksum doesn't match the one already on the website.")

   return (True,'')

# return list of supported modnames
def getsupportedmods( botrunnername ):
   return dbconnection.querytolistwithparams("select mod_name "\
      " from mods, botrunners, botrunner_supportedmods "\
      " where mods.mod_id = botrunner_supportedmods.mod_id "\
      " and botrunners.botrunner_name = %s ",
      ( botrunnername, ) )

def setbotrunnersupportsthismod( botrunnername, modname ):
   # Now, register the mod as supported mod
   rows = dbconnection.dictcursor.execute("select * from botrunners, botrunner_supportedmods, mods " \
      " where botrunners.botrunner_id = botrunner_supportedmods.botrunner_id "\
      " and botrunners.botrunner_name = %s "\
      " and botrunner_supportedmods.mod_id = mods.mod_id "\
      " and mods.mod_name = %s ",
      ( botrunnername, modname ) )
   #print rows
   if rows == 0:
      dbconnection.dictcursor.execute("insert into botrunner_supportedmods "\
         " ( botrunner_id, mod_id ) "\
         " select botrunner_id, mod_id "\
         " from botrunners, mods "\
         " where botrunners. botrunner_name = %s "\
         " and mods.mod_name = %s ",
         ( botrunnername, modname ) )
   return (True,'')

