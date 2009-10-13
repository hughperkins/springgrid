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
