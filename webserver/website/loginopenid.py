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

# handles user login

import cgitb; cgitb.enable()
import cgi
import os
import sys
import urlparse

from utils import *
from core import *

import openid
from openid.consumer import consumer
from openid.store import sqlstore

sqlalchemysetup.setup()

def go():
   openidurl = formhelper.getValue('openidurl')

   mystore = sqlstore.MySQLStore( sqlalchemysetup.session.connection().connection.connection, associations_table='openid_associations', nonces_table = 'openid_nonces' )

   sessiondata = {}
   myconsumer = consumer.Consumer( sessiondata, mystore)
   fullpagewebpath = 'http://' + os.getenv('HTTP_HOST') + os.getenv('REQUEST_URI')

   if formhelper.getValue('openid.claimed_id') == None:
      if openidurl == None or openidurl == '':  # user didn't enter an id
         jinjahelper.rendertemplate('genericmessage.html', message = 'Logon error: Please fill in the openid field, and try again.' )
         return

      # user entered an id, so send a request to openid provider
      myrequest = myconsumer.begin( openidurl )

      # print redirect to openid provider page
      print "Content-type: text/html"
      print "Location: " + myrequest.redirectURL(os.path.dirname( fullpagewebpath ),fullpagewebpath )
      print '\n\n'
      return

   # in theory, we arrived here from the openid provider page redirect
   # get query string dict from openid provider redirect:
   _querystringdict = urlparse.parse_qs(os.getenv("QUERY_STRING"))
   querystringdict = {}
   for key in _querystringdict.keys():
      querystringdict[key] = _querystringdict[key][0]

   # get openid auth result:
   result = myconsumer.complete(querystringdict, fullpagewebpath )
      
   if result.__class__ != openid.consumer.consumer.SuccessResponse:
      jinjahelper.message('OpenID failed authentication.  Please check and try again.')
      return

   openidurl = result.identity_url.split('/')[2]
   loginhelper.logonUserWithAuthenticatedOpenID( openidurl )
   jinjahelper.rendertemplate('login.html', message = 'Logged on ok as ' + openidurl, menus = menu.getmenus(), headers = loginhelper.cookie.output() )

try:
   go()
finally:
   sqlalchemysetup.close()


