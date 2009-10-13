# Copyright Hugh Perkins 2004, 2009
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
import MySQLdb

import filehelper

try:
   import config
except:
   pass
   # Just ignore, but it means we haven't been configured yet
   #print "Warning: config file not found"

connection = None
cursor = None
dictcursor = None # This should probably be your cursor of choice...

def connectdbwiththesecredentials( dbuser, dbpassword, dbname, dbhost ):
   global connection, cursor, dictcursor
   connection = MySQLdb.connect( host = dbhost,
     user = dbuser,
     passwd = dbpassword,
     db = dbname )
   cursor = connection.cursor()
   dictcursor = connection.cursor(MySQLdb.cursors.DictCursor)
   return cursor

def executesqlfile(sqlfilepath):
   global dictcursor
   #first load file, then remove any bits of lines from '#' onwards, then join together
   # then split on the ";" then execute each bit one by one
   sqlcontents = filehelper.readFile(sqlfilepath)
   sqllines = sqlcontents.split("\n")
   sqlwithoutcomments = ''
   for line in sqllines:
      linewithoutcomments = line.split("#")[0] # this supposes there is no # in data and so on, but there probably isn't in our data for now....
      sqlwithoutcomments = sqlwithoutcomments + " " + linewithoutcomments
   #print sqlwithoutcomments
   sqlstatements = sqlwithoutcomments.split(";")
   for sqlstatement in sqlstatements:
      trimmedsqlstatement = sqlstatement.strip()
      if trimmedsqlstatement != '':
         #print trimmedsqlstatement
         dictcursor.execute(trimmedsqlstatement)
         nextAllSets(dictcursor)

def connectdb():
   return connectdbwiththesecredentials(config.dbuser, config.dbpassword, config.dbname, config.dbhost )

def disconnectdb():
   global connection, cursor, dictcursor
   dictcursor.close()
   cursor.close()
   connection.close()

# returns a list(?) containing the results from the query
# which should return a single column of data
def querytolist( querysql ):
   cursor.execute( querysql )
   row = cursor.fetchone()
   resultlist = []
   while row != None:
      resultlist.append( row[0] )
      row = cursor.fetchone()
   return resultlist

# returns a list(?) containing the results from the query
# which should return a single column of data
def querytolistwithparams( querysql, params ):
   cursor.execute( querysql, params )
   row = cursor.fetchone()
   resultlist = []
   while row != None:
      resultlist.append( row[0] )
      row = cursor.fetchone()
   return resultlist
   
# querysql is the sql string
# the result is a list of maps, ie something like:
# ( { 'somecolumn': 'somevalue' }, {'somecolumn': 'anothervalue' } )
def querytomaplist( querysql ):
   dictcursor.execute( querysql )
   return dictcursor.fetchall()

# do nextset() until no more sets
def nextAllSets(cursor):
   while cursor.nextset() != None:
      pass

