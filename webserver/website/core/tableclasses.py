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

from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, and_, schema, Table, UniqueConstraint
from sqlalchemy.orm import backref, relation

from utils import *
import loginhelper

Base = sqlalchemy.ext.declarative.declarative_base()

class Map(Base):
   __tablename__ = 'maps'

   map_id = Column(Integer,primary_key=True)
   map_name = Column(String(255), unique = True)
   map_archivechecksum = Column(String(255))
   map_url = Column(String(255))

   def __init__(self, map_name ):
      self.map_name = map_name

class Mod(Base):
   __tablename__ = 'mods'

   mod_id =Column(Integer,primary_key=True)
   mod_name = Column(String(255), unique = True)
   mod_archivechecksum = Column(String(255))
   mod_url = Column(String(255))

   def __init__(self, mod_name ):
      self.mod_name = mod_name

account_roles = Table('role_members', Base.metadata,
   Column('role_id', Integer,ForeignKey('roles.role_id'),nullable=False),
   Column('account_id', Integer,ForeignKey('accounts.account_id'),nullable=False),
   UniqueConstraint('role_id','account_id')
)

class Role(Base):
   __tablename__ = 'roles'

   def __init__(self, role_name ):
      self.role_name = role_name

   role_id = Column(Integer,primary_key=True)
   role_name = Column(String(255), unique = True, nullable = False)

class OpenID(Base):
   __tablename__ = 'openids'

   account_id = Column(Integer, ForeignKey('accounts.account_id'), primary_key = True)
   openid = Column(String(255), primary_key = True)

   def __init__( self, openid ):
      self.openid = openid

class PasswordInfo(Base):
   __tablename__ = 'passwords'

   account_id = Column(Integer, ForeignKey('accounts.account_id'), primary_key = True)
   passwordsalt = Column(String(255), nullable = False)
   passwordhash = Column(String(255), nullable = False)

   def __init__(self, password ):
      self.passwordsalt = loginhelper.createSalt()
      self.passwordhash = md5.md5( password + self.passwordsalt ).hexdigest()

   def checkPassword( self, password ):
      return ( md5.md5( password + self.passwordsalt ).hexdigest() == self.passwordhash )

   def changePassword( self, newpassword ):
      self.passwordsalt = loginhelper.createSalt()
      self.passwordhash = md5.md5( newpassword + self.passwordsalt ).hexdigest()

class Account(Base):
   __tablename__ = 'accounts'

   account_id = Column(Integer,primary_key=True)
   username = Column(String(255), unique = True, nullable = False)
   userfullname = Column(String(255))
   useremailaddress = Column(String(255))

   roles = relation("Role", secondary = account_roles )
   passwordinfo = relation('PasswordInfo', uselist = False)
   openids = relation('OpenID')

   def __init__(self, username, userfullname ):
      self.username = username
      self.userfullname = userfullname

   def addRole( self, role ):
      self.roles.append(role)

ai_allowedmaps = Table( 'ai_allowedmaps', Base.metadata,
   Column('ai_id', Integer,ForeignKey('ais.ai_id'),nullable = False),
    Column('map_id', Integer,ForeignKey('maps.map_id'),nullable = False),
   UniqueConstraint( 'ai_id', 'map_id' )
)

ai_allowedmods = Table( 'ai_allowedmods', Base.metadata,
   Column('ai_id', Integer,ForeignKey('ais.ai_id'),nullable = False),
   Column('mod_id', Integer,ForeignKey('mods.mod_id'),nullable = False),
   UniqueConstraint( 'ai_id', 'mod_id' )
)

ai_allowedoptions = Table('ai_allowedoptions', Base.metadata,
   Column('ai_id', Integer, ForeignKey('ais.ai_id'),nullable = False ),
   Column('option_id',Integer,ForeignKey('aioptions.option_id'),nullable = False),
   UniqueConstraint('ai_id', 'option_id')
)

class AI(Base):
   __tablename__ = 'ais'

   ai_id = Column(Integer,primary_key=True)
   ai_name = Column(String(64), nullable = False)
   ai_version = Column(String(64), nullable = False)
   ai_downloadurl = Column(String(255))
   ai_needscompiling = Column(Boolean )
   ai_owneraccount_id = Column(Integer,ForeignKey('accounts.account_id'))

   __table_args__ = (schema.UniqueConstraint('ai_name','ai_version'), {} )

   allowedmaps = relation("Map", secondary = ai_allowedmaps )
   allowedmods = relation("Mod", secondary = ai_allowedmods )
   allowedoptions = relation("AIOption", secondary = ai_allowedoptions)

   owneraccount = relation("Account")

   def __init__( self, ai_name, ai_version ):
      self.ai_name = ai_name
      self.ai_version = ai_version
      self.needscompiling = True

