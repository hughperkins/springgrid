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

scriptdir = os.path.dirname( os.path.realpath( __file__ ) )

def createall(user,password,dbname,dbhost):
   sys.path.append(scriptdir + "/tables")
   import dbtables
   dbtables.createtables(user,password,dbname,dbhost)

   sys.path.append(scriptdir + "/staticdata")
   import dbstaticdata
   dbstaticdata.adddata(user,password,dbname,dbhost)

def dropall(user,password,dbname,dbhost):
   sys.path.append(scriptdir + "/tables")
   import dbtables
   dbtables.droptables(user,password,dbname,dbhost)

def main():
   print "Not supported, please cd into website and run python websetupdb.py"
   return

   if len(sys.argv) < 4:
      print "Usage: createall.py user password databasename hostname"
      sys.exit(1)
   user=sys.argv[1]
   password=sys.argv[2]
   dbname=sys.argv[3]
   dbhost=sys.argv[4]

   createall(user,password,dbname,dbhost)

if __name__ == '__main__':
   main()   


