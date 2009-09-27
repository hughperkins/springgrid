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

# lets a user add a single account to the database
#
# This is mostly for bootstrapping, to make the website immediately useful

import cgitb; cgitb.enable()
import cgi

from utils import *
from core import *

dbconnection.connectdb()

loginhelper.processCookie()

menu.printPageTop()

print '<form action="changepassword.py" method="post"'
print '<table border="1" cellpadding="3">'
print '<tr><td>Old password:</td><td><input type="password" name="oldpassword"/></td></tr>'
print '<tr><td>New password:</td><td><input type="password" name="password"/></td></tr>'
print '<tr><td>Confirm password:</td><td><input type="password" name="confirmpassword"/></td></tr>'
print '<tr><td></td><td><input type="submit" value="Change password"/></td></tr>'
print '</table>'
print '</form>'

menu.printPageBottom()