class Cookie(Base):
   __tablename__ = 'cookies'

   def __init__( self, cookiereference, account ):
      self.cookiereference = cookiereference
      self.account = account

   cookiereference = Column(String(255),primary_key=True)
   #username = Column(String(255))
   # we can change to use account_id in the future
   account_id = Column(Integer,ForeignKey('accounts.account_id'), nullable = False)

   account = relation("Account")

botrunner_supportedmaps = Table( 'botrunner_supportedmaps', Base.metadata,
   Column('botrunner_id', Integer,ForeignKey('botrunners.botrunner_id'),nullable = False),
   Column('map_id', Integer,ForeignKey('maps.map_id'),nullable = False),
   UniqueConstraint('botrunner_id', 'map_id' )
)

botrunner_supportedmods = Table( 'botrunner_supportedmods', Base.metadata,
   Column('botrunner_id', Integer,ForeignKey('botrunners.botrunner_id'),nullable = False),
   Column('mod_id', Integer,ForeignKey('mods.mod_id'),nullable = False),
   UniqueConstraint('botrunner_id', 'mod_id' )
)

botrunner_supportedais = Table( 'botrunner_supportedais', Base.metadata,
   Column('botrunner_id', Integer,ForeignKey('botrunners.botrunner_id'), nullable = False),
   Column('ai_id', Integer,ForeignKey('ais.ai_id'), nullable = False ),
   UniqueConstraint('botrunner_id', 'ai_id' )
)

botrunner_assignedoptions = Table( 'botrunner_assignedoptions', Base.metadata,
   Column('botrunner_id',Integer,ForeignKey('botrunners.botrunner_id'),nullable = False),
   Column('botrunner_option_id',Integer,ForeignKey('aioptions.option_id'),nullable = False),
   UniqueConstraint('botrunner_id','botrunner_option_id')
)

class BotRunnerSession(Base):
   __tablename__ = 'botrunner_sessions'

   botrunner_id = Column(Integer,ForeignKey('botrunners.botrunner_id'), primary_key = True )
   botrunner_session_id = Column(String(255), primary_key = True)
   lastpingstatus = Column(String(255), nullable = False)
   lastpingtime = Column(String(255), nullable = False)
   downloadingai_id = Column(Integer,ForeignKey('ais.ai_id'), nullable = True)

   downloadingai = relation("AI")  # keep track of any ai being downloaded by this session

   def __init__(self, botrunner_session_id ):
      self.botrunner_session_id = botrunner_session_id

      self.pingtimeok = False # used by viewbotrunners.py
      self.lastpingtimestring = '' # used by viewbotrunners.py

class BotRunner(Base):
   __tablename__ = 'botrunners'

   botrunner_id = Column(Integer,primary_key=True)
   botrunner_name = Column(String(255), unique = True, nullable = False)
   botrunner_sharedsecret = Column(String(255), nullable = False)
   botrunner_owneraccountid = Column(Integer, ForeignKey('accounts.account_id') )
   rowspan = 0 # used by viewbotrunners.py

   owneraccount = relation("Account")
   options = relation("AIOption", secondary = botrunner_assignedoptions )
   supportedmaps = relation("Map", secondary = botrunner_supportedmaps )
   supportedmods = relation("Mod", secondary = botrunner_supportedmods )
   supportedais = relation("AI", secondary = botrunner_supportedais )
   sessions = relation("BotRunnerSession",uselist = True)

   rowspan = 0

   def __init__( self, botrunner_name, botrunner_sharedsecret ):
      self.botrunner_name = botrunner_name
      self.botrunner_sharedsecret = botrunner_sharedsecret

class AIOption(Base):
   __tablename__ = 'aioptions'

   option_id = Column(Integer,primary_key=True)
   option_name = Column(String(255), unique = True, nullable = False)

   def __init__(self, option_name):
      self.option_name = option_name

matchrequest_options = Table( 'matchrequest_options', Base.metadata,
   Column('matchrequest_id', Integer,ForeignKey('matchrequestqueue.matchrequest_id'), nullable = False),
   Column('option_id',Integer,ForeignKey('aioptions.option_id'),nullable = False),
   UniqueConstraint('matchrequest_id', 'option_id' )
)

class MatchRequest(Base):
   __tablename__ = 'matchrequestqueue'

   matchrequest_id=Column(Integer,primary_key=True)
   map_id =Column(Integer, ForeignKey('maps.map_id'), nullable = False)
   mod_id =Column(Integer, ForeignKey('mods.mod_id'), nullable = False)
   ai0_id = Column(Integer, ForeignKey('ais.ai_id'), nullable = False)
   ai1_id = Column(Integer, ForeignKey('ais.ai_id'), nullable = False)

   map = relation("Map" )
   mod = relation("Mod" )
   ai0 = relation("AI", primaryjoin = ai0_id == AI.ai_id )
   ai1 = relation("AI", primaryjoin = ai1_id == AI.ai_id )

   matchrequestinprogress = relation("MatchRequestInProgress", uselist=False)
   matchresult = relation("MatchResult", uselist=False)
   options = relation("AIOption", secondary = matchrequest_options )

   def __init__( self, ai0, ai1, map, mod, league = None ):
      self.ai0 = ai0
      self.ai1 = ai1
      self.map = map
      self.mod = mod

