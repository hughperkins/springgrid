#!/usr/bin/python

# Copyright Hugh Perkins 2009
# hughperkins@gmail.com http://manageddreams.com
#
# This program is free software; you can redistribute it and/or aiify it
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

# lets a user add a single ai to the database
#
# This is mostly for bootstrapping, to make the website immediately useful

import cgitb; cgitb.enable()
import cgi

from utils import *
from core import *

dbconnection.connectdb()

loginhelper.processCookie()

menu.printPageTop()

if not roles.isInRole(roles.aiadmin):
   print "You must be logged in as an aiadmin"
else:
   ainame = formhelper.getValue("ainame")
   aiversion = formhelper.getValue("aiversion")
   aioption = formhelper.getValue("aioption")

   if aiversion != None and ainame != None and aioption != None and ainame != "" and aiversion != "" and aioption != "":
      rows = dbconnection.cursor.execute( "insert into ai_allowedoptions "\
         "( ai_id, option_id  ) "\
         " select ai_id, option_id "\
         " from ais, aioptions "\
         " where ais.ai_name = %s "\
         " and ais.ai_version = %s "\
         " and aioptions.option_name = %s ",
         ( ainame, aiversion, aioption ) )
      if rows == 1:
         print "Added ok"
      else:
         print "Something went wrong.  Please check your values and try again."
   else:
      print "Please fill in the fields and try again"

dbconnection.disconnectdb()

menu.printPageBottom()

