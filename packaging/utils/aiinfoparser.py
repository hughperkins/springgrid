import os
import sys

import filehelper

# very simplistic flat parser, assumes everything is flat, and that value line always immediately follows key line
# it tracks { and } slightly, just in case we have some nested infos in the future, which
# will be ignored, but at least wont confuse the root namespace dictionary we are reading here
def parse( filepath ):
   contents = filehelper.readFile(filepath)
   dict = {}
   level = 0
   for line in contents.split("\n"):
      line = line.strip()
      if line.startswith("-"):
         continue
      level = level + line.count("{")
      level = level - line.count("}")
      if level == 2:
         if line.startswith ('key'):
            key = line.split("=")[1].strip().split(",")[0].replace("'","")
         if line.startswith ('value'):
            value = line.split("=")[1].strip().split(",")[0].replace("'","")
            dict[key] = value
   return dict

