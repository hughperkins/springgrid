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

import md5

import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import backref, relation

from utils import *
import loginhelper

Base = sqlalchemy.ext.declarative.declarative_base()

class Map(Base):
   __tablename__ = 'maps'

   map_id =Column(Integer,primary_key=True)
   map_name = Column(String(255))
   map_archivechecksum = Column(String(255))
   map_url = Column(String(255))

class Mod(Base):
   __tablename__ = 'mods'

   mod_id =Column(Integer,primary_key=True)
   mod_name = Column(String(255))
   mod_archivechecksum = Column(String(255))
   mod_url = Column(String(255))

class Role(Base):
   __tablename__ = 'roles'

   def __init__(self, role_name ):
      self.role_name = role_name

   role_id = Column(Integer,primary_key=True)
   role_name = Column(String(255))

class RoleMember(Base):
   __tablename__ = 'role_members'

   role_id = Column(Integer,ForeignKey('roles.role_id'),primary_key=True)
   account_id = Column(Integer,ForeignKey('accounts.account_id'),primary_key=True)

   role = relation("Role")

   def __init__(self, role ):
      self.role = role

class Account(Base):
   __tablename__ = 'accounts'

   account_id = Column(Integer,primary_key=True)
   username = Column(String(255))
   userfullname = Column(String(255))
   useremailaddress = Column(String(255))
   passwordsalt = Column(String(255))
   passwordhash = Column(String(255))

   roles = relation("RoleMember")

   def __init__(self, username, userfullname, password ):
      self.username = username
      self.userfullname = userfullname

      self.passwordsalt = loginhelper.createSalt()
      self.passwordhash = md5.md5( password + self.passwordsalt ).hexdigest()

   def checkPassword( self, password ):
      return ( md5.md5( password + self.passwordsalt ).hexdigest() == self.passwordhash )

   def changePassword( self, newpassword ):
      self.passwordsalt = loginhelper.createSalt()
      self.passwordhash = md5.md5( newpassword + self.passwordsalt ).hexdigest()

   def addRole( self, role ):
      rolemember = RoleMember( role )
      self.roles.append(rolemember)

class AI(Base):
   __tablename__ = 'ais'

   ai_id = Column(Integer,primary_key=True)
   ai_name = Column(String(255))
   ai_version = Column(String(255))
   ai_downloadurl = Column(String(255))
   ai_owneraccount_id = Column(Integer,ForeignKey('accounts.account_id'))

   allowedmaps = relation("AIAllowedMap")
   allowedmods = relation("AIAllowedMod")
   allowedoptions = relation("AIAllowedOption")

   owneraccount = relation("Account")

class AIAllowedMap(Base):
   __tablename__ = 'ai_allowedmaps'

   ai_id = Column(Integer,ForeignKey('ais.ai_id'),primary_key=True)
   map_id = Column(Integer,ForeignKey('maps.map_id'),primary_key=True)

   ai = relation("AI")
   map = relation("Map")

class AIAllowedMod(Base):
   __tablename__ = 'ai_allowedmods'

   ai_id = Column(Integer,ForeignKey('ais.ai_id'),primary_key=True)
   mod_id = Column(Integer,ForeignKey('mods.mod_id'),primary_key=True)

   ai = relation("AI")
   mod = relation("Mod")

class AIAllowedOption(Base):
   __tablename__ = 'ai_allowedoptions'

   ai_id = Column(Integer,ForeignKey('ais.ai_id'),primary_key=True)
   option_id = Column(Integer,ForeignKey('aioptions.option_id'),primary_key=True)

   ai = relation("AI")
   option = relation("AIOption")

class Cookie(Base):
   __tablename__ = 'cookies'

   def __init__( self, cookiereference, account ):
      self.cookiereference = cookiereference
      self.account = account

   cookiereference = Column(String(255),primary_key=True)
   #username = Column(String(255))
   # we can change to use account_id in the future
   account_id = Column(Integer,ForeignKey('accounts.account_id'))

   account = relation("Account")

class BotRunnerOption(Base):
   __tablename__ = 'botrunner_options'

   botrunner_option_id = Column(Integer,primary_key=True)
   botrunner_option_name = Column(String(255))

class BotRunnerSupportedMap(Base):
   __tablename__ = 'botrunner_supportedmaps'

   botrunner_id = Column(Integer,ForeignKey('botrunners.botrunner_id'),primary_key=True)
   map_id = Column(Integer,ForeignKey('maps.map_id'),primary_key=True)

   botrunner = relation("BotRunner")
   map = relation("Map")

class BotRunnerSupportedMod(Base):
   __tablename__ = 'botrunner_supportedmods'

   botrunner_id = Column(Integer,ForeignKey('botrunners.botrunner_id'),primary_key=True)
   mod_id = Column(Integer,ForeignKey('mods.mod_id'),primary_key=True)

   botrunner = relation("BotRunner")
   mod = relation("Mod")

class BotRunnerAssignedOption(Base):
   __tablename__ = 'botrunner_assignedoptions'

   botrunner_id = Column(Integer,ForeignKey('botrunners.botrunner_id'),primary_key=True)
   botrunner_option_id = Column(Integer,ForeignKey('botrunner_options.botrunner_option_id'),primary_key=True)

   option = relation("BotRunnerOption")

class BotRunner(Base):
   __tablename__ = 'botrunners'

   botrunner_id = Column(Integer,primary_key=True)
   botrunner_name = Column(String(255))
   botrunner_sharedsecret = Column(String(255))
   botrunner_lastpingtime = Column(String(255))
   botrunner_lastpingstatus = Column(String(255))
   botrunner_owneraccountid = Column(Integer, ForeignKey('accounts.account_id') )

   owneraccount = relation("Account")
   options = relation("BotRunnerAssignedOption")

