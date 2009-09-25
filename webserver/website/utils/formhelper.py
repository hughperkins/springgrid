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

import cgi
import os

# helps with form stuff

# Generator to buffer file chunks
# This function from http://webpython.codepoint.net/cgi_big_file_upload
def fbuffer(f, chunk_size=10000):
   while True:
      chunk = f.read(chunk_size)
      if not chunk: break
      yield chunk

form = None

def getform():
   global form
   if form == None:
      form = cgi.FieldStorage()
   return form
 
def getValue( fieldname ):
   form = getform()
   if not form.has_key(fieldname):
      return None
   return form[fieldname].value

# takes a file at fieldname
# and writes it to disk at outputpath
# returns true if succeeds
# or false if no such field item
def writeIncomingFileToDisk( fieldname, outputpath ):
   form = getform()
   fileitem = form[fieldname]
   if fileitem == None:
      print "no replay field detected in incoming post"
      return False # file not uploaded

   if fileitem.file == None:
      print "no replay file uploaded"
      return False # file not uploaded

   filehandle = fileitem.file
   print "output path: " + outputpath
   outputfilehandle = open(outputpath, 'wb', 10000)
   for chunk in fbuffer(filehandle):
      print "writing chunk..."
      outputfilehandle.write(chunk)
   outputfilehandle.close()
   return True


