#!/usr/bin/python

import sys
import os
import time
import subprocess
import traceback

scriptdir = os.path.dirname( os.path.realpath( __file__ ) )

env = os.environ
env['SPRING_DATADIR'] = "/media/springwritabledat:/media/springdata:/media/spring"

while True:
   try:
      popen = subprocess.Popen([sys.executable, scriptdir + "/botrunner.py", "--configpath=" + scriptdir + "/config_vbox.py" ], env = env )
      popen.wait()
   except:
      print str(sys.exc_info()) + "\n" + str( traceback.extract_tb( sys.exc_traceback ) ) 
   time.sleep( 1 )


