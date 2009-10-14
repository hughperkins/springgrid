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

import os
import sys

from utils import *

scriptdir = os.path.dirname( os.path.realpath( __file__ ) )

# returns list of exceptions
def adddata(user,name,dbname,dbhost):
   exceptions = []
   for sqlfilename in os.listdir(scriptdir):
      if sqlfilename.find(".sql") != -1:
         #print sqlfilename
         #filecontents = filehelper.readFile( scriptdir + "/" + sqlfilename )
         try:
            dbconnection.executesqlfile(scriptdir + "/" + sqlfilename)
            #dbconnection.cursor.execute( filecontents )
         except:
            # just print, and carry on
            exceptions.append( str( sys.exc_value ) )
            # print "Exception: " + str( sys.exc_value )
         dbconnection.nextAllSets(dbconnection.cursor)
   return exceptions         

def usage():
   print "Usage: " + sys.argv[0] + " username password dbname dbhostname"

def main():
   if len( sys.argv) < 6:
      usage()
      return
   username = sys.argv[1]
   password = sys.argv[2]
   dbname = sys.argv[3]
   hostname = sys.argv[4]

if __name__ == '__main__':
   print "Not supported, please cd into website and run python websetupdb.py"
   # main()

