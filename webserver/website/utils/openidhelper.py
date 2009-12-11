import os
import sys
from openid.consumer import consumer
from openid.store import sqlstore

def createtables(engine):
   sqlalchemyconnection = engine.connect()
   getstore( engine, sqlalchemyconnection ).createTables()
   sqlalchemyconnection.close()

def droptables(engine):
   sqlalchemyconnection = engine.connect()
   try:
      # sqlalchemyconnection.connection.connection.query('drop table ' + getassociationstablename() )
      sqlalchemyconnection.connection.cursor().execute('drop table ' + getassociationstablename() )
   except:
      pass
   try:
      sqlalchemyconnection.connection.cursor().execute('drop table ' + getnoncestablename() )
   except:
      pass
   # sqlalchemyconnection.commit()
   sqlalchemyconnection.connection.commit()
   sqlalchemyconnection.close()

def getassociationstablename():
   return 'openid_associations'

def getnoncestablename():
   return 'openid_nonces'

def getstore( engine, sqlalchemyconnection ):
   if engine.name == 'postgres':
      return sqlstore.PostgreSQLStore( sqlalchemyconnection.connection.connection, associations_table=getassociationstablename(), nonces_table = getnoncestablename() )
   if engine.name == 'mysql':
      return sqlstore.MySQLStore( sqlalchemyconnection.connection.connection, associations_table=getassociationstablename(), nonces_table = getnoncestablename() )

   return sqlstore.SQLiteStore( sqlalchemyconnection.connection.connection, associations_table=getassociationstablename(), nonces_table = getnoncestablename() )

