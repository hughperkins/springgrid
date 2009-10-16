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
import sqlalchemysetup
from tableclasses import *
import botrunnerhelper

# returns True if exists, or added ok, otherwise False
def addmodifdoesntexist(modname, modarchivechecksum):
   mod = sqlalchemysetup.session.query(Map).filter(Map.mod_name == modname ).first()
   if mod == None:
      try:
         mod = Map( modname, modarchivechecksum )
         sqlalchemysetup.session.add(mod)
         sqlalchemysetup.session.commit()
      except:
         return(False, "error adding to db: " + str( sys.exc_value ) )

      return (True,'')

   if mod.mod_archivechecksum != modarchivechecksum:
      return (False,"mod archive checksum doesn't match the one already on the website.")

   return (True,'')

def getmod( modname ):
   return sqlalchemysetup.session.query(Map).filter(Map.mod_name == modname ).first()

# return list of supported modnames
def getsupportedmods( botrunnername ):
   botrunner = sqlalchemysetup.session.query(BotRunner).filter(BotRunner.botrunner_name == botrunnername ).first()
   if botrunner == None:
      return []
   if botrunner.supportedmods == None:
      return []
   supportedmodnames = []
   for mod in botrunner.supportedmods:
      supportedmodnames.append(mod.mod.mod_name)
   return supportedmodnames

def setbotrunnersupportsthismod( botrunnername, modname ):
   # Now, register the mod as supported mod
   botrunner = botrunnerhelper.getbotrunner( botrunnername )
   mod = getmod(modname)
   botrunner.supportedmods.append(BotRunnerSupportedMap(mod))
   sqlalchemysetup.session.commit()
   return (True,'')

