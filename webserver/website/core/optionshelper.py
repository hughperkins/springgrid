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

# manages options

from sqlalchemy.orm import join

from utils import *
import loginhelper
import tableclasses
import sqlalchemysetup
from tableclasses import *

optionnames = [ 'instancelocaldata', 'dummymatch' ]

# adds any missing options to the table, can be called as many times as you like
def addstaticdata():
   global optionnames

   optionrows = sqlalchemysetup.session.query(AIOption).all()
   for optionname in optionnames:
      optionfound = False
      for optionrow in optionrows:
         if optionrow.option_name == optionname:
            optionfound = True
      if not optionfound:
         option = AIOption( optionname )
         sqlalchemysetup.session.add(option)
         sqlalchemysetup.session.flush()

# returns AIOption object using sqlalchemy
def getOption( optionname ):
   global optionnames
   addstaticdata()
   if optionname not in optionnames:
      raise Exception("Invalid option name " + optionnaame )
   return sqlalchemysetup.session.query(AIOption).filter(AIOption.option_name == optionname ).first()

# in:
# - options is a list of option objects to search
# - option is an option object to search for
# returns true if option found in options
def containsOption(option, options):
   if option == None:
      raise Exception( "ERROR: no option specified" )

   for thisoption in options:
      if thisoption.option_name == option.option_name:
         return True
   return False

# self test function
def test():
   pass

# running as main doesn't work for me (yet?) because the import
# doesn't work.  If someone has the solution?
if __name__ == '__main__':
   test()




