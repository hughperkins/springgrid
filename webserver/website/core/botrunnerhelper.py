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

import cgi

from utils import *
#from core import *

botrunnername = ""

def botrunnerauthorized():
   global botrunnername 

   botrunnername = formhelper.getValue("botrunnername")
   sharedsecret = formhelper.getValue("sharedsecret")
   return validatesharedsecret( botrunnername, sharedsecret )

def validatesharedsecret(lbotrunnername, sharedsecret):
   global botrunnername
   dbconnection.cursor.execute("select botrunner_sharedsecret from botrunners where botrunner_name=%s", (lbotrunnername,) )
   row = dbconnection.cursor.fetchone()
   if row == None:
      return False
   actualsharedsecret = row[0]
   if actualsharedsecret == sharedsecret:
      botrunnername = lbotrunnername
      return True
   return False

def getOwnerUsername(botrunnername):
   rows = dbconnection.cursor.execute("select username from "\
      " botrunners, accounts " \
      " where botrunners.botrunner_owneraccountid = account_id "\
      " and botrunners.botrunner_name = %s ",
      ( botrunnername ) )
   if rows == 0:
      return ''
   row = dbconnection.cursor.fetchone()
   if row == None:
      return
   return row[0]



