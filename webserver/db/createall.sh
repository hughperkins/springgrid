#!/bin/bash

user=$1
password=$2
dbname=$3
dbhost=$4

scriptdir=$(dirname $0)

if [[ x$dbhost == x ]]; then {
   echo Usage:
   echo $0 [user] [password] [dbname] [hostname]
   exit 1
} fi

cd tables
./createall.sh $1 $2 $3 $4

cd ../staticdata
./adddata.sh $1 $2 $3 $4


