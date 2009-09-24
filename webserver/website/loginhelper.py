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

import cgitb; cgitb.enable()
import Cookie
import MySQLdb
import random
import cgi
import string
import os
import os.path

import dbconnection
   
gusername = ""  # first call loginhelper.processCookie().  If the user
                # is already logged in after that, then gusername will no
                # longer be blank
                # testing gusername != '' is sufficient to check if the user
                # is logged in
loginhtml = ""
cookiereference = 0
cookie = Cookie.SimpleCookie()

def GenerateRef():
   return random.randint(0,1000000)

def logonUser(username, password):
   global gusername
   global loginhtml
   global cookie
   global cookiereference

   gusername = ""
   dbconnection.cursor.execute( "select password from accounts where username=%s", ( username, ) )
   row = dbconnection.cursor.fetchone()
   if row == None:
      loginhtml =  "<h4>Logon error: Please check your username and password.</h4>"
      return

   if row[0] != password:
      loginhtml = "<h4>Logon error: Please check your username and password.</h4>"
      return

   cookiereference = str( GenerateRef() )

   cookie = Cookie.SimpleCookie()
   cookie["cookiereference"] = cookiereference

   dbconnection.cursor.execute("delete from cookies where username=%s", (username,))
   dbconnection.cursor.execute("insert into cookies (username,cookiereference)" \
         " values (%s, %s )", (username, cookiereference, ) )

   gusername = username
   loginhtml = "<p>Logged in as: " + gusername + "</p>"

# def ChangePassword( cursor, form, sLogin ):
#    global loginhtml
#    sNewPassword = form["NewPassword"].value
#    query = "update accounts set s_password = '" + sNewPassword + "' where s_login = '" + sLogin + "'"
   # print query
#    cursor.execute( query )
#    loginhtml = loginhtml + "<p>Password updated</p>"

def processCookie():
  global cookie, cookiereference, gusername, loginhtml

  cookie = Cookie.SimpleCookie( os.environ.get("HTTP_COOKIE"))
  refnum = 0
  c = cookie.output( "Cookie: " )
  if(c):
     if cookie.has_key( "cookiereference" ):
        cookiereference = cookie["cookiereference"].value

  dbconnection.cursor.execute("select username from cookies where cookiereference=%s", (cookiereference,))
  row = dbconnection.cursor.fetchone()
  if row != None:
     gusername = row[0]
      
  if gusername != "": 
     loginhtml = "<p>Logged in as: " + gusername + "</p>"
  else:  
     cookie = Cookie.SimpleCookie()
     cookiereference = 0

def logoutUser():
   global cookie, cookiereference, gusername, loginhtml
   
   dbconnection.cursor.execute("delete from cookies where username=%s", (gusername,))
   
   cookiereference = '0'
   cookie = Cookie.SimpleCookie()
   gusername = ""
   loginhtml = ""



