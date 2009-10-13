#/usr/bin/python

import sys
import os

from unitsync import unitsync

if os.name == 'posix': location = '/usr/lib/spring/unitsync.so'
elif os.name == 'nt': location = 'unitsync.dll'
unitsync = unitsync.Unitsync(location)

unitsync.Init(True,1)
print unitsync.GetWritableDataDirectory()
#help(unitsync)

for i in xrange( unitsync.GetMapCount() ):
   print unitsync.GetMapName(i)
   print unitsync.GetMapArchiveCount(unitsync.GetMapName(i))
   print unitsync.GetMapArchiveName(0)
   #print unitsync.GetMapArchiveName(1)
   print unitsync.GetArchiveChecksum( unitsync.GetMapArchiveName(0))

