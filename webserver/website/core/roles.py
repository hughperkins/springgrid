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

# manages roles

from utils import *

# returns if the logged-in user is in the named role
def isInRole(rolename):
   if not loginhelper.isLoggedOn():
      return False
   username = loginhelper.getUsername()
   return isInRole( username, rolename )

# This is slightly easier to test, so factor it out:
def isInRole(username, rolename):
   rows = dbconnection.cursor.execute("select role_name "\
      " from role_members, accounts, roles "\
      " where role_name = %s "\
      " and username = %s "\
      " and roles.role_id = role_members.role_id "\
      " and accounts.account_id = role_members.account_id ",
      ( rolename, username, ) )
   return ( rows == 1 )

def test():
   # This supposes original static data is in the db
   if not tester.testBoolean('check if admin is accountadmin', isInRole( 'admin', 'accountadmin'), True ):
      return
   if not tester.testBoolean('check if guest is accountadmin', isInRole( 'guest', 'accountadmin'), False ):
      return
   print "PASS"

# running as main doesn't work for me (yet?) because the import
# doesn't work.  If someone has the solution?
if __name__ == '__main__':
   test()