class AIOption(Base):
   __tablename__ = 'aioptions'

   option_id = Column(Integer,primary_key=True)
   option_name = Column(String(255))

   def __init__(self, option_name):
      self.option_name = option_name

class MatchRequestOption(Base):
   __tablename__ = 'matchrequest_options'

   matchrequest_id = Column(Integer,ForeignKey('matchrequestqueue.matchrequest_id'), primary_key=True)
   option_id = Column(Integer,ForeignKey('aioptions.option_id'),primary_key=True)

   option = relation("AIOption")

class MatchRequest(Base):
   __tablename__ = 'matchrequestqueue'

   matchrequest_id=Column(Integer,primary_key=True)
   map_id =Column(Integer, ForeignKey('maps.map_id'))
   mod_id =Column(Integer, ForeignKey('mods.mod_id'))
   ai0_id = Column(Integer, ForeignKey('ais.ai_id'))
   ai1_id = Column(Integer, ForeignKey('ais.ai_id'))

   map = relation("Map" )
   mod = relation("Mod" )
   ai0 = relation("AI", primaryjoin = ai0_id == AI.ai_id )
   ai1 = relation("AI", primaryjoin = ai1_id == AI.ai_id )

   options = relation("MatchRequestOption")

class MatchRequestInProgress(Base):
   __tablename__ = 'matchrequests_inprogress'

   matchrequest_id = Column(Integer,ForeignKey('matchrequestqueue.matchrequest_id'),primary_key=True )
   botrunner_id = Column(Integer,ForeignKey('botrunners.botrunner_id'))
   datetimeassigned = Column(String(255))

   matchrequest = relation("MatchRequest", backref=backref('matchrequestinprogress', uselist=False))
   botrunner= relation("BotRunner")

class MatchResult(Base):
   __tablename__ = 'matchresults'

   matchrequest_id = Column(Integer,ForeignKey('matchrequestqueue.matchrequest_id'),primary_key=True )
   matchresult = Column(String(255))
   matchrequest = relation("MatchRequest", backref=backref('matchresult', uselist=False))

class League(Base):
   __tablename__ = 'leagues'

   league_id = Column(Integer,primary_key = True )
   league_name = Column(String(255))
   league_creatorid = Column(Integer,ForeignKey('accounts.account_id'))
   map_id = Column(Integer,ForeignKey('maps.map_id'))
   mod_id = Column(Integer,ForeignKey('mods.mod_id'))

   creator = relation("Account")
   map = relation("Map")
   mod = relation("Mod")

class LeagueOption(Base):
   __tablename__ = 'leagueoptions'

   league_id = Column(Integer,ForeignKey('leagues.league_id'),primary_key=True)
   option_id = Column(Integer,ForeignKey('aioptions.option_id'),primary_key=True)

   league = relation("League", backref='options')
   option = relation("AIOption")

class LeagueGroup(Base):
   __tablename__ = 'leaguegroups'

   leaguegroup_id = Column(Integer,primary_key = True)
   leaguegroup_name = Column(String(255))
   leaguegroup_creatorid = Column(Integer,ForeignKey("accounts.account_id"))
   
   creator = relation("Account")

# members who are leaguegruops
class LeagueGroupLeagueMember(Base):
   __tablename__ = 'leaguegroup_leaguemembers'

   leaguegroup_id = Column(Integer,ForeignKey('leaguegroups.leaguegroup_id'),primary_key = True)
   league_id = Column(Integer,ForeignKey('leagues.league_id'),primary_key = True)

   leaguegroup = relation("LeagueGroup", backref="leaguemembers")
   league = relation("League")

# members who are leagues (leaf nodes)
def LeagueGroupLeagueGroupMember(Base):
   __tablename__ = 'leaguegroup_leaguegroupmembers'

   leaguegroup_id = Column(Integer,ForeignKey('leaguegroups.leaguegroup_id'),primary_key = True)
   childleaguegroup_id = Column(Integer,ForeignKey('leaguegroups.leaguegroup_id'),primary_key=True)

   leaguegroup = relation("LeagueGroup", backref="leaguemembers", primaryjoin = leaguegroup_id == LeagueGroup.leaguegroup_id )
   childleaguegroup = relation("LeagueGroup", backref="leaguegroupmembers", primaryjoin = childleaguegroup_id == LeagueGroup.leaguegroup_id)

def addstaticdata(session):
   # maybe roles static data could be created by core/roles.py?
   # anyway, for now... :
   accountadminrole = Role("accountadmin")
   aiadminrole = Role("aiadmin")
   modadminrole = Role("modadmin")
   mapadminrole = Role("mapadmin")
   leagueadminrole = Role("leagueadmin")

   session.add(accountadminrole)
   session.add(aiadminrole)
   session.add(modadminrole)
   session.add(mapadminrole)
   session.add(leagueadminrole)

   account = Account("admin","admin", "admin")
   session.add(account)
   account.addRole( accountadminrole )
   account.addRole( aiadminrole )
   account.addRole( modadminrole )
   account.addRole( mapadminrole )
   account.addRole( leagueadminrole )

   session.add(Account("guest","guest","guest"))

   aioption_cheatingequalslose = AIOption('cheatingequalslose')
   aioption_cheatingallowed = AIOption('cheatingallowed')
   aioption_dummymatch = AIOption('dummymatch')
   session.add(aioption_cheatingequalslose)
   session.add(aioption_cheatingallowed)
   session.add(aioption_dummymatch)

def createall(engine):
   Base.metadata.create_all(engine)

def dropall(engine):
   Base.metadata.drop_all(engine)



