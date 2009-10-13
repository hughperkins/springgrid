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

from utils import *

def printPageTop( headers = 'Content-type: text/html\n\n' ):
   print getPageTop( headers )

def additem( title, link ):
   return '<a href="' + link + '"><div class="menuitem">' + title + '</div></a>'

def addmenu( title, itemlist ):
   html = ''
   html = html + '<div class="menu">'
   html = html + '<div class="popuptitle">' + title + '</div>'
   html = html + '<div class="popup">'
   for item in itemlist:
      html = html + item
   html = html + '</div>'
   html = html + '</div>'
   return html

bodycontent = ''

def addBodyContent( html ):
  bodycontent = bodycontent + html;

def getPageTop( headers = 'Content-type: text/html\n\n' ):
   page = headers + "\n\n"
   page = page + "<html>"\
    "<head>"\
    "<title>AILadder</title>"\
    "</head>"\
    "<body>"

   page = page + '<link rel="stylesheet" rev="stylesheet" href="style.css">'

   page = page + '<div class="header">'
   #if loginhelper.isLoggedOn():
   #   page = page + loginhelper.getUsername()
   page = page + '</div>'

   page = page + '<div class="mainmenu">'

   accountitems = []
   if loginhelper.isLoggedOn():
      accountitems = ( additem( 'Change Password', 'changepasswordform.py' ),
      additem( 'Logout', 'logout.py' ) )
      page = page + addmenu( 'User: ' + loginhelper.getUsername(), accountitems )
   else:
      accountitems = ( additem( 'Login', 'loginform.py' ) )
      page = page + addmenu( 'Login', accountitems )

   page = page + addmenu( 'League', ( additem( 'View league group results', 'viewleaguegroupresults.py' ),
      additem( 'View league results', 'viewleagueresults.py' ),
      additem( 'View match results', 'viewresults.py' ) ) )

   page = page + addmenu( 'Runner', ( additem( 'View request queue', 'viewrequests.py' ),
      additem( 'Add request to queue', 'submitrequestform.py' ) ) )

   page = page + addmenu( 'Configuration', ( additem( 'Setup notes', 'setupnotes.py' ),
      additem( 'View league groups', 'viewleaguegroups.py' ),
      additem( 'View leagues', 'viewleagues.py' ),
      additem( 'View available bot runners', 'viewbotrunners.py' ),
      additem( 'View available maps', 'viewmaps.py' ),
      additem( 'View available mods', 'viewmods.py' ),
      additem( 'View available ais', 'viewais.py' ),
      additem( 'View accounts', 'viewaccounts.py' ) ) )

   page = page + addmenu( 'About', ( additem( 'About', 'about.py' ) ) )

   page = page + '</div>'

   page = page + '<div class="contents">'

   page = page + bodycontent

#   page = page + filehelper.readFile("menu.html")
   return page

def printPageBottom():
   print getPageBottom()

def getPageBottom():
   return ""\
    "</div>"\
    "</body>"\
    "</html>"


