import os
import sys
from openid.consumer import consumer
from openid.store import sqlstore

def createtables(engine):
   sqlalchemyconnection = engine.connect()
   getstore( sqlalchemyconnection ).createTables()
   sqlalchemyconnection.close()

def droptables(engine):
   sqlalchemyconnection = engine.connect()
   try:
      sqlalchemyconnection.connection.connection.query('drop table ' + getassociationstablename() )
   except:
      pass
   try:
      sqlalchemyconnection.connection.connection.query('drop table ' + getnoncestablename() )
   except:
      pass
   sqlalchemyconnection.close()

def getassociationstablename():
   return 'openid_associations'

def getnoncestablename():
   return 'openid_nonces'

def getstore( sqlalchemyconnection ):
   return sqlstore.MySQLStore( sqlalchemyconnection.connection.connection, associations_table=getassociationstablename(), nonces_table = getnoncestablename() )

