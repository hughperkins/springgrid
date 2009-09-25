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

import utils.loginhelper as loginhelper
import utils.dbconnection as dbconnection
import utils.formhelper as formhelper
import utils.htmlformshelper as htmlformshelper

calcenginename = ""

def calcengineauthorized():
   global calcenginename 

   calcenginename = formhelper.getValue("calcenginename")
   sharedsecret = formhelper.getValue("sharedsecret")
   return validatesharedsecret( calcenginename, sharedsecret )

def validatesharedsecret(lcalcenginename, sharedsecret):
   global calcenginename
   dbconnection.cursor.execute("select calcengine_sharedsecret from calcengines where calcengine_name=%s", (lcalcenginename,) )
   row = dbconnection.cursor.fetchone()
   if row == None:
      return False
   actualsharedsecret = row[0]
   if actualsharedsecret == sharedsecret:
      calcenginename = lcalcenginename
      return True
   return False




