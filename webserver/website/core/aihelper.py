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

def addaiifdoesntexist(ainame, aiversion):
   rows = dbconnection.dictcursor.execute("select * from ais where ai_name = %s and ai_version = %s", (ainame, aiversion) )
   if rows == 0:
      try:
         rows = dbconnection.dictcursor.execute( "insert into ais ( ai_name, ai_version ) "\
            " values ( %s, %s )", ( ainame, aiversion ) )
      except:
         return(False,"error adding to db: " + str( sys.exc_value ) )

      if rows != 1:
         return(False,"error adding to db")

   return (True,'')


