#!/bin/bash

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


user=$1
password=$2
dbname=$3
dbhost=$4

scriptdir=$(dirname $0)

echo ""
echo "Note that this is deprecrated.  Please cd into the website directory and run 'python consolesetupdb.py' instead"
echo ""

if [[ x$dbhost == x ]]; then {
   echo Usage:
   echo $0 [user] [password] [dbname] [hostname]
   exit 1
} fi

cd tables
./dropall.sh $1 $2 $3 $4

# don't need to drop staticdata, since dropping tables handles that


