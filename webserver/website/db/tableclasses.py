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

import sqlalchemy
import sqlalchemy.ext.declarative
import sqlalchemy.orm

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import backref, relation

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

class AI(Base):
   __tablename__ = 'ais'

   ai_id = Column(Integer,primary_key=True)
   ai_name = Column(String(255))
   ai_version = Column(String(255))

class Account(Base):
   __tablename__ = 'accounts'

   account_id = Column(Integer,primary_key=True)
   username = Column(String(255))
   userfullname = Column(String(255))
   useremailaddress = Column(String(255))
   passwordsalt = Column(String(255))
   passwordhash = Column(String(255))

class BotRunner(Base):
   __tablename__ = 'botrunners'

   botrunner_id = Column(Integer,primary_key=True)
   botrunner_name = Column(String(255))
   botrunner_sharedsecret = Column(String(255))
   botrunner_lastpingtime = Column(String(255))
   botrunner_lastpingstatus = Column(String(255))
   botrunner_owneraccountid = Column(Integer, ForeignKey('accounts.account_id') )

   owneraccount = relation("Account")

class AIOption(Base):
   __tablename__ = 'aioptions'

   option_id = Column(Integer,primary_key=True)
   option_name = Column(String(255))

class MatchRequestOption(Base):
   __tablename__ = 'matchrequest_options'

   matchrequest_id = Column(Integer,ForeignKey('matchrequestqueue.matchrequest_id'), primary_key=True)
   option_id = Column(Integer,ForeignKey('aioptions.option_id'))

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

def createall():
   Base.metadata.create_all(engine)



