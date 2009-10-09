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

try:
   # if we can import config, then we already configured the website and set up the database
   import config
   print "Content-type: text/html\n\n"
   print "Unauthorized"
except:
   print "Content-type: text/html\n\n"
   print "<html>"
   print "<head>"
   print "<title>AILadder - setup</title>"
   print "</head>"
   print "<body>"
   print "<h3>AILadder - setup</h3>"
   print "<p>Please enter the following details and press submit</p>"
   print "<p>Please ensure the database exists already, that the user you specify has access to that database, and that the database is running</p>"
   print "<form method='post' action='websetupdb.py'>"
   print "<table cellpadding='3' border='1'>"
   print "<tr><td>MySQL database name:</td><td><input type='text' name='dbname' value='ailadder'></td></tr>"
   print "<tr><td>MySQL database hostname:</td><td><input type='text' name='dbhost' value='localhost'></td></tr>"
   print "<tr><td>MySQL database username:</td><td><input type='text' name='dbuser' value=''></td></tr>"
   print "<tr><td>MySQL database password:</td><td><input type='password' name='dbpassword' value=''></td></tr>"
   print "<tr><td></td><td><input type='submit' value='Setup'></td></tr>"
   print "</table>"
   print "</form>"
   print "</body>"
   print "</html>"

