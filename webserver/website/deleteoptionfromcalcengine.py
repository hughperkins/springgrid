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

def go():
   calcenginename = formhelper.getValue('calcenginename')
   optionname = formhelper.getValue('optionname')

   if not loginhelper.isLoggedOn():
      print "Please logon first."
      return

   if calcenginename == None or optionname == None or calcenginename == '' or optionname == '':
      print "Please fill in the fields and try again"
      return

   calcengineownername = calcenginehelper.getOwnerUsername( calcenginename ) 
   if calcengineownername != loginhelper.getUsername():
      print "You must be the calcengine owner"
      return

   rows = dbconnection.cursor.execute( "delete calcengine_assignedoptions.* "\
         " from calcengine_assignedoptions, calcengines, calcengine_options "\
         " where calcengines.calcengine_name = %s "\
         " and calcengine_option_name = %s "\
         " and calcengine_assignedoptions.calcengine_id = calcengines.calcengine_id "\
         " and calcengine_assignedoptions.calcengine_option_id = calcengine_options.calcengine_option_id ",
       ( calcenginename, optionname ) )
   if rows != 1:
      print "Something went wrong.  Please check your values and try again."
      return

   print "Removed ok"

go()

dbconnection.disconnectdb()

menu.printPageBottom()

