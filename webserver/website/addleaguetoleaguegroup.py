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

import cgitb; cgitb.enable()
import cgi

from utils import *
from core import *

dbconnection.connectdb()
sqlalchemysetup.setup()

loginhelper.processCookie()

menu.printPageTop()

if loginhelper.gusername == '':
   print "You must login first"
else:
   leaguegroupname = formhelper.getValue('leaguegroupname')
   leaguename = formhelper.getValue('leaguename')

   if leaguegroupname != None and leaguegroupname != '' and leaguename != None and leaguename != '':
      rows = dbconnection.cursor.execute( "insert into leaguegroup_leaguemembers "\
         "( leaguegroup_id, league_id ) "\
         " select leaguegroup_id, league_id from "\
         " leaguegroups, leagues "\
         " where leaguegroups.leaguegroup_name = %s "\
         " and leagues.league_name = %s ",
         ( leaguegroupname, leaguename ) )
      if rows == 1:
         print "Added ok"
      else:
         print "Something went wrong.  Please check your values and try again."
   else:
      print "Please fill in the fields and try again"

dbconnection.disconnectdb()
sqlalchemysetup.close()

menu.printPageBottom()

