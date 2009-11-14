#!/bin/bash

sitehostname=manageddreams.com
# sitehostname=localhost
pagepath=/springgridstaging/api_webservice.py
# pagepath=/springgrid/api_webservice.py

contentfile=$(mktemp)
cat >$contentfile << EOF
<?xml version="1.0"?>
<methodCall>
  <methodName>getais</methodName>
  <params>
  </params>
</methodCall>
EOF

cat $contentfile
contentsize=$(cat $contentfile | wc -c)
echo $contentsize

httpcontentfile=$(mktemp)
cat >$httpcontentfile << EOF
POST ${pagepath} HTTP/1.0
Host: ${sitehostname}
Content-type: text/xml
Content-length: $contentsize

EOF

cat ${contentfile} >> ${httpcontentfile}
cat ${httpcontentfile}

nc ${sitehostname} 80 <${httpcontentfile}

