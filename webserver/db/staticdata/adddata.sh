#!/bin/bash

user=$1
password=$2
dbname=$3
dbhost=$4

if [[ x$dbhost == x ]]; then {
   echo Usage:
   echo $0 [user] [password] [dbname] [hostname]
   exit 1
} fi

for sqlfile in $(ls *.sql); do {
      # echo $sqlfile
      mysql -u $user --password=$password --host=$dbhost $dbname <$sqlfile
} done;


