# Copyright Hugh Perkins 2004, 2009
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

# functions for login, cookies etc...

import Cookie
import MySQLdb
import random
import cgi
import string
import os
import os.path

import dbconnection

import stringhelper
   
gusername = ""  # first call loginhelper.processCookie().  If the user
                # is already logged in after that, then gusername will no
                # longer be blank
                # testing gusername != '' is sufficient to check if the user
                # is logged in
loginhtml = ""
cookiereference = ''
cookie = Cookie.SimpleCookie()

saltlength = 200

def GenerateRef():
   return stringhelper.getRandomAlphaNumericString(40)

def isLoggedOn():
   global gusername
   return ( gusername != '')

def getUsername():
   global gusername
   return gusername

# returns a salt string
def createSalt():
   global saltlength
   return stringhelper.getRandomPrintableString(saltlength)

# returns True if password correct, otherwise false
def validateUsernamePassword( username, password ):
   rows = dbconnection.cursor.execute( "select username from accounts where username=%s and passwordhash = md5(concat(%s, passwordsalt))", ( username, password, ) )
   return ( rows == 1 )

def logonUser(username, password):
   global gusername
   global loginhtml
   global cookie
   global cookiereference

   gusername = ""
   if not validateUsernamePassword( username, password ):
      loginhtml =  "<h4>Logon error: Please check your username and password.</h4>"
      return

   cookiereference = GenerateRef()

   cookie = Cookie.SimpleCookie()
   cookie["cookiereference"] = cookiereference

   dbconnection.cursor.execute("delete from cookies where username=%s", (username,))
   dbconnection.cursor.execute("insert into cookies (username,cookiereference)" \
         " values (%s, %s )", (username, cookiereference, ) )

   gusername = username
   loginhtml = "<p>Logged in as: " + gusername + "</p>"

def changePassword( username, password ):
   passwordsalt = createSalt()
   rows = dbconnection.cursor.execute( "update accounts "\
      " set passwordsalt = %s, "\
      " passwordhash = md5( concat( %s, %s ) ) "\
      " where username = %s ",
      ( passwordsalt, password, passwordsalt, username, ) )
   return (rows == 1 )

def processCookie():
  global cookie, cookiereference, gusername, loginhtml

  gusername = ''
  cookie = Cookie.SimpleCookie( os.environ.get("HTTP_COOKIE"))
  c = cookie.output( "Cookie: " )
  if(not c):
     return

  if not cookie.has_key( "cookiereference" ):
      return

  cookiereference = str( cookie["cookiereference"].value )

  dbconnection.cursor.execute("select username from cookies where cookiereference=%s", (cookiereference,))
  row = dbconnection.cursor.fetchone()

  if row == None:
     return

  gusername = row[0]

  if gusername == '':
     return

  loginhtml = "<p>Logged in as: " + gusername + "</p>"

def logoutUser():
   global cookie, cookiereference, gusername, loginhtml
   
   dbconnection.cursor.execute("delete from cookies where username=%s", (gusername,))
   
   cookiereference = '0'
   cookie = Cookie.SimpleCookie()
   gusername = ""
   loginhtml = ""



