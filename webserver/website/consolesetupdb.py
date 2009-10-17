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

import sys
import os

from core import sqlalchemysetup

scriptdir = os.path.dirname( os.path.realpath( __file__ ) )

def create():
   print "creating all..."
   sqlalchemysetup.createalltables()

def drop():
   print "dropping all..."
   sqlalchemysetup.dropalltables()

def usage():
   print "Usage: " + sys.argv[0] + " username password dbname dbhostname [create|drop]"

setupdb = None

def main():
   global setupdb
   if len( sys.argv) < 6:
      usage()
      return
   username = sys.argv[1]
   password = sys.argv[2]
   dbname = sys.argv[3]
   hostname = sys.argv[4]
   action = sys.argv[5]

   if action == 'create':
      sqlalchemysetup.setupwithcredentials('mysql', username, password, hostname, dbname )
      create()
      sqlalchemysetup.close()
   elif action == 'drop':
      sqlalchemysetup.setupwithcredentials('mysql', username, password, hostname, dbname )
      drop()
      sqlalchemysetup.close()
   elif action == 'reload':
      sqlalchemysetup.setupwithcredentials('mysql', username, password, hostname, dbname )
      drop()
      create()
      sqlalchemysetup.close()
   else:
      usage()

if __name__ == '__main__':
   main()

