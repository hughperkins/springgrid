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

import cgitb; cgitb.enable()


from core import *

version = None
try:
   import version
except:
   pass

menu.printPageTop()


print '<h3>AILadder - About</h3>'

print '<table border="1" cellpadding="3">'
if version != None:
   print '<tr><td>Version:</td><td>' + str( version.version ) + '</td></tr>'
else:
   print '<tr><td>Version:</td><td>Dev code, not versioned.</td></tr>'
print '<tr><td>License:</td><td>GPL v2</td></tr>'
print '<tr><td>Authors:</td><td><a href="http://manageddreams.com">Hugh Perkins</a></td></tr>'
print '<tr><td>Download url:</td><td><a href="http://github.com/hughperkins/ailadder/archives/master">http://github.com/hughperkins/ailadder/archives/master</a></td></tr>'
print '<tr><td>Source-code:</td><td><a href="http://github.com/hughperkins/ailadder">http://github.com/hughperkins/ailadder</a></td></tr>'
print '</table>'

menu.printPageBottom()

