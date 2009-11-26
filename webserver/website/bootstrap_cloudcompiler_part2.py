#!/usr/bin/python

# generates a bash script that, when run, will download what we needd, and launch
# the botrunner :-O
#
# This script assumes it will be run on disposable ec2 cloud nodes, and does not
# take any steps to protect the os from being compromised
#

import sys
import os

from core import *
from utils import *

jinjahelper.rendertemplate('bootstrap_cloudcompiler_part2.html', websiteurl=websiteurl = cgihelper.getScriptWebUrl() )