class MatchRequestInProgress(Base):
   __tablename__ = 'matchrequests_inprogress'

   matchrequest_id = Column(Integer,ForeignKey('matchrequestqueue.matchrequest_id'),primary_key=True )
   botrunner_id = Column(Integer,ForeignKey('botrunners.botrunner_id'),ForeignKey('botrunner_sessions.botrunner_id'), nullable = False)
   botrunner_session_id = Column(String(255),ForeignKey('botrunner_sessions.botrunner_session_id'), nullable = False)
   datetimeassigned = Column(String(255), nullable = False)

   botrunner= relation("BotRunner")
   botrunnersession = relation("BotRunnerSession", primaryjoin=and_( botrunner_id == BotRunnerSession.botrunner_id, botrunner_session_id == BotRunnerSession.botrunner_session_id ) )

   def __init__(self, botrunner, botrunnersession, datetimeassigned ):
      self.botrunner = botrunner
      self.botrunnersession = botrunnersession
      self.datetimeassigned = datetimeassigned

class MatchResult(Base):
   __tablename__ = 'matchresults'

   matchrequest_id = Column(Integer,ForeignKey('matchrequestqueue.matchrequest_id'),primary_key=True )
   matchresult = Column(String(255), nullable = False)

   def __init__(self, matchresult ):
      self.matchresult = matchresult

# simple flat config for now
class Config(Base):
   __tablename__ = 'config'

   config_key = Column(String(255),primary_key = True )
   config_value = Column(String(255), nullable = False)
   config_type = Column(String(255), nullable = False)

   # sets value of config_type appropriately, according to config_value type
   # to int, float, string or boolean
   def __init__(self, config_key, config_value ):
      self.config_key = config_key
      self.setValue( config_value )

   def setValue( self, config_value ):
      self.config_value = str(config_value)
      if type(config_value) == int:
         self.config_type = 'int'
      elif type(config_value) == float:
         self.config_type = 'float'
      elif type(config_value) == str:
         self.config_type = 'string'
      elif type(config_value) == bool:
         self.config_type = 'boolean'

   # returns config_value converted into appropriate type, according t o value of config_type
   def getValue(self):
      if self.config_type == 'int':
         return int(self.config_value)
      if self.config_type == 'float':
         return float(self.config_value)
      if self.config_type == 'string':
         return self.config_value
      if self.config_type == 'boolean':
         if self.config_value.lower() == 'true':
            return True
         return False
      
def addstaticdata(session):
   import confighelper # have to import it here, otherwise Config table can't be easily
                       # imported inside confighelper, because circular import loop
   confighelper.applydefaults()

   import roles
   roles.addstaticdata()
   account = Account("admin","admin" )
   account.passwordinfo = PasswordInfo('admin')
   session.add(account)
   account.addRole( roles.getRole('accountadmin') )
   account.addRole( roles.getRole('aiadmin') )
   account.addRole( roles.getRole('mapadmin') )
   account.addRole( roles.getRole('modadmin') )
   account.addRole( roles.getRole('leagueadmin') )
   account.addRole( roles.getRole('botrunneradmin') )
   account.addRole( roles.getRole('requestadmin') )

   # session.add(Account("guest","guest","guest"))

   aioption_cheatingequalslose = AIOption('cheatingequalslose')
   aioption_cheatingallowed = AIOption('cheatingallowed')
   aioption_dummymatch = AIOption('dummymatch')
   session.add(aioption_cheatingequalslose)
   session.add(aioption_cheatingallowed)
   session.add(aioption_dummymatch)

   # add a couple of default mods/maps/ais:
   map = Map( 'SmallDivide.sd7')
   map.map_url = 'http://spring-portal.com/index.php/docman/doc_download/104-smalldivide'
   session.add(map)

   mod = Mod('Balanced Annihilation v7.04')
   mod.mod_url = 'http://spring-portal.com/index.php/docman/doc_details/314-balanced-annihilation-v704'
   session.add(mod)

   ai = AI('E323AI','2.83')
   ai.ai_download_url = 'http://github.com/Error323/E323AI/tarball/v2.83'
   ai.ai_needscompiling = True
   session.add(ai)

def createall(engine):
   Base.metadata.create_all(engine)
   openidhelper.createtables(engine)

def dropall(engine):
   Base.metadata.drop_all(engine)
   openidhelper.droptables(engine)



