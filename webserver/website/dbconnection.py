
import sys
import os
import MySQLdb

import config

connection = None
cursor = None

def connectdb():
   global connection, cursor
   connection = MySQLdb.connect( host = config.dbhost,
     user = config.dbuser,
     passwd = config.dbpassword,
     db = config.dbname )
   cursor = connection.cursor()
   return cursor

def disconnectdb():
   cursor.close()
   connection.close()

